"""
TruEditor - Production Ayarları
===============================
Canlı ortam için güvenlik odaklı ayarlar.

KULLANIM:
  export DJANGO_SETTINGS_MODULE=core.settings.production
  veya
  export ENV=production

ZORUNLU ENV VARIABLES:
  - SECRET_KEY
  - DATABASE_URL
  - REDIS_URL
  - ALLOWED_HOSTS
  - CORS_ALLOWED_ORIGINS
  - CSRF_TRUSTED_ORIGINS

Geliştirici: Abdullah Doğan
"""

import os
os.environ.setdefault('ENV', 'production')

from .base import *

# ============================================
# PRODUCTION OVERRIDES
# ============================================

DEBUG = False

# ============================================
# WHITENOISE (Static Files)
# ============================================

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# ============================================
# SECURITY (Zorunlu)
# ============================================

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 yıl
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ============================================
# CORS (Production - Sadece izin verilenler)
# ============================================

CORS_ALLOW_ALL_ORIGINS = False

# ============================================
# CELERY (Production - Async)
# ============================================

CELERY_TASK_ALWAYS_EAGER = False

# ============================================
# LOGGING (Production - Sadece WARNING+)
# ============================================

LOGGING['root']['level'] = 'WARNING'
LOGGING['loggers']['django']['level'] = 'WARNING'

print("[TruEditor] Production settings loaded")
