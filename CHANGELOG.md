# Changelog

Bu dosya, TruEditor projesindeki tüm önemli değişiklikleri içerir.

Format [Keep a Changelog](https://keepachangelog.com/tr/1.0.0/) standardına,
versiyon numaraları [Semantic Versioning](https://semver.org/lang/tr/) standardına uygundur.

## [Unreleased]

### Eklenen (Added)
- Proje temel yapılandırma dosyaları oluşturuldu
  - `.cursorrules` - Cursor AI geliştirme kuralları
  - `README.md` - Proje dokümantasyonu
  - `CHANGELOG.md` - Değişiklik günlüğü
  - `.gitignore` - Git ignore kuralları
  - `.env.example` - Ortam değişkenleri şablonu

### Değiştirilen (Changed)
- (Henüz yok)

### Kaldırılan (Removed)
- (Henüz yok)

### Düzeltilen (Fixed)
- (Henüz yok)

### Güvenlik (Security)
- (Henüz yok)

---

## Versiyon Geçmişi

### [1.0.0] - Planlanan
#### Eklenen
- Author Module (Yazar Modülü)
  - ORCID ile zorunlu kimlik doğrulama
  - Makale gönderim sihirbazı (6 adım)
  - Sürükle-bırak dosya yükleme
  - Otomatik kayıt (autosave)
  - PDF oluşturma (Celery + WeasyPrint)
  - Gönderim takibi
  
- Backend Altyapısı
  - Django 5.x + DRF
  - PostgreSQL veritabanı
  - Redis cache ve message broker
  - Celery asenkron görevler
  - AWS S3 dosya depolama
  
- Frontend Arayüzü
  - Vue.js 3 + TypeScript
  - Pinia state management
  - TailwindCSS styling
  - Modern animasyonlar
  - Responsive tasarım
  
- Marka Kimliği
  - TruEditor logosu
  - Landing page
  - Renk paleti ve tipografi

---

## Gelecek Sürümler (Planlanan)

### [1.1.0] - Reviewer Module
- Hakem davet sistemi
- İnceleme formları
- Değerlendirme raporları
- Hakem dashboard'u

### [1.2.0] - Editor Module
- Editör ataması
- Karar verme arayüzü
- İş akışı yönetimi
- Editör dashboard'u

### [1.3.0] - Admin Module
- Kullanıcı yönetimi
- Sistem ayarları
- Gelişmiş raporlama
- Analitik dashboard

### [2.0.0] - Gelişmiş Özellikler
- Çoklu dil desteği
- Dark mode
- Mobil uygulama (PWA)
- Gelişmiş bildirim sistemi
- Entegrasyon API'leri

---

## Katkıda Bulunanlar

- Proje sahibi ve ana geliştirici: [İsim]

---

[Unreleased]: https://github.com/username/trueditor/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/trueditor/releases/tag/v1.0.0
