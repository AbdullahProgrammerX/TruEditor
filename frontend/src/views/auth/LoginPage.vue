<script setup lang="ts">
/**
 * TruEditor - Login Page
 * ======================
 * ORCID ile giriş sayfası.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(false)
const error = ref<string | null>(null)
const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})

async function loginWithORCID() {
  isLoading.value = true
  error.value = null

  try {
    const authUrl = await authStore.getORCIDLoginUrl()
    // Redirect to ORCID OAuth page
    window.location.href = authUrl
  } catch (err: any) {
    error.value = err.response?.data?.error?.message || 'ORCID bağlantısı kurulamadı'
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-6">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary-500/5 rounded-full blur-3xl"></div>
    </div>

    <!-- Login Card -->
    <div 
      class="relative w-full max-w-md transform transition-all duration-700"
      :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
    >
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <RouterLink to="/" class="inline-flex items-center gap-3 group">
            <div class="w-12 h-12 bg-primary-500 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <span class="text-white font-bold text-2xl">T</span>
            </div>
            <span class="text-2xl font-bold text-gray-800">TruEditor</span>
          </RouterLink>
        </div>

        <!-- Title -->
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-800 mb-2">Hoş Geldiniz</h1>
          <p class="text-gray-600">ORCID hesabınızla giriş yapın</p>
        </div>

        <!-- Error message -->
        <div 
          v-if="error"
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm animate-fade-in"
        >
          {{ error }}
        </div>

        <!-- ORCID Login Button -->
        <button
          @click="loginWithORCID"
          :disabled="isLoading"
          class="w-full btn-orcid text-lg py-4 flex items-center justify-center gap-3 hover:scale-[1.02] transition-transform"
        >
          <template v-if="isLoading">
            <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Bağlanıyor...</span>
          </template>
          <template v-else>
            <!-- ORCID Icon -->
            <svg class="w-6 h-6" viewBox="0 0 256 256" fill="currentColor">
              <circle cx="128" cy="128" r="128" fill="currentColor"/>
              <g fill="white">
                <path d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 63.1c-5.8 0-10.5 4.7-10.5 10.5s4.7 10.5 10.5 10.5 10.5-4.7 10.5-10.5-4.7-10.5-10.5-10.5z"/>
                <path d="M108.9 79.1h41.6c39.6 0 57 28.3 57 53.6 0 27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7C191.7 111.2 178 93 googletag.cmd.push(function() {
                  149.2 93h-24.9v79.4z"/>
              </g>
            </svg>
            <span>ORCID ile Giriş Yap</span>
          </template>
        </button>

        <!-- Info -->
        <div class="mt-8 text-center">
          <p class="text-sm text-gray-500 mb-4">
            ORCID hesabınız yok mu?
          </p>
          <a 
            href="https://orcid.org/register"
            target="_blank"
            rel="noopener noreferrer"
            class="text-sm text-secondary-600 hover:text-secondary-700 font-medium"
          >
            Ücretsiz ORCID hesabı oluşturun →
          </a>
        </div>

        <!-- Divider -->
        <div class="mt-8 pt-8 border-t border-gray-100">
          <p class="text-xs text-gray-400 text-center">
            Giriş yaparak 
            <a href="#" class="text-secondary-600 hover:underline">Kullanım Koşulları</a>
            ve 
            <a href="#" class="text-secondary-600 hover:underline">Gizlilik Politikası</a>'nı 
            kabul etmiş olursunuz.
          </p>
        </div>
      </div>

      <!-- Back to home -->
      <div class="mt-6 text-center">
        <RouterLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
          ← Ana sayfaya dön
        </RouterLink>
      </div>
    </div>
  </div>
</template>
