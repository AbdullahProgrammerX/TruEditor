<script setup lang="ts">
/**
 * TruEditor - Root App Component
 * ===============================
 */
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ToastContainer from '@/components/common/ToastContainer.vue'

const authStore = useAuthStore()
const isAppReady = ref(false)

onMounted(() => {
  authStore.initAuth()
  setTimeout(() => {
    isAppReady.value = true
  }, 1200)
})
</script>

<template>
  <!-- Splash Screen -->
  <Transition name="splash">
    <div v-if="!isAppReady" class="splash-screen">
      <div class="splash-content">
        <!-- Animated Logo -->
        <div class="splash-logo">
          <svg width="80" height="80" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" class="splash-icon">
            <defs>
              <linearGradient id="splash-bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#1e3a5f"/>
                <stop offset="100%" stop-color="#1a56db"/>
              </linearGradient>
              <linearGradient id="splash-accent" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#34d399"/>
                <stop offset="100%" stop-color="#10b981"/>
              </linearGradient>
            </defs>
            <rect width="512" height="512" rx="96" fill="url(#splash-bg)"/>
            <rect class="splash-bar-h" x="120" y="128" width="272" height="36" rx="6" fill="white" opacity="0.95"/>
            <rect class="splash-bar-v" x="196" y="128" width="36" height="260" rx="6" fill="white" opacity="0.95"/>
            <rect class="splash-bar-accent" x="196" y="352" width="196" height="36" rx="6" fill="url(#splash-accent)" opacity="0.9"/>
            <circle class="splash-dot" cx="404" cy="148" r="24" fill="#34d399"/>
          </svg>
        </div>
        <h1 class="splash-title">
          <span class="splash-tru">Tru</span><span class="splash-editor">Editor</span>
        </h1>
        <div class="splash-loader">
          <div class="splash-loader-bar"></div>
        </div>
      </div>
    </div>
  </Transition>

  <!-- App Content -->
  <div id="app" class="min-h-screen">
    <RouterView />
    <ToastContainer />
  </div>
</template>

<style scoped>
.splash-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1e40af 100%);
}

.splash-content {
  text-align: center;
}

.splash-logo {
  margin-bottom: 24px;
  animation: splashLogoIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.splash-icon {
  filter: drop-shadow(0 8px 24px rgba(30, 58, 95, 0.5));
}

.splash-bar-h {
  animation: slideRight 0.5s 0.2s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.splash-bar-v {
  animation: slideDown 0.5s 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.splash-bar-accent {
  animation: slideRight 0.4s 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.splash-dot {
  animation: popIn 0.3s 0.65s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.splash-title {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0 0 20px;
  animation: fadeInUp 0.5s 0.4s ease-out both;
}

.splash-tru {
  color: #ffffff;
}

.splash-editor {
  color: rgba(255, 255, 255, 0.6);
}

.splash-loader {
  width: 120px;
  height: 3px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  margin: 0 auto;
  overflow: hidden;
  animation: fadeIn 0.3s 0.6s ease-out both;
}

.splash-loader-bar {
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, #34d399, #10b981);
  border-radius: 4px;
  animation: loaderFill 0.8s 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Splash exit */
.splash-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.splash-leave-to {
  opacity: 0;
  transform: scale(1.05);
}

@keyframes splashLogoIn {
  from { opacity: 0; transform: scale(0.8) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes slideRight {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 0.95; transform: translateX(0); }
}
@keyframes slideDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 0.95; transform: translateY(0); }
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes loaderFill {
  from { width: 0; }
  to { width: 100%; }
}
</style>
