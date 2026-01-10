<script setup lang="ts">
/**
 * TruEditor - Landing Page
 * ========================
 * Modern, profesyonel ve animasyonlu landing page.
 * Akademik dergi yönetim sistemi için tasarlandı.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Animation states
const isLoaded = ref(false)
const showFeatures = ref(false)
const showStats = ref(false)

onMounted(() => {
  // Staggered entrance animations
  setTimeout(() => {
    isLoaded.value = true
  }, 100)
  
  setTimeout(() => {
    showFeatures.value = true
  }, 600)
  
  setTimeout(() => {
    showStats.value = true
  }, 1000)
  
  // Redirect if already authenticated
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})

// Navigate to login
function goToLogin() {
  router.push('/login')
}

// Features data
const features = [
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
    </svg>`,
    title: 'ORCID Entegrasyonu',
    description: 'Tek tıkla güvenli giriş. Şifre hatırlama derdi yok, veri girişi %80 azalır.',
    color: 'from-emerald-500 to-teal-600'
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
    </svg>`,
    title: 'Akıllı Gönderim Sihirbazı',
    description: 'Adım adım rehberlik ile kolay makale gönderimi. Hiçbir adımı kaçırmazsınız.',
    color: 'from-blue-500 to-indigo-600'
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
    </svg>`,
    title: 'Sürükle-Bırak Dosya',
    description: 'Manuel sıralama yok. Dosyalarınızı sürükleyip bırakarak kolayca düzenleyin.',
    color: 'from-violet-500 to-purple-600'
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
    </svg>`,
    title: 'Otomatik Kayıt',
    description: 'Verileriniz anlık olarak kaydedilir. Sayfa kapansa bile veri kaybı olmaz.',
    color: 'from-amber-500 to-orange-600'
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
    </svg>`,
    title: 'Asenkron PDF',
    description: 'PDF oluşturulurken beklemek yok. Arka planda hazırlanır, bildirim alırsınız.',
    color: 'from-rose-500 to-pink-600'
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
    </svg>`,
    title: 'Gerçek Zamanlı Takip',
    description: 'Gönderimlerinizin her aşamasını anlık takip edin. Her zaman bilgilendirilirsiniz.',
    color: 'from-cyan-500 to-blue-600'
  },
]

// Stats data
const stats = [
  { value: '500+', label: 'Akademisyen', suffix: '' },
  { value: '2000+', label: 'Makale', suffix: '' },
  { value: '99.9', label: 'Uptime', suffix: '%' },
  { value: '< 3', label: 'Saniye PDF', suffix: 'sn' },
]
</script>

<template>
  <div class="min-h-screen bg-gradient-hero overflow-hidden">
    
    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Grid pattern -->
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjAyIi8+PC9nPjwvc3ZnPg==')] opacity-40"></div>
      
      <!-- Glowing orbs -->
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow delay-500"></div>
      <div class="absolute top-1/2 left-10 w-64 h-64 bg-emerald-500/15 rounded-full blur-3xl animate-pulse-slow delay-300"></div>
      
      <!-- Floating shapes -->
      <div class="absolute top-32 right-20 w-4 h-4 bg-white/20 rounded-full animate-float"></div>
      <div class="absolute top-48 left-32 w-3 h-3 bg-blue-400/30 rounded-full animate-float delay-200"></div>
      <div class="absolute bottom-40 right-40 w-5 h-5 bg-purple-400/20 rounded-full animate-float delay-400"></div>
    </div>

    <!-- Header / Navbar -->
    <header class="relative z-20">
      <nav class="max-w-7xl mx-auto px-6 py-6">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div 
            class="flex items-center gap-3 transition-all duration-700 ease-out"
            :class="isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'"
          >
            <div class="relative">
              <div class="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-lg shadow-white/20">
                <span class="text-primary-500 font-bold text-2xl">T</span>
              </div>
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-slate-900"></div>
            </div>
            <div>
              <span class="text-2xl font-bold text-white tracking-tight">TruEditor</span>
              <p class="text-xs text-white/50 -mt-1">Editorial Manager</p>
            </div>
          </div>

          <!-- Nav Links & CTA -->
          <div 
            class="flex items-center gap-6 transition-all duration-700 ease-out delay-100"
            :class="isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'"
          >
            <a href="#features" class="text-white/70 hover:text-white transition-colors hidden md:block">
              Özellikler
            </a>
            <a href="#about" class="text-white/70 hover:text-white transition-colors hidden md:block">
              Hakkında
            </a>
            <button
              @click="goToLogin"
              class="group flex items-center gap-2 px-5 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full text-white font-medium transition-all duration-300"
            >
              <svg class="w-5 h-5 text-[#a6ce39]" viewBox="0 0 256 256" fill="currentColor">
                <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0zm-14.837 191.167h-27.22V95.667h27.22v95.5zm-13.61-108.5c-8.721 0-15.79-7.308-15.79-16.326 0-9.017 7.069-16.326 15.79-16.326 8.721 0 15.79 7.309 15.79 16.326 0 9.018-7.069 16.326-15.79 16.326zm111.28 108.5h-27.219v-46.5c0-11.084-.199-25.334-15.438-25.334-15.459 0-17.834 12.084-17.834 24.542v47.292h-27.196V95.667h26.109v13.042h.366c3.635-6.892 12.518-14.167 25.76-14.167 27.554 0 32.652 18.125 32.652 41.708v54.917z"/>
              </svg>
              <span>ORCID ile Giriş</span>
            </button>
          </div>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <main class="relative z-10">
      <section class="max-w-7xl mx-auto px-6 pt-16 md:pt-24 pb-20">
        <div class="text-center max-w-4xl mx-auto">
          
          <!-- Badge -->
          <div
            class="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-sm text-white/90 mb-8 transition-all duration-700 ease-out delay-150"
            :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-5'"
          >
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            Akademik Yayıncılıkta Yeni Nesil
          </div>

          <!-- Headline -->
          <h1
            class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-white leading-tight mb-6 transition-all duration-700 ease-out delay-200"
            :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          >
            Makale Gönderimi
            <span class="block mt-2 text-gradient">Artık Çok Kolay</span>
          </h1>

          <!-- Subheadline -->
          <p
            class="text-lg md:text-xl text-white/70 max-w-2xl mx-auto mb-10 leading-relaxed transition-all duration-700 ease-out delay-300"
            :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          >
            ORCID entegrasyonlu, modern ve kullanıcı dostu akademik dergi yönetim sistemi. 
            <span class="text-white/90 font-medium">Karmaşık formlar</span> ve 
            <span class="text-white/90 font-medium">uzun bekleme süreleri</span> artık geçmişte kaldı.
          </p>

          <!-- CTA Buttons -->
          <div
            class="flex flex-col sm:flex-row justify-center gap-4 mb-16 transition-all duration-700 ease-out delay-400"
            :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          >
            <button
              @click="goToLogin"
              class="group relative inline-flex items-center justify-center gap-3 px-8 py-4 bg-[#a6ce39] hover:bg-[#95ba33] text-white font-bold text-lg rounded-xl shadow-lg shadow-[#a6ce39]/30 hover:shadow-xl hover:shadow-[#a6ce39]/40 transition-all duration-300 hover:-translate-y-1"
            >
              <svg class="w-6 h-6" viewBox="0 0 256 256" fill="currentColor">
                <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0zm-14.837 191.167h-27.22V95.667h27.22v95.5zm-13.61-108.5c-8.721 0-15.79-7.308-15.79-16.326 0-9.017 7.069-16.326 15.79-16.326 8.721 0 15.79 7.309 15.79 16.326 0 9.018-7.069 16.326-15.79 16.326zm111.28 108.5h-27.219v-46.5c0-11.084-.199-25.334-15.438-25.334-15.459 0-17.834 12.084-17.834 24.542v47.292h-27.196V95.667h26.109v13.042h.366c3.635-6.892 12.518-14.167 25.76-14.167 27.554 0 32.652 18.125 32.652 41.708v54.917z"/>
              </svg>
              ORCID ile Hemen Başla
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
              </svg>
            </button>
            
            <a
              href="#features"
              class="inline-flex items-center justify-center gap-2 px-8 py-4 border-2 border-white/30 hover:border-white/50 text-white font-semibold text-lg rounded-xl hover:bg-white/5 transition-all duration-300"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Özellikleri Keşfet
            </a>
          </div>

          <!-- Stats -->
          <div
            class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto transition-all duration-700 ease-out delay-500"
            :class="showStats ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
          >
            <div v-for="stat in stats" :key="stat.label" class="text-center">
              <div class="text-3xl md:text-4xl font-bold text-white mb-1">
                {{ stat.value }}<span class="text-emerald-400">{{ stat.suffix }}</span>
              </div>
              <div class="text-sm text-white/50">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section id="features" class="relative py-24 bg-gradient-to-b from-transparent to-slate-900/50">
        <div class="max-w-7xl mx-auto px-6">
          <div class="text-center mb-16">
            <h2
              class="text-3xl md:text-4xl font-bold text-white mb-4 transition-all duration-700 ease-out"
              :class="showFeatures ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
            >
              Neden TruEditor?
            </h2>
            <p
              class="text-white/60 max-w-2xl mx-auto transition-all duration-700 ease-out delay-100"
              :class="showFeatures ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
            >
              Geleneksel dergi yönetim sistemlerinin tüm sorunlarını çözdük. 
              Modern teknoloji ile akademik yayıncılığı yeniden tanımlıyoruz.
            </p>
          </div>

          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="(feature, index) in features"
              :key="feature.title"
              class="group relative p-6 bg-white/5 hover:bg-white/10 backdrop-blur-sm border border-white/10 hover:border-white/20 rounded-2xl transition-all duration-500 hover:-translate-y-1"
              :class="showFeatures ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
              :style="{ transitionDelay: `${150 + index * 100}ms` }"
            >
              <!-- Icon -->
              <div 
                class="w-14 h-14 rounded-xl bg-gradient-to-br flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform duration-300"
                :class="feature.color"
                v-html="feature.icon"
              ></div>
              
              <!-- Content -->
              <h3 class="text-xl font-semibold text-white mb-2">{{ feature.title }}</h3>
              <p class="text-white/60 leading-relaxed">{{ feature.description }}</p>
              
              <!-- Hover glow effect -->
              <div class="absolute inset-0 rounded-2xl bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-500" :class="feature.color"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section id="about" class="relative py-24">
        <div class="max-w-4xl mx-auto px-6 text-center">
          <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
            Akademik Yayıncılığı <span class="text-gradient">Dönüştürmeye</span> Hazır mısınız?
          </h2>
          <p class="text-white/60 mb-10 max-w-2xl mx-auto">
            TruEditor ile makale gönderimi artık dakikalar içinde tamamlanıyor. 
            Hemen ORCID hesabınızla giriş yapın ve farkı deneyimleyin.
          </p>
          <button
            @click="goToLogin"
            class="inline-flex items-center gap-3 px-10 py-5 bg-white text-primary-600 font-bold text-lg rounded-xl shadow-lg shadow-white/20 hover:shadow-xl hover:shadow-white/30 transition-all duration-300 hover:-translate-y-1"
          >
            <svg class="w-6 h-6 text-[#a6ce39]" viewBox="0 0 256 256" fill="currentColor">
              <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0zm-14.837 191.167h-27.22V95.667h27.22v95.5zm-13.61-108.5c-8.721 0-15.79-7.308-15.79-16.326 0-9.017 7.069-16.326 15.79-16.326 8.721 0 15.79 7.309 15.79 16.326 0 9.018-7.069 16.326-15.79 16.326zm111.28 108.5h-27.219v-46.5c0-11.084-.199-25.334-15.438-25.334-15.459 0-17.834 12.084-17.834 24.542v47.292h-27.196V95.667h26.109v13.042h.366c3.635-6.892 12.518-14.167 25.76-14.167 27.554 0 32.652 18.125 32.652 41.708v54.917z"/>
            </svg>
            Ücretsiz Başlayın
          </button>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-white/10 py-8">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-2 text-white/50">
            <div class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">T</span>
            </div>
            <span class="font-medium">TruEditor</span>
          </div>
          <p class="text-white/40 text-sm">
            © 2026 TruEditor. Tüm hakları saklıdır. Abdullah Doğan tarafından geliştirildi.
          </p>
          <div class="flex items-center gap-4 text-white/40 text-sm">
            <a href="#" class="hover:text-white transition-colors">Gizlilik</a>
            <a href="#" class="hover:text-white transition-colors">Kullanım Şartları</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
