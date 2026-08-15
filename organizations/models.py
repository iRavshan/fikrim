from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import qrcode
from io import BytesIO


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
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.qr_code:
            # Generate QR code
            # We use a default host if SITE_URL is not set
            site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            feedback_url = f"{site_url}/feedback/{self.id}/"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(feedback_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            self.qr_code.save(f"qr_{self.id}.png", ContentFile(buffer.getvalue()), save=False)
            
        super().save(*args, **kwargs)

class Feedback(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField(verbose_name="Fikr va mulohaza")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.organization.name} at {self.created_at}"
