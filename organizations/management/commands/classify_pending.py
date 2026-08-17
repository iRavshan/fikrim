"""Toifasi aniqlanmay qolgan fikrlarni qayta tasniflaydi.

Gemini chaqiruvi muvaffaqiyatsiz bo'lganda fikr 'boshqa' toifasiga
tushadi va uni haqiqiy 'boshqa' dan ajratib bo'lmaydi. Shu sababli API
vaqtincha ishlamay qolsa, fikrlar jimgina tasniflanmagan holda qoladi.

Bu buyruq shundaylarni qaytadan tasniflaydi. Uni API ishlayotgan
istalgan muhitdan ishga tushirish mumkin — jumladan lokal kompyuterdan,
agar serverdagi chaqiruv ishlamayotgan bo'lsa.

Misollar:
    python manage.py classify_pending --dry-run
    python manage.py classify_pending --limit 20
"""

from django.core.management.base import BaseCommand

from organizations.models import Feedback
from organizations.utils import classify_feedback


class Command(BaseCommand):
    help = "Toifasi 'boshqa' bo'lgan fikrlarni Gemini orqali qayta tasniflaydi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', type=int, default=50,
            help="Bir marta qayta ishlanadigan fikrlar soni (standart: 50)",
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Bazaga yozmasdan, faqat natijani ko'rsatadi",
        )

    def handle(self, *args, **options):
        limit = options['limit']
        quruq = options['dry_run']

        fikrlar = list(
            Feedback.objects.filter(category='boshqa').order_by('-created_at')[:limit]
        )

        if not fikrlar:
            self.stdout.write("Qayta tasniflanadigan fikr topilmadi.")
            return

        self.stdout.write(
            f"{len(fikrlar)} ta fikr tekshiriladi"
            + (" (quruq rejim, bazaga yozilmaydi)" if quruq else "")
            + "\n"
        )

        ozgargan = 0
        for fikr in fikrlar:
            toifa = classify_feedback(fikr.text)
            belgi = " " if toifa == 'boshqa' else "*"
            self.stdout.write(
                f"  {belgi} {toifa:<10} <- {fikr.text[:52]}"
            )
            if toifa != 'boshqa':
                ozgargan += 1
                if not quruq:
                    Feedback.objects.filter(pk=fikr.pk).update(category=toifa)

        xulosa = f"\nTayyor: {ozgargan} ta fikr toifasi aniqlandi, " \
                 f"{len(fikrlar) - ozgargan} tasi 'boshqa' bo'lib qoldi."
        if ozgargan:
            self.stdout.write(self.style.SUCCESS(xulosa))
        else:
            # Bitta ham aniqlanmasa, ehtimol API umuman ishlamayapti
            self.stdout.write(self.style.WARNING(
                xulosa + "\nBitta ham toifa aniqlanmadi — Gemini chaqiruvi "
                "ishlayotganini tekshiring (kalit, kvota, tarmoq)."
            ))
