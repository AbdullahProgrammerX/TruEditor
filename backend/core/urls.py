"""
TruEditor - URL Yapılandırması
==============================
Tüm API endpoint'leri /api/v1/ prefix'i altında sunulur.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# API versiyonu
API_VERSION = 'v1'

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path(f'api/{API_VERSION}/', include([
        # Health Check
        path('health/', include('apps.common.urls')),
        
        # Authentication (ORCID)
        path('auth/', include('apps.users.urls')),
        
        # Submissions (Author Module)
        path('submissions/', include('apps.submissions.urls')),
        
        # Files
        path('files/', include('apps.files.urls')),
        
        # Notifications
        path('notifications/', include('apps.notifications.urls')),
    ])),
]

# Development ortamında media dosyalarını serve et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug Toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Admin panel özelleştirme
admin.site.site_header = 'TruEditor Yönetim Paneli'
admin.site.site_title = 'TruEditor Admin'
admin.site.index_title = 'Hoş Geldiniz'
