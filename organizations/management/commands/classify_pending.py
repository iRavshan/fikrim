"""Toifalanmay qolgan fikrlarni qayta tasniflaydi.

Fikr yuborilganda toifalash fon oqimida bajariladi. Bu oqim yiqilishi
mumkin: Gemini javob bermasligi, kvota tugashi yoki konteyner qayta
ishga tushib oqimni uzib yuborishi mumkin. Bunday holatda fikr
saqlanadi, lekin classified_at NULL bo'lib qoladi.

Bu buyruq aynan shundaylarni topib qayta uradi. Muvaffaqiyatsiz
urinish classified_at ni o'zgartirmaydi, shuning uchun keyingi ishga
tushishda fikr yana navbatda turadi — API tiklangach o'zi tasniflanadi.

Cron bilan muntazam ishga tushirilishi ko'zda tutilgan. Qo'lda ham
ishlatish mumkin, jumladan lokal kompyuterdan.

Misollar:
    python manage.py classify_pending --dry-run
    python manage.py classify_pending --limit 20
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from organizations.models import Feedback
from organizations.utils import classify_feedback


class Command(BaseCommand):
    help = "Toifalanmay qolgan fikrlarni Gemini orqali qayta tasniflaydi"

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

        # Eng yangi fikrlar birinchi: kvota cheklangan bo'lsa, rahbar uchun
        # eng dolzarb bo'lganlari tasniflanadi.
        fikrlar = list(
            Feedback.objects
            .filter(classified_at__isnull=True)
            .order_by('-created_at')[:limit]
        )

        if not fikrlar:
            self.stdout.write("Toifalanmagan fikr yo'q — hammasi joyida.")
            return

        qolgan = Feedback.objects.filter(classified_at__isnull=True).count()
        self.stdout.write(
            f"Navbatda {qolgan} ta fikr, shundan {len(fikrlar)} tasi olinadi"
            + (" (quruq rejim, bazaga yozilmaydi)" if quruq else "")
            + "\n"
        )

        aniqlangan = 0
        yiqilgan = 0
        for fikr in fikrlar:
            toifa = classify_feedback(fikr.text)

            if toifa is None:
                yiqilgan += 1
                self.stdout.write(f"  ! yiqildi    <- {fikr.text[:52]}")
                # Ketma-ket yiqilishlar API umuman ishlamayotganini
                # bildiradi. Qolganini bekorga urib, kvota sarflamaymiz.
                if yiqilgan >= 3 and aniqlangan == 0:
                    self.stdout.write(self.style.ERROR(
                        "\nKetma-ket 3 ta chaqiruv yiqildi — to'xtatildi.\n"
                        "Sababni ko'rish uchun: python manage.py gemini_holati"
                    ))
                    return
                continue

            aniqlangan += 1
            belgi = " " if toifa == 'boshqa' else "*"
            self.stdout.write(f"  {belgi} {toifa:<10} <- {fikr.text[:52]}")
            if not quruq:
                Feedback.objects.filter(pk=fikr.pk).update(
                    category=toifa, classified_at=timezone.now()
                )

        xulosa = f"\nTayyor: {aniqlangan} ta toifalandi"
        if yiqilgan:
            self.stdout.write(self.style.WARNING(
                f"{xulosa}, {yiqilgan} tasi yiqildi va navbatda qoldi."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(xulosa + "."))
