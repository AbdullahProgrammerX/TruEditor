# FAZ-16: Yazışma Geçmişi & Karar Mektubu

**Tarih:** 2026-03-11  
**Durum:** Tamamlandı

---

## Yapılanlar

### 1. Correspondence Modeli (Backend)

- **`Correspondence`** modeli `submissions` app'ine eklendi
- Alanlar: `submission`, `sender`, `message_type`, `subject`, `body`, `is_read`, `read_at`
- 4 mesaj tipi: `author_to_editor`, `editor_to_author`, `decision_letter`, `system`
- `mark_read()` metodu ile okundu işaretleme
- Django Admin'de `CorrespondenceAdmin` kaydı

### 2. API Endpoint'leri

- **`GET /submissions/{id}/correspondence/`** — Tüm yazışmaları listeler, editör mesajlarını otomatik okundu işaretler
- **`POST /submissions/{id}/correspondence/`** — Yazar editöre mesaj gönderir (draft hariç)
- Yeni mesaj gönderildiğinde atanmış editöre e-posta bildirimi

### 3. Frontend: Messages Sekmesi

- Submission Detail sayfasına **"Messages"** sekmesi eklendi (5 sekme oldu)
- Mesaj thread'i: Yazar mesajları sağda (primary), editör mesajları solda (blue)
- Okunmamış mesaj sayısı tab'da kırmızı badge ile gösterilir
- **Karar mektubu** özel yeşil kutuda ayrı görüntülenir

### 4. Mesaj Gönderme Formu

- Subject (opsiyonel) + body textarea
- "Send Message" butonu (loading state ile)
- Draft submission'larda form devre dışı

---

## Değiştirilen Dosyalar

| Dosya | Değişiklik |
|-------|-----------|
| `backend/apps/submissions/models.py` | `Correspondence` modeli eklendi |
| `backend/apps/submissions/serializers.py` | `CorrespondenceSerializer`, `CorrespondenceCreateSerializer` |
| `backend/apps/submissions/views.py` | `correspondence` action endpoint (GET/POST) |
| `backend/apps/submissions/admin.py` | `CorrespondenceAdmin` kaydı |
| `backend/apps/submissions/migrations/0006_correspondence.py` | Migration |
| `frontend/src/types/submission.ts` | `CorrespondenceMessage` interface |
| `frontend/src/stores/submission.ts` | `sendCorrespondence`, `fetchCorrespondence` actions |
| `frontend/src/views/submission/SubmissionDetail.vue` | Messages tab, mesaj gönderme formu, karar mektubu UI |

---

## Mesaj Tipleri

| Tip | Açıklama | UI |
|-----|----------|----|
| `author_to_editor` | Yazarın editöre gönderdiği | Sağ hizalı, primary renk |
| `editor_to_author` | Editörün yazara gönderdiği | Sol hizalı, blue renk |
| `decision_letter` | Karar mektubu | Özel yeşil kutu, üstte gösterilir |
| `system` | Sistem mesajı | Gri, ortalanmış |
