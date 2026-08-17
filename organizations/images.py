"""Bemor yuborgan rasmni anonim va yengil holga keltirish.

Telefonda olingan rasm o'zi bilan EXIF ma'lumotlarini olib yuradi: GPS
koordinatalari, telefon modeli va seriya raqami, aniq sana-vaqt. Bizning
mahsulotimiz bemorga mutlaqo anonimlik va'da qilgani uchun bu ma'lumotlar
bazaga tushmasligi shart — aks holda shifoxona rahbari rasmni yuklab olib,
uni kim va qayerdan yuborganini taxmin qila oladi.

Shuning uchun rasm saqlashdan oldin butunlay qayta yoziladi: Pillow yangi
tasvir obyektiga faqat piksellarni ko'chiradi, metama'lumotlar esa
ko'chirilmaydi. Shu yo'l bilan hajmi ham kichrayadi.
"""

import io
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps

# Uzun tomonining eng katta o'lchami. Telefon rasmi odatda 3000-4000 piksel
# bo'ladi va 3-12 MB joy egallaydi; 1600 piksel muammoni ko'rsatish uchun
# yetarli, hajmi esa 200-400 KB ga tushadi.
MAX_SIDE = 1600

JPEG_QUALITY = 82

# Bitta fikrga biriktirish mumkin bo'lgan rasmlar soni. Har bir rasm
# alohida qayta ishlanib R2 ga yuklanadi, shuning uchun son cheksiz
# bo'lsa bemor javobni uzoq kutadi.
MAX_IMAGES = 10

# Barcha rasmlarning umumiy hajmi (qayta ishlashdan oldingi, xom holat).
MAX_TOTAL_MB = 50
MAX_TOTAL_BYTES = MAX_TOTAL_MB * 1024 * 1024


def validate_images(files):
    """Yuklangan rasmlar ro'yxatini tekshiradi.

    Muammo bo'lsa foydalanuvchiga ko'rsatiladigan xabarni, aks holda
    None qaytaradi.
    """
    if not files:
        return None

    if len(files) > MAX_IMAGES:
        return (
            f"Eng ko'pi bilan {MAX_IMAGES} ta rasm biriktirish mumkin. "
            f"Siz {len(files)} ta tanladingiz."
        )

    jami = sum(f.size for f in files)
    if jami > MAX_TOTAL_BYTES:
        return (
            f"Rasmlarning umumiy hajmi {MAX_TOTAL_MB} MB dan oshmasligi kerak. "
            f"Hozirgi hajm: {jami / 1024 / 1024:.1f} MB."
        )

    return None


def sanitize_image(uploaded_file):
    """Yuklangan rasmni metama'lumotsiz, kichraytirilgan JPEG'ga aylantiradi.

    Fayl nomi ham saqlanmaydi — original nom ("IMG_Alisher_uy.jpg" kabi)
    o'zi ham ma'lumot sizdirishi mumkin, shuning uchun tasodifiy nom
    beriladi.
    """
    img = Image.open(uploaded_file)

    # EXIF ichidagi burilish belgisini avval piksellarga qo'llaymiz, aks
    # holda metama'lumot o'chirilgach rasm yon tomonga ag'darilib qoladi.
    img = ImageOps.exif_transpose(img)

    # JPEG shaffoflikni qo'llab-quvvatlamaydi, shuning uchun shaffof
    # rasmlarni oq fonga joylashtiramiz.
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
        fon = Image.new('RGB', img.size, (255, 255, 255))
        fon.paste(img, mask=img.split()[-1])
        img = fon
    else:
        img = img.convert('RGB')

    img.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    # exif argumenti berilmagani uchun yangi faylga hech qanday
    # metama'lumot yozilmaydi.
    img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    buffer.seek(0)

    nom = f"{uuid.uuid4().hex}.jpg"
    return InMemoryUploadedFile(
        buffer, 'ImageField', nom, 'image/jpeg', buffer.getbuffer().nbytes, None
    )
