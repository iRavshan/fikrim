"""Gemini API yordamida fikr-mulohazalarni avtomatik toifalash."""

import json
import logging
import urllib.request
import urllib.error

from django.conf import settings

logger = logging.getLogger(__name__)

# Ruxsat etilgan toifa kalitlari — modelda CATEGORY_CHOICES bilan mos
ALLOWED_CATEGORIES = {'xodimlar', 'sharoit', 'tibbiy', 'moliyaviy', 'boshqa'}

# Gemini ga yuboriladigan tizim ko'rsatmasi
SYSTEM_PROMPT = (
    "Sen tibbiy muassasalarga kelib tushgan bemor fikr-mulohazalarini tasniflovchi "
    "yordamchisan. Har bir fikrni faqat bitta toifaga ajrat.\n\n"
    "Toifalar:\n"
    "- xodimlar — shifokor, hamshira, qabul xodimi, xizmat ko'rsatish madaniyati, "
    "munosabat, muomala haqida\n"
    "- sharoit — bino holati, tozalik, jihozlar, mebel, texnik ta'minot, "
    "sovuq/issiqlik, Wi-Fi, navbat tizimi haqida\n"
    "- tibbiy — davolash sifati, tashxis, dori-darmon, laboratoriya, "
    "operatsiya, tibbiy xatolik haqida\n"
    "- moliyaviy — narxlar, to'lov, sug'urta, ortiqcha pul undirish, "
    "chegirma haqida\n"
    "- boshqa — yuqoridagi toifalarga kirmagan fikrlar\n\n"
    "Javobingda FAQAT toifa kalitini yoz (masalan: xodimlar). "
    "Boshqa hech narsa yozma."
)


def classify_feedback(text: str) -> str:
    """Berilgan matnni Gemini API orqali toifaga ajratadi.

    API kalit o'rnatilmagan bo'lsa yoki so'rov muvaffaqiyatsiz bo'lsa
    xavfsiz ravishda 'boshqa' toifasini qaytaradi.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        logger.warning("GEMINI_API_KEY o'rnatilmagan, fikr 'boshqa' toifasiga tushdi.")
        return 'boshqa'

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-3.5-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\nFikr matni:\n{text}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 256,
            # gemini-3.5-flash "thinking" modeli. Tasniflash oddiy vazifa
            # bo'lgani uchun fikrlash o'chiriladi: aks holda thinking butun
            # token limitini yeb qo'yadi va javob MAX_TOKENS bilan uziladi.
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode('utf-8'))

        # Gemini 3.5-flash "thinking" model — javob parts ichida
        # thinking va oddiy text alohida keladi.
        # Oxirgi non-empty text part'ni olamiz.
        candidate = body.get("candidates", [{}])[0]
        parts = candidate.get("content", {}).get("parts", [])

        # Javob token limitiga urilib uzilgan bo'lsa, qaytgan matn to'liq
        # emas va tasniflash ishonchsiz bo'ladi — buni jimgina o'tkazmaymiz.
        if candidate.get("finishReason") == "MAX_TOKENS":
            logger.warning(
                "Gemini javobi token limitida uzildi, toifa aniqlanmadi. "
                "maxOutputTokens yoki thinkingConfig sozlamasini tekshiring."
            )
            return 'boshqa'

        raw = ""
        for part in parts:
            part_text = part.get("text", "").strip()
            # "thought" flagli part'lar thinking bo'ladi, ularni o'tkazamiz
            if part.get("thought"):
                continue
            if part_text:
                raw = part_text.lower()

        # Javobda noto'g'ri yoki kutilmagan qiymat bo'lsa 'boshqa' qaytariladi
        if raw in ALLOWED_CATEGORIES:
            return raw

        # Ba'zan model qo'shimcha so'z yozishi mumkin, shuning uchun
        # har bir ruxsat etilgan kalit mavjudligini tekshiramiz
        for cat in ALLOWED_CATEGORIES:
            if cat in raw:
                return cat

        logger.info("Gemini kutilmagan javob qaytardi: %s", raw)
        return 'boshqa'

    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError,
            KeyError, IndexError, TimeoutError) as exc:
        logger.error("Gemini API so'rovida xatolik: %s", exc)
        return 'boshqa'

