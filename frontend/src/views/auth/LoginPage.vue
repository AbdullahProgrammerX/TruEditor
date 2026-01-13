<script setup lang="ts">
/**
 * TruEditor - Login Page
 * ======================
 * ORCID authentication login page with modern design.
 * 
 * Developer: Abdullah Dogan
 */
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

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
    window.location.href = authUrl
  } catch (err: any) {
    error.value = err.response?.data?.error?.message || 'Could not connect to ORCID'
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-hero overflow-hidden flex items-center justify-center p-4 sm:p-6">
    <!-- Animated Background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjAyIi8+PC9nPjwvc3ZnPg==')] opacity-40"></div>
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-1/2 left-10 w-64 h-64 bg-emerald-500/15 rounded-full blur-3xl animate-pulse-slow"></div>
    </div>

    <!-- Login Card -->
    <div 
      class="relative w-full max-w-md transform transition-all duration-700"
      :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'"
    >
      <div class="bg-white/95 backdrop-blur-sm rounded-2xl sm:rounded-3xl shadow-2xl p-6 sm:p-8">
        <!-- Logo -->
        <div class="text-center mb-6 sm:mb-8">
          <RouterLink to="/" class="inline-flex items-center gap-2 sm:gap-3 group">
            <div class="relative">
              <div class="w-11 h-11 sm:w-14 sm:h-14 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl sm:rounded-2xl flex items-center justify-center shadow-lg shadow-primary-500/30 group-hover:scale-105 transition-transform">
                <span class="text-white font-bold text-xl sm:text-2xl">T</span>
              </div>
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-white"></div>
            </div>
            <div class="text-left">
              <span class="text-xl sm:text-2xl font-bold text-gray-800 tracking-tight">TruEditor</span>
              <p class="text-xs text-gray-500 -mt-0.5">Academic Publishing</p>
            </div>
          </RouterLink>
        </div>

        <!-- Title -->
        <div class="text-center mb-6 sm:mb-8">
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
          <p class="text-gray-500 text-sm sm:text-base">Sign in with your ORCID account to continue</p>
        </div>

        <!-- Error message -->
        <div 
          v-if="error"
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-3 animate-fade-in"
        >
          <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {{ error }}
        </div>

        <!-- ORCID Login Button -->
        <button
          @click="loginWithORCID"
          :disabled="isLoading"
          class="w-full py-4 sm:py-5 bg-[#a6ce39] hover:bg-[#95ba33] text-white font-bold text-base sm:text-lg rounded-xl shadow-lg shadow-[#a6ce39]/30 hover:shadow-xl hover:shadow-[#a6ce39]/40 transition-all duration-300 flex items-center justify-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed"
          :class="!isLoading && 'hover:scale-[1.02]'"
        >
          <template v-if="isLoading">
            <svg class="w-5 h-5 sm:w-6 sm:h-6 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Connecting...</span>
          </template>
          <template v-else>
            <svg class="w-6 h-6 sm:w-7 sm:h-7" viewBox="0 0 256 256" fill="currentColor">
              <circle cx="128" cy="128" r="128" fill="currentColor"/>
              <g fill="white">
                <path d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 63.1c-5.8 0-10.5 4.7-10.5 10.5s4.7 10.5 10.5 10.5 10.5-4.7 10.5-10.5-4.7-10.5-10.5-10.5z"/>
                <path d="M108.9 79.1h41.6c39.6 0 57 28.3 57 53.6 0 27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7C191.7 111.2 178 93 149.2 93h-24.9v79.4z"/>
              </g>
            </svg>
            <span>Sign in with ORCID</span>
          </template>
        </button>

        <!-- Info -->
        <div class="mt-6 sm:mt-8 text-center">
          <p class="text-sm text-gray-500 mb-3">
            Don't have an ORCID account?
          </p>
          <a 
            href="https://orcid.org/register"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-semibold group"
          >
            Create a free ORCID account
            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>

        <!-- Divider -->
        <div class="mt-6 sm:mt-8 pt-6 sm:pt-8 border-t border-gray-100">
          <p class="text-xs text-gray-400 text-center">
            By signing in, you agree to our 
            <a href="#" class="text-primary-600 hover:underline">Terms of Service</a>
            and 
            <a href="#" class="text-primary-600 hover:underline">Privacy Policy</a>.
          </p>
        </div>
      </div>

      <!-- Back to home -->
      <div class="mt-6 text-center">
        <RouterLink 
          to="/" 
          class="inline-flex items-center gap-2 text-sm text-white/70 hover:text-white transition-colors group"
        >
          <svg class="w-4 h-4 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to home
        </RouterLink>
      </div>
    </div>
  </div>
</template>
