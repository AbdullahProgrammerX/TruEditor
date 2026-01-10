"""
TruEditor - Production Ayarları
===============================
Canlı ortam için güvenlik odaklı ayarlar.
"""

import os
import dj_database_url
from .base import *

# ============================================
# DEBUG MODU (Production'da kapalı)
# ============================================

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ============================================
# VERİTABANI (PostgreSQL)
# ============================================

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ============================================
# GÜVENLİK AYARLARI
# ============================================

# HTTPS zorunlu
SECURE_SSL_REDIRECT = True

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 yıl
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie güvenliği
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# X-Frame-Options
X_FRAME_OPTIONS = 'DENY'

# Content-Type sniffing koruması
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS Filter
SECURE_BROWSER_XSS_FILTER = True

# CSRF güvenilir origin'ler
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# ============================================
# STATİK DOSYALAR (WhiteNoise)
# ============================================

# WhiteNoise middleware (SecurityMiddleware'den hemen sonra)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Django 5.x için STORAGES kullanılır
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================================
# EMAIL (SMTP)
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'TruEditor <noreply@trueditor.com>')

# ============================================
# CORS (Production - Sadece izin verilen origin'ler)
# ============================================

CORS_ALLOW_ALL_ORIGINS = False

# ============================================
# CACHE (Redis)
# ============================================

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# ============================================
# CELERY (Production - Redis)
# ============================================

CELERY_TASK_ALWAYS_EAGER = False

# ============================================
# LOGGING (Production - Sentry)
# ============================================

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production',
    )

# Production logging - Render'da sadece console kullan
LOGGING['root']['handlers'] = ['console']
LOGGING['root']['level'] = 'WARNING'

# Django logları
LOGGING['loggers']['django']['level'] = 'WARNING'

print("[PROD] Production ayarlari yuklendi")
