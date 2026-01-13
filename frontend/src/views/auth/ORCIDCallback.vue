<script setup lang="ts">
/**
 * TruEditor - ORCID OAuth Callback Handler
 * =========================================
 * Handles the OAuth callback from ORCID authentication.
 */
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isProcessing = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  const code = route.query.code as string
  const errorParam = route.query.error as string

  if (errorParam) {
    error.value = 'ORCID authorization was cancelled'
    isProcessing.value = false
    return
  }

  if (!code) {
    error.value = 'Invalid authorization code'
    isProcessing.value = false
    return
  }

  try {
    await authStore.handleORCIDCallback(code)
    
    // Check if profile is complete
    if (!authStore.profileCompleted) {
      // New user or incomplete profile - go to onboarding
      router.replace('/complete-profile')
    } else {
      // Profile complete - go to intended page or dashboard
      const redirect = route.query.redirect as string || '/dashboard'
      router.replace(redirect)
    }
  } catch (err: any) {
    error.value = err.response?.data?.error?.message || 'Login failed'
    isProcessing.value = false
  }
})

function retryLogin() {
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-6">
    <div class="text-center">
      <!-- Processing state -->
      <template v-if="isProcessing">
        <div class="mb-8">
          <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        </div>
        <h2 class="text-xl font-semibold text-gray-800 mb-2">Signing in...</h2>
        <p class="text-gray-600">Verifying your ORCID account</p>
      </template>

      <!-- Error state -->
      <template v-else-if="error">
        <div class="mb-8">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto">
            <svg class="w-8 h-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        </div>
        <h2 class="text-xl font-semibold text-gray-800 mb-2">Login Failed</h2>
        <p class="text-gray-600 mb-6">{{ error }}</p>
        <button @click="retryLogin" class="btn-primary">
          Try Again
        </button>
      </template>
    </div>
  </div>
</template>
