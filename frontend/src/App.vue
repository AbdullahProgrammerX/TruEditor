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
  }, 1100)
})
</script>

<template>
  <Transition name="splash">
    <div v-if="!isAppReady" class="splash-screen">
      <div class="splash-content">
        <!-- Same asset as headers: no inner SVG animation (avoids perceived misalignment) -->
        <div class="splash-logo">
          <img src="/logo-icon.svg" width="80" height="80" alt="" class="splash-logo-img" />
        </div>
        <h1 class="splash-title">
          <span class="splash-tru">Tru</span><span class="splash-editor">Editor</span>
        </h1>
        <p class="splash-tagline">Manuscript submission system</p>
        <div class="splash-loader" aria-hidden="true">
          <div class="splash-loader-bar"></div>
        </div>
      </div>
    </div>
  </Transition>

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
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  max-width: 20rem;
  padding: 0 1.5rem;
}

.splash-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  margin: 0 auto 1.25rem;
  flex-shrink: 0;
  animation: splashReveal 0.45s ease-out both;
}

.splash-logo-img {
  display: block;
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.splash-title {
  /* Serif wordmark: aligns with scholarly / publisher-facing products (Elsevier, Wiley-style gravitas) */
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin: 0 0 0.35rem;
  animation: splashFade 0.4s 0.12s ease-out both;
}

.splash-tru {
  color: #ffffff;
}

.splash-editor {
  color: rgba(255, 255, 255, 0.65);
}

.splash-tagline {
  margin: 0 0 1.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.45);
  animation: splashFade 0.4s 0.2s ease-out both;
}

.splash-loader {
  width: 120px;
  height: 3px;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 4px;
  overflow: hidden;
  animation: splashFade 0.35s 0.28s ease-out both;
}

.splash-loader-bar {
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, #34d399, #10b981);
  border-radius: 4px;
  animation: loaderFill 0.75s 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.splash-leave-active {
  transition: opacity 0.35s ease;
}
.splash-leave-to {
  opacity: 0;
}

@keyframes splashReveal {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes splashFade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes loaderFill {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}
</style>
