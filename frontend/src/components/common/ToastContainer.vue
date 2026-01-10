<script setup lang="ts">
/**
 * TruEditor - Toast Notifications Container
 * ==========================================
 */
import { ref, onMounted, onUnmounted } from 'vue'

interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration: number
}

const toasts = ref<Toast[]>([])
let toastId = 0

// Toast event handler
function handleToast(event: CustomEvent<Omit<Toast, 'id'>>) {
  const toast: Toast = {
    id: ++toastId,
    ...event.detail,
    duration: event.detail.duration || 5000,
  }
  
  toasts.value.push(toast)
  
  // Auto remove
  setTimeout(() => {
    removeToast(toast.id)
  }, toast.duration)
}

function removeToast(id: number) {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

// Icon and color based on type
function getToastStyles(type: Toast['type']) {
  const styles = {
    success: {
      bg: 'bg-green-50',
      border: 'border-green-500',
      icon: '✓',
      iconBg: 'bg-green-500',
    },
    error: {
      bg: 'bg-red-50',
      border: 'border-red-500',
      icon: '✕',
      iconBg: 'bg-red-500',
    },
    warning: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-500',
      icon: '!',
      iconBg: 'bg-yellow-500',
    },
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-500',
      icon: 'i',
      iconBg: 'bg-blue-500',
    },
  }
  return styles[type]
}

onMounted(() => {
  window.addEventListener('toast', handleToast as EventListener)
})

onUnmounted(() => {
  window.removeEventListener('toast', handleToast as EventListener)
})

// Global toast function
;(window as any).toast = (type: Toast['type'], message: string, duration = 5000) => {
  window.dispatchEvent(new CustomEvent('toast', {
    detail: { type, message, duration }
  }))
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 flex flex-col gap-3 max-w-sm">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'flex items-start gap-3 p-4 rounded-lg shadow-lg border-l-4 animate-slide-in-right',
            getToastStyles(toast.type).bg,
            getToastStyles(toast.type).border,
          ]"
        >
          <!-- Icon -->
          <div
            :class="[
              'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-white text-sm font-bold',
              getToastStyles(toast.type).iconBg,
            ]"
          >
            {{ getToastStyles(toast.type).icon }}
          </div>
          
          <!-- Message -->
          <p class="flex-1 text-sm text-gray-800">
            {{ toast.message }}
          </p>
          
          <!-- Close button -->
          <button
            @click="removeToast(toast.id)"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
          >
            ✕
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
