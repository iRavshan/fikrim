from django.db import models
from django.contrib.auth.models import User
import uuid

class Organization(models.Model):
    ORG_TYPES = [
        ('xususiy_kasalxona', 'Xususiy kasalxona'),
        ('davlat_shifoxonasi', 'Davlat shifoxonasi'),
        ('dorixona', 'Dorixona'),
        ('kafe', 'Kafe'),
        ('restoran', 'Restoran'),
        ('muzey', 'Muzey'),
        ('teatr', 'Teatr'),
        ('maktab', 'Maktab'),
        ('oliy_talim', "Oliy ta'lim muassasasi"),
        ('bank', 'Bank'),
        ('bogcha', "Bog'cha"),
        ('boshqa', 'Boshqa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations')
    name = models.CharField(max_length=255, verbose_name="Tashkilot nomi")
    org_type = models.CharField(max_length=50, choices=ORG_TYPES, verbose_name="Tashkilot turi")
    address = models.TextField(verbose_name="Manzili")
    # Eskirgan: QR endi diskda saqlanmaydi, organization_qr view'ida
    # so'rov kelganda generatsiya qilinadi. Maydon eski yozuvlar uchun qoldirilgan.
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField(verbose_name="Fikr va mulohaza")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.organization.name} at {self.created_at}"
