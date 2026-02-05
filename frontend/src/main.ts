/**
 * TruEditor - Vue.js Application Entry Point
 * ==========================================
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { MotionPlugin } from '@vueuse/motion'

import App from './App.vue'
import router from './router'
import { setOnUnauthorized } from './services/api'
import { useAuthStore } from './stores/auth'

// Global styles
import './style.css'

// Create Vue app
const app = createApp(App)

// Pinia - State Management
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Router
app.use(router)

// 401 handler: clear auth and navigate to login without full reload (avoids login/dashboard loop)
const authStore = useAuthStore()
setOnUnauthorized(() => {
  authStore.clearAuth()
  router.push('/login')
})

// Motion Plugin - Animations
app.use(MotionPlugin)

// Mount app
app.mount('#app')

// Log environment
console.log(`🚀 TruEditor Frontend v1.0.0`)
console.log(`📡 API: ${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'}`)
