from django.db import models
from django.contrib.auth.models import User
import uuid

class Organization(models.Model):
    # Birinchi bosqichda faqat tibbiy muassasalar bilan ishlaymiz.
    ORG_TYPES = [
        ('xususiy_kasalxona', 'Xususiy kasalxona'),
        ('davlat_shifoxonasi', 'Davlat shifoxonasi'),
        ('xususiy_klinika', 'Xususiy klinika'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations')
    name = models.CharField(max_length=255, verbose_name="Tashkilot nomi")
    org_type = models.CharField(max_length=50, choices=ORG_TYPES, verbose_name="Tashkilot turi")
    address = models.TextField(verbose_name="Manzili")
    # Eskirgan: QR endi diskda saqlanmaydi, so'rov kelganda generatsiya qilinadi.
    # Maydon eski yozuvlar uchun qoldirilgan.
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    """Bemorlar xonasi. Har bir xonaning o'z QR kodi bo'ladi."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=32, verbose_name="Xona raqami")
    name = models.CharField(max_length=120, blank=True, verbose_name="Bo'lim yoki izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Bitta tashkilotda xona raqami takrorlanmasin
        unique_together = ('organization', 'number')
        # Raqam bo'yicha saralash "10" ni "2" dan oldin qo'yardi, shuning uchun
        # yaratilgan tartib saqlanadi (ommaviy yaratishda 1, 2, 3 ... tartibida)
        ordering = ['created_at']

    def __str__(self):
        return f"{self.number}-xona"


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('xodimlar', 'Xodimlar va xizmat ko\'rsatish'),
        ('sharoit', 'Texnik ta\'minot va sharoitlar'),
        ('tibbiy', 'Tibbiy xizmat va dori-darmon'),
        ('moliyaviy', 'Moliyaviy masalalar va narxlar'),
        ('boshqa', 'Boshqa masalalar'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='feedbacks')
    # Xona o'chirilsa fikr yo'qolmasin, faqat bog'lanish uzilsin
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks'
    )
    text = models.TextField(verbose_name="Fikr va mulohaza")
    # Eskirgan: rasmlar endi FeedbackImage modelida saqlanadi. Maydon eski
    # yozuvlar uchun qoldirilgan va yangi kod uni ishlatmaydi. Ustunni
    # o'chirish alohida, kod deploy bo'lgandan keyingi qadam bo'ladi.
    image = models.ImageField(
        upload_to='feedback/', blank=True, null=True, verbose_name="Rasm"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='boshqa',
        verbose_name="Toifa",
        db_index=True,
    )
    # Toifalash muvaffaqiyatli bajarilgan vaqt. NULL bo'lsa — toifa hali
    # aniqlanmagan: chaqiruv yiqilgan yoki umuman bajarilmagan.
    #
    # Bu maydonsiz haqiqiy 'boshqa' bilan "aniqlab bo'lmadi" bir xil
    # ko'rinadi. Aynan shuning uchun avval qayta urinish imkonsiz edi:
    # 'boshqa' larni qayta so'rasak, chin 'boshqa' fikrlar har safar
    # qaytadan Gemini'ga yuborilaverardi va kvota behuda sarflanardi.
    classified_at = models.DateTimeField(
        null=True, blank=True, db_index=True, verbose_name="Toifalangan vaqt"
    )
    # Takrorlanishni aniqlash uchun sha256(salt + xona + IP). Xom IP manzil
    # bazaga yozilmaydi va hashdan qayta tiklab bo'lmaydi, shuning uchun
    # bemor anonim qoladi.
    submitter_hash = models.CharField(max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.organization.name} at {self.created_at}"


class FeedbackImage(models.Model):
    """Fikrga biriktirilgan rasm. Bitta fikrda bir nechta rasm bo'lishi mumkin.

    Saqlashdan oldin har bir rasm images.sanitize_image() orqali o'tkaziladi:
    EXIF (GPS koordinatalari, telefon modeli, sana) tozalanadi va hajmi
    kichraytiriladi.
    """

    feedback = models.ForeignKey(
        Feedback, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='feedback/', verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Bemor tanlagan tartib saqlanadi
        ordering = ['created_at', 'id']

    def __str__(self):
        return f"Rasm #{self.pk} (fikr {self.feedback_id})"

