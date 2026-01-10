"""
TruEditor - Submissions App Config
"""

from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.submissions'
    verbose_name = 'Makale Gönderimleri'
    
    def ready(self):
        """
        Uygulama hazır olduğunda signal'ları import et.
        """
        try:
            import apps.submissions.signals  # noqa
        except ImportError:
            pass
