"""
TruEditor - Celery Yapılandırması
=================================
Asenkron görev işleme için Celery ayarları.
PDF oluşturma, email gönderme gibi ağır işler burada işlenir.
"""

import os
from celery import Celery

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Celery uygulaması oluştur
app = Celery('trueditor')

# Django settings'ten Celery ayarlarını oku
# CELERY_ prefix'i ile başlayan tüm ayarları kullan
app.config_from_object('django.conf:settings', namespace='CELERY')

# apps/ altındaki tüm tasks.py dosyalarını otomatik keşfet
app.autodiscover_tasks()

# ============================================
# CELERY GÖREV AYARLARI
# ============================================

app.conf.update(
    # Görev sonuçlarını Redis'te sakla
    result_expires=3600,  # 1 saat
    
    # Görev retry ayarları
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Worker ayarları
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Zaman aşımı
    task_soft_time_limit=600,  # 10 dakika (soft)
    task_time_limit=900,  # 15 dakika (hard)
    
    # Seri hale getirme
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

# ============================================
# PERIYODIK GÖREVLER (Celery Beat)
# ============================================

app.conf.beat_schedule = {
    # Örnek: Her gün gece yarısı eski PDF'leri temizle
    # 'cleanup-old-pdfs': {
    #     'task': 'apps.submissions.tasks.cleanup_old_pdfs',
    #     'schedule': crontab(hour=0, minute=0),
    # },
    
    # Örnek: Her saat ORCID profillerini senkronize et
    # 'sync-orcid-profiles': {
    #     'task': 'apps.users.tasks.sync_orcid_profiles',
    #     'schedule': crontab(minute=0),
    # },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Debug görevi - Celery'nin çalışıp çalışmadığını test etmek için.
    
    Kullanım:
        from core.celery import debug_task
        debug_task.delay()
    """
    print(f'Request: {self.request!r}')
