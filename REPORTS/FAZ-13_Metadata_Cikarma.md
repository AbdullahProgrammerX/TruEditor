# FAZ-13: Metadata Çıkarma (Extraction)

**Tamamlanma Tarihi:** 2026-03-02  
**Geliştirici:** Abdullah Doğan  

---

## Özet

Yüklenen ana metin dosyasından (DOCX/PDF) başlık, özet ve anahtar kelimeleri otomatik olarak çıkarıp wizard alanlarına dolduran bir metadata çıkarma sistemi geliştirildi.

---

## Backend

### metadata_extractor.py
- **DOCX desteği:** `python-docx` ile
  - Başlık: Document properties + ilk paragraf heuristic
  - Abstract: "Abstract" / "Özet" / "Öz" başlık tespiti
  - Keywords: "Keywords:" / "Anahtar Kelimeler:" / "Anahtar Sözcükler:" pattern
  - Yazar satırlarını atlama (heuristic)
- **PDF desteği:** `pdfplumber` ile
  - Başlık: PDF metadata + ilk satır heuristic  
  - Abstract ve keywords: İlk 3 sayfadan metin çıkarma
- **Hata toleransı:** Çıkarma başarısız olursa sessizce `ExtractedMetadata()` döner
- **Türkçe + İngilizce:** Her iki dilde bölüm başlıkları tanınır

### API Endpoint
- `POST /api/v1/files/{id}/extract_metadata/`
- Sadece `main_text` ve `revision` dosyaları
- Response: `{ extracted: bool, title?, abstract?, keywords[] }`

### Bağımlılıklar
- `pdfplumber>=0.10` eklendi (python-docx zaten mevcuttu)

---

## Frontend

### useFileUpload Composable
- `extractMetadata(fileId)` fonksiyonu eklendi
- `lastExtractedMetadata` reactive ref
- `main_text` veya `revision` yükleme sonrası otomatik `extract_metadata` çağrısı

### StepFileUpload Component
- `metadataExtracted` emit eklendi
- `lastExtractedMetadata` watch ile parent'a bildirim

### NewSubmission Wizard
- `onMetadataExtracted` handler
- Boş alanları otomatik doldurur (title, abstract, keywords)
- Dolu alanları dokunmaz (kullanıcı verisi korunur)
- Toast bildirimi: "Auto-filled from file: title, abstract, keywords"

---

## Değişen Dosyalar

| Dosya | Tür |
|-------|-----|
| `backend/apps/files/metadata_extractor.py` | Yeni |
| `backend/apps/files/views.py` | Güncelleme |
| `backend/requirements/base.txt` | Güncelleme |
| `frontend/src/composables/useFileUpload.ts` | Güncelleme |
| `frontend/src/components/submission/wizard/StepFileUpload.vue` | Güncelleme |
| `frontend/src/views/submission/NewSubmission.vue` | Güncelleme |
