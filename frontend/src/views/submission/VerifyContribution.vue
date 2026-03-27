<script setup lang="ts">
/**
 * TruEditor - Co-Author Verification Page
 * =========================================
 * Public page where co-authors verify or decline their authorship
 * via the token link sent in the notification email.
 */
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{
  token: string
  isDecline?: boolean
}>()

const isLoading = ref(true)
const isSuccess = ref(false)
const isError = ref(false)
const errorMessage = ref('')
const authorName = ref('')
const manuscriptTitle = ref('')
const manuscriptId = ref('')
const alreadyDone = ref(false)

const apiBase = import.meta.env.VITE_API_URL || '/api/v1'

onMounted(async () => {
  try {
    const endpoint = props.isDecline
      ? `${apiBase}/submissions/verify/${props.token}/decline/`
      : `${apiBase}/submissions/verify/${props.token}/`

    const response = await axios.post(endpoint)
    const data = response.data?.data || response.data

    authorName.value = data.author_name || ''
    manuscriptTitle.value = data.manuscript_title || ''
    manuscriptId.value = data.manuscript_id || ''
    alreadyDone.value = data.already_verified || data.already_declined || false
    isSuccess.value = true
  } catch (err: any) {
    isError.value = true
    errorMessage.value =
      err.response?.data?.error?.message ||
      err.response?.data?.message ||
      'This verification link is invalid or has expired.'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2 mb-4">
          <img src="/logo-icon.svg" alt="TruEditor" class="brand-logo brand-logo--login brand-logo--on-light" />
          <span class="text-2xl font-bold text-gray-900 tracking-tight">Tru<span class="text-primary-400">Editor</span></span>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full border-4 border-gray-200 border-t-primary-500 animate-spin"></div>
        <p class="text-gray-600 font-medium">{{ isDecline ? 'Processing your response...' : 'Verifying your contribution...' }}</p>
      </div>

      <!-- Success: Verified -->
      <div v-else-if="isSuccess && !isDecline" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-green-500 to-emerald-500 px-6 py-8 text-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-white">
            {{ alreadyDone ? 'Already Verified' : 'Contribution Verified!' }}
          </h2>
        </div>
        <div class="p-6 space-y-4">
          <p class="text-gray-700 text-center">
            {{ alreadyDone
              ? 'Your contribution has been previously verified.'
              : 'Thank you for confirming your authorship.'
            }}
          </p>
          <div v-if="manuscriptId || manuscriptTitle" class="bg-gray-50 rounded-xl p-4 space-y-2 text-sm">
            <div v-if="manuscriptId" class="flex justify-between">
              <span class="text-gray-500">Manuscript ID</span>
              <span class="font-mono font-semibold text-primary-600">{{ manuscriptId }}</span>
            </div>
            <div v-if="manuscriptTitle" class="flex justify-between gap-4">
              <span class="text-gray-500 flex-shrink-0">Title</span>
              <span class="text-gray-800 font-medium text-right">{{ manuscriptTitle }}</span>
            </div>
            <div v-if="authorName" class="flex justify-between">
              <span class="text-gray-500">Author</span>
              <span class="text-gray-800 font-medium">{{ authorName }}</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 text-center">You can close this page now.</p>
        </div>
      </div>

      <!-- Success: Declined -->
      <div v-else-if="isSuccess && isDecline" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="bg-gradient-to-r from-orange-500 to-red-500 px-6 py-8 text-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-white">
            {{ alreadyDone ? 'Already Declined' : 'Authorship Declined' }}
          </h2>
        </div>
        <div class="p-6 space-y-4">
          <p class="text-gray-700 text-center">
            {{ alreadyDone
              ? 'You have previously declined authorship on this manuscript.'
              : 'You have declined authorship. The submitting author has been notified.'
            }}
          </p>
          <div v-if="manuscriptTitle" class="bg-gray-50 rounded-xl p-4 text-sm">
            <div class="flex justify-between gap-4">
              <span class="text-gray-500 flex-shrink-0">Title</span>
              <span class="text-gray-800 font-medium text-right">{{ manuscriptTitle }}</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 text-center">You can close this page now.</p>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="isError" class="bg-white rounded-2xl shadow-sm border border-red-100 overflow-hidden">
        <div class="bg-gradient-to-r from-red-500 to-red-600 px-6 py-8 text-center">
          <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 class="text-xl font-bold text-white">Verification Failed</h2>
        </div>
        <div class="p-6 text-center">
          <p class="text-gray-700 mb-4">{{ errorMessage }}</p>
          <p class="text-xs text-gray-500">If you believe this is an error, please contact the submitting author.</p>
        </div>
      </div>
    </div>
  </div>
</template>
