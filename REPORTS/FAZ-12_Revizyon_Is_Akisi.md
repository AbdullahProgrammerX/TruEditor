# FAZ-12: Revizyon İş Akışı

**Tamamlanma Tarihi:** 2026-03-02  
**Geliştirici:** Abdullah Doğan  

---

## Özet

Yazarların editör tarafından istenen revizyonları yönetebilmesi için kapsamlı bir revizyon iş akışı geliştirildi. Sistem, versiyonlama, hakem yanıtı ve dosya yönetimini içerir.

---

## Backend Değişiklikleri

### Model Güncellemeleri
- `Submission` modeline eklenen alanlar:
  - `revision_response` (TextField) — Yazarın hakem yorumlarına yanıtı
  - `revision_submitted_at` (DateTimeField) — Revizyonun gönderilme zamanı
- `submit_revision()` FSM geçişi güncellendi (timestamp kaydı)
- Dosya yükleme sırasında `revision_number` otomatik olarak atanıyor

### API Endpoints
- `POST /api/v1/submissions/{id}/submit_revision/` — Revizyon gönderimi
  - `revision_response` zorunlu alan
  - FSM: `revision_required` → `revision_submitted`
  - Status history kaydı
  - E-posta bildirimi (status_change şablonu)

### Migration
- `0005_add_revision_response_fields` — revision_response + revision_submitted_at

---

## Frontend Değişiklikleri

### Yeni Sayfa: SubmitRevision.vue
**Route:** `/submissions/:id/revise`

Sayfa bileşenleri:
1. **Editör Notları Kartı** — Revizyon isteği detayları ve deadline
2. **Hakemlere Yanıt** — Textarea (min 20 karakter)
3. **Dosya Yükleme** — Revizyon dosyaları (drag & drop)
4. **Önceki Dosyalar** — Eski revizyonlardan dosyalar (read-only)
5. **Sidebar** — Submit butonu, checklist, revizyon bilgileri
6. **Onay Modalı** — Son doğrulama

### Detail Sayfası Güncellemeleri
- `revision_required` durumunda "Submit Revision" butonu
- Additional sekmesinde editör isteği + yazar yanıtı birlikte gösterim
- Yazar yanıtı tarihiyle birlikte mor renk temasıyla gösterilir

### Store Güncellemeleri
- `submitRevision(id, revisionResponse)` action eklendi
- TypeScript tipleri güncellendi

---

## Dosya Yönetimi

- Yüklenen dosyalar otomatik olarak `submission.revision_number` ile etiketlenir
- Revizyon sayfasında yalnızca mevcut revizyon numarasına ait dosyalar gösterilir
- Önceki revizyonlardaki dosyalar ayrı bölümde, salt okunur olarak listelenir
- `system_pdf` dosyaları listelerden filtrelenir

## İş Akışı

```
Editor: request_revision(notes, deadline) → revision_required [revision_number++]
Author: Dosya yükle + Yanıt yaz → submit_revision → revision_submitted
Editor: Kabul veya yeni revizyon isteyebilir
```

---

## Değişen Dosyalar

| Dosya | Tür |
|-------|-----|
| `backend/apps/submissions/models.py` | Güncelleme |
| `backend/apps/submissions/views.py` | Güncelleme |
| `backend/apps/submissions/serializers.py` | Güncelleme |
| `backend/apps/files/serializers.py` | Güncelleme |
| `backend/apps/submissions/migrations/0005_*.py` | Yeni |
| `frontend/src/views/submission/SubmitRevision.vue` | Yeni |
| `frontend/src/views/submission/SubmissionDetail.vue` | Güncelleme |
| `frontend/src/stores/submission.ts` | Güncelleme |
| `frontend/src/types/submission.ts` | Güncelleme |
| `frontend/src/router/index.ts` | Güncelleme |
