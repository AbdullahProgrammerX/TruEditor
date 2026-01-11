"""
TruEditor - Temel Django Ayarları
=================================
Tüm ortamlar için ortak ayarlar burada tanımlanır.

ÖNEMLI: Bu dosya platform-agnostic olmalı.
Tüm ortam farklılıkları environment variable'lar ile yönetilir.

Geliştirici: Abdullah Doğan
"""

import os
from pathlib import Path
from datetime import timedelta

# ============================================
# ENVIRONMENT DETECTION
# ============================================
# ENV değerleri: development, staging, production
ENV = os.environ.get('ENV', 'development')

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================
# SECRET KEY (Zorunlu environment variable)
# ============================================
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY and ENV != 'development':
    raise ValueError("SECRET_KEY environment variable is required for non-development environments")
SECRET_KEY = SECRET_KEY or 'django-insecure-dev-only-key-do-not-use-in-production'

# ============================================
# DEBUG (Environment'a göre)
# ============================================
DEBUG = os.environ.get('DEBUG', str(ENV == 'development')).lower() == 'true'

# ============================================
# ALLOWED HOSTS
# ============================================
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]

# ============================================
# UYGULAMA TANIMLARI
# ============================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_fsm',
    'storages',
]

LOCAL_APPS = [
    'apps.common',
    'apps.users',
    'apps.submissions',
    'apps.files',
    'apps.notifications',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ============================================
# TEMPLATES
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ============================================
# VERİTABANI (Platform-Agnostic)
# ============================================
# DATABASE_URL formatı: postgresql://user:pass@host:port/dbname

import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production/Staging: PostgreSQL via DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: SQLite (varsayılan)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================
# ŞİFRE DOĞRULAMA
# ============================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================
# ULUSLARARASILAŞTIRMA
# ============================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# ============================================
# STATİK VE MEDYA DOSYALARI
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static klasörü varsa ekle (opsiyonel)
_static_dir = BASE_DIR / 'static'
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# DEFAULT PRIMARY KEY
# ============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# ÖZEL KULLANICI MODELİ
# ============================================

AUTH_USER_MODEL = 'users.User'

# ============================================
# DJANGO REST FRAMEWORK
# ============================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'EXCEPTION_HANDLER': 'apps.common.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.environ.get('THROTTLE_ANON', '100/hour'),
        'user': os.environ.get('THROTTLE_USER', '1000/hour')
    }
}

# ============================================
# SIMPLE JWT AYARLARI
# ============================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(os.environ.get('JWT_ACCESS_LIFETIME_MINUTES', 15))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=int(os.environ.get('JWT_REFRESH_LIFETIME_DAYS', 7))
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

# ============================================
# CORS AYARLARI (Platform-Agnostic)
# ============================================

CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 
    'http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173'
).split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS if origin.strip()]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Development'ta tüm origin'lere izin ver (CORS_ALLOW_ALL geçersiz kılar)
if ENV == 'development':
    CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL', 'true').lower() == 'true'

# ============================================
# CSRF TRUSTED ORIGINS
# ============================================

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS if origin.strip()]

# ============================================
# ORCID AYARLARI
# ============================================

ORCID_CLIENT_ID = os.environ.get('ORCID_CLIENT_ID', '')
ORCID_CLIENT_SECRET = os.environ.get('ORCID_CLIENT_SECRET', '')
ORCID_REDIRECT_URI = os.environ.get('ORCID_REDIRECT_URI', 'http://localhost:3000/auth/orcid/callback')

# ORCID API URL'leri (sandbox vs production)
ORCID_BASE_URL = os.environ.get('ORCID_BASE_URL', 'https://sandbox.orcid.org')
ORCID_API_URL = os.environ.get('ORCID_API_URL', 'https://api.sandbox.orcid.org')

# ============================================
# DOSYA DEPOLAMA (S3-Compatible / Platform-Agnostic)
# ============================================
# USE_S3=true ile etkinleştir
# AWS S3, MinIO, DigitalOcean Spaces, vb. ile çalışır

USE_S3 = os.environ.get('USE_S3', 'false').lower() == 'true'

if USE_S3:
    # S3-Compatible Storage Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-central-1')
    
    # Custom endpoint (MinIO, DigitalOcean Spaces, vb. için)
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
    
    # S3 Ayarları
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'private'
    AWS_QUERYSTRING_EXPIRE = 900  # 15 dakika
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    
    # Django 5.x STORAGES formatı
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    # Local Storage (development)
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# ============================================
# REDIS / CACHE (Platform-Agnostic)
# ============================================
# REDIS_URL formatı: redis://user:pass@host:port/db
# veya: rediss://... (SSL için)

REDIS_URL = os.environ.get('REDIS_URL')

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    # Local Memory Cache (development)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ============================================
# CELERY (Platform-Agnostic)
# ============================================
# Broker: Redis, RabbitMQ, SQS, vb.
# Tüm broker'lar CELERY_BROKER_URL ile yapılandırılır

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL or 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)

# Celery Core Settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = int(os.environ.get('CELERY_TASK_TIME_LIMIT', 1800))  # 30 dakika

# Task Design Rules (Scalability için)
CELERY_TASK_ACKS_LATE = True  # Crash durumunda task'ı tekrar çalıştır
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fair distribution

# Development'ta senkron çalıştırma (CELERY_EAGER=true ile)
CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_EAGER', 'false').lower() == 'true'
CELERY_TASK_EAGER_PROPAGATES = CELERY_TASK_ALWAYS_EAGER

# ============================================
# DOSYA YÜKLEMELERI
# ============================================

MAX_UPLOAD_SIZE = int(os.environ.get('MAX_UPLOAD_SIZE', 52428800))  # 50MB
ALLOWED_EXTENSIONS = os.environ.get(
    'ALLOWED_EXTENSIONS', 
    '.doc,.docx,.pdf,.jpg,.jpeg,.png,.tiff,.tif'
).split(',')

# ============================================
# PDF OLUŞTURMA
# ============================================

WEASYPRINT_FONT_DIR = BASE_DIR / 'static' / 'fonts'
PDF_DPI = int(os.environ.get('PDF_DPI', 150))

# ============================================
# LOGGING (Platform-Agnostic - Console Only)
# ============================================
# Stateless backend: Asla file logging kullanma
# Logs container/platform tarafından yönetilir

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO' if ENV != 'development' else 'DEBUG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        'json': {
            'format': '{{"level": "{levelname}", "time": "{asctime}", "module": "{module}", "message": "{message}"}}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose' if DEBUG else 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================
# SECURITY SETTINGS (Non-Development)
# ============================================

if ENV != 'development':
    # HTTPS zorunlu
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'true').lower() == 'true'
    
    # HSTS
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie güvenliği
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Headers
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# ============================================
# EMAIL (Platform-Agnostic)
# ============================================

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 
    'django.core.mail.backends.console.EmailBackend' if ENV == 'development' 
    else 'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'TruEditor <noreply@trueditor.com>')

# ============================================
# SENTRY (Error Tracking - Opsiyonel)
# ============================================

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN and ENV != 'development':
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.celery import CeleryIntegration
        
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                CeleryIntegration(),
            ],
            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', 0.1)),
            send_default_pii=False,
            environment=ENV,
        )
    except ImportError:
        pass

# ============================================
# HEALTH CHECK
# ============================================

HEALTH_CHECK_ENABLED = True

# ============================================
# STARTUP LOG
# ============================================

print(f"[TruEditor] Environment: {ENV} | Debug: {DEBUG}")
