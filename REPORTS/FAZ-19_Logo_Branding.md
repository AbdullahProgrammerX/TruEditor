# FAZ-19: Logo & Branding — Tamamlanma Raporu

**Tarih:** 27 Mart 2026  
**Durum:** ✅ Tamamlandı

---

## 1. Yapılan İşler

### 1.0 Rakip / sektör benchmark (özet)

Kurumsal makale gönderim ve editöryal yönetim ürünleri (ör. **ScholarOne Manuscripts**, **Editorial Manager**, büyük yayıncı portalları) genelde şu görsel dilde toplanır:

- **Güven ve kurumsallık:** koyu mavi / lacivert ağırlıklı palet, sade arayüz.
- **İkonografi:** soyut veya minimal **belge / sayfa** motifleri; abartılı harf oyunlarından kaçınma.
- **Wordmark:** okunaklı sans veya akademik bağlamda serif vurgusu; dar tracking, net hiyerarşi.
- **Vurgu rengi:** tek bir ikincil renk (CTA / durum), görsel gürültü sınırlı.

TruEditor ikonu bu çizgiye göre **merkezlenmiş belge + katlanmış köşe + metin satırları + tek emerald çizgi** olarak yeniden tanımlandı.

### 1.1 Logo Tasarımı (SVG)

Vektörel logo sistemi; **manuscript / editorial** alanına uygun, optik olarak merkezlenmiş sayfa ikonu.

**Logo Varyantları:**

| Dosya | Kullanım Alanı | Açıklama |
|-------|---------------|----------|
| `favicon.svg` | Tarayıcı tab ikonu | 512×512, gradient zemin |
| `logo-icon.svg` | Header’lar, splash (img) | Kare uygulama ikonu |
| `logo-full.svg` | Tam marka şeridi | İkon + Inter wordmark + alt satır |
| `logo-white.svg` | Koyu zemin | Açık ikon + beyaz wordmark |
| `og-image.svg` | OG / Twitter | 1200×630 tanıtım görseli |

**Logo öğeleri:**
- **Zemin:** Yuvarlatılmış kare, üç duraklı navy → mavi gradient (`#1e3a5f` → `#1e4a7a` → `#1a56db`).
- **Beyaz sayfa:** Yuvarlatılmış dikdörtgen; sağ üst **katlanmış köşe** (yayıncılık belgesi çağrışımı).
- **Gri metin satırları:** Sayfa içeriğini temsil eden dört çizgi (`#e8eef5`).
- **Emerald çizgi:** Sayfanın altında **ortalanmış** tek vurgu (`#34d399` — revizyon / onay çağrışımı, mevcut accent paleti ile uyumlu).

### 1.2 Favicon & Meta Tag'ler

**`index.html` Güncellemeleri:**
- `<link rel="apple-touch-icon">` eklendi
- `<meta name="author">` eklendi
- **Open Graph meta tag'leri:** `og:type`, `og:title`, `og:description`, `og:image`, `og:site_name`, `og:locale`
- **Twitter Card meta tag'leri:** `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- Description metni güncellendi

### 1.3 Marka Renk Paleti Finalizasyonu

`style.css` `@theme` bloğu güncellendi:

| Token | Renk | Kullanım |
|-------|------|----------|
| `--color-brand` | `#1e3a5f` | Ana marka rengi (navy blue) |
| `--color-brand-light` | `#1a56db` | Gradient ikinci renk (bright blue) |
| `--color-brand-accent` | `#34d399` | Vurgu/accent (emerald green) |
| Primary 50-900 | Navy scale | Buton, header, linkler |
| Secondary 50-900 | Blue scale | Focus, hover, badge'ler |
| Accent 50-900 | Emerald scale | Başarı, aktif durumlar |
| ORCID | `#a6ce39` | ORCID entegrasyon butonları |

**Tipografi (değişiklik yok, finalize edildi):**
- **Sans:** Inter (tüm UI)
- **Serif:** Playfair Display (dekoratif)
- **Mono:** JetBrains Mono (kod/ID)

### 1.4 E-posta Şablonları Branding

`backend/templates/email/_base.html` tamamen güncellendi:
- **Header gradient:** `#1e3a5f` → `#1a56db` (frontend ile uyumlu hale getirildi)
- **Inline SVG logo** header'a eklendi (e-posta istemcileri için uyumlu)
- **Wordmark:** "Tru**Editor**" formatında (iki tonlu)
- **Alt yazı:** "MANUSCRIPT SYSTEM" (uppercase, letter-spacing)
- **Footer:** "TruEditor — Next Generation Academic Publishing" marka mesajı
- **Buton stilleri:** Gradient butonlar (`.btn`, `.btn-green`, `.btn-red`)

### 1.5 Splash / Loading Screen

`App.vue` splash ekranı, **logo kayması algısını** gidermek için güncellendi:
- **Logo:** `/logo-icon.svg` dosyası `<img>` ile gösterilir (header ile piksel uyumu); SVG parçalarına ayrı `transform` animasyonu **yoktur**.
- **Kutu hizası:** `80×80` sabit flex konteyner, `object-fit: contain`.
- **Animasyon:** Yalnızca **opacity** ile kısa görünüm + metin / progress bar için hafif fade-in; çıkışta sadece **fade** (scale yok).
- **Wordmark:** Splash’te **Playfair Display** (projede zaten yüklü serif) — yayıncı arayüzlerindeki ciddiyet ile uyum.
- **Alt satır:** "Manuscript submission system" (uppercase, letter-spacing).
- **Süre:** ~1.1 saniye (auth init ile paralel).

### 1.6 Tüm Sayfalarda Logo Güncellemesi

Aşağıdaki sayfalardaki eski metin tabanlı "T" logoları SVG logo ile değiştirildi:

| Sayfa | Dosya |
|-------|-------|
| Landing Page | `views/LandingPage.vue` (header + footer) |
| Login | `views/auth/LoginPage.vue` |
| Dashboard | `views/dashboard/Dashboard.vue` (header + footer) |
| Submissions List | `views/submission/SubmissionsList.vue` |
| Submission Detail | `views/submission/SubmissionDetail.vue` |
| Submit Revision | `views/submission/SubmitRevision.vue` |
| Complete Profile | `views/profile/CompleteProfile.vue` |
| Verify Contribution | `views/submission/VerifyContribution.vue` |

**Wordmark formatı:** `Tru`(beyaz/koyu) + `Editor`(hafif soluk) — tüm sayfalarda tutarlı.

---

## 2. Dosya Değişiklikleri Özeti

### Yeni Dosyalar
- `frontend/public/logo-icon.svg` — Kare ikon logo
- `frontend/public/logo-full.svg` — Tam logo (ikon + wordmark, açık arka plan)
- `frontend/public/logo-white.svg` — Beyaz varyant (koyu arka plan)
- `frontend/public/og-image.svg` — Open Graph sosyal paylaşım resmi

### Güncellenen Dosyalar
- `frontend/public/favicon.svg` — Yeni profesyonel tasarım
- `frontend/index.html` — Meta tag'ler (OG, Twitter Card, apple-touch-icon)
- `frontend/src/style.css` — Brand token'lar, palette isimlendirme
- `frontend/src/App.vue` — Splash screen eklendi
- `backend/templates/email/_base.html` — Inline SVG logo + güncel branding
- 8 Vue component — Logo güncellemeleri

### Silinen Dosyalar
- `frontend/src/assets/vue.svg` — Varsayılan Vue logosu (artık kullanılmıyor)

---

## 3. Marka Kimliği Özeti

```
┌──────────────────────────────────────────────┐
│  TruEditor Brand Identity                     │
├──────────────────────────────────────────────┤
│  Logo: Stylized "T" with document motif      │
│  Primary: #1e3a5f (Navy Blue)                │
│  Secondary: #1a56db (Bright Blue)            │
│  Accent: #34d399 (Emerald Green)             │
│  ORCID: #a6ce39 (ORCID Green)               │
│  Font: Inter (UI), Playfair Display (Deco)   │
│  Tagline: "Next Generation Academic Pub."    │
│  Sub-brand: "Manuscript System"              │
└──────────────────────────────────────────────┘
```
