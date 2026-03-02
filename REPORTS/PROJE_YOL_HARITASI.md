# TruEditor - Proje Yol Haritası

**Son Güncelleme:** 2026-01-23  
**Geliştirici:** Abdullah Doğan  
**Referans:** Editorial Manager (EM) Author Module analizi

---

## Tamamlanan Fazlar

| Faz | Başlık | Durum |
|-----|--------|-------|
| FAZ-0 | Proje Kuralları & Yapı | ✅ Tamamlandı |
| FAZ-1 | Django Backend Kurulumu | ✅ Tamamlandı |
| FAZ-1.5 | Vue Frontend Kurulumu | ✅ Tamamlandı |
| FAZ-2 | Production Ready Mimari | ✅ Tamamlandı |
| FAZ-3 | Veritabanı Modelleri (FSM, Author, Submission) | ✅ Tamamlandı |
| FAZ-4 | Deployment - Canlıya Alma (Render + Vercel + Neon) | ✅ Tamamlandı |
| FAZ-5 | ORCID Entegrasyonu & Kimlik Doğrulama | ✅ Tamamlandı |
| FAZ-6 | Author Module Backend API | ✅ Tamamlandı |
| FAZ-7 | Author Module Frontend (6 Adımlı Wizard) | ✅ Tamamlandı |
| FAZ-8 | S3 Dosya Yönetimi (Cloudflare R2) | ✅ Tamamlandı |
| FAZ-9 | Gönderi Detay Sayfası | ✅ Tamamlandı |
| FAZ-10 | PDF Oluşturma & Önizleme | ✅ Tamamlandı |
| FAZ-11 | E-posta Bildirim Sistemi | ✅ Tamamlandı |
| FAZ-12 | Revizyon İş Akışı | ✅ Tamamlandı |

---

## Yüksek Öncelik Fazları (Sistemi Kullanılabilir Kılan)

### FAZ-9: Gönderi Detay Sayfası (Submission Detail)

**Neden Kritik:** Yazar, gönderimini yaptıktan sonra detaylarını göremiyor. EM'de yazar her zaman gönderiminin tüm bilgilerini takip edebilir.

**Kapsam:**
- [ ] Gönderi detay sayfası (tam görünüm)
  - Durum badge'i ve geçmiş timeline
  - Makale bilgileri (başlık, özet, anahtar kelimeler, dil)
  - Yazar listesi (sıralı, sorumlu yazar işaretli)
  - Yüklenen dosyalar listesi (indirme bağlantıları ile)
  - Ek bilgiler (etik, çıkar çatışması, fonlama vb.)
  - Hakem önerileri / itirazları
  - Editöre gönderilen notlar
- [ ] Durum geçmişi modeli aktifleştirme
  - `SubmissionStatusHistory` kaydının FSM geçişlerinde otomatik oluşturulması
  - Timeline UI bileşeni
- [ ] Aksiyon butonları (duruma göre dinamik)
  - Draft → "Düzenle" / "Sil" / "Gönder"
  - Submitted → "Geri Çek"
  - Revision Required → "Revize Et" / "Revizyonu Reddet"
- [ ] Dosya indirme (presigned URL ile)
- [ ] Yazdır / PDF olarak kaydet butonu

**Tahmini Süre:** 1-2 gün  
**Bağımlılıklar:** Yok (mevcut API yeterli)

---

### FAZ-10: PDF Oluşturma & Önizleme

**Neden Kritik:** EM'de her gönderi bir PDF'e dönüştürülür ve yazar onayına sunulur. Bu, editör değerlendirmesi için de gereklidir.

**Kapsam:**

#### Backend
- [ ] PDF şablonu tasarımı (WeasyPrint)
  - Kapak sayfası (dergi adı, makale tipi, tarih, manuscript ID)
  - Makale bilgileri (başlık, özet, anahtar kelimeler)
  - Yazar listesi ve kurum bilgileri
  - Ana metin içeriği (dosyadan çekilecek)
- [ ] `build_pdf` endpoint implementasyonu (mevcut stub)
  - Celery task olarak çalışacak (arka plan)
  - PDF'i R2'ye yükle
  - `task_status` endpoint ile durum sorgulama
- [ ] PDF dosyasını `ManuscriptFile` olarak kaydetme (tip: `system_pdf`)

#### Frontend
- [ ] PDF oluşturma butonu (Detay sayfasında)
- [ ] PDF oluşturma durumu göstergesi (loading/progress)
- [ ] PDF önizleme (tarayıcı içi PDF viewer)
- [ ] PDF onaylama adımı (isteğe bağlı)

**Tahmini Süre:** 2-3 gün  
**Bağımlılıklar:** FAZ-9 (detay sayfası), Celery/Redis yapılandırması

---

### FAZ-11: E-posta Bildirim Sistemi

**Neden Kritik:** EM'de her önemli işlem bir e-posta ile bildirilir. Kullanıcı sistemle etkileşimde olduğunda bilgilendirilmeli.

**Kapsam:**

#### Backend
- [ ] E-posta servisi kurulumu (`apps/notifications/`)
  - HTML e-posta şablonları (TruEditor markalı)
  - E-posta gönderme servisi (SMTP / Resend / SendGrid)
  - Celery task ile asenkron gönderim
- [ ] E-posta şablonları:
  - **Kayıt hoş geldiniz e-postası** - Yeni kullanıcı ORCID ile kayıt olduğunda
  - **Gönderim onayı** - Makale başarıyla gönderildiğinde (manuscript ID ile)
  - **Durum değişikliği** - Gönderimin durumu değiştiğinde
  - **Revizyon talebi** - Editör revizyon istediğinde
  - **Karar bildirimi** - Kabul / Red kararı verildiğinde
- [ ] E-posta gönderim geçmişi (loglama)
- [ ] E-posta tercihleri (kullanıcı hangi bildirimleri almak istiyor)

#### Frontend
- [ ] Profil sayfasında e-posta bildirim tercihleri
- [ ] Gönderim sonrası "Onay e-postası gönderildi" bildirimi

**Tahmini Süre:** 2-3 gün  
**Bağımlılıklar:** SMTP sağlayıcı yapılandırması (Resend veya SendGrid ücretsiz plan)

---

### FAZ-12: Revizyon İş Akışı ✅ Tamamlandı

**Tamamlanma Tarihi:** 2026-03-02

**Yapılanlar:**

#### Backend
- [x] `revision_response` ve `revision_submitted_at` alanları Submission modeline eklendi
- [x] `submit_revision` FSM geçişi güncellendi (timestamp kaydı)
- [x] `submit_revision` API endpoint oluşturuldu (POST /submissions/{id}/submit_revision/)
- [x] Dosya yükleme sırasında `revision_number` otomatik atanıyor
- [x] Revizyon durumu e-posta bildirimi (mevcut status_change şablonu)
- [x] Serializer güncellendi (revision_response, revision_submitted_at)

#### Frontend
- [x] `/submissions/:id/revise` — Tam kapsamlı revizyon sayfası
  - Editörün revizyon notları ve deadline gösterimi
  - Hakemlere yanıt (textarea, min 20 karakter)
  - Revizyon dosyası yükleme (drag & drop)
  - Önceki dosyaları görüntüleme (read-only)
  - Checklist (yanıt / dosya / upload durumu)
  - Onay modalı
- [x] Detail sayfasına "Submit Revision" butonu (revision_required durumunda)
- [x] Additional sekmesinde editör isteği + yazar yanıtı birlikte gösterim
- [x] TypeScript tipleri güncellendi (revision_response, revision_submitted_at)
- [ ] "Revizyonu Reddet" butonu ve onay dialogu
- [ ] Revizyon geçmişi timeline

**Tahmini Süre:** 3-4 gün  
**Bağımlılıklar:** FAZ-9 (detay sayfası), FAZ-10 (PDF - isteğe bağlı)

---

### FAZ-13: Metadata Çıkarma (Extraction)

**Neden Kritik:** EM'de yüklenen dosyadan Başlık, Özet, Anahtar Kelimeler ve Yazarlar otomatik çıkarılır. Bu, veri girişini büyük ölçüde azaltır.

**Kapsam:**

#### Backend
- [ ] DOCX dosyasından metadata çıkarma (`python-docx`)
  - Başlık (document properties + ilk satır analizi)
  - Özet (Abstract bölümü tespiti)
  - Anahtar kelimeler (Keywords bölümü tespiti)
  - Yazar isimleri (belge özellikleri + metin analizi)
- [ ] PDF dosyasından metadata çıkarma (`PyPDF2` / `pdfplumber`)
  - Başlık (PDF metadata + ilk satır)
  - Özet
- [ ] Metadata çıkarma API endpoint'i
  - `POST /files/{id}/extract_metadata/`
  - Sonuç: `{ title, abstract, keywords[], authors[] }`
- [ ] Hata toleransı (çıkarma başarısız olursa sessizce devam et)

#### Frontend
- [ ] Dosya yükleme sonrası otomatik metadata çıkarma tetikleme
- [ ] Çıkarılan verileri wizard alanlarına önerme (overwrite değil, öneri)
- [ ] "Otomatik dolduruldu" bildirim mesajı
- [ ] Kullanıcının önerileri kabul/red etme seçeneği

**Tahmini Süre:** 2-3 gün  
**Bağımlılıklar:** FAZ-8 (dosya yükleme)

---

## Orta Öncelik Fazları (Kaliteyi Artıran)

### FAZ-14: Dosya Sıralama UI (Sürükle-Bırak)

**Kapsam:**
- [ ] Frontend sürükle-bırak dosya sıralama (vuedraggable veya native HTML5 DnD)
- [ ] Dosya açıklama (description) alanı ekleme
- [ ] Dosya sıra numarası gösterimi
- [ ] Backend reorder endpoint zaten mevcut

**Tahmini Süre:** 0.5-1 gün

---

### FAZ-15: Kayıt Onay E-postası & Hoş Geldiniz Akışı

**Kapsam:**
- [ ] ORCID ile ilk kayıt sonrası hoş geldiniz e-postası
- [ ] E-posta doğrulama mekanizması (isteğe bağlı)
- [ ] Hesap oluşturma onay sayfası
- [ ] Profil tamamlama hatırlatma e-postası (profil eksikse 24 saat sonra)

**Tahmini Süre:** 0.5-1 gün  
**Bağımlılıklar:** FAZ-11 (e-posta servisi)

---

### FAZ-16: Yazışma Geçmişi & Karar Mektubu

**Kapsam:**
- [ ] `Correspondence` modeli (gönderen, alıcı, konu, içerik, tarih)
- [ ] Yazışma geçmişi API endpoint'leri
- [ ] Detay sayfasında yazışma sekmesi
- [ ] Karar mektubu görüntüleme
- [ ] Editöre mesaj gönderme formu

**Tahmini Süre:** 1-2 gün  
**Bağımlılıklar:** FAZ-9 (detay sayfası)

---

### FAZ-17: Ortak Yazar Erişimi & Doğrulama

**Kapsam:**
- [ ] Ortak yazarlara bildirim gönderme
- [ ] Ortak yazar katkı doğrulaması
- [ ] Ortak yazarların gönderiyi görüntüleyebilmesi
- [ ] "Authorship" sütunu (Sorumlu Yazar / Ortak Yazar)

**Tahmini Süre:** 2-3 gün  
**Bağımlılıklar:** FAZ-11 (e-posta), FAZ-9 (detay sayfası)

---

### FAZ-18: Çok Dilli Arayüz (i18n - TR/EN)

**Kapsam:**
- [ ] Vue i18n kurulumu
- [ ] Tüm frontend metinlerin çeviri dosyalarına taşınması
- [ ] Türkçe ve İngilizce dil dosyaları
- [ ] Dil değiştirme butonu (header'da)
- [ ] Backend hata mesajlarının çoklu dil desteği

**Tahmini Süre:** 2-3 gün  
**Bağımlılıklar:** Yok

---

### FAZ-19: Logo & Branding

**Kapsam:**
- [ ] TruEditor logosu tasarımı (favicon, header, e-posta)
- [ ] Marka renk paleti ve tipografi finalizasyonu
- [ ] Landing page görsel iyileştirmeleri
- [ ] E-posta şablonlarına marka kimliği ekleme
- [ ] Favicon ve meta tag'ler (Open Graph, Twitter Card)
- [ ] Loading ekranı / splash screen

**Tahmini Süre:** 1 gün

---

## İleri Aşama (Gelecek Planı - Şimdilik Beklemede)

Bu özellikler EM'in gelişmiş özelliklerdir. Temel sistem tamamlandıktan sonra değerlendirilecektir.

| # | Özellik | Açıklama |
|---|---------|----------|
| A | Benzerlik Kontrolü (Plagiarism) | iThenticate / Turnitin entegrasyonu |
| B | Referans Kontrolü | PubMed / CrossRef ile referans doğrulama |
| C | Görsel Kalite Kontrolü (AQC) | Yüklenen görsellerin çözünürlük/format kontrolü |
| D | Ücretler ve Ödemeler | Gönderim ücreti, PayPal/Stripe entegrasyonu |
| E | Editör Modülü | Editör dashboard, atama, karar verme |
| F | Hakem Modülü | Hakem daveti, değerlendirme formu, karar |
| G | Davetli Makaleler | Yazar davet sistemi, kabul/red |
| H | GDPR - Hesap Silme | Kullanıcı verilerini silme/anonimleştirme |

---

## Genel Zaman Çizelgesi

```
Tamamlandı:  FAZ-0 → FAZ-8  (Temel altyapı + Yazar submission wizard)
             ════════════════════════════════════════════════

Yüksek:      FAZ-9        FAZ-10       FAZ-11       FAZ-12       FAZ-13
             Detail       PDF          E-posta      Revizyon     Metadata
             Sayfa        Oluşturma    Bildirim     İş Akışı     Çıkarma
             (1-2 gün)    (2-3 gün)    (2-3 gün)    (3-4 gün)    (2-3 gün)
             ─────────────────────────────────────────────────────────────

Orta:        FAZ-14       FAZ-15       FAZ-16       FAZ-17       FAZ-18
             Dosya        Kayıt        Yazışma      Ortak        Çok Dilli
             Sıralama     Onay Mail    Geçmişi      Yazar        Arayüz
             (0.5-1 gün)  (0.5-1 gün)  (1-2 gün)    (2-3 gün)    (2-3 gün)
             ─────────────────────────────────────────────────────────────

Son:         FAZ-19
             Logo & Branding
             (1 gün)
             ─────────────

İleri:       [A] Plagiarism  [B] Referans  [C] AQC  [D] Ödeme
             [E] Editör      [F] Hakem     [G] Davet  [H] GDPR
             ═══════════════════════════════════════════════════
```

---

## EM Karşılaştırma Özeti

| Kategori | EM Özellik Sayısı | TruEditor Mevcut | Tamamlanma |
|----------|-------------------|------------------|------------|
| Kayıt & Giriş | 12 | 6 | %50 |
| Makale Gönderme | 16 | 14 | %88 |
| PDF & Onay | 4 | 0 | %0 |
| Takip & İzleme | 8 | 2 | %25 |
| Revizyon | 8 | 1 | %12 |
| E-posta Bildirim | 5 | 0 | %0 |
| **Toplam** | **53** | **23** | **%43** |

> **Hedef:** Yüksek öncelikli fazlar tamamlandığında → %75+  
> **Hedef:** Orta öncelikli fazlar tamamlandığında → %90+

---

## Notlar

- Ücretler/ödemeler modülü EM'in bir parçası olmasına rağmen, açık erişim (open access) dergilerde gönderim ücreti almayan modeller yaygınlaşmaktadır. Bu nedenle MVP kapsamı dışında tutulmuştur.
- Editör ve Hakem modülleri ayrı bir yol haritası belgesinde planlanacaktır.
- Her faz tamamlandığında `REPORTS/FAZ-X_*.md` raporu oluşturulacaktır.
