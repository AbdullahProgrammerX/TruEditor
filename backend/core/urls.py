"""
TruEditor - URL Yapılandırması
==============================
Tüm API endpoint'leri /api/v1/ prefix'i altında sunulur.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# API versiyonu
API_VERSION = 'v1'


def setup_admin(request):
    """Temporary endpoint to promote admin. Remove after use."""
    import os
    from apps.users.models import User

    secret = request.GET.get('key', '')
    if secret != 'trueditor-setup-2026':
        return JsonResponse({'error': 'forbidden'}, status=403)

    orcid_id = os.environ.get('ADMIN_ORCID_ID', '').strip()
    password = os.environ.get('ADMIN_PASSWORD', '').strip()

    if not orcid_id or not password:
        return JsonResponse({
            'error': 'ADMIN_ORCID_ID or ADMIN_PASSWORD env vars not set',
            'has_orcid': bool(orcid_id),
            'has_password': bool(password),
        })

    try:
        user = User.objects.get(orcid_id=orcid_id)
    except User.DoesNotExist:
        all_users = list(User.objects.values_list('orcid_id', 'email'))
        return JsonResponse({'error': f'User not found', 'users': all_users})

    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save(update_fields=['password', 'is_staff', 'is_superuser'])

    return JsonResponse({
        'success': True,
        'email': user.email,
        'orcid_id': user.orcid_id,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Temporary setup endpoint
    path('setup-admin/', setup_admin),
    
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
