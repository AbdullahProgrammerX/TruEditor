# TruEditor Enterprise Yol Haritası

**Versiyon:** 2.0 (YZ Entegrasyonlu)  
**Tarih:** 2026-01-23  
**Son Güncelleme:** 2026-01-23  
**Hazırlayan:** Abdullah Doğan  
**Durum:** Planlama Aşaması  

> Bu yol haritası, mevcut bitirme projesi (FAZ-0 ~ FAZ-19) tamamlandıktan sonra TruEditor'ü
> kurumsal (enterprise) seviyeye taşıyacak kapsamlı geliştirme planını içerir.
> v2 güncellemesi: TÜBİTAK 7250401 "YZ Destekli Hakem Öneri Sistemi" entegrasyonu
> ve otonom iş akışı YZ bileşenleri eklendi.
> Başlangıç komutu kullanıcıdan gelecektir.

---

## İçindekiler

1. [Mevcut Durum Özeti](#mevcut-durum-özeti)
2. [Hedef Mimari](#hedef-mimari)
3. [YZ Teknoloji Yığını](#yz-teknoloji-yığını)
4. [Faz E-1: Yazar Modülü ve YZ Kalite Ölçümü](#faz-e-1-yazar-modülü-ve-yz-kalite-ölçümü)
5. [Faz E-AI: YZ Altyapı ve Model Katmanı](#faz-e-ai-yz-altyapı-ve-model-katmanı)
6. [Faz E-2: Editör Modülü ve Otonom İş Akışı](#faz-e-2-editör-modülü-ve-otonom-iş-akışı)
7. [Faz E-3: Hakem Modülü ve YZ Rapor Sınıflandırma](#faz-e-3-hakem-modülü-ve-yz-rapor-sınıflandırma)
8. [Faz E-4: Sistem Yöneticisi Modülü](#faz-e-4-sistem-yöneticisi-modülü)
9. [Faz E-5: Gelişmiş PDF, İntihal Motoru ve JATS XML](#faz-e-5-gelişmiş-pdf-intihal-motoru-ve-jats-xml)
10. [Faz E-6: Bulut Altyapısı Migration](#faz-e-6-bulut-altyapısı-migration)
11. [Faz E-7: Güvenlik ve Performans](#faz-e-7-güvenlik-ve-performans)
12. [Faz E-8: Entegrasyonlar ve Standartlar](#faz-e-8-entegrasyonlar-ve-standartlar)
13. [Faz E-9: Ticarileştirme](#faz-e-9-ticarileştirme)
14. [Bağımlılık Diyagramı](#bağımlılık-diyagramı)
15. [Genel Zaman Çizelgesi](#genel-zaman-çizelgesi)
16. [TÜBİTAK v4 Öneri Geri Bildirimi](#tübitak-v4-öneri-geri-bildirimi)

---

## Mevcut Durum Özeti

Bitirme projesi tamamlandığında elimizdeki teknoloji yığını:

| Katman | Teknoloji | Notlar |
|--------|-----------|--------|
| Frontend | Vue.js 3, Pinia, TailwindCSS, TypeScript | Vercel üzerinde deploy |
| Backend | Django 5.x, DRF, django-fsm, Celery/Redis | Render üzerinde deploy |
| Veritabanı | PostgreSQL | Neon (managed) |
| Dosya Depolama | Cloudflare R2 (S3-uyumlu) | Presigned URL ile |
| Kimlik Doğrulama | ORCID OAuth 2.0, JWT (SimpleJWT) | Tek giriş yöntemi |
| E-posta | Resend (django-anymail) | HTML şablonlar |
| CI/CD | GitHub Actions | Test + lint |
| PDF | WeasyPrint + Celery | Senkron/asenkron |

**Django Uygulamaları:** `users`, `submissions`, `files`, `notifications`, `common`

**Mevcut Modeller:**
- `User` — ORCID tabanlı özel kullanıcı modeli
- `Submission` — FSM durum makinesi ile makale yaşam döngüsü
- `Author` — Gönderim yazarları (sıralı, sorumlu yazar işaretli)
- `Correspondence` — Yazar-editör yazışma geçmişi
- `SubmissionStatusHistory` — Durum geçişi kayıtları
- `ManuscriptFile` — Yüklenen dosyalar (tip, sıra, revizyon numarası)
- `EmailLog` — E-posta gönderim kayıtları
- `EmailPreference` — Kullanıcı bildirim tercihleri

**Tamamlanan Özellikler (FAZ-0 ~ FAZ-19):**
- Çok adımlı gönderim sihirbazı (6 adım)
- ORCID ile kayıt ve giriş
- Dosya yükleme (sürükle-bırak, sıralama, presigned URL)
- PDF oluşturma ve önizleme
- E-posta bildirim sistemi (şablonlar, tercihler, loglar)
- Revizyon iş akışı (.R1, .R2)
- Metadata çıkarma (DOCX/PDF -> başlık, özet, anahtar kelimeler)
- Yazışma geçmişi ve karar mektubu
- Ortak yazar erişimi ve doğrulama
- Çok dilli arayüz (TR/EN — i18n)
- Logo ve branding

**İlişkili Proje:**
- TÜBİTAK 7250401 — "Yapay Zeka Destekli Uluslararası Hakem Öneri Sistemi" (31.08.2026 bitiş)
- Bu motor, enterprise yol haritasının hakem eşleştirme ve otonom atama bileşenlerinin çekirdeğidir

**Eksik Kritik Modüller:**
- YZ Makale Kalite Ölçümü (dil, referans yaşı, görsel, kelime/sayfa)
- Otonom İş Akışı Yöneticisi (gecikme önleme, yarı otonom kararlar)
- Editör Modülü (Kanban, atama, embedding tabanlı eşleştirme)
- Hakem Modülü (Magic Link, JSONB formlar, kör hakemlik, YZ rapor sınıflandırma)
- YZ İntihal/Benzerlik Kontrolü
- Sistem Yöneticisi Modülü (dergi yapılandırma, RBAC)
- Multi-tenant mimari
- AWS bulut altyapısı (ECS, Aurora, Fargate)

---

## Hedef Mimari

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           KULLANICI KATMANI                              │
│   Yazarlar  ·  Editörler  ·  Hakemler  ·  Sistem Yöneticileri           │
└───────────────────────────┬──────────────────────────────────────────────┘
                            │ HTTPS
                     ┌──────▼──────┐
                     │  CloudFront  │  CDN + SSL Termination
                     │    + WAF     │  DDoS / SQL Injection Koruması
                     └──────┬──────┘
                            │
               ┌────────────┴────────────┐
               │                         │
      ┌────────▼────────┐      ┌────────▼────────┐
      │  Vue.js 3 SPA   │      │  Django REST API │
      │  (S3 + CF)      │      │  (ECS Fargate)   │
      │                 │      │                  │
      │  · Pinia Store  │◄────►│  · DRF Views     │
      │  · Vue Router   │ API  │  · FSM Engine    │
      │  · TailwindCSS  │      │  · Permissions   │
      │  · i18n (TR/EN) │      │  · YZ Endpoints  │
      └─────────────────┘      └───────┬──────────┘
                                       │
                  ┌────────────────┬────┴────┬──────────────────┐
                  │                │         │                  │
         ┌───────▼──────┐ ┌──────▼───────┐ │ ┌───────▼──────┐ │
         │ Aurora PG v2 │ │ ElastiCache  │ │ │   AWS S3     │ │
         │ (Multi-tenant│ │   Redis      │ │ │ (Dosyalar)   │ │
         │  + pgvector) │ │ (Cache+Queue)│ │ └──────────────┘ │
         └──────────────┘ └──────┬───────┘ │                  │
                                 │         │                  │
                        ┌────────▼─────┐   │  ┌──────────────▼──────────┐
                        │Celery Workers│   │  │  7250401 Hakem Öneri    │
                        │(ECS Fargate) │   │  │  Sistemi API            │
                        │              │   │  │  (Harici REST Servis)   │
                        │ · PDF Motor  │   │  └─────────────────────────┘
                        │ · E-posta    │   │
                        │ · Metadata   │   │
                        │ · YZ Analiz  │◄──┘
                        │ · İntihal    │
                        └──────────────┘

    YZ Katmanı: pgvector (embedding), LLM API, NLP pipeline
    Altyapı Yönetimi: Terraform (IaC)
    CI/CD: GitHub Actions → ECS Deploy (Zero-downtime)
    İzleme: Datadog APM + Sentry Error Tracking
    E-posta: Amazon SES (+ SendGrid fallback)
```

### Mimari Geçiş Tablosu

| Bileşen | Mevcut | Hedef (Enterprise) |
|---------|--------|-------------------|
| Frontend Hosting | Vercel | CloudFront + S3 (veya ECS) |
| Backend Hosting | Render | AWS ECS Fargate |
| Veritabanı | Neon PostgreSQL | Aurora Serverless v2 + pgvector |
| Dosya Depolama | Cloudflare R2 | AWS S3 (veya R2 koruma — maliyet analizi) |
| Cache / Queue | Render Redis | Amazon ElastiCache Redis |
| E-posta | Resend | Amazon SES + SendGrid |
| CI/CD | GitHub Actions (test) | GitHub Actions (test + deploy, zero-downtime) |
| IaC | Yok | Terraform |
| WAF | Yok | AWS WAF |
| İzleme | Yok | Datadog APM + Sentry |
| Multi-tenant | Yok | Tenant discriminator (paylaşımlı şema) |
| SSO | Yok | Auth0/Keycloak (SAML/Shibboleth) |
| YZ / NLP | Yok | pgvector + LLM API + NLP pipeline |
| Hakem Öneri | Yok | 7250401 API entegrasyonu |
| Otonom Motor | Yok | Celery Beat + Event-driven workflow |

---

## YZ Teknoloji Yığını

Enterprise yol haritasındaki yapay zeka bileşenlerinin teknoloji seçimleri:

| Bileşen | Teknoloji Seçenekleri | Kullanım Alanı |
|---------|----------------------|----------------|
| Embedding Modeli | Sentence-BERT / OpenAI text-embedding-3-small | Makale-editör semantik eşleştirme, benzerlik tespiti |
| Vektör Veritabanı | pgvector (PostgreSQL extension) | Embedding depolama ve cosine similarity sorguları |
| LLM Entegrasyonu | OpenAI GPT-4o API / yerel Llama 3 (fallback) | Dil kalitesi puanlama, rapor sınıflandırma, revizyon değişiklik tespiti |
| NLP Kütüphaneleri | spaCy, Hugging Face transformers | Metin ön işleme, referans yaşı çıkarma, entity extraction |
| Referans Analizi | regex + spaCy NER + custom parser | Yayın yılı extraction, min/max/avg istatistik |
| Görsel Analiz | Pillow (DPI check) + custom heuristics | Görsel çözünürlük ve kalite puanlama |
| Benzerlik Motoru | Cosine similarity on embeddings | İntihal ve duplicate submission tespiti |
| Otonom Motor | Celery Beat + Django signals + custom event handler | Gecikme tespiti, otomatik hakem atama, revizyon yönlendirme |
| Hakem Öneri | 7250401 REST API (harici servis) | Otonom hakem eşleştirme ve atama |

**Model Stratejisi:**
- **Hibrit yaklaşım:** Basit kurallar (referans yaşı, sayfa sayısı) için kural tabanlı sistem; karmaşık analiz (dil kalitesi, rapor sınıflandırma) için LLM API
- **Fallback:** LLM API erişilemezse "yarı otonom asistan" moduna geçiş (YZ sadece tespit yapar, karar editöre kalır)
- **Halüsinasyon önleme:** Yapılandırılmış çıktı (structured output / JSON mode), prompt mühendisliği, human-in-the-loop onay adımları

---

## Faz E-1: Yazar Modülü ve YZ Kalite Ölçümü

**Süre:** 4–5 hafta  
**Bağımlılık:** FAZ-19 (Bitirme Projesi) tamamlanmış olmalı  
**Ara Çıktı:** Enterprise seviye Yazar Modülü + Kurumsal SSO + YZ Kalite Ön Filtresi

### E-1.1 Kurumsal Kimlik Doğrulama (SSO)

| Görev | Detay |
|-------|-------|
| Auth0 / Keycloak entegrasyonu | Identity provider olarak kurulacak; Django backend `python-social-auth` veya `django-allauth` ile bağlanacak |
| SAML 2.0 / Shibboleth desteği | Üniversite kurumsal e-posta ile tek tıkla giriş; `python3-saml` kütüphanesi |
| ORCID OAuth 2.0 v3 güncellemesi | Mevcut v2 entegrasyonunun v3 Public API'ye yükseltilmesi |
| Fallback mekanizması | SSO/ORCID devre dışı kalırsa e-posta/şifre ile giriş (Strategy Pattern) |

### E-1.2 Büyük Dosya Yükleme Altyapısı

| Görev | Detay |
|-------|-------|
| Chunked Upload (Parçalı Yükleme) | `tus.io` açık protokolü veya özel implementasyon; 500 MB+ dosya desteği |
| Resume desteği | Ağ kopması durumunda kaldığı parçadan devam |
| S3-uyumlu Presigned URL | Mevcut Cloudflare R2 altyapısı üzerinde; AWS migration'da S3'e geçiş şeffaf olacak |
| Frontend upload UI | İlerleme çubuğu, hız göstergesi, iptal/devam butonları |

### E-1.3 Yazar Modülü Genişletme

| Görev | Detay |
|-------|-------|
| `SubmissionType` modeli | Araştırma makalesi, derleme, editöre mektup, vaka sunumu vb.; dergi bazlı yapılandırılabilir |
| `JournalConfig` modeli | Dergi adı, ISSN, yayıncı bilgileri, varsayılan ayarlar |
| Çoklu affiliasyon desteği | Author modeline `AuthorAffiliation` many-to-many ilişkisi |
| Gelişmiş co-author doğrulama | E-posta ile onay iş akışı, ORCID eşleştirme |
| Rate limiting | Django REST throttling; endpoint bazlı limit (submissions: 10/saat) |

### E-1.4 YZ Destekli Makale Kalite Ölçümü (YENİ)

Makale sisteme yüklendiği anda otomatik tetiklenen YZ kalite analizi:

| Ölçüm | Yöntem | Çıktı |
|-------|--------|-------|
| Yazım dili puanlaması | LLM API (GPT-4o) ile dilbilgisel analiz | 0–100 puan + tespit edilen sorunlar listesi |
| Referans yaşı dağılımı | Regex + NLP ile referans listesinden yıl çıkarma | Min, max, ortalama yıl; güncellik skoru |
| Kelime / sayfa sayısı | `python-docx` / `pdfplumber` ile metin çıkarma | Kelime sayısı, sayfa sayısı, dergi eşiğiyle karşılaştırma |
| Görsel kalitesi | Pillow ile DPI kontrolü + boyut analizi | Her görselin DPI değeri ve kalite uyarıları |

**Yeni Model:** `QualityReport`

| Alan | Tip | Açıklama |
|------|-----|----------|
| `submission` | OneToOneField | İlgili gönderim |
| `language_score` | FloatField | Dil kalitesi puanı (0–100) |
| `language_issues` | JSONField | Tespit edilen dilbilgisel sorunlar |
| `reference_stats` | JSONField | `{"min_year": 1998, "max_year": 2025, "avg_year": 2019, "count": 42}` |
| `word_count` | IntegerField | Toplam kelime sayısı |
| `page_count` | IntegerField | Toplam sayfa sayısı |
| `image_quality` | JSONField | `[{"name": "fig1.png", "dpi": 300, "ok": true}, ...]` |
| `overall_score` | FloatField | Genel kalite puanı (0–100) |
| `created_at` | DateTimeField | Analiz tarihi |
| `status` | CharField | pending / processing / completed / failed |

**İş Akışı:**
1. Yazar dosya yükler
2. Celery task tetiklenir: `analyze_submission_quality`
3. Paralel olarak: dil analizi + referans çıkarma + görsel kontrolü
4. `QualityReport` oluşturulur
5. Editöre "YZ Ön Filtre Raporu" olarak sunulur (makale detay sayfasında)

### E-1.5 Frontend İyileştirmeleri

| Görev | Detay |
|-------|-------|
| WCAG 2.1 AA uyumluluk | Renk kontrastı, klavye navigasyonu, ARIA etiketleri, ekran okuyucu desteği |
| Yazar dashboard analitik | Gönderim sayıları, ortalama yanıt süresi, durum dağılımı grafikleri |
| YZ kalite raporu görüntüleme | Yazar ve editör tarafında kalite skoru kartları ve detay paneli |
| Mobile-responsive optimizasyon | Tüm formlar ve tabloların mobil uyumluluğu |
| Hata kurtarma | Form verisi localStorage'da yedekleme, offline uyarıları |

---

## Faz E-AI: YZ Altyapı ve Model Katmanı

**Süre:** 3–4 hafta  
**Bağımlılık:** E-1 tamamlanmış olmalı (E-2 ile paralel başlayabilir)  
**Ara Çıktı:** Tüm YZ bileşenlerinin ortak altyapısı ve 7250401 entegrasyon adaptörü

> Bu faz, E-2 ve E-3'ün ihtiyaç duyduğu YZ altyapısını hazırlar.
> E-1'de temel kalite ölçümü yapılır; E-AI'da daha derin NLP ve otonom motor kurulur.

### E-AI.1 Vektör Veritabanı Altyapısı

**Yeni Django App:** `backend/apps/ai/`

| Görev | Detay |
|-------|-------|
| pgvector kurulumu | PostgreSQL extension; `CREATE EXTENSION vector;` |
| Embedding depolama modeli | `ArticleEmbedding(submission, vector, model_version, created_at)` |
| Editör profil embedding | `EditorExpertiseEmbedding(user, expertise_text, vector, updated_at)` |
| Cosine similarity sorguları | `SELECT * FROM embeddings ORDER BY vector <=> query_vector LIMIT 5` |
| Embedding güncelleme pipeline | Makale yüklendiğinde/güncellendiğinde otomatik embedding oluşturma |

### E-AI.2 NLP Analiz Pipeline

| Bileşen | Detay |
|---------|-------|
| Metin ön işleme | Tokenization, lowercase, stopword removal (spaCy TR/EN) |
| Referans parser | Regex + NER ile referans listesinden yıl, yazar, dergi çıkarma |
| Embedding üretimi | Makale başlık + özet + anahtar kelimeler -> vektör (Sentence-BERT veya OpenAI) |
| Metin karşılaştırma | Önceki/yeni revizyon arasında semantik diff (embedding distance + text diff) |

### E-AI.3 LLM Entegrasyon Katmanı

```python
class LLMService:
    """Tüm LLM çağrılarını yöneten merkezi servis"""

    def analyze_language_quality(self, text: str) -> LanguageReport:
        """Yazım dili kalitesi analizi (structured JSON output)"""

    def classify_review_report(self, report_text: str) -> ReviewClassification:
        """Hakem raporunu sınıflandırma (positive/negative/revision/insufficient)"""

    def detect_revision_changes(self, old_text: str, new_text: str) -> RevisionDiff:
        """Revizyon değişikliklerini tespit ve bayrak oluşturma"""

    def generate_decision_letter(self, reviews: list, template: str) -> str:
        """Karar mektubu taslağı oluşturma"""

    def assess_desk_reject(self, quality_report: dict) -> DeskRejectRecommendation:
        """Ön ret önerisi (kalite skoru + gerekçe)"""
```

- OpenAI API birincil sağlayıcı; JSON mode ile yapılandırılmış çıktı
- Fallback: yerel Llama 3 modeli (API erişilemezse)
- Rate limiting ve maliyet takibi
- Prompt şablonları versiyonlama (DB'de saklanır)

### E-AI.4 7250401 Hakem Öneri Sistemi API Adaptörü

| Görev | Detay |
|-------|-------|
| API client modülü | `ReviewerRecommendationClient` — 7250401 REST API'ye bağlantı |
| Aday listesi çekme | Makale metni/anahtar kelimeleri gönderip, sıralı hakem önerisi alma |
| Çıkar çatışması filtreleme | Aynı kurumdan yazar-hakem eşleşmesini engelleme (yerel kontrol) |
| Fallback mekanizması | API erişilemezse yerel keyword-based matching'e geçiş |
| Cache katmanı | Aynı makale için tekrarlı sorguları Redis'te cache'leme |

### E-AI.5 Otonom İş Akışı Motoru (Event-Driven)

Celery Beat + Django signals ile olay-güdümlü otonom motor:

```
┌──────────────────────────────────────────────────────────┐
│                    OTONOM MOTOR                           │
│                                                          │
│  Periyodik Tarama (Celery Beat, her 15 dk):              │
│  ┌─────────────────────────────────────────────────┐     │
│  │ 1. Hakem davet süresi dolmuş mu?                │     │
│  │    → Evet: Hatırlatma e-postası gönder           │     │
│  │    → 2. kez dolmuş mu? Otonom yeni hakem öner    │     │
│  │                                                  │     │
│  │ 2. Hakem daveti reddedildi mi?                   │     │
│  │    → 7250401 API'den yeni hakem listesi çek      │     │
│  │    → Editöre öner VEYA otonom davet gönder       │     │
│  │                                                  │     │
│  │ 3. Revizyon yüklendi mi?                         │     │
│  │    → YZ ile değişiklikleri analiz et              │     │
│  │    → Bayrak oluştur (major/minor değişiklik)     │     │
│  │    → Eski hakemlere otonom yönlendir              │     │
│  │                                                  │     │
│  │ 4. Tüm hakem raporları geldi mi?                 │     │
│  │    → Raporları YZ ile sınıflandır                 │     │
│  │    → Karar özeti hazırla                          │     │
│  │    → Editöre "tek tıkla karar" bildirimi gönder   │     │
│  └─────────────────────────────────────────────────┘     │
│                                                          │
│  Otonomi Seviyeleri (JournalConfig'den yapılandırılır):  │
│  · TAM OTONOM: Sistem kararı uygular, editörü bilgilendirir │
│  · YARI OTONOM: Sistem önerir, editör onaylar             │
│  · ASISTAN: Sistem tespit yapar, kararı editör verir      │
└──────────────────────────────────────────────────────────┘
```

**Yeni Modeller:**

| Model | Alanlar | Açıklama |
|-------|---------|----------|
| `AutonomousAction` | submission, action_type, trigger_event, status, result, created_at | Otonom motorun gerçekleştirdiği her aksiyonun logu |
| `AutonomyConfig` | journal, feature, level (full/semi/assistant), enabled | Dergi bazlı otonomi seviyesi yapılandırması |
| `AIPromptTemplate` | name, version, system_prompt, user_prompt_template, active | LLM prompt şablonları |

---

## Faz E-2: Editör Modülü ve Otonom İş Akışı

**Süre:** 8–10 hafta  
**Bağımlılık:** E-1 ve E-AI tamamlanmış olmalı  
**Ara Çıktı:** Tam fonksiyonel Editör Modülü + Kanban + ACID Durum Makinesi + YZ Otonom Motor

> Bu faz, tüm projenin en büyük ve en kritik Ar-Ge modülüdür.
> Akademik yayıncılığın çekirdek iş akışını yönetir ve YZ otonomisini entegre eder.

### E-2a: Core Editor Backend (3–4 hafta)

#### Rol ve Yetki Sistemi

```
Editor-in-Chief (EiC)
  ├── Tüm gönderileri görür
  ├── Associate Editor atar
  ├── Son kararı verir (Accept / Reject)
  ├── Desk Reject yetkisi
  └── Otonomi seviyesi yapılandırma

Associate Editor (AE)
  ├── Atanan gönderileri görür
  ├── Hakem davet eder
  ├── Hakem raporlarını değerlendirir
  └── EiC'ye karar önerisi sunar

Section Editor (SE)
  ├── Belirli makale türlerini görür
  └── AE yetkilerine sahip (kendi alanında)
```

**Yeni Django App:** `backend/apps/editor/`  
**Yeni Modeller:**
- `EditorRole` — Kullanıcı-dergi-rol ilişkisi (EiC, AE, SE)
- `EditorAssignment` — Gönderinin hangi editöre atandığı, tarih, notlar
- `DecisionTemplate` — Karar mektubu şablonları (Accept, Reject, Major Revision, Minor Revision)
- `EditorNote` — Dahili notlar (yazara görünmez)

#### Embedding Tabanlı Alan Editörü Eşleştirmesi (YENİ)

```
Makale yüklenir
    │
    ▼
Makale embedding oluşturulur (E-AI pipeline)
    │
    ▼
Tüm editörlerin uzmanlık embedding'leri ile cosine similarity hesaplanır
    │
    ▼
Top-3 en uygun editör önerisi editöre sunulur
    │
    ▼
EiC onaylar veya farklı editör seçer
```

- Editör uzmanlık profili: ORCID yayın listesi + elle girilen anahtar kelimeler -> embedding
- Eşleşme skoru: 0–1 arası cosine similarity
- UI'da editör kartlarında "uyumluluk yüzdesi" gösterilir

#### Durum Makinesi (FSM) Upgrade

Mevcut FSM'ye eklenecek yeni durumlar ve geçişler:

```
                    ┌──────────────┐
                    │    draft     │
                    └──────┬───────┘
                           │ submit
                    ┌──────▼───────┐
                    │  submitted   │──── YZ Kalite Raporu oluşturulur
                    └──────┬───────┘
                           │
                ┌──────────┼──────────┐
                │ assign_editor       │ desk_reject (YZ önerisiyle)
         ┌──────▼───────┐     ┌──────▼───────┐
         │ under_review  │     │ desk_rejected │
         └──────┬───────┘     └──────────────┘
                │
         ┌──────▼───────┐
         │  awaiting_    │──── YZ: Raporları sınıflandır + karar özeti hazırla
         │  decision     │
         └──────┬───────┘
                │
     ┌──────────┼──────────┬──────────┐
     │          │          │          │
┌────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌───▼────┐
│accepted│ │rejected│ │revision│ │revision│
│        │ │        │ │required│ │required│
└────────┘ └────────┘ │(major) │ │(minor) │
                      └───┬────┘ └───┬────┘
                          │          │
                   ┌──────▼──────────▼──────┐
                   │   revision_submitted    │──── YZ: Değişiklikleri tespit + bayrak
                   └─────────┬──────────────┘
                             │ Otonom: Eski hakemlere yönlendir
                             ▼
```

**Pessimistic Locking implementasyonu:**

```python
from django.db import transaction

def make_decision(submission_id, decision, editor):
    with transaction.atomic():
        submission = (
            Submission.objects
            .select_for_update(nowait=False)
            .get(id=submission_id)
        )
        # FSM geçişi güvenli şekilde yapılır
        # Aynı anda iki editör karar veremez
```

#### Yarı Otonom Süreçler (YENİ)

| Süreç | YZ Aksiyonu | Editör Rolü |
|-------|------------|-------------|
| Desk Reject önerisi | Kalite skoru < eşik ise "Ön ret önerisi" oluşturur | Onaylar veya reddeder |
| Editör eşleştirme | Top-3 alan editörü önerir | Seçer veya farklı editör atar |
| Revizyon değişiklik tespiti | Önceki/yeni versiyonu karşılaştırır, bayrak oluşturur | Bayrağı inceler |
| Karar mektubu taslağı | Hakem raporlarından otomatik mektup taslağı oluşturur | Düzenler ve gönderir |
| Revizyon yönlendirme | Revize makaleyi eski hakemlere otomatik yönlendirir | Bilgilendirilir, gerekirse müdahale eder |

#### API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/editor/dashboard/` | Editör dashboard istatistikleri |
| GET | `/api/editor/queue/` | Yeni gönderim kuyruğu |
| POST | `/api/editor/submissions/{id}/assign/` | AE'ye atama |
| GET | `/api/editor/submissions/{id}/ai-suggest-editors/` | YZ editör eşleştirme önerisi |
| POST | `/api/editor/submissions/{id}/desk-reject/` | Ön değerlendirmede red |
| GET | `/api/editor/submissions/{id}/ai-desk-reject-assessment/` | YZ desk reject önerisi |
| POST | `/api/editor/submissions/{id}/decision/` | Karar verme |
| GET | `/api/editor/submissions/{id}/ai-decision-summary/` | YZ karar özeti |
| POST | `/api/editor/submissions/{id}/ai-generate-letter/` | YZ karar mektubu taslağı |
| GET | `/api/editor/submissions/{id}/ai-revision-diff/` | YZ revizyon değişiklik raporu |
| GET | `/api/editor/submissions/{id}/reviews/` | Hakem raporları |
| POST | `/api/editor/submissions/{id}/invite-reviewer/` | Hakem daveti |
| CRUD | `/api/editor/decision-templates/` | Karar mektubu şablonları |
| CRUD | `/api/editor/notes/{submission_id}/` | Dahili notlar |

### E-2b: Editor Frontend (3–4 hafta)

#### Editör Dashboard

Bileşenler:
- **İstatistik Kartları:** Toplam gönderim, bekleyen karar, ortalama karar süresi, kabul oranı
- **YZ Asistan Kartı:** Otonom aksiyonlar özeti, bekleyen öneriler sayısı
- **Grafikler:** Aylık gönderim trendi (Chart.js), durum dağılımı (pie chart)
- **Aksiyon Gerektiren Liste:** Atanmamış gönderiler, geciken hakemlikler, YZ bayrakları

#### Kanban Board

- Vue.js sürükle-bırak (vuedraggable veya native DnD) ile durum geçişi
- Kart üzerinde: manuscript ID, başlık, yazar, YZ kalite skoru badge, atanan editör
- YZ önerileri: kartlarda "YZ Desk Reject Önerisi" veya "YZ Eşleşme %92" badge
- Tıklama ile detay paneli (side sheet)

#### YZ Asistan Paneli (YENİ)

- Makale detayında "YZ Asistan" sekmesi
- Kalite raporu görüntüleme (dil skoru, referans istatistikleri, görsel kalite)
- Editör eşleştirme önerileri (uyumluluk yüzdesi ile)
- Revizyon diff görüntüleme (değişiklik bayrakları)
- Tek tıkla karar mektubu oluşturma
- Otonom aksiyon geçmişi (ne yapıldı, ne zaman)

### E-2c: Editör İletişim ve Otomasyon (1–2 hafta)

| Görev | Detay |
|-------|-------|
| Dahili not sistemi | Editörler arası notlar; yazara görünmez |
| Otomatik hatırlatıcılar | Celery periodic tasks: geciken hakemlik (7/14/21 gün), bekleyen karar |
| Otonom motor bildirimleri | YZ aksiyonları hakkında editöre in-app + e-posta bildirim |
| Editör bildirim merkezi | In-app bildirimler + e-posta özet (günlük/haftalık digest) |

---

## Faz E-3: Hakem Modülü ve YZ Rapor Sınıflandırma

**Süre:** 5–6 hafta  
**Bağımlılık:** E-2 tamamlanmış olmalı (editör atama sistemi + otonom motor gerekli)  
**Ara Çıktı:** 7250401 entegreli, Magic Link erişimli, YZ rapor sınıflandırmalı Hakem Modülü

### E-3a: Hakem Veritabanı ve Davet Sistemi (1–2 hafta)

#### Yeni Modeller

**`Reviewer`** — Hakem profili (User'dan bağımsız olabilir)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `user` | FK (nullable) | Sistemde kayıtlı ise bağlantı |
| `email` | EmailField | Davet e-postası |
| `first_name`, `last_name` | CharField | İsim bilgisi |
| `orcid_id` | CharField (nullable) | ORCID tanımlayıcı |
| `institution` | CharField | Kurum |
| `expertise_keywords` | ArrayField | Uzmanlık alanları (PostgreSQL array) |
| `expertise_embedding` | VectorField (nullable) | pgvector uzmanlık embedding'i |
| `total_reviews` | IntegerField | Toplam değerlendirme sayısı |
| `avg_review_days` | FloatField | Ortalama değerlendirme süresi (gün) |
| `ai_quality_score` | FloatField (nullable) | YZ tarafından hesaplanan hakem kalite puanı |
| `is_available` | BooleanField | Müsaitlik durumu |

**`ReviewInvitation`** — Hakem daveti

| Alan | Tip | Açıklama |
|------|-----|----------|
| `submission` | FK | İlgili gönderim |
| `reviewer` | FK | Davet edilen hakem |
| `invited_by` | FK (User) | Daveti gönderen editör |
| `source` | CharField | manual / ai_suggested / autonomous | Davet kaynağı |
| `token` | UUIDField | Magic Link token |
| `token_expires_at` | DateTimeField | Token geçerlilik süresi |
| `status` | CharField | pending / accepted / declined / expired / completed |
| `invited_at` | DateTimeField | Davet tarihi |
| `responded_at` | DateTimeField (nullable) | Yanıt tarihi |
| `deadline` | DateField | Değerlendirme son tarihi |

**`Review`** — Hakem değerlendirmesi

| Alan | Tip | Açıklama |
|------|-----|----------|
| `invitation` | OneToOneField | İlgili davet |
| `submission` | FK | İlgili gönderim |
| `reviewer` | FK | Değerlendiren hakem |
| `form_schema` | JSONField | Kullanılan form şeması (snapshot) |
| `form_data` | JSONField | Doldurulan form verileri |
| `recommendation` | CharField | accept / minor_revision / major_revision / reject |
| `comments_to_editor` | TextField | Editöre özel notlar |
| `comments_to_author` | TextField | Yazara iletilecek yorumlar |
| `ai_classification` | CharField (nullable) | YZ sınıflandırma: positive / negative / revision / insufficient |
| `ai_quality_score` | FloatField (nullable) | YZ rapor kalite puanı |
| `is_draft` | BooleanField | Taslak mı |
| `submitted_at` | DateTimeField (nullable) | Teslim tarihi |

#### Magic Link Sistemi

- Token süresi yapılandırılabilir: 7 / 14 / 30 gün (JournalConfig'den)
- Token tek kullanımlık veya çoklu kullanımlık seçeneği
- Kabul/red sonrası token durumu güncellenir
- Red durumunda otonom motor tetiklenir (yeni hakem önerisi)

### E-3b: 7250401 Entegrasyonu ve Otonom Hakem Atama (1–2 hafta) (YENİ)

```
Hakem daveti reddedildi / süre doldu
         │
         ▼
Otonom motor algılar (Celery Beat tarama)
         │
         ▼
7250401 API'ye makale bilgileri gönderilir
         │
         ▼
Sıralı hakem önerisi listesi alınır
         │
         ▼
Çıkar çatışması filtresi uygulanır (yerel)
         │
         ▼
Otonomi seviyesine göre:
├── TAM OTONOM → Otomatik davet e-postası gönderilir, editör bilgilendirilir
├── YARI OTONOM → Editöre "1 tıkla onayla" bildirimi gönderilir
└── ASISTAN → Editöre öneri listesi sunulur, editör seçer
```

### E-3c: Dinamik Değerlendirme Formları (1 hafta)

- JSONB form şeması (E-4 Admin modülünde form builder ile yönetilir)
- Hakemler için dinamik Vue.js form render
- Otomatik kayıt (draft mode)
- Form versiyonlama

### E-3d: Kör Hakemlik (1 hafta)

| Tip | Yazar → Hakem | Hakem → Yazar | Uygulama |
|-----|--------------|--------------|----------|
| Single-blind | Görünür | Gizli | Varsayılan; hakem kimliği maskelenir |
| Double-blind | Gizli | Gizli | Dosyalardan yazar bilgisi temizlenir |

- PDF/DOCX metadata temizleme
- Dosya adı anonimleştirme
- API serializer'da yazar bilgisi filtreleme

### E-3e: YZ Rapor Sınıflandırma ve Hakem Puanlama (1 hafta) (YENİ)

Hakem raporu gönderildiğinde otomatik tetiklenen YZ analizi:

| Analiz | Yöntem | Çıktı |
|--------|--------|-------|
| Rapor sınıflandırma | LLM ile metin sınıflandırma | positive / negative / revision / insufficient |
| Rapor kalite puanı | Detay düzeyi + gerekçe kalitesi + tutarlılık analizi | 0–100 puan |
| Yetersiz rapor tespiti | Çok kısa, gerekçesiz, tutarsız raporların otomatik tespiti | Editöre uyarı |
| Hakem kalite güncelleme | Tüm raporlardan kümülatif hakem skoru hesaplama | Reviewer.ai_quality_score güncelleme |

---

## Faz E-4: Sistem Yöneticisi Modülü

**Süre:** 2–3 hafta  
**Bağımlılık:** E-2 ve E-3 tamamlanmış olmalı  
**Ara Çıktı:** Yapılandırılabilir Dergi Yönetim Paneli + RBAC + Otonomi Ayarları

### E-4.1 Dergi / Tenant Yapılandırma Paneli

**Yeni Django App:** `backend/apps/journals/`

| Model | Alanlar | Açıklama |
|-------|---------|----------|
| `Journal` | name, issn, publisher, logo, description, config | Dergi tanımı |
| `JournalConfig` | review_type, default_deadline, submission_types, max_file_size, allowed_file_types | Dergi ayarları (JSONB) |
| `WorkflowConfig` | states, transitions, auto_actions | İş akışı yapılandırması |
| `EmailTemplate` | journal, event_type, subject, body_html | Dergi bazlı e-posta şablonları |

Ek yapılandırma (YENİ):
- **Otonomi seviyesi ayarları:** Her YZ özelliği için tam/yarı/asistan modu
- **YZ eşik değerleri:** Desk reject için minimum kalite skoru, rapor yetersizlik eşiği
- **7250401 API bağlantı ayarları:** API URL, token, timeout

### E-4.2 Rol Tabanlı Erişim Kontrolü (RBAC)

```
Permission Matrix:

                      | Gönderim | Atama | Karar | Hakem  | YZ       | Ayarlar | Kullanıcı |
                      | Görme    | Yapma | Verme | Davet  | Otonom   | Değiştir| Yönetimi  |
──────────────────────┼──────────┼───────┼───────┼────────┼──────────┼─────────┼───────────┤
Sistem Yöneticisi     |    ✓     |   ✓   |   ✓   |   ✓    |  Yapıl.  |    ✓    |     ✓     |
Editor-in-Chief       |    ✓     |   ✓   |   ✓   |   ✓    |  Onay    |    -    |     -     |
Associate Editor      |  Atanan  |   -   | Öneri |   ✓    |  Görüntü |    -    |     -     |
Section Editor        |  Alanı   |   -   | Öneri |   ✓    |  Görüntü |    -    |     -     |
Yazar                 |  Kendi   |   -   |   -   |   -    |    -     |    -    |     -     |
Hakem                 |  Atanan  |   -   |   -   |   -    |    -     |    -    |     -     |
```

### E-4.3 Sistem Dashboard ve Denetim

- **Global İstatistikler:** Toplam gönderim, kabul oranı, ortalama karar süresi
- **YZ Metrikleri:** Otonom aksiyon sayısı, başarı oranı, ortalama YZ yanıt süresi
- **Denetim Logları:** Tüm durum geçişleri + YZ otonom aksiyonları loglanır
- **CSV/Excel export**

---

## Faz E-5: Gelişmiş PDF, İntihal Motoru ve JATS XML

**Süre:** 3–4 hafta  
**Bağımlılık:** E-1 tamamlanmış olmalı (bağımsız çalışabilir, E-2/E-3 ile paralel)  
**Ara Çıktı:** PDF Motoru + YZ İntihal Kontrolü + JATS XML Export

> **Kritik Not:** Bu fazda motor lokalde (Celery/Redis) geliştirilir.
> AWS Fargate'e taşıma işlemi E-6 fazında yapılacaktır.

### E-5.1 Celery Worker Optimizasyonu

| Görev | Detay |
|-------|-------|
| Bellek limitleri | `worker_max_memory_per_child = 512MB`; limit aşımında worker restart |
| Hard timeout | `task_time_limit = 300` (5 dakika) |
| Soft timeout | `task_soft_time_limit = 240` (4 dakika) |
| Result backend temizleme | `result_expires = 3600` |
| Worker sayısı yapılandırma | `--autoscale=4,2` |

### E-5.2 PDF Şablon İyileştirmeleri

- **Satır numaralı prova:** Hakem değerlendirmesi için satır referansı
- **Filigran:** "CONFIDENTIAL — UNDER REVIEW" watermark
- **Kapak sayfası:** Dergi adı, manuscript ID, makale türü, gönderim tarihi, yazarlar
- **Sayfa numaralandırma:** Sayfa X/Y formatı

### E-5.3 Format Desteği Genişletme

| Format | Yöntem | Notlar |
|--------|--------|--------|
| DOCX → PDF | `python-docx` → HTML → WeasyPrint | Tablo, görsel desteği iyileştirilecek |
| LaTeX → PDF | `pandoc` veya `subprocess` ile `pdflatex` | Temel destek |
| Görsel optimizasyonu | `Pillow` ile boyut/çözünürlük optimizasyonu | PDF boyutunu küçültme |

### E-5.4 Gerçek Zamanlı İlerleme Bildirimi

- Django Channels (WebSocket) veya Server-Sent Events (SSE)
- PDF ve YZ analiz süreçleri için ilerleme bildirimi
- Frontend'de toast/modal ile gösterim

### E-5.5 YZ Benzerlik / İntihal Kontrolü (YENİ)

| Görev | Detay |
|-------|-------|
| Embedding tabanlı benzerlik | Makale embedding'i ile mevcut DB'deki tüm makalelerin karşılaştırılması |
| Duplicate submission tespiti | Aynı makale (veya çok benzer) tekrar gönderildiğinde otomatik uyarı |
| Eşik yapılandırma | JournalConfig'de benzerlik eşiği (varsayılan: %80) |
| Editöre rapor | Benzerlik skoru + en benzer makaleler listesi |
| Harici intihal servisi | iThenticate/Turnitin API entegrasyonu (isteğe bağlı, E-8'de) |

```python
def check_similarity(submission_id):
    embedding = get_submission_embedding(submission_id)
    similar = ArticleEmbedding.objects.annotate(
        similarity=CosineDistance('vector', embedding)
    ).filter(similarity__lt=0.2).exclude(
        submission_id=submission_id
    ).order_by('similarity')[:10]
    # Benzerlik raporu oluştur
```

### E-5.6 JATS XML Export (YENİ)

| Görev | Detay |
|-------|-------|
| Metadata → JATS XML dönüşümü | Başlık, özet, anahtar kelimeler, yazarlar |
| XML doğrulama | JATS DTD ile validation |
| Export endpoint | `GET /api/submissions/{id}/jats-xml/` |
| Toplu export | Admin panelinden seçili makalelerin JATS export'u |

### E-5.7 PDF Karşılaştırma

- Revizyon sonrası önceki ve yeni PDF arasında diff
- Metin bazlı karşılaştırma (pdfplumber ile metin çıkarıp diff)
- Editör görünümünde yan yana karşılaştırma arayüzü

---

## Faz E-6: Bulut Altyapısı Migration

**Süre:** 4–6 hafta  
**Bağımlılık:** E-1 ~ E-5 ürün modülleri tamamlanmış olmalı  
**Ara Çıktı:** AWS üzerinde çalışan, otomatik ölçeklenen kurumsal altyapı

> **Strateji:** "Önce Ürün, Sonra Altyapı" — Premature optimization tuzağından kaçınma.

### E-6a: Konteynerizasyon ve Orkestrasyon (2–3 hafta)

#### Docker Optimizasyonu

```
Konteynerler:
├── web            (Django + Gunicorn)
├── celery-worker  (PDF + e-posta + metadata + YZ analiz)
├── celery-beat    (Otonom motor periyodik taramalar)
├── redis          (ElastiCache'e geçene kadar)
└── postgres       (Aurora'ya geçene kadar)
```

#### AWS ECS Fargate Deployment

| Bileşen | ECS Konfigürasyonu |
|---------|-------------------|
| Web Service | 2 vCPU, 4 GB RAM; min 2 / max 10 task; ALB health check |
| Celery Worker | 2 vCPU, 4 GB RAM; min 1 / max 5 task |
| Celery Beat | 0.5 vCPU, 1 GB RAM; 1 task (singleton) |
| PDF Worker | 4 vCPU, 8 GB RAM; min 0 / max 10 task (event-driven) |
| YZ Worker | 2 vCPU, 4 GB RAM; min 1 / max 3 task (YZ analiz + embedding) |

### E-6b: Veritabanı ve Depolama Migration (1–2 hafta)

- Neon → Aurora Serverless v2 (pgvector extension dahil)
- Multi-tenant şema tasarımı (shared schema + tenant discriminator)
- Cloudflare R2 veya AWS S3 kararı (maliyet analizi)

### E-6c: Kod Olarak Altyapı — Terraform (1 hafta)

```
terraform/
├── modules/
│   ├── vpc/
│   ├── ecs/
│   ├── aurora/        # pgvector extension dahil
│   ├── elasticache/
│   ├── s3/
│   ├── cloudfront/
│   ├── waf/
│   └── secrets/
├── environments/
│   ├── staging/
│   └── production/
├── main.tf
├── variables.tf
└── outputs.tf
```

---

## Faz E-7: Güvenlik ve Performans

**Süre:** 3–4 hafta  
**Bağımlılık:** E-6 tamamlanmış olmalı  
**Ara Çıktı:** Güvenli, performanslı, izlenebilir sistem

### E-7.1 AWS WAF ve Ağ Güvenliği

| Kural | Açıklama |
|-------|----------|
| SQL Injection koruması | AWS Managed Rules — SQLi rule group |
| XSS koruması | AWS Managed Rules — XSS rule group |
| Rate limiting | IP başına 1000 req/5dk; login endpoint için 10 req/dk |
| Bot koruması | AWS Bot Control; scraping engeli |

### E-7.2 Uygulama Güvenliği

| Görev | Detay |
|-------|-------|
| JWT güçlendirme | Access token: 15 dk, Refresh token: 7 gün; token rotation |
| Güvenlik başlıkları | HSTS, CSP, X-Frame-Options, X-Content-Type-Options |
| OWASP Top 10 denetimi | Tüm API endpoint'lerinin sistematik taranması |
| Bağımlılık taraması | Dependabot + Snyk |
| KVKK/GDPR uyumluluk | Veri silme endpoint'i, veri export'u, şifreli depolama |
| YZ veri güvenliği | LLM API'ye gönderilen verilerde PII maskeleme |

### E-7.3 Performans Optimizasyonu

- Redis cache stratejisi (API yanıt, sorgu sonucu, embedding cache)
- Veritabanı sorgu optimizasyonu (N+1, indeks, pgvector HNSW indeks)
- Frontend optimizasyonu (code splitting, lazy loading, Brotli)

### E-7.4 İzleme ve Gözlemlenebilirlik

| Araç | Kullanım |
|------|----------|
| Datadog APM | Backend tracing, YZ API yanıt süreleri |
| Sentry | Hata yakalama, stack trace |
| CloudWatch | AWS kaynak metrikleri |
| Custom dashboard | Otonom motor metrikleri, YZ başarı oranları |

### E-7.5 Yük Testi

| Aşama | Kullanıcı | Hedef |
|-------|-----------|-------|
| 1 | 100 eşzamanlı | Baseline |
| 2 | 1.000 eşzamanlı | Darboğaz tespiti |
| 3 | 5.000 eşzamanlı | Auto-scale doğrulama |
| 4 | 10.000 eşzamanlı | Enterprise hedef: < 250ms |

### E-7.6 Penetrasyon Testi

- Üçüncü parti bağımsız siber güvenlik firması
- OWASP ASVS kapsamında
- Rapor sonuçlarına göre düzeltme sprint'i

---

## Faz E-8: Entegrasyonlar ve Standartlar

**Süre:** 3–4 hafta  
**Bağımlılık:** E-4 (admin yapılandırma) tamamlanmış olmalı  
**Ara Çıktı:** Uluslararası standartlara uyumlu entegrasyon katmanı

### E-8.1 DOI Entegrasyonu (CrossRef)

| Görev | Detay |
|-------|-------|
| CrossRef API entegrasyonu | Kabul edilen makalelere DOI atama |
| Metadata gönderimi | CrossRef XML formatında metadata deposit |
| DOI çözümleme ve UI gösterimi | Kabul makalelerde DOI badge |

### E-8.2 İntihal Kontrolü (Harici)

| Görev | Detay |
|-------|-------|
| iThenticate API entegrasyonu | E-5'teki yerel benzerlik kontrolüne ek olarak harici tarama |
| Benzerlik skoru gösterimi | Editör dashboard'da % benzerlik |
| Eşik yapılandırma | JournalConfig'de maksimum kabul edilebilir oran |

### E-8.3 OAI-PMH (Open Archives Initiative)

| Görev | Detay |
|-------|-------|
| OAI-PMH endpoint | `/oai/` — Identify, ListRecords, GetRecord, ListSets |
| Dublin Core mapping | Submission metadata → Dublin Core XML |

### E-8.4 Diğer Entegrasyonlar

- **ORCID API v3** güncellemesi
- **COUNTER istatistikleri** (isteğe bağlı)
- **COPE** etik ilkelerine uygunluk belgelendirme

---

## Faz E-9: Ticarileştirme

**Süre:** 2–3 hafta  
**Bağımlılık:** E-7 ve E-8 tamamlanmış olmalı  
**Ara Çıktı:** Ticarileştirmeye hazır SaaS ürünü (THS 9)

### E-9.1 Multi-tenant Onboarding

| Görev | Detay |
|-------|-------|
| Self-service kayıt | Yeni dergi/kurum kayıt formu |
| Dergi kurulum sihirbazı | Bilgiler → roller → formlar → otonomi ayarları → aktivasyon |
| DNS yapılandırma | `dergi-adi.trueditor.com` subdomain |

### E-9.2 Ödeme ve Faturalama

| Görev | Detay |
|-------|-------|
| Stripe entegrasyonu | Abonelik planları (Starter / Professional / Enterprise + AI) |
| Plan yönetimi | YZ özellikleri üst planlarda; base plan sadece temel modüller |
| Fatura oluşturma | Otomatik PDF fatura |

### E-9.3 Migration Araçları

| Kaynak | Yöntem |
|--------|--------|
| OJS | XML import |
| Editorial Manager | CSV/XML import |
| Manuel | Excel/CSV toplu yükleme |

### E-9.4 Pazarlama ve Dokümantasyon

| Görev | Detay |
|-------|-------|
| Ürün landing page | Özellik karşılaştırma, YZ demo, fiyatlandırma |
| API dokümantasyonu | Swagger / OpenAPI 3.0 |
| Kullanıcı kılavuzu | Rol bazlı: yazar, editör, hakem, admin |
| Video eğitimler | Her modül + YZ özellikleri walkthrough |

---

## Bağımlılık Diyagramı

```
FAZ-19 (Bitirme Projesi Tamamlanır)
    │
    ▼
E-1: Yazar + YZ Kalite Ölçümü ──────────────────────────────┐
    │                                                         │
    ├───────────────────────┐                                 │
    │                       │                                 │
    ▼                       ▼                                 ▼
E-AI: YZ Altyapı      E-5: PDF + İntihal             (paralel)
    │  ◄── 7250401 API      + JATS XML
    │                       │
    ▼                       │
E-2: Editör + Otonom Motor  │
    │                       │
    ▼                       │
E-3: Hakem + YZ Rapor       │
    │                       │
    ▼                       │
E-4: Sistem Yöneticisi      │
    │                       │
    └───────────┬───────────┘
                │
                ▼
        E-6: Bulut Migration (AWS)
                │
                ▼
        E-7: Güvenlik & Performans
                │
                ▼
        E-8: Entegrasyonlar & Standartlar
                │
                ▼
        E-9: Ticarileştirme (THS 9)
```

---

## Genel Zaman Çizelgesi

```
Hafta:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17
        ┌───┬───┬───┬───┬───┐
E-1     │ Yazar + SSO + YZ  │
        │ Kalite Ölçümü     │
        └───┴───┴───┴───┴───┘
                    ┌───┬───┬───┬───┐
E-AI                │ YZ Altyapı    │
                    │ + 7250401 API │ (E-2 ile kısmen paralel)
                    └───┴───┴───┴───┘
                                ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
E-2                             │          Editör + Otonom Motor         │
                                │ E-2a Backend+YZ │ E-2b Frontend+YZ    │
                                └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
        ┌───┬───┬───┬───┐
E-5     │ PDF + İntihal │   (E-1 sonrası paralel)
        │ + JATS XML    │
        └───┴───┴───┴───┘

Hafta: 17  18  19  20  21  22  23  24  25  26  27  28  29  30
                                ┌───┬───┬───┬───┬───┬───┐
E-3                             │  Hakem + YZ Rapor     │
                                │  + 7250401 Entegrasyon │
                                └───┴───┴───┴───┴───┴───┘
                                                        ┌───┬───┬───┐
E-4                                                     │Admin + YZ │
                                                        │ Config    │
                                                        └───┴───┴───┘

Hafta: 27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42
                                        ┌───┬───┬───┬───┬───┬───┐
E-6                                     │   Bulut Migration     │
                                        │ ECS + Aurora + TF     │
                                        └───┴───┴───┴───┴───┴───┘
                                                                ┌───┬───┬───┬───┐
E-7                                                             │Güvenlik&Perf.│
                                                                └───┴───┴───┴───┘

Hafta: 39  40  41  42  43  44  45  46  47  48  49  50
                                ┌───┬───┬───┬───┐
E-8                             │Entegrasyonlar │
                                └───┴───┴───┴───┘
                                                ┌───┬───┬───┐
E-9                                             │Ticarileşt.│
                                                └───┴───┴───┘
```

**Toplam Tahmini Süre: ~42–50 hafta (10–12 ay)**

---

## Özet Tablo

| Faz | Başlık | Süre | Bağımlılık | Ana Çıktı |
|-----|--------|------|------------|-----------|
| E-1 | Yazar + YZ Kalite | 4–5 hafta | FAZ-19 | SSO + Chunked Upload + YZ Kalite Ölçümü |
| E-AI | YZ Altyapı | 3–4 hafta | E-1 | pgvector + NLP Pipeline + 7250401 API + Otonom Motor |
| E-2 | Editör + Otonom Motor | 8–10 hafta | E-1, E-AI | Kanban + FSM + Embedding Eşleşme + Yarı Otonom Süreçler |
| E-3 | Hakem + YZ Rapor | 5–6 hafta | E-2 | Magic Link + JSONB Forms + Otonom Atama + Rapor Sınıflandırma |
| E-4 | Sistem Yöneticisi | 2–3 hafta | E-2, E-3 | RBAC + Journal Config + Otonomi Ayarları |
| E-5 | PDF + İntihal + JATS | 3–4 hafta | E-1 | PDF Motor + YZ Benzerlik + JATS XML Export |
| E-6 | Bulut Migration | 4–6 hafta | E-1~E-5 | AWS ECS + Aurora (pgvector) + Terraform |
| E-7 | Güvenlik & Performans | 3–4 hafta | E-6 | WAF + APM + Load Test + Pen Test |
| E-8 | Entegrasyonlar | 3–4 hafta | E-4 | DOI + iThenticate + OAI-PMH |
| E-9 | Ticarileştirme | 2–3 hafta | E-7, E-8 | Onboarding + Stripe + Docs |
| **TOPLAM** | | **42–50 hafta** | | **YZ Destekli Otonom Enterprise SaaS (THS 9)** |

---

## Notlar

1. **"Önce Ürün, Sonra Altyapı" Stratejisi:** E-1 ~ E-5 ürün modüllerini tamamladıktan sonra E-6'da tek seferde AWS'ye taşınır.

2. **YZ Model Stratejisi:** Hibrit yaklaşım — basit kurallar (referans yaşı, sayfa sayısı) kural tabanlı; karmaşık analiz (dil, rapor sınıflandırma) LLM API. Fallback her zaman "yarı otonom asistan" modu.

3. **7250401 Entegrasyonu:** Hakem Öneri Sistemi (31.08.2026 bitiş) ile REST API üzerinden entegrasyon. Motor bu projenin dışında, sadece API client yazılır.

4. **Otonomi Seviyeleri:** Her dergi kendi otonomi seviyesini yapılandırabilir (tam/yarı/asistan). Tam otonom modda bile kritik kararlar (accept/reject) editör onayı gerektirir.

5. **PDF Motor → Fargate Geçişi:** E-5'te lokalde geliştirilen PDF ve YZ motorları, E-6'da AWS Fargate'e taşınır.

6. **ECS vs EKS:** Başlangıçta ECS Fargate; 10.000+ eşzamanlı kullanıcıda EKS'e geçiş.

7. **Maliyet:** LLM API kullanımı için aylık ~$50–200 arası maliyet öngörülür (makale hacmine bağlı). pgvector yerel olduğu için ek maliyet yok.

8. **Bu yol haritası başlatılmadan önce mevcut bitirme projesi yol haritası (FAZ-17, FAZ-18, FAZ-19) tamamlanacaktır.** Başlama komutu kullanıcıdan gelecektir.

---

## TÜBİTAK v4 Öneri Geri Bildirimi

v4 önerisinin (Trueditör_Oneri_Deneme_4.docx) teknik analizi ve düzeltme önerileri:

### Güçlü Yönler (Doğru Yapılanlar)

1. **THS 3 seviyesi** — önceki proje altyapısına referansla savunulabilir
2. **7250401 proje referansı** — A.0 bölümünde organik bağ kurulmuş, hakem için ikna edici
3. **Başlangıç: 01.09.2026** — 7250401 bitiş sonrası (31.08.2026), temiz geçiş
4. **DevOps 5 ay** (İP-5 + İP-6 tam kapsama) — v2'deki 2 ay sorunu giderilmiş
5. **Bütçe dönemsel dağılımı doğru** — 510K + 765K + 900K + 345K = 2,520K
6. **Adam-ay dağılımı doğru** — 12 + 18 + 21 + 8 = 59
7. **YZ odaklı anlatım** — TÜBİTAK değerlendirmesinde büyük avantaj
8. **İP-4/İP-5 sıralama tutarlı** — İP-4 "lokal", İP-5 "buluta taşıma"
9. **Proje adı güçlü** — "Yapay Zeka Destekli Otonom Akademik Editoryal Yönetim Platformu"
10. **Yenilik sınıflandırması doğru** — Ülke için yeni ürün + yeni süreç yeniliği

### Düzeltilmesi Gereken Teknik Konular

**1. YZ Altyapı Maliyetleri Eksik (Orta Önem)**

Öneri ciddi YZ yetenekleri vaat ediyor ama bütçede:
- GPU/model servisi maliyeti yok (embedding modelleri compute gerektirir)
- LLM API maliyetleri yok (OpenAI API kullanılacaksa aylık maliyet)
- 60.000 TL bulut bütçesi hem PDF motoru hem YZ inference hem DB testi için yetersiz olabilir

**Öneri:** Hizmet alımlarında 60.000 TL bulut bütçesinin açıklamasına "YZ model eğitim/çıkarım (inference) kaynakları dahil" ifadesini ekleyin. Veya ayrı bir "YZ API ve Bulut Compute" kalemi.

**2. YZ Model Stratejisi Netleştirilmeli (Düşük Önem)**

Teknik belirsizlik bölümünde "halüsinasyon" ve "LLM uyarlama" sorunları güzel ele alınmış. Ancak:
- Hangi LLM modeli kullanılacak net değil (GPT? BERT? Yerel Llama?)
- Eğitim verisi kaynağı belirtilmemiş
- Model güncellik ve bakım stratejisi yok

TÜBİTAK hakemi sorabilir — ama bu düzeyde detay genellikle beklenmez.

**3. "%70 İş Yükü Azaltma" İddiası (Düşük Önem)**

Ekonomik bölümde "editörlerin iş yükünü %70 oranında azaltan" ifadesi var. Bu henüz kanıtlanmamış — "hedeflenmektedir" şeklinde yazılması daha güvenli.

**4. 4 Dönem Yapısı Doğrulanmalı (Bilgi)**

Proje 01.09.2026'da başladığı için TÜBİTAK'ın 6'şar aylık dönem yapısı farklı düşebilir:
- 2026/II (Eyl-Ara): 4 ay
- 2027/I (Oca-Haz): 6 ay
- 2027/II (Tem-Ara): 6 ay
- 2028/I (Oca-Şub): 2 ay

Bu dağılım M030 tablosunda doğru yansıtılmış. PRODİS girişinde dönem başlangıç/bitiş tarihlerine dikkat edilmeli.

### Genel Sonuç

v4 önerisi teknik olarak **güçlü, tutarlı ve yapılabilir**. YZ odaklı yeniden konumlandırma ve 7250401 entegrasyonu çok stratejik hamleler. Yukarıdaki düzeltmeler minör niteliktedir — öneri bu haliyle TÜBİTAK 1507'ye sunulabilir kalitededir.
