<script setup lang="ts">
/**
 * TruEditor - Root App Component
 * ===============================
 */
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ToastContainer from '@/components/common/ToastContainer.vue'

const authStore = useAuthStore()

// Initialize auth on app mount
onMounted(() => {
  authStore.initAuth()
})
</script>

<template>
  <div id="app" class="min-h-screen">
    <RouterView />
    <ToastContainer />
  </div>
</template>
