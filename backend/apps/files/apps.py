"""
TruEditor - Files App Config
"""

from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.files'
    verbose_name = 'Dosya Yönetimi'
