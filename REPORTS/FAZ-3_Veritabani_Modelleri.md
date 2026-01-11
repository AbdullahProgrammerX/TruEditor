# Faz 3: Veritabanı Modelleri - Tamamlama Raporu

**Tarih:** 2026-01-11
**Geliştirici:** Abdullah Doğan

---

## Özet

TruEditor veritabanı modelleri başarıyla oluşturuldu. User model genişletildi, Submission modeli FSM durum yönetimi ile kuruldu, ManuscriptFile ve Author modelleri eklendi.

---

## Oluşturulan Modeller

### 1. User Model (Genişletildi)

ORCID tabanlı kullanıcı modeli aşağıdaki yeni alanlarla genişletildi:

| Alan Grubu | Alanlar |
|------------|---------|
| **İletişim** | phone, country, city, address |
| **Akademik** | title (unvan), expertise_areas, bio, website |
| **Roller** | is_chief_editor, reviewer_interests |
| **Durum** | email_verified, profile_completed |
| **ORCID** | orcid_token_expires |

**Toplam Alan Sayısı:** 30+

### 2. Submission Model (Yeni)

Makale gönderimi modeli FSM durum yönetimi ile:

| Alan Grubu | Alanlar |
|------------|---------|
| **Kimlik** | id (UUID), manuscript_id (TRU-YYYY-NNNN) |
| **İlişkiler** | submitter, assigned_editor |
| **Makale** | title, title_en, abstract, abstract_en, keywords, article_type, language |
| **Etik** | cover_letter, ethics_statement, conflict_of_interest, funding_statement |
| **Wizard** | wizard_step (1-6), wizard_data |
| **Revizyon** | revision_number, revision_notes, revision_deadline |
| **Editör** | editor_notes, editor_decision, editor_decision_date |
| **Tarihler** | created_at, submitted_at, accepted_at, published_at |

**FSM Durumları:**
```
draft → submitted → under_review → revision_required → accepted → published
                                 ↘ rejected
                  ↘ withdrawn
```

**FSM Geçişleri:**
- `submit()` - Taslağı gönder
- `start_review(editor)` - İnceleme başlat
- `request_revision(notes, days)` - Revizyon talep et
- `submit_revision()` - Revizyonu gönder
- `accept(notes)` - Kabul et
- `reject(notes)` - Reddet
- `withdraw()` - Geri çek
- `publish()` - Yayınla

### 3. ManuscriptFile Model (Yeni)

Dosya yönetimi modeli:

| Alan Grubu | Alanlar |
|------------|---------|
| **Kimlik** | id (UUID), submission, uploaded_by |
| **Dosya** | file, file_type, original_filename, file_size, mime_type |
| **Meta** | description, caption, order |
| **Revizyon** | revision_number, replaces |
| **Durum** | is_active, is_primary |
| **Güvenlik** | checksum, virus_scanned, virus_scan_date |

**Dosya Türleri:**
- main_text - Ana Metin
- cover_letter - Kapak Mektubu
- title_page - Başlık Sayfası
- tables - Tablolar
- figures - Şekiller
- supplementary - Ek Dosyalar
- ethics_approval - Etik Onay Belgesi
- revision - Revizyon Dosyası

### 4. Author Model (Yeni)

Yazar bilgileri modeli:

| Alan | Açıklama |
|------|----------|
| submission | Bağlı gönderim |
| user | Sistemde kayıtlı kullanıcı (opsiyonel) |
| orcid_id | ORCID ID |
| given_name, family_name | Ad Soyad |
| email | Email |
| institution, department | Kurum bilgileri |
| country, city | Konum |
| order | Yazar sırası (1 = birinci yazar) |
| is_corresponding | Sorumlu yazar mı? |
| contribution | CRediT katkı beyanı |

### 5. Yardımcı Modeller

- **SubmissionStatusHistory** - Durum değişiklik geçmişi
- **FileDownloadLog** - Dosya indirme logları

---

## Veritabanı Şeması

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
│  (ORCID tabanlı kimlik doğrulama)                           │
└─────────────────────────────────────────────────────────────┘
         │
         │ submitter / assigned_editor
         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Submission                              │
│  (FSM durum yönetimi)                                       │
│  draft → submitted → under_review → accepted → published    │
└─────────────────────────────────────────────────────────────┘
         │                    │
         │ authors            │ files
         ▼                    ▼
┌─────────────────┐  ┌─────────────────────────────────────────┐
│     Author      │  │           ManuscriptFile                 │
│  (Yazar listesi)│  │  (Dosya yönetimi)                       │
└─────────────────┘  └─────────────────────────────────────────┘
```

---

## Migration Dosyaları

| Uygulama | Migration | Açıklama |
|----------|-----------|----------|
| users | 0002_user_address_... | User model genişletme |
| submissions | 0001_initial | Submission, Author, StatusHistory |
| files | 0001_initial | ManuscriptFile, FileDownloadLog |

---

## Index'ler (Performans)

**User:**
- orcid_id (unique)
- email
- is_active
- is_reviewer
- is_editor

**Submission:**
- manuscript_id (unique)
- status
- submitter
- assigned_editor
- created_at
- submitted_at

**ManuscriptFile:**
- (submission, file_type)
- uploaded_by
- is_active

**Author:**
- (submission, order) - unique
- email
- orcid_id

---

## Test Sonuçları

- ✅ `makemigrations` - 3 migration dosyası oluşturuldu
- ✅ `migrate` - Tüm migration'lar uygulandı
- ✅ `check` - Sistem kontrolü başarılı (0 hata)

---

## Bilinen Sorunlar

1. **django-fsm deprecation warning**:
   - Uyarı: django-fsm viewflow'a taşındı
   - Durum: Şimdilik görmezden gelinebilir, çalışıyor
   - Çözüm: İleride viewflow.fsm'e migrate edilebilir

---

## Sonraki Adımlar

### Faz 4: ORCID Authentication
1. [ ] ORCID OAuth backend endpoint'leri
2. [ ] Token yönetimi
3. [ ] Frontend ORCID entegrasyonu

### Faz 5: Author Module API
1. [ ] Submission CRUD endpoints
2. [ ] File upload/download endpoints
3. [ ] Author management endpoints

---

## Model Özeti

| Model | Alanlar | İlişkiler |
|-------|---------|-----------|
| User | ~30 | - |
| Submission | ~25 | User (2), Author (M), File (M) |
| Author | ~15 | Submission, User |
| ManuscriptFile | ~15 | Submission, User |
| SubmissionStatusHistory | ~5 | Submission, User |
| FileDownloadLog | ~5 | ManuscriptFile, User |

**Toplam:** 6 model, ~100 alan

---

**Rapor Sonu**
