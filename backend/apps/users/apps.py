"""
TruEditor - Users App Config
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Kullanıcı Yönetimi'
    
    def ready(self):
        """
        Uygulama hazır olduğunda signal'ları import et.
        """
        try:
            import apps.users.signals  # noqa
        except ImportError:
            pass
