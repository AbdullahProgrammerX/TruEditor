"""
TruEditor - Staging Ayarları
============================
Test/Staging ortamı için özel ayarlar.
Production'a en yakın ortam - gerçek servislerle test yapılır.

KULLANIM:
  export DJANGO_SETTINGS_MODULE=core.settings.staging
  veya
  export ENV=staging

ZORUNLU ENV VARIABLES:
  - SECRET_KEY
  - DATABASE_URL
  - ALLOWED_HOSTS
  - CORS_ALLOWED_ORIGINS
  - CSRF_TRUSTED_ORIGINS

Geliştirici: Abdullah Doğan
"""

import os
os.environ.setdefault('ENV', 'staging')

from .base import *

# ============================================
# STAGING OVERRIDES
# ============================================

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

# ============================================
# WHITENOISE (Static Files)
# ============================================

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# ============================================
# SSL REDIRECT (Staging'de opsiyonel)
# ============================================
# Render preview URL'leri için kapatılabilir

SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'true').lower() == 'true'

# ============================================
# CORS (Staging - Sadece izin verilenler)
# ============================================

CORS_ALLOW_ALL_ORIGINS = False

print("[TruEditor] Staging settings loaded")
