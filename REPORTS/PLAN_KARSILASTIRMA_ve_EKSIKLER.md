# TruEditor - Plan Karşılaştırması ve Eksikler Raporu

**Tarih:** 13 Ocak 2026  
**Plan Dosyası:** `editorial_manager_development_ebf4a387.plan.md`

---

## 📊 Plan vs Mevcut Durum Karşılaştırması

| Faz | Plan Durumu | Mevcut Durum | Tamamlanma |
|-----|-------------|--------------|------------|
| **Faz 0** | ✅ completed | ✅ Tamamlandı | %100 |
| **Faz 1 (Backend)** | ✅ completed | ✅ Tamamlandı | %100 |
| **Faz 1 (Frontend)** | ✅ completed | ✅ Tamamlandı | %100 |
| **Faz 2** | ⏳ pending | ✅ Tamamlandı | %100 |
| **Faz 3** | ⏳ pending | ✅ Tamamlandı | %100 |
| **Faz 4** | ⏳ pending | ✅ Tamamlandı* | %100 |
| **Faz 5** | ⏳ pending | ✅ Tamamlandı | %100 |
| **Faz 6** | ⏳ pending | ✅ Tamamlandı | %100 |
| **Faz 7** | ⏳ pending | ✅ Tamamlandı | %100 |
| **Faz 8** | ⏳ pending | ❌ Yapılmadı | %0 |
| **Faz 9** | ⏳ pending | ❌ Yapılmadı | %0 |
| **Faz 10** | ⏳ pending | 🟡 Kısmen | %70 |

*Not: Faz 4 plan'da Railway için, ancak Render kullanıldı - işlevsel olarak tamamlandı sayılabilir.

---

## ❌ EKSİK FAZLAR (Detaylı)

### ✅ Faz 6: Author Module Backend API - %100

#### ✅ Mevcut:
- `backend/apps/submissions/models.py` - Modeller hazır
- `backend/apps/submissions/migrations/` - Migration'lar var

#### ❌ Eksikler:

**1. Serializers (`backend/apps/submissions/serializers.py` - YOK)**
- [ ] `SubmissionListSerializer` - Dashboard için özet bilgiler
- [ ] `SubmissionDetailSerializer` - Tüm detaylar
- [ ] `SubmissionCreateSerializer` - Yeni gönderim
- [ ] `SubmissionUpdateSerializer` - Güncelleme
- [ ] `AuthorshipSerializer` - Yazar bilgileri

**2. Views (`backend/apps/submissions/views.py` - BOŞ)**
- [ ] `SubmissionViewSet` (ModelViewSet):
  - [ ] `list` - Yazarın kendi gönderimleri (status filtresi)
  - [ ] `create` - Yeni gönderim (DRAFT olarak)
  - [ ] `retrieve` - Tekil gönderim detayı
  - [ ] `update/partial_update` - Güncelleme (sadece DRAFT ve REVISION_REQUESTED)
  - [ ] `destroy` - Silme (sadece DRAFT)
  - [ ] `@action build_pdf` - PDF oluşturma tetikle (Celery task)
  - [ ] `@action approve` - Yazar onayı
  - [ ] `@action submit` - Gönderiyi tamamla
- [ ] Permissions: `IsAuthenticated + IsOwnerOrReadOnly`
- [ ] Optimization: `select_related('submitter'), prefetch_related('authors', 'files')`

**3. URLs (`backend/apps/submissions/urls.py` - Kontrol edilmeli)**
- [ ] Router registration: `router.register('submissions', SubmissionViewSet)`
- [ ] Endpoints:
  - [ ] `GET/POST /api/v1/submissions/`
  - [ ] `GET/PUT/PATCH/DELETE /api/v1/submissions/{id}/`
  - [ ] `POST /api/v1/submissions/{id}/build_pdf/`
  - [ ] `POST /api/v1/submissions/{id}/approve/`
  - [ ] `POST /api/v1/submissions/{id}/submit/`

**4. File Management (`backend/apps/files/`)**
- [ ] `serializers.py`:
  - [ ] `ManuscriptFileSerializer`
  - [ ] `FileUploadSerializer` (multipart form data)
  - [ ] `FileReorderSerializer` (sıra değiştirme)
- [ ] `views.py` - `ManuscriptFileViewSet`:
  - [ ] `list` - Submission'a ait dosyalar
  - [ ] `create` - Dosya yükleme (S3'e)
  - [ ] `destroy` - Dosya silme
  - [ ] `@action reorder` - Dosya sırası güncelleme (bulk)
  - [ ] `@action presigned_url` - Güvenli indirme URL'i

---

### ✅ Faz 7: Author Module Frontend - %100

**Rapor:** `FAZ-7_Author_Module_Frontend.md`

#### Tamamlanan:
- Submission store (Pinia), TypeScript tipleri, SubmissionTable, SkeletonLoader, AnimatedCounter, StatusBadge
- 6 adımlı wizard: StepArticleType, StepFileUpload (placeholder), StepArticleInfo, StepAuthors, StepAdditionalInfo, StepReviewSubmit
- NewSubmission.vue: ilerleme çubuğu, otomatik kayıt (30 sn), route guard
- Dashboard: store entegrasyonu, SubmissionTable ile liste
- useAutosave composable
- Dosya yükleme gerçek API'ye Faz 8'de bağlanacak; PDF oluşturma Faz 9'da

---

### ❌ Faz 8: S3 Dosya Yönetimi Entegrasyonu - %0

#### Eksikler:

**Backend:**
- [ ] `core/settings/base.py` - S3 ayarları:
  - [ ] `DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'`
  - [ ] `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (env'den)
  - [ ] `AWS_STORAGE_BUCKET_NAME`
  - [ ] `AWS_S3_REGION_NAME`
  - [ ] `AWS_S3_FILE_OVERWRITE = False`
  - [ ] `AWS_DEFAULT_ACL = 'private'`
  - [ ] `AWS_QUERYSTRING_EXPIRE = 900` (15 dakika)
- [ ] `apps/files/services.py` - `FileService`:
  - [ ] `upload_file(file, submission_id, file_type)` - S3'e yükle, ManuscriptFile kaydı oluştur
  - [ ] `delete_file(file_id)` - S3'ten sil, kaydı kaldır
  - [ ] `get_presigned_url(file_id)` - S3'ten imzalı URL al
  - [ ] `reorder_files(submission_id, file_ids_ordered)` - Dosya sıralarını güncelle
- [ ] `apps/files/views.py` - `FileUploadView`:
  - [ ] `POST` - Dosya yükle (multipart)
  - [ ] Validasyonlar:
    - [ ] Max dosya boyutu: 50MB
    - [ ] İzin verilen tipler: `.doc`, `.docx`, `.pdf`, `.jpg`, `.png`, `.tiff`
    - [ ] Submission DRAFT veya REVISION_REQUESTED durumunda olmalı
- [ ] Presigned URL endpoint:
  - [ ] `GET /api/v1/files/{id}/download/`
  - [ ] Dosya sahibi veya editor kontrolü
  - [ ] 15 dakikalık geçerli URL döndür

**Frontend:**
- [ ] `composables/useFileUpload.ts`:
  - [ ] `uploadFile(file, submissionId, fileType)`
  - [ ] Progress tracking
  - [ ] Error handling
  - [ ] Retry logic
- [ ] `components/submission/FileDropzone.vue`:
  - [ ] Drag-and-drop alanı
  - [ ] Dosya tipi ve boyut validasyonu
  - [ ] Upload progress göstergesi
  - [ ] Hata mesajları
- [ ] `components/submission/FileList.vue`:
  - [ ] Yüklenen dosyalar listesi
  - [ ] Sürükle-bırak sıralama (vuedraggable)
  - [ ] Dosya tipi ikonu
  - [ ] Boyut bilgisi
  - [ ] İndirme/Silme butonları

---

### ❌ Faz 9: Celery + WeasyPrint PDF Oluşturma - %0

#### Eksikler:

**Backend:**
- [ ] `core/celery.py`:
  - [ ] Celery app yapılandırması
  - [ ] Redis broker URL (env'den)
  - [ ] Task autodiscover
- [ ] `apps/submissions/tasks.py`:
  - [ ] `@shared_task def generate_submission_pdf(submission_id)`:
    - [ ] Submission'i ve ilgili dosyaları getir
    - [ ] HTML template'i render et (`submission_pdf.html`)
    - [ ] WeasyPrint ile PDF'e çevir
    - [ ] S3'e yükle
    - [ ] `Submission.pdf_file` alanını güncelle
    - [ ] Durumu `PDF_BUILDING -> WAITING_APPROVAL`'a çek
    - [ ] Hata durumunda loglama ve bildirim
- [ ] `templates/pdf/submission_pdf.html`:
  - [ ] Profesyonel PDF şablon
  - [ ] Başlık, yazarlar, özet
  - [ ] Yüklenen dosyaların listesi
  - [ ] Sayfa numaraları
  - [ ] Tarih damgası
  - [ ] Türkçe karakter desteği (@font-face)
- [ ] `apps/submissions/views.py` - `build_pdf` action:
  - [ ] `@action(detail=True, methods=['post'])`
  - [ ] Validasyon: DRAFT durumunda olmalı
  - [ ] FSM transition: `DRAFT -> PDF_BUILDING`
  - [ ] Task: `generate_submission_pdf.delay(submission.id)`
  - [ ] Response: `{'task_id': task.id, 'status': 'processing'}` (202)
- [ ] `apps/submissions/views.py` - `task_status` action:
  - [ ] `@action(detail=True, methods=['get'])`
  - [ ] Task ID'den durum kontrolü
  - [ ] `AsyncResult(task_id)` ile sonuç döndür
- [ ] `static/fonts/`:
  - [ ] Open Sans veya Roboto font dosyaları (Türkçe karakter destekli)
  - [ ] CSS @font-face tanımları

**Frontend:**
- [ ] PDF oluşturma UI:
  - [ ] 'PDF Oluştur' butonu
  - [ ] Loading spinner (işlem sürerken)
  - [ ] Polling ile task durumu kontrolü (her 3 saniye)
  - [ ] Tamamlandığında:
    - [ ] Toast bildirimi
    - [ ] PDF önizleme linki
    - [ ] 'Onayla' butonu aktif
- [ ] `components/submission/PDFPreview.vue`:
  - [ ] iframe ile PDF gösterimi
  - [ ] 'Yeni Sekmede Aç' butonu
  - [ ] 'İndir' butonu

---

### ✅ Faz 4: Deployment - %100

**Not:** Plan'da Railway için, ancak Render kullanıldı. İşlevsel olarak tamamlandı sayılabilir.

- ✅ Backend → Render.com
- ✅ Frontend → Vercel
- ✅ Database → Neon PostgreSQL
- ✅ Cache → Upstash Redis
- ✅ Health check endpoints

---

### 🟡 Faz 10: Logo, Branding ve Landing Page - %70

#### ✅ Mevcut:
- ✅ Landing page var (`views/LandingPage.vue`)
- ✅ Modern tasarım
- ✅ Animasyonlar

#### ❌ Eksikler:

**1. Logo Tasarımı**
- [ ] `frontend/src/assets/images/logo.svg` - Ana logo (Kalem + Belge + Checkmark)
  - [ ] Minimalist, modern çizgi tasarımı
  - [ ] Ana renk: #1e3a5f (koyu mavi)
  - [ ] Vurgu rengi: #3b82f6 (açık mavi)
  - [ ] Boyutlar: 40x40 (ikon), 180x40 (yatay logo)
- [ ] `frontend/src/assets/images/logo-icon.svg` - Sadece ikon versiyonu
  - [ ] 32x32, 64x64, 128x128 boyutları
- [ ] `frontend/src/assets/images/logo-white.svg` - Beyaz versiyon (koyu arka plan için)

**2. Favicon ve App Icons**
- [ ] `public/favicon.ico`
- [ ] `public/apple-touch-icon.png`
- [ ] `public/android-chrome-192x192.png`
- [ ] `public/android-chrome-512x512.png`

**3. Logo Component**
- [ ] `components/common/Logo.vue`:
  - [ ] TruEditor SVG logosu
  - [ ] Farklı boyutlar (sm, md, lg, xl)
  - [ ] Animasyonlu versiyon (hover'da)

---

## 🎨 TASARIM KURALLARI (Plan'dan)

### Renk Paleti
- Primary: `#1e3a5f` (Koyu Mavi) - Ana marka rengi, başlıklar
- Secondary: `#3b82f6` (Açık Mavi) - Butonlar, vurgular
- Accent: `#10b981` (Yeşil) - Başarı mesajları, CTA
- ORCID Green: `#a6ce39` - ORCID butonları
- Warning: `#f59e0b` - Uyarılar, revizyon
- Error: `#ef4444` - Hatalar, red

### Tipografi
- Başlıklar: Inter (Bold, SemiBold)
- Metin: Source Sans Pro (Regular)
- Kod: JetBrains Mono

### UI/UX Kuralları
- Modern, animasyonlu arayüz
- @vueuse/motion ile sayfa geçiş animasyonları
- Skeleton loading tüm listelerde
- Hover efektleri, micro-interactions
- Staggered animations (liste öğeleri için)
- Smooth scroll
- Toast animasyonları (slide-in/fade-out)
- Progress bar animasyonları (wizard adımlarında)

### Emoji Kullanımı
- ❌ **EMOJI KULLANILMAMALI** (ciddiyeti bozuyor)
- ✅ İkonlar: Heroicons kullanılmalı
- ✅ Durum göstergeleri: Badge'ler, renkli noktalar

---

## 📋 ÖNCELİKLİ YAPILACAKLAR (Sırayla)

*(Faz 7 tamamlandı – bkz. FAZ-7_Author_Module_Frontend.md)*

### 1. Faz 8: S3 Dosya Yönetimi (Yüksek Öncelik)
- AWS S3 entegrasyonu
- File upload/download, presigned URL'ler
- StepFileUpload gerçek API'ye bağlama
- Drag & drop component'ler

### 2. Faz 9: PDF Generation (Orta Öncelik)
- Celery task setup
- WeasyPrint entegrasyonu
- PDF template
- Frontend polling (build_pdf, task_status)

### 3. Faz 10: Logo & Branding (Düşük Öncelik)
- Logo tasarımı
- Favicon'lar
- Logo component

---

## 📝 NOTLAR

1. **Emoji Kullanımı:** Tüm sayfalarda emoji kontrolü yapılmalı, kaldırılmalı
2. **Tasarım Tutarlılığı:** Tüm yeni component'ler mevcut tasarım sistemine uygun olmalı
3. **Animasyonlar:** Plan'daki animasyon kurallarına uyulmalı
4. **Responsive:** Tüm yeni sayfalar mobile-first olmalı
5. **TypeScript:** Tüm yeni kod TypeScript ile yazılmalı
6. **Türkçe Yorumlar:** Kod yorumları Türkçe olmalı (plan'a göre)

---

**Son Güncelleme:** 23 Ocak 2026
