# FAZ-17: Ortak Yazar Erişimi & Doğrulama

**Tarih:** 2026-03-27  
**Durum:** Tamamlandı

---

## Yapılanlar

### 1. Author Model Güncellemesi (Backend)

- **`VerificationStatus`** enum eklendi: `pending`, `verified`, `declined`, `not_required`
- Yeni alanlar: `verification_status`, `verification_token` (UUID, unique), `verified_at`, `notified_at`
- `is_submitter` property: Yazarın aynı zamanda gönderici olup olmadığını kontrol eder
- Yeni index: `(user, verification_status)` — co-author sorgularını hızlandırır
- Migration: `0007_add_author_verification_fields`

### 2. İzin Sistemi (Permissions)

- `IsOwnerOrReadOnly` → `IsOwnerOrCoAuthorReadOnly` olarak yeniden adlandırıldı
- `is_coauthor()` helper fonksiyonu: `Author.user` üzerinden ortak yazarlık kontrolü
- Submitter: okuma + yazma izni
- Co-author: yalnızca okuma izni (GET)
- Edit, delete, withdraw gibi işlemler yalnızca submitter'a açık

### 3. Queryset & Filtreleme

- `get_queryset()` güncellendi: Kullanıcının kendi gönderimlerini VE ortak yazar olduğu gönderimlerini döner
- Draft durumundaki gönderimler co-author listesinden hariç tutulur
- `?role=mine` / `?role=coauthor` query parametresi ile rol bazlı filtreleme
- `?status=...` ile mevcut durum filtresi korunur

### 4. Doğrulama Endpoint'leri (Public)

- **`POST /api/v1/submissions/verify/<token>/`** — Token ile katkı doğrulama (auth gerekmez)
- **`POST /api/v1/submissions/verify/<token>/decline/`** — Token ile yazarlık reddetme
- Her iki endpoint GET isteklerini de kabul eder (e-posta linkinden tıklama)
- Reddetme durumunda submitter'a otomatik e-posta bildirimi
- İdempotent: Zaten doğrulanmış/reddedilmiş kayıtlar için uygun mesaj döner

### 5. Bildirim Sistemi

- **`notify-coauthors`** action endpoint'i: Submitter manuel bildirim tetikler
- **Otomatik bildirim:** Makale submit edildiğinde tüm co-author'lara bildirim gönderilir
- `COAUTHOR_NOTIFICATION` email tipi `EmailLog.EmailType`'a eklendi
- `send_coauthor_notification()` fonksiyonu oluşturuldu
- **`coauthor_notification.html`** e-posta şablonu: Makale bilgileri, yazar sırası, verify/decline butonları

### 6. Serializer Güncellemeleri

- `AuthorshipSerializer`: `verification_status`, `verification_status_display`, `verified_at`, `notified_at` alanları
- `SubmissionListSerializer`: `role` alanı (`submitter` veya `coauthor`)
- `SubmissionDetailSerializer`: `role` alanı eklendi

### 7. Frontend: Submission Listesi

- **Role sütunu** eklendi: "Submitter" (mavi) veya "Co-Author" (amber) badge
- **Rol filtre tabs:** All / My Submissions / Co-authored — URL query ile senkronize
- Co-author gönderilerinde edit ve delete butonları otomatik gizlenir

### 8. Frontend: Submission Detay Sayfası

- **Co-author banner:** Sayfanın üstünde "You are a co-author on this submission" bilgilendirmesi
- Write aksiyonlar (edit, delete, withdraw, generate PDF, send message) co-author için gizli
- PDF indirme/görüntüleme herkes için erişilebilir
- **Authors tab'ında verification badge'leri:**
  - Yeşil: Verified (onay ikonu)
  - Sarı: Pending
  - Kırmızı: Declined
- Correspondence: "Only the submitter can send messages to the editor." uyarısı

### 9. Frontend: Doğrulama Sayfası

- **`/verify/:token`** — Katkı doğrulama sayfası (public, auth gerekmez)
- **`/verify/:token/decline`** — Yazarlık reddetme sayfası
- Başarılı doğrulama: Yeşil başlık, makale bilgileri
- Başarılı reddetme: Turuncu/kırmızı başlık, submitter bilgilendirildi mesajı
- Hata durumu: Geçersiz veya süresi dolmuş link mesajı
- Loading state: Animasyonlu spinner

### 10. TypeScript Tip Güncellemeleri

- `VerificationStatus` tipi eklendi
- `Author` interface'ine verification alanları eklendi
- `SubmissionRole` tipi: `submitter` | `coauthor`
- `SubmissionListItem` ve `Submission` interface'lerine `role` eklendi
- `SubmissionFilters`'a `role` eklendi

---

## Değiştirilen Dosyalar

### Backend
| Dosya | Değişiklik |
|---|---|
| `apps/submissions/models.py` | Author modeline verification alanları ve VerificationStatus enum |
| `apps/submissions/views.py` | Co-author queryset, verify/decline endpoints, notify-coauthors action |
| `apps/submissions/serializers.py` | role alanı, verification status alanları |
| `apps/submissions/permissions.py` | IsOwnerOrCoAuthorReadOnly, is_coauthor helper |
| `apps/submissions/urls.py` | verify ve decline public URL'leri |
| `apps/submissions/admin.py` | AuthorAdmin'e verification_status ve readonly alanları |
| `apps/notifications/email_service.py` | send_coauthor_notification fonksiyonu |
| `apps/notifications/models.py` | COAUTHOR_NOTIFICATION email tipi |
| `templates/email/coauthor_notification.html` | Co-author bildirim e-posta şablonu |
| `apps/submissions/migrations/0007_...` | Author verification alanları migration |

### Frontend
| Dosya | Değişiklik |
|---|---|
| `src/types/submission.ts` | VerificationStatus, SubmissionRole, role alanları |
| `src/stores/submission.ts` | role filtre parametresi desteği |
| `src/router/index.ts` | /verify/:token rotaları |
| `src/components/submission/SubmissionTable.vue` | Role sütunu, co-author edit/delete gizleme |
| `src/views/submission/SubmissionsList.vue` | Role filter tabs UI |
| `src/views/submission/SubmissionDetail.vue` | Co-author banner, read-only kısıtlamalar, verification badges |
| `src/views/submission/VerifyContribution.vue` | Yeni sayfa: public doğrulama/reddetme |

---

## API Endpoint Özeti

| Method | URL | Auth | Açıklama |
|---|---|---|---|
| GET | `/api/v1/submissions/?role=coauthor` | JWT | Co-author gönderimlerini filtrele |
| POST | `/api/v1/submissions/{id}/notify-coauthors/` | JWT | Co-author bildirimlerini gönder |
| POST/GET | `/api/v1/submissions/verify/{token}/` | Public | Katkı doğrula |
| POST/GET | `/api/v1/submissions/verify/{token}/decline/` | Public | Yazarlığı reddet |

---

## Akış Diyagramı

```
Yazar makaleyi submit eder
         │
         ▼
  ┌─────────────────┐
  │ Co-author'lara   │
  │ otomatik e-posta │
  │ gönderilir       │
  └────────┬────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  [Verify]   [Decline]
     │           │
     ▼           ▼
  status =    status =
  verified    declined
     │           │
     │           ▼
     │     Submitter'a
     │     bildirim
     ▼
  Co-author artık
  gönderiyi görebilir
  (read-only)
```
