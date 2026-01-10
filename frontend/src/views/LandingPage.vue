<script setup lang="ts">
/**
 * TruEditor - Landing Page
 * ========================
 * Modern ve animasyonlu landing page.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Animation states
const isVisible = ref(false)

onMounted(() => {
  // Trigger entrance animations
  setTimeout(() => {
    isVisible.value = true
  }, 100)
  
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
    icon: '🔐',
    title: 'ORCID Entegrasyonu',
    description: 'Tek tıkla güvenli giriş. Email/şifre hatırlama derdi yok.',
  },
  {
    icon: '📝',
    title: 'Akıllı Gönderim Sihirbazı',
    description: 'Adım adım rehberlik ile kolay makale gönderimi.',
  },
  {
    icon: '📁',
    title: 'Sürükle-Bırak Dosya Yönetimi',
    description: 'Dosyalarınızı kolayca yükleyin ve sıralayın.',
  },
  {
    icon: '⚡',
    title: 'Otomatik Kayıt',
    description: 'Verileriniz anlık olarak kaydedilir, veri kaybı yok.',
  },
  {
    icon: '📄',
    title: 'Hızlı PDF Oluşturma',
    description: 'Arka planda PDF oluşturma, beklemeden devam edin.',
  },
  {
    icon: '📊',
    title: 'Gerçek Zamanlı Takip',
    description: 'Gönderimlerinizin durumunu anlık takip edin.',
  },
]
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-600 overflow-hidden">
    <!-- Animated background elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-white/5 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-1/2 -left-20 w-60 h-60 bg-secondary-500/20 rounded-full blur-3xl animate-pulse-slow animation-delay-500"></div>
      <div class="absolute bottom-20 right-1/4 w-40 h-40 bg-accent-500/20 rounded-full blur-2xl animate-pulse-slow animation-delay-300"></div>
    </div>

    <!-- Header -->
    <header class="relative z-10">
      <nav class="max-w-7xl mx-auto px-6 py-6">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div 
            class="flex items-center gap-3 transform transition-all duration-700"
            :class="isVisible ? 'translate-x-0 opacity-100' : '-translate-x-10 opacity-0'"
          >
            <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-lg">
              <span class="text-primary-500 font-bold text-xl">T</span>
            </div>
            <span class="text-2xl font-bold text-white">TruEditor</span>
          </div>

          <!-- CTA Button -->
          <button
            @click="goToLogin"
            class="btn bg-white text-primary-600 hover:bg-gray-100 transform transition-all duration-700"
            :class="isVisible ? 'translate-x-0 opacity-100' : 'translate-x-10 opacity-0'"
          >
            <span class="mr-2">ORCID ile Giriş</span>
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0z"/>
            </svg>
          </button>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <main class="relative z-10 max-w-7xl mx-auto px-6 pt-16 pb-24">
      <div class="text-center">
        <!-- Badge -->
        <div
          class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm text-white/90 px-4 py-2 rounded-full text-sm mb-8 transform transition-all duration-700 delay-100"
          :class="isVisible ? 'translate-y-0 opacity-100' : '-translate-y-5 opacity-0'"
        >
          <span class="w-2 h-2 bg-accent-400 rounded-full animate-pulse"></span>
          Akademik Yayıncılıkta Yeni Nesil
        </div>

        <!-- Headline -->
        <h1
          class="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight transform transition-all duration-700 delay-200"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          Makale Gönderimi<br />
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-accent-400 to-accent-300">
            Artık Daha Kolay
          </span>
        </h1>

        <!-- Subheadline -->
        <p
          class="text-xl text-white/80 max-w-2xl mx-auto mb-12 transform transition-all duration-700 delay-300"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          ORCID entegrasyonlu, modern ve kullanıcı dostu akademik dergi yönetim sistemi. 
          Karmaşık formlar, uzun bekleme süreleri artık geçmişte kaldı.
        </p>

        <!-- CTA Buttons -->
        <div
          class="flex flex-wrap justify-center gap-4 transform transition-all duration-700 delay-400"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          <button
            @click="goToLogin"
            class="btn-orcid text-lg px-8 py-4 shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
          >
            <svg class="w-6 h-6 mr-3" viewBox="0 0 256 256" fill="currentColor">
              <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0z"/>
            </svg>
            ORCID ile Başla
          </button>
          
          <a
            href="#features"
            class="btn-outline text-lg px-8 py-4 border-white/30 text-white hover:bg-white/10"
          >
            Özellikler
          </a>
        </div>
      </div>

      <!-- Features Section -->
      <section id="features" class="mt-32">
        <h2
          class="text-3xl font-bold text-white text-center mb-16 transform transition-all duration-700 delay-500"
          :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
        >
          Neden TruEditor?
        </h2>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(feature, index) in features"
            :key="feature.title"
            class="group bg-white/10 backdrop-blur-sm rounded-2xl p-6 hover:bg-white/20 transition-all duration-300 hover:scale-105 transform"
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
            :style="{ transitionDelay: `${600 + index * 100}ms` }"
          >
            <div class="text-4xl mb-4">{{ feature.icon }}</div>
            <h3 class="text-xl font-semibold text-white mb-2">{{ feature.title }}</h3>
            <p class="text-white/70">{{ feature.description }}</p>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-white/10 py-8">
      <div class="max-w-7xl mx-auto px-6 text-center text-white/50 text-sm">
        <p>© 2026 TruEditor. Tüm hakları saklıdır.</p>
      </div>
    </footer>
  </div>
</template>
