# ============================================
# TruEditor - Settings Package
# ============================================
# Ortama göre ayarları yükle
# ============================================

import os

# Varsayılan olarak development ayarlarını kullan
# Production'da DJANGO_SETTINGS_MODULE=core.settings.production olarak ayarla
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *
