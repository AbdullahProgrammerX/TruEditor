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
| **Faz 4** | ⏳ pending | 🟡 Kısmen | %20 |
| **Faz 5** | ⏳ pending | 🟡 Kısmen | %30 |
| **Faz 6** | ⏳ pending | ❌ Yapılmadı | %0 |
| **Faz 7** | ⏳ pending | ❌ Yapılmadı | %0 |
| **Faz 8** | ⏳ pending | ✅ Tamamlandı* | %100 |
| **Faz 9** | ⏳ pending | 🟡 Kısmen | %70 |

*Not: Faz 8 plan'da Railway için, ancak Render kullanıldı - işlevsel olarak tamamlandı sayılabilir.

---

## ❌ EKSİK FAZLAR (Detaylı)

### 🔴 Faz 4: Author Module Backend API - %20

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

### 🟡 Faz 5: Author Module Frontend - %30

#### ✅ Mevcut:
- `views/dashboard/Dashboard.vue` - Dashboard sayfası var (modern tasarım)
- `views/submission/NewSubmission.vue` - Skeleton var (placeholder)
- `views/submission/SubmissionDetail.vue` - Skeleton var

#### ❌ Eksikler:

**1. Dashboard İyileştirmeleri**
- [ ] `components/submission/SubmissionTable.vue` - Submission listesi component'i
  - [ ] Skeleton loading
  - [ ] Kolonlar: ID, Başlık, Durum, Tarih, İşlemler
  - [ ] Staggered fade-in animasyonları
  - [ ] Durum badge'leri (renkli, pill şeklinde)
  - [ ] İşlemler dropdown menu (animasyonlu açılma)
  - [ ] Pagination (animasyonlu geçiş)
  - [ ] Status filtresi (dropdown, animasyonlu)
  - [ ] Boş durum: Lottie animasyonu
- [ ] `components/common/AnimatedCounter.vue` - Sayıların yukarı doğru sayma animasyonu
- [ ] `components/common/SkeletonLoader.vue` - Kart ve tablo skeleton'ları, shimmer efekti
- [ ] `stores/submission.ts` - Submission state management:
  - [ ] State: `submissions[]`, `currentSubmission`, `isLoading`, `error`
  - [ ] Actions: `fetchSubmissions`, `fetchSubmission`, `createSubmission`, `updateSubmission`, `deleteSubmission`
  - [ ] Filters: `byStatus`
  - [ ] Getters: `draftCount`, `submittedCount`, `revisionCount`, `acceptedCount`

**2. Submission Wizard (6 Adım) - `views/submission/SubmissionWizard.vue`**
- [ ] Stepper component (üst kısımda ilerleme göstergesi)
- [ ] **Adım 1: `components/submission/wizard/StepArticleType.vue`**
  - [ ] Radio button grubu ile makale tipi seçimi
  - [ ] Her tip için kısa açıklama
  - [ ] Seçim yapılmadan ilerleme engeli
- [ ] **Adım 2: `components/submission/wizard/StepFileUpload.vue`**
  - [ ] Drag-and-drop alan (vuedraggable)
  - [ ] Dosya tipi seçimi (Ana Belge, Kapak Mektubu, Şekil, Tablo, Ek)
  - [ ] Yükleme progress bar
  - [ ] Dosya listesi (sürükle-bırak ile sıralama)
  - [ ] Dosya silme
  - [ ] Desteklenen formatlar bilgisi
- [ ] **Adım 3: `components/submission/wizard/StepArticleInfo.vue`**
  - [ ] Başlık input (required)
  - [ ] Özet textarea (karakter sayacı ile, max 500)
  - [ ] Anahtar kelimeler (tag input, min 3, max 6)
  - [ ] Word dosyasından otomatik çıkarılan verileri göster (varsa)
  - [ ] 'Dosyadan Çek' butonu
- [ ] **Adım 4: `components/submission/wizard/StepAuthors.vue`**
  - [ ] Yazar listesi (sıra numarası ile)
  - [ ] Yazar ekleme modal:
    - [ ] Ad, Soyad, Email, Kurum, ORCID
    - [ ] 'Sorumlu Yazar mı?' checkbox
  - [ ] Sürükle-bırak ile sıra değiştirme
  - [ ] Yazar düzenleme ve silme
  - [ ] En az 1 sorumlu yazar zorunlu
- [ ] **Adım 5: `components/submission/wizard/StepAdditionalInfo.vue`**
  - [ ] Hakem önerileri (opsiyonel) - Ad, Email, Kurum (3 adete kadar)
  - [ ] Hakem itirazı (opsiyonel)
  - [ ] Editöre not (textarea)
  - [ ] Çıkar çatışması beyanı (checkbox)
- [ ] **Adım 6: `components/submission/wizard/StepReviewSubmit.vue`**
  - [ ] Tüm girilen bilgilerin özeti
  - [ ] Dosya listesi önizleme
  - [ ] Yazar listesi
  - [ ] 'PDF Oluştur' butonu
  - [ ] PDF hazır olduğunda:
    - [ ] PDF önizleme (iframe veya yeni sekmede)
    - [ ] 'Onayla ve Gönder' butonu
    - [ ] 'Düzenle' butonu

**3. Wizard State Management**
- [ ] `stores/submission.ts` - Wizard state:
  - [ ] `currentStep`, `totalSteps`
  - [ ] `formData` (tüm adım verileri)
  - [ ] `isDirty` (kaydedilmemiş değişiklik var mı)
  - [ ] `autosave` (30 saniyede bir backend'e PUT)
- [ ] `composables/useAutosave.ts`:
  - [ ] Debounced autosave logic
  - [ ] Kayıt durumu göstergesi (Kaydediliyor... / Kaydedildi)

**4. Navigation**
- [ ] İleri/Geri butonları
- [ ] Adım atlama (tamamlanmış adımlara)
- [ ] Sayfa kapatma uyarısı (isDirty ise)

**5. Emoji Temizliği**
- [ ] `NewSubmission.vue` - Emoji'ler kaldırılmalı (plan'a göre ciddiyet bozuyor)
- [ ] Tüm sayfalarda emoji kontrolü

---

### ❌ Faz 6: S3 Dosya Yönetimi Entegrasyonu - %0

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

### ❌ Faz 7: Celery + WeasyPrint PDF Oluşturma - %0

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

### ✅ Faz 8: Deployment - %100

**Not:** Plan'da Railway için, ancak Render kullanıldı. İşlevsel olarak tamamlandı sayılabilir.

- ✅ Backend → Render.com
- ✅ Frontend → Vercel
- ✅ Database → Neon PostgreSQL
- ✅ Cache → Upstash Redis
- ✅ Health check endpoints

---

### 🟡 Faz 9: Logo, Branding ve Landing Page - %70

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

### 1. Faz 4: Author Module Backend API (Yüksek Öncelik)
- Submission serializers
- Submission views (CRUD + actions)
- File management serializers & views
- URL routing

### 2. Faz 5: Author Module Frontend (Yüksek Öncelik)
- Submission wizard (6 adım)
- Dashboard iyileştirmeleri
- State management (Pinia store)
- Auto-save composable
- Emoji temizliği

### 3. Faz 6: S3 Dosya Yönetimi (Yüksek Öncelik)
- AWS S3 entegrasyonu
- File upload/download
- Presigned URL'ler
- Drag & drop component'ler

### 4. Faz 7: PDF Generation (Orta Öncelik)
- Celery task setup
- WeasyPrint entegrasyonu
- PDF template
- Frontend polling

### 5. Faz 9: Logo & Branding (Düşük Öncelik)
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

**Son Güncelleme:** 13 Ocak 2026, 20:30
