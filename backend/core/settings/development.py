"""
TruEditor - Development Ayarları
================================
Geliştirme ortamı için özel ayarlar.
"""

from .base import *

# ============================================
# DEBUG MODU
# ============================================

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ============================================
# VERİTABANI (SQLite - Development)
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================
# EMAIL (Console Backend)
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================
# CORS (Geliştirme için tüm origin'lere izin ver)
# ============================================

CORS_ALLOW_ALL_ORIGINS = True

# ============================================
# DEBUG TOOLBAR
# ============================================

try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass

# ============================================
# DJANGO EXTENSIONS
# ============================================

try:
    import django_extensions
    INSTALLED_APPS += ['django_extensions']
except ImportError:
    pass

# ============================================
# LOGGING (Verbose for development)
# ============================================

LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# ============================================
# CELERY (Development)
# ============================================

# Development'ta senkron çalıştır (Redis gerektirmez)
CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_EAGER', 'True').lower() == 'true'
CELERY_TASK_EAGER_PROPAGATES = True

# ============================================
# S3 (Development - Local Storage)
# ============================================

# Development'ta varsayılan olarak local storage kullan
if not USE_S3:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ============================================
# CACHE (Development - Local Memory)
# ============================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ============================================
# SIMPLE JWT (Development - Uzun süreli tokenlar)
# ============================================

from datetime import timedelta

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=1)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)

print("[DEV] Development ayarlari yuklendi")
