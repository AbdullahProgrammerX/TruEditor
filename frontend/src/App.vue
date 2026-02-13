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
    <!-- Router View with transitions -->
    <RouterView v-slot="{ Component, route }">
      <Transition
        name="page"
        mode="out-in"
      >
        <component :is="Component" :key="route.path" />
      </Transition>
    </RouterView>
    
    <!-- Global Toast Notifications -->
    <ToastContainer />
  </div>
</template>

<style>
/* Page transition animations (opacity only - no transform to avoid sticky header flicker) */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}
</style>
