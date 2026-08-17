"""Gemini sozlamasini tekshiradi va bitta jonli chaqiruv qiladi.

Toifalash lokalda ishlab, serverda ishlamasligi mumkin — sabab odatda
muhit o'zgaruvchilarida bo'ladi. Loglarni kutish o'rniga bu buyruq
javobni darhol beradi.

Railway muhitida tekshirish uchun:
    railway run python manage.py gemini_holati

Bu buyruq ma'lumotlar bazasiga umuman tegmaydi, shuning uchun DB
ishlamayotgan bo'lsa ham natija beradi.
"""

import json
import time
import urllib.error
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand

from organizations.utils import (
    ALLOWED_CATEGORIES,
    REQUEST_TIMEOUT,
    SYSTEM_PROMPT,
    classify_feedback,
)

# Javobi oldindan ma'lum sinov matni — natija 'sharoit' bo'lishi kerak.
SINOV_MATNI = "Xonalar sovuq, konditsioner ishlamayapti."
KUTILGAN = 'sharoit'

MODEL = "gemini-3.5-flash"


class Command(BaseCommand):
    help = "Gemini kaliti va chaqiruvi ishlayotganini tekshiradi"

    def handle(self, *args, **options):
        kalit = getattr(settings, 'GEMINI_API_KEY', '')

        self.stdout.write("── 1. Kalit ──")
        if not kalit:
            self.stdout.write(self.style.ERROR(
                "  GEMINI_API_KEY bo'sh.\n\n"
                "  Sabab shu. Toifalash umuman bajarilmayapti.\n"
                "  Railway > loyiha > Variables ichiga qo'shing. Nomi aynan\n"
                "  GEMINI_API_KEY bo'lishi kerak (GEMINI_KEY yoki\n"
                "  GOOGLE_API_KEY emas), keyin xizmat qayta ishga tushadi."
            ))
            return
        # Kalitning o'zi chop etilmaydi — loglar saqlanib qolishi mumkin.
        self.stdout.write(self.style.SUCCESS(
            f"  O'rnatilgan (uzunligi {len(kalit)}, boshlanishi {kalit[:6]}...)"
        ))

        self.stdout.write("\n── 2. Model mavjudmi ──")
        try:
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models"
                f"?key={kalit}&pageSize=200"
            )
            with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
                javob = json.loads(resp.read().decode('utf-8'))
            nomlar = {
                m["name"].removeprefix("models/") for m in javob.get("models", [])
            }
            if MODEL in nomlar:
                self.stdout.write(self.style.SUCCESS(f"  {MODEL} mavjud"))
            else:
                self.stdout.write(self.style.ERROR(
                    f"  {MODEL} ro'yxatda yo'q. Mavjud flash modellar:\n  "
                    + ", ".join(sorted(n for n in nomlar if "flash" in n))
                ))
                return
        except urllib.error.HTTPError as exc:
            tanasi = exc.read().decode('utf-8', 'replace')[:400]
            self.stdout.write(self.style.ERROR(f"  HTTP {exc.code}: {tanasi}"))
            if exc.code in (400, 403):
                self.stdout.write(
                    "  Kalit noto'g'ri yoki Generative Language API yoqilmagan."
                )
            return
        except Exception as exc:
            self.stdout.write(self.style.ERROR(
                f"  Tarmoq xatosi: {type(exc).__name__}: {exc}"
            ))
            return

        self.stdout.write("\n── 3. Jonli tasniflash ──")
        self.stdout.write(f'  Matn: "{SINOV_MATNI}"')
        boshlandi = time.time()
        natija = classify_feedback(SINOV_MATNI)
        ketgan = time.time() - boshlandi

        if natija is None:
            self.stdout.write(self.style.ERROR(
                f"  Yiqildi ({ketgan:.1f} soniya). Sabab yuqoridagi log\n"
                "  qatorida yozilgan."
            ))
            return

        self.stdout.write(f"  Natija: {natija}  ({ketgan:.1f} soniya)")
        if natija == KUTILGAN:
            self.stdout.write(self.style.SUCCESS("\nToifalash to'liq ishlayapti."))
        elif natija in ALLOWED_CATEGORIES:
            self.stdout.write(self.style.WARNING(
                f"\nChaqiruv ishladi, lekin '{KUTILGAN}' kutilgan edi.\n"
                "Tizim ishlayapti, faqat prompt aniqligi past."
            ))

        # Fon oqimi 16-18 soniya yashashi kerak. Konteyner bundan tez
        # to'xtasa oqim uzilib qoladi va toifalash bajarilmaydi.
        if ketgan > 12:
            self.stdout.write(self.style.WARNING(
                f"\nEslatma: chaqiruv {ketgan:.0f} soniya oldi. Fon oqimi\n"
                "shuncha vaqt yashashi kerak. Agar Railway'da App Sleeping\n"
                "yoqilgan bo'lsa, oqim tugamasdan uzilishi mumkin —\n"
                "classify_pending cron zaxira sifatida shuni qutqaradi."
            ))
