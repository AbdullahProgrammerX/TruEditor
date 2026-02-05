# Faz 7: Author Module Frontend (Submission Wizard) - Tamamlandı

**Tarih:** 23 Ocak 2026  
**Durum:** Tamamlandı

---

## Özet

Faz 7 kapsamında Author Module için frontend tamamlandı. Makale gönderim sihirbazı (6 adım), submission state yönetimi (Pinia), dashboard entegrasyonu, ortak bileşenler ve TypeScript tipleri eklendi. Dosya yükleme adımı Faz 8 (S3) ile gerçek API'ye bağlanacak şekilde placeholder olarak bırakıldı.

---

## Tamamlanan İşlemler

### 1. TypeScript Tipleri

**Dosya:** `frontend/src/types/submission.ts`

- **SubmissionStatus**, **ArticleType**, **FileType**, **Language** – enum benzeri tipler ve display sabitleri
- **Author**, **AuthorInput** – yazar verisi
- **ManuscriptFile** – dosya bilgisi
- **SubmissionListItem**, **Submission** – liste ve detay
- **SubmissionCreateInput**, **SubmissionUpdateInput** – API payload
- **WizardData**, **SuggestedReviewer**, **OpposedReviewer** – wizard verisi
- **PaginatedResponse**, **SubmissionFilters**, **SubmissionStats** – API ve dashboard

**Dosya:** `frontend/src/types/index.ts` – tiplerin merkezi export’u

### 2. Submission Store (Pinia)

**Dosya:** `frontend/src/stores/submission.ts`

- **State:** submissions, currentSubmission, filters, wizardStep, wizardData, isDirty, loading/saving
- **Liste:** fetchSubmissions, setPage, setPageSize, filterByStatus, search, clearFilters
- **CRUD:** fetchSubmission, createSubmission, updateSubmission, deleteSubmission
- **Aksiyonlar:** submitForReview, withdraw
- **Yazarlar:** addAuthor, updateAuthor, removeAuthor, reorderAuthors
- **Wizard:** setWizardStep, nextStep, prevStep, updateWizardData, saveWizardProgress, resetWizard
- **Getters:** stats, draftCount, submittedCount, revisionCount, acceptedCount, byStatus, totalPages, isEditable

### 3. Ortak Bileşenler

**Dosya:** `frontend/src/components/common/SkeletonLoader.vue`

- Tipler: text, card, table, avatar, button, custom
- Shimmer animasyonu, satır/sütun sayısı ayarı

**Dosya:** `frontend/src/components/common/AnimatedCounter.vue`

- Hedef değere sayma animasyonu
- Easing (linear, easeOut, easeInOut), prefix/suffix, ayırıcı

**Dosya:** `frontend/src/components/common/StatusBadge.vue`

- Submission durumu için renkli badge (SUBMISSION_STATUS sabitleriyle)
- Boyut: sm, md, lg; opsiyonel ikon

### 4. Submission Bileşenleri

**Dosya:** `frontend/src/components/submission/SubmissionTable.vue`

- Skeleton loading, boş durum (Lottie yerine ikon)
- Kolonlar: Manuscript (başlık, ID, tip), Status, Authors, Last Updated, Actions
- StatusBadge, dropdown menü (View, Edit, Delete)
- Pagination (Previous/Next)
- Emit: pageChange, delete, view, edit

**Wizard adımları:** `frontend/src/components/submission/wizard/`

| Adım | Bileşen | Açıklama |
|------|---------|----------|
| 1 | StepArticleType.vue | Makale tipi seçimi (radio), ARTICLE_TYPES ile |
| 2 | StepFileUpload.vue | Drag-and-drop, dosya tipi seçimi, simüle yükleme (Faz 8’de S3) |
| 3 | StepArticleInfo.vue | Başlık, özet (max 5000), anahtar kelimeler (3–10), dil |
| 4 | StepAuthors.vue | Yazar listesi, modal (ad/soyad, email, kurum, ORCID, corresponding), sıra (yukarı/aşağı) |
| 5 | StepAdditionalInfo.vue | Cover letter, etik, conflict of interest, funding, önerilen/reddedilen hakemler (max 3), editöre not |
| 6 | StepReviewSubmit.vue | Özet kartları, “Edit” linkleri, onay checkbox, Submit Manuscript |

### 5. NewSubmission.vue (Wizard Konteyner)

**Dosya:** `frontend/src/views/submission/NewSubmission.vue`

- 6 adımlı wizard, üstte ilerleme çubuğu ve adım göstergeleri
- Adım geçişi: sadece tamamlanmış/mevcut adıma tıklanabilir
- Validasyon: her adım için canGoNext (article type, dosya, başlık/özet/keywords, yazarlar)
- Otomatik kayıt: 30 saniyede bir saveProgress; header’da “Saving…” / “Saved …”
- Yeni gönderim: createSubmission; sonra updateSubmission ile wizard_step ve wizard_data
- Final submit: saveProgress → addAuthor (döngü) → submitForReview → dashboard’a yönlendirme
- Route guard: onBeforeRouteLeave ile kaydedilmemiş değişiklik uyarısı
- Transition: fade + slide ile adım değişimi

### 6. Auto-save Composable

**Dosya:** `frontend/src/composables/useAutosave.ts`

- useAutosave(data, saveFn, options): delay (debounce), interval
- isSaving, lastSavedAt, error, isDirty, statusText
- save(), resetDirty(), cancel()

### 7. Dashboard Entegrasyonu

**Dosya:** `frontend/src/views/dashboard/Dashboard.vue`

- useSubmissionStore, SubmissionTable kullanımı
- İstatistikler: stats (draft, submitted, underReview, accepted) store’dan
- totalSubmissions store’dan
- onMounted: submissionStore.fetchSubmissions()
- “My Submissions” bölümü: SubmissionTable (items, loading, currentPage, totalPages)
- handlePageChange, handleDeleteSubmission; viewSubmission(id: string) ile detay sayfasına gidiş
- Eski mock recentSubmissions ve getStatusStyles kaldırıldı

---

## Oluşturulan / Güncellenen Dosyalar

| Dosya | İşlem |
|-------|--------|
| frontend/src/types/submission.ts | Yeni |
| frontend/src/types/index.ts | Yeni |
| frontend/src/stores/submission.ts | Yeni |
| frontend/src/components/common/SkeletonLoader.vue | Yeni |
| frontend/src/components/common/AnimatedCounter.vue | Yeni |
| frontend/src/components/common/StatusBadge.vue | Yeni |
| frontend/src/components/submission/SubmissionTable.vue | Yeni |
| frontend/src/components/submission/wizard/StepArticleType.vue | Yeni |
| frontend/src/components/submission/wizard/StepFileUpload.vue | Yeni |
| frontend/src/components/submission/wizard/StepArticleInfo.vue | Yeni |
| frontend/src/components/submission/wizard/StepAuthors.vue | Yeni |
| frontend/src/components/submission/wizard/StepAdditionalInfo.vue | Yeni |
| frontend/src/components/submission/wizard/StepReviewSubmit.vue | Yeni |
| frontend/src/composables/useAutosave.ts | Yeni |
| frontend/src/views/submission/NewSubmission.vue | Güncellendi |
| frontend/src/views/dashboard/Dashboard.vue | Güncellendi |

---

## Teknik Notlar

- **Tailwind v4:** Scoped stillerde `@apply` kullanılmadı; düz CSS (padding, border, border-radius vb.) kullanıldı.
- **API:** Store, `api.get/post/patch/delete` ile `/submissions/` ve `/submissions/{id}/` kullanıyor. Backend Faz 6 ile uyumludur.
- **Yazar endpoint’i:** Store’da addAuthor, updateAuthor, removeAuthor, reorderAuthors tanımlı; backend’de nested veya ayrı author endpoint’leri varsa URL’ler buna göre güncellenebilir.
- **Dosya yükleme:** StepFileUpload şu an simüle ilerleme ve lokal state kullanıyor; Faz 8’de `/files/` ve S3 presigned URL ile değiştirilecek.

---

## Bilinen Sınırlamalar

1. Dosya yükleme (Adım 2) gerçek API’ye bağlı değil; Faz 8’de tamamlanacak.
2. Backend’de author endpoint’leri nested (`/submissions/{id}/authors/`) veya ayrı ise store’daki path’ler kontrol edilmeli.
3. PDF oluşturma (build_pdf) ve task_status frontend’de henüz kullanılmıyor; Faz 9 ile entegre edilebilir.

---

## Sonraki Adımlar

- **Faz 8:** S3 dosya yönetimi, gerçek dosya yükleme ve StepFileUpload entegrasyonu
- **Faz 9:** Celery + WeasyPrint ile PDF oluşturma; wizard son adımda “PDF Oluştur” ve önizleme

---

**Rapor sonu.**
