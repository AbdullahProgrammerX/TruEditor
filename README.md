# TruEditor

<p align="center">
  <img src="frontend/src/assets/images/logo.svg" alt="TruEditor Logo" width="200">
</p>

<p align="center">
  <strong>Akademik Yayıncılıkta Yeni Nesil</strong>
</p>

<p align="center">
  ORCID entegrasyonlu, modern ve kullanıcı dostu akademik dergi yönetim sistemi
</p>

<p align="center">
  <a href="#özellikler">Özellikler</a> •
  <a href="#teknolojiler">Teknolojiler</a> •
  <a href="#kurulum">Kurulum</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#api-dokümantasyonu">API</a>
</p>

---

## 🎯 Hakkında

TruEditor, akademik dergilerin makale gönderim ve değerlendirme süreçlerini yönetmek için tasarlanmış modern bir web uygulamasıdır. ORCID entegrasyonu ile güvenli kimlik doğrulama, sürükle-bırak dosya yönetimi ve gerçek zamanlı PDF oluşturma özellikleri sunar.

## ✨ Özellikler

### 🔐 ORCID Entegrasyonu
- **Zorunlu ORCID ile Giriş**: Tüm kullanıcılar ORCID hesaplarıyla sisteme giriş yapar
- **Otomatik Profil Senkronizasyonu**: Ad, soyad, kurum bilgileri ORCID'den çekilir
- **Tek Tıkla Giriş**: Email/şifre hatırlama derdi yok

### 📝 Makale Gönderim Sihirbazı
- **Adım Adım Rehberlik**: 6 adımlı kolay gönderim süreci
- **Sürükle-Bırak Dosya Yükleme**: Dosyaları kolayca sıralayın
- **Otomatik Kayıt**: Verileriniz otomatik olarak kaydedilir
- **Akıllı Meta Veri Çıkarımı**: Word dosyasından başlık ve özet çekme

### ⚡ Hızlı PDF Oluşturma
- **Arka Planda İşlem**: PDF oluşturulurken çalışmaya devam edin
- **Gerçek Zamanlı Bildirim**: PDF hazır olduğunda anında haberdar olun
- **Profesyonel Çıktı**: Türkçe karakter desteği ile temiz PDF

### 🎨 Modern Arayüz
- **Animasyonlu Geçişler**: Akıcı kullanıcı deneyimi
- **Responsive Tasarım**: Mobil uyumlu
- **Skeleton Loading**: Veri yüklenirken güzel görünüm

## 🛠 Teknolojiler

### Backend
| Teknoloji | Versiyon | Açıklama |
|-----------|----------|----------|
| Python | 3.11+ | Programlama dili |
| Django | 5.x | Web framework |
| Django REST Framework | 3.14+ | API framework |
| PostgreSQL | 15+ | Veritabanı |
| Redis | 7+ | Cache ve message broker |
| Celery | 5.x | Asenkron görev kuyruğu |
| WeasyPrint | 60+ | PDF oluşturma |

### Frontend
| Teknoloji | Versiyon | Açıklama |
|-----------|----------|----------|
| Vue.js | 3.x | JavaScript framework |
| TypeScript | 5.x | Type-safe JavaScript |
| Pinia | 2.x | State management |
| TailwindCSS | 3.x | CSS framework |
| Vite | 5.x | Build tool |

### Altyapı
| Teknoloji | Açıklama |
|-----------|----------|
| Railway | Hosting platformu |
| AWS S3 | Dosya depolama |
| GitHub Actions | CI/CD |

## 📁 Proje Yapısı

```
TruEditor/
├── backend/                 # Django backend
│   ├── core/               # Proje ayarları
│   │   ├── settings/
│   │   ├── celery.py
│   │   └── urls.py
│   ├── apps/
│   │   ├── users/          # Kullanıcı yönetimi
│   │   ├── submissions/    # Makale gönderimleri
│   │   ├── files/          # Dosya yönetimi
│   │   └── notifications/  # Bildirimler
│   └── requirements/
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   └── services/
│   └── public/
├── REPORTS/                # Geliştirme raporları
├── .cursorrules           # AI geliştirme kuralları
├── .env.example           # Ortam değişkenleri şablonu
└── README.md
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/your-username/TruEditor.git
cd TruEditor
```

### 2. Backend Kurulumu
```bash
# Virtual environment oluşturun
cd backend
python -m venv venv

# Aktifleştirin (Windows)
venv\Scripts\activate

# Aktifleştirin (Linux/Mac)
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements/development.txt

# .env dosyasını oluşturun
cp ../.env.example .env
# .env dosyasını düzenleyin

# Veritabanı migration'larını çalıştırın
python manage.py migrate

# Geliştirme sunucusunu başlatın
python manage.py runserver
```

### 3. Frontend Kurulumu
```bash
cd frontend

# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm run dev
```

### 4. Celery Worker (Opsiyonel - PDF için)
```bash
cd backend
celery -A core worker -l info
```

## ⚙️ Ortam Değişkenleri

`.env` dosyasında aşağıdaki değişkenleri yapılandırın:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/trueditor

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=trueditor-files
AWS_S3_REGION_NAME=eu-central-1

# ORCID OAuth
ORCID_CLIENT_ID=your-orcid-client-id
ORCID_CLIENT_SECRET=your-orcid-client-secret
ORCID_REDIRECT_URI=http://localhost:8000/api/v1/auth/orcid/callback/

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 📖 Kullanım

### ORCID ile Giriş
1. Ana sayfada "ORCID ile Giriş Yap" butonuna tıklayın
2. ORCID hesabınızla giriş yapın
3. TruEditor'a yetki verin
4. Otomatik olarak dashboard'a yönlendirilirsiniz

### Makale Gönderme
1. Dashboard'da "Yeni Gönderim Başlat" butonuna tıklayın
2. Makale tipini seçin
3. Dosyalarınızı sürükle-bırak ile yükleyin
4. Başlık, özet ve anahtar kelimeleri girin
5. Ortak yazarları ekleyin
6. PDF oluşturun ve onaylayın
7. Gönderin!

## 📚 API Dokümantasyonu

API endpoint'leri `/api/v1/` prefix'i altında sunulmaktadır.

### Authentication
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/auth/orcid/login/` | GET | ORCID login URL'i |
| `/auth/orcid/callback/` | POST | OAuth callback |
| `/auth/logout/` | POST | Çıkış yap |
| `/auth/token/refresh/` | POST | Token yenile |
| `/auth/profile/` | GET/PUT | Profil bilgileri |

### Submissions
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/submissions/` | GET | Gönderim listesi |
| `/submissions/` | POST | Yeni gönderim |
| `/submissions/{id}/` | GET | Gönderim detayı |
| `/submissions/{id}/` | PUT/PATCH | Güncelleme |
| `/submissions/{id}/` | DELETE | Silme |
| `/submissions/{id}/build_pdf/` | POST | PDF oluştur |
| `/submissions/{id}/approve/` | POST | Onayla |

### Files
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/files/` | POST | Dosya yükle |
| `/files/{id}/` | DELETE | Dosya sil |
| `/files/{id}/download/` | GET | İndir (presigned URL) |
| `/files/reorder/` | POST | Sıralama güncelle |

## 🗺 Yol Haritası

### ✅ Mevcut (v1.0)
- [x] ORCID Authentication
- [x] Author Module
- [x] Makale gönderim sihirbazı
- [x] PDF oluşturma
- [x] Dosya yönetimi

### 🔜 Planlanan
- [ ] Reviewer Module (Hakem değerlendirme)
- [ ] Editor Module (Editör yönetimi)
- [ ] Admin Module (Sistem yönetimi)
- [ ] Email bildirimleri
- [ ] Çoklu dil desteği
- [ ] Dark mode

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Proje Sahibi**: [İsim]
- **Email**: [email]
- **GitHub**: [github-link]

---

<p align="center">
  TruEditor ile ❤️ yapıldı
</p>
