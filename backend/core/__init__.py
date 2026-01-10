"""
TruEditor - Core Package
========================
Django projesi ana modülü.
"""

# Celery uygulamasını Django ile birlikte yükle
# Bu, Django başlatıldığında Celery'nin de hazır olmasını sağlar
from .celery import app as celery_app

__all__ = ('celery_app',)

__version__ = '1.0.0'
