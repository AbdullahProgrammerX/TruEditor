# FAZ-11: E-posta Bildirim Sistemi — Tamamlandı

**Tarih:** 23 Ocak 2026  
**Geliştirici:** Abdullah Doğan  
**Commit:** `a384c2c` — `feat(FAZ-11): email notification system with preferences and HTML templates`

---

## Özet

E-posta bildirim sistemi kuruldu. Kullanıcılar artık gönderim, durum değişikliği ve geri çekme işlemleri sonrasında HTML formatlı bildirim e-postası alacak. Profil sayfasından bildirim tercihleri yönetilebilir.

---

## Backend Değişiklikleri

### 1. Models (`apps/notifications/models.py`)

**EmailLog** — Her gönderilen e-postanın kaydı:
- `email_type`: welcome, submission_confirmation, status_change, withdrawal_confirmation, revision_request, decision, other
- `status`: pending, sent, failed
- `error_message`: Hata durumunda detay
- İlişkiler: `recipient` (User), `submission` (Submission)

**EmailPreference** — Kullanıcı başına bildirim tercihleri:
- `submission_confirmation` — Gönderim onayı
- `status_updates` — Durum değişiklikleri
- `revision_requests` — Revizyon talepleri
- `decision_notifications` — Editöryal kararlar
- `system_announcements` — Sistem duyuruları
- `get_for_user()` class method ile otomatik oluşturma

### 2. Email Service (`apps/notifications/email_service.py`)
Merkezi e-posta gönderim servisi:
- `send_welcome_email(user)` — İlk ORCID girişinde
- `send_submission_confirmation(submission)` — Gönderim sonrası
- `send_status_change(submission, old, new, notes)` — Durum değişikliğinde
- `send_withdrawal_confirmation(submission)` — Geri çekme sonrası

Tüm fonksiyonlar:
- Kullanıcı tercihlerini kontrol eder
- HTML template render eder
- `EmailLog` kaydı oluşturur
- Hata durumunda `FAILED` status ile loglar
- E-posta yoksa `None` döner

### 3. HTML E-posta Şablonları (`templates/email/`)
- `_base.html` — Marka header, gradient, footer, responsive layout
- `welcome.html` — Hoş geldiniz, ORCID bilgisi, başlangıç adımları
- `submission_confirmation.html` — Manuscript ID, başlık, makale tipi, yazar/dosya sayısı
- `status_change.html` — Eski/yeni durum badge'leri, notlar
- `withdrawal_confirmation.html` — Geri çekme onayı

### 4. API Endpoints
- `GET /api/v1/notifications/preferences/` — Mevcut tercihleri getir
- `PUT /api/v1/notifications/preferences/` — Tercihleri güncelle (partial)
- `GET /api/v1/notifications/email-log/` — Son 50 e-posta logu

### 5. Hook Entegrasyonları
- **Submit action** (`views.py`): `send_submission_confirmation()` çağrılıyor
- **Withdraw action** (`views.py`): `send_withdrawal_confirmation()` çağrılıyor
- **ORCID callback** (`users/views.py`): Yeni kullanıcılara `send_welcome_email()` gönderiliyor
- Tüm e-posta çağrıları `try/except` ile sarılı — e-posta hatası ana işlemi bloklamıyor

### 6. Django Settings
- `FRONTEND_URL` eklendi (e-posta içi linkler için)
- Mevcut `EMAIL_*` ayarları kullanılıyor (development: console, production: SMTP)

---

## Frontend Değişiklikleri

### 1. Profil Sayfası — Email Notifications Bölümü
- 5 adet toggle switch (submission, status, revision, decision, announcements)
- Her toggle anında API'ye PUT isteği gönderir
- Başarısız olursa önceki değere geri döner
- `onMounted`'da mevcut tercihler yüklenir

### 2. Gönderim Sonrası Bildirim
- Submit toast mesajı güncellendi: "A confirmation email has been sent." eklendi

---

## Teknik Notlar

| Konu | Detay |
|------|-------|
| **E-posta Motoru** | Django `EmailMultiAlternatives` (HTML + plain text) |
| **Çalışma Modu** | Senkron (Celery ile async yapılabilir) |
| **Development** | Console backend (e-postalar terminale yazılır) |
| **Production** | SMTP backend (Gmail, SendGrid, vb.) |
| **Loglama** | `EmailLog` modeli ile tam izlenebilirlik |
| **Tercih Kontrolü** | Her e-posta gönderiminden önce tercih kontrol edilir |
| **Hata Toleransı** | E-posta hatası ana akışı kesmez |

---

## Aktifleştirme (Production)

E-postaların gerçekten gönderilmesi için Render'da şu env vars gerekli:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=TruEditor <noreply@trueditor.com>
FRONTEND_URL=https://trueditor.vercel.app
```

Gmail için "App Passwords" kullanılmalı (2FA aktif olmalı).
