"""
TruEditor - Development Ayarları
================================
Yerel geliştirme ortamı için özel ayarlar.

KULLANIM:
  export DJANGO_SETTINGS_MODULE=core.settings.development
  veya
  export ENV=development

Geliştirici: Abdullah Doğan
"""

import os
os.environ.setdefault('ENV', 'development')

from .base import *

# ============================================
# DEVELOPMENT OVERRIDES
# ============================================

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']

# ============================================
# CORS (Development - Tüm origin'ler)
# ============================================

CORS_ALLOW_ALL_ORIGINS = True

# ============================================
# DEBUG TOOLBAR (Opsiyonel)
# ============================================

try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass

# ============================================
# DJANGO EXTENSIONS (Opsiyonel)
# ============================================

try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

# ============================================
# JWT (Development - Uzun süreli tokenlar)
# ============================================

from datetime import timedelta
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=24)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)

# ============================================
# CELERY (Development - Eager mode)
# ============================================
# Redis olmadan çalışabilir

CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_EAGER', 'true').lower() == 'true'
CELERY_TASK_EAGER_PROPAGATES = True

print("[TruEditor] Development settings loaded")
