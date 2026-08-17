import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-9^@7)5)lu)^ni9-w+*4#r5*49%+5yq9+xhh8-y#ze=h@kh(ft%')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://*.rlwy.net').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'organizations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'railway'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Birlamchi kalit maydonining turi.
# Ochiq yozilmagan bo'lsa, javob Django versiyasiga qarab o'zgaradi:
# 6.0 gacha AutoField, undan keyin BigAutoField. Shu sababli lokal va
# production har xil versiyada bo'lganda makemigrations har safar
# maydonni u yoqdan bu yoqqa o'zgartirmoqchi bo'lardi. Qiymat ochiq
# ko'rsatilgani uchun endi ikkala muhitda ham bir xil natija chiqadi.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')

# Gemini API — fikr-mulohazalarni avtomatik toifalash uchun
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')


# ── Rasmlarni saqlash: Cloudflare R2 ────────────────────────────────────
# Railway fayl tizimi har deployda tozalanadi, shuning uchun bemor yuborgan
# rasmlar u yerda saqlanmaydi — QR kodlardan farqli, rasmni qayta
# generatsiya qilib bo'lmaydi. R2 S3 bilan mos, shuning uchun django-storages
# ning S3 backend'i ishlatiladi.
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID', '')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY', '')
R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', '')
R2_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL', '')
# Bucket'ning ommaviy manzili. django-storages faqat host nomini kutadi,
# Cloudflare panelidan nusxa olinganda esa manzil "https://" bilan keladi.
# Ikkala shakl ham ishlashi uchun sxema va oxirgi chiziq olib tashlanadi —
# aks holda havola "https://https://..." bo'lib, rasmlar ochilmaydi.
R2_PUBLIC_DOMAIN = os.environ.get('R2_PUBLIC_DOMAIN', '').strip()
R2_PUBLIC_DOMAIN = (
    R2_PUBLIC_DOMAIN
    .removeprefix('https://')
    .removeprefix('http://')
    .rstrip('/')
)

_R2_SOZLANGAN = all([
    R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_ENDPOINT_URL,
])

if _R2_SOZLANGAN:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'access_key': R2_ACCESS_KEY_ID,
                'secret_key': R2_SECRET_ACCESS_KEY,
                'bucket_name': R2_BUCKET_NAME,
                'endpoint_url': R2_ENDPOINT_URL,
                'region_name': 'auto',
                'signature_version': 's3v4',
                # R2 ACL'ni qo'llab-quvvatlamaydi, ommaviy kirish bucket
                # sozlamasidan beriladi.
                'default_acl': None,
                # Imzosiz, muddatsiz URL — rasm <img> tegida ochilishi kerak.
                'querystring_auth': False,
                # Bir xil nomli fayl ustiga yozilmasin.
                'file_overwrite': False,
                'custom_domain': R2_PUBLIC_DOMAIN or None,
            },
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
else:
    # R2 sozlanmagan — lokal diskka tushamiz. Lokal ishlash uchun bu yetarli,
    # lekin production'da bu rasmlar deployda yo'qolishini anglatadi.
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
