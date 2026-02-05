# TruEditor - Faz Numaraları Rehberi

**Son Güncelleme:** 23 Ocak 2026

---

## 📋 Faz Numaraları (Kronolojik Sıra)

### ✅ Tamamlanan Fazlar

| Faz | İsim | Durum | Rapor |
|-----|------|-------|-------|
| **Faz 0** | Proje Kuralları | ✅ | `FAZ-0_Proje_Kurallari.md` |
| **Faz 1** | Django Backend Kurulumu | ✅ | `FAZ-1_Django_Backend_Kurulumu.md` |
| **Faz 1.5** | Vue.js Frontend Kurulumu | ✅ | `FAZ-1.5_Vue_Frontend_Kurulumu.md` |
| **Faz 2** | Production-Ready Mimari | ✅ | `FAZ-2_Production_Ready_Mimari.md` |
| **Faz 3** | Veritabanı Modelleri | ✅ | `FAZ-3_Veritabani_Modelleri.md` |
| **Faz 4** | Deployment (Canlıya Alma) | ✅ | `FAZ-4_Deployment_Canliya_Alma.md` |
| **Faz 5** | ORCID Entegrasyonu & UI Güncellemesi | ✅ | `FAZ-5_ORCID_Entegrasyonu_ve_UI_Guncellemesi.md` |
| **Faz 6** | Author Module Backend API | ✅ | `FAZ-6_Author_Module_Backend_API.md`<br>`FAZ-6_Author_Module_Backend_API_TEST.md` |
| **Faz 7** | Author Module Frontend (Wizard) | ✅ | `FAZ-7_Author_Module_Frontend.md` |

### ⏳ Planlanan Fazlar

| Faz | İsim | Öncelik |
|-----|------|---------|
| **Faz 8** | S3 Dosya Yönetimi | Yüksek |
| **Faz 9** | PDF Generation (Celery + WeasyPrint) | Orta |
| **Faz 10** | Logo & Branding | Düşük |

---

## 📁 Rapor Yapısı

### Ana Raporlar
- `FAZ-{NUMARA}_{ISIM}.md` - Ana faz raporu

### Sub-Raporlar
- `FAZ-{NUMARA}_{ISIM}_TEST.md` - Test raporu
- `FAZ-{NUMARA}_{ISIM}_DEPLOYMENT.md` - Deployment raporu (gerekirse)
- `FAZ-{NUMARA}_{ISIM}_REVIEW.md` - Review raporu (gerekirse)

### Özel Raporlar
- `PLAN_KARSILASTIRMA_ve_EKSIKLER.md` - Plan karşılaştırması
- `PROJE_DURUM_RAPORU.md` - Genel proje durumu

---

## 🔄 Faz Ekleme Kuralları

1. **Kronolojik Sıra:** Fazlar kronolojik sıraya göre numaralandırılır
2. **Sub-Fazlar:** Ara işlemler için `.5` kullanılabilir (örn: Faz 1.5)
3. **Rapor İsimlendirme:** `FAZ-{NUMARA}_{KISA_ISIM}.md` formatı
4. **Test Raporları:** `_TEST` suffix ile sub-rapor olarak eklenir
5. **Güncelleme:** Yeni faz eklendiğinde bu dosya güncellenir

---

## 📝 Notlar

- Faz numaraları **asla değiştirilmez** (tarihsel kayıt için)
- Eksik fazlar için numara **atlanmaz** (sıralı devam eder)
- Sub-raporlar ana raporun altında organize edilir
- Her faz tamamlandığında rapor oluşturulur

---

**Son Güncelleme:** 23 Ocak 2026
