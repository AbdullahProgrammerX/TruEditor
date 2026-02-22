# FAZ-10: PDF Oluşturma & Önizleme — Tamamlandı

**Tarih:** 23 Ocak 2026  
**Geliştirici:** Abdullah Doğan  
**Commit:** `5818aeb` — `feat(FAZ-10): PDF generation and preview with WeasyPrint`

---

## Özet

Bu fazda, gönderilerin profesyonel bir PDF belgesine dönüştürülmesi ve tarayıcı içinde önizlenebilmesi sağlandı. WeasyPrint birincil motor olarak kullanılırken, xhtml2pdf yedek (fallback) olarak eklendi.

---

## Backend Değişiklikleri

### 1. PDF Şablonu (`backend/templates/pdf/submission.html`)
- **Kapak sayfası:** TruEditor markası, makale türü, başlık, yazarlar, manuscript ID, dil, tarih
- **Özet bölümü:** Türkçe/İngilizce abstract desteği
- **Anahtar kelimeler:** Badge stilinde gösterim
- **Yazarlar bölümü:** İsim, kurum, e-posta, ORCID, katkı, corresponding author
- **Dosyalar tablosu:** Yüklenen dosyaların listesi
- **Ek bilgiler:** Ön yazı, etik beyanı, çıkar çatışması, fonlama
- **Sayfa numaralandırma** ve **header/footer**

### 2. PDF Servisi (`backend/apps/submissions/pdf_service.py`)
- `generate_submission_pdf()` — Ana fonksiyon
  - Submission verilerini Django template'e render eder
  - HTML'i PDF'e çevirir (WeasyPrint → xhtml2pdf → reportlab fallback)
  - Önceki system_pdf'leri deaktif eder (soft delete)
  - Yeni PDF'i ManuscriptFile olarak R2/local storage'a kaydeder
- **3 seviyeli fallback zinciri:**
  1. WeasyPrint (tam CSS desteği, profesyonel çıktı)
  2. xhtml2pdf (pure Python, system dependency gerektirmez)
  3. reportlab (minimal text-only PDF)

### 3. `build_pdf` Endpoint Güncellemesi (`views.py`)
- **Önceki:** Stub "Phase 7'de gelecek" mesajı
- **Şimdi:** Gerçek PDF oluşturma + presigned download URL dönüşü
- Endpoint: `POST /api/v1/submissions/{id}/build_pdf/`
- Response: `file_id`, `filename`, `file_size`, `download_url`

### 4. Yeni Dosya Tipi: `system_pdf`
- `ManuscriptFile.FileType.SYSTEM_PDF` eklendi
- Migration: `0003_add_system_pdf_file_type`

### 5. Bağımlılıklar
- `xhtml2pdf>=0.2.11` — requirements/base.txt'e eklendi (fallback)
- `build.sh` — WeasyPrint system paketleri (libpango, libpangocairo, fonts-liberation vb.)

---

## Frontend Değişiklikleri

### 1. Submission Detail Page (`SubmissionDetail.vue`)
- **"Generate PDF" / "Regenerate PDF" butonu** — Sağ sidebar Actions bölümünde
  - Loading animasyonu (spinner) PDF oluşturulurken
  - Daha önce PDF oluşturulmuşsa "Regenerate PDF" olarak gösterir
- **"View / Download PDF" butonu** — PDF oluşturulduktan sonra görünür
  - Presigned URL ile tarayıcının native PDF viewer'ında açar
  - Mevcut system_pdf dosyası varsa doğrudan onu indirir
- `system_pdf` dosya tipi file listesinden gizlenir (kullanıcı dosyalarıyla karışmaması için)

### 2. Type Güncellemeleri (`submission.ts`)
- `system_pdf` FileType olarak eklendi
- FILE_TYPES mapping güncellendi

---

## Teknik Notlar

| Konu | Detay |
|------|-------|
| **PDF Motoru** | WeasyPrint (birincil), xhtml2pdf (yedek) |
| **Çalışma Modu** | Senkron (Celery gerektirmez) |
| **Depolama** | ManuscriptFile olarak R2/S3/local'a kaydedilir |
| **Versiyonlama** | Her yeni oluşturmada önceki system_pdf deaktif edilir |
| **Dosya Adı Formatı** | `{MANUSCRIPT_ID}_{YYYYMMDD_HHMMSS}.pdf` |
| **Boyut Tahmini** | ~50-200KB (metin ağırlıklı submission'lar için) |

---

## Test Kontrol Listesi

- [x] PDF template render kontrolü
- [x] TypeScript build başarılı (vue-tsc + vite build)
- [x] Django system check sorunsuz
- [x] Migration sorunsuz çalışıyor
- [x] Frontend "Generate PDF" butonu doğru konumda
- [x] Mevcut PDF varken "Regenerate PDF" yazısı gösteriyor
- [x] system_pdf dosya listesinden gizleniyor
