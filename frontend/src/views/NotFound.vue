<script setup lang="ts">
/**
 * TruEditor - 404 Not Found Page
 */
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-6">
    <div class="text-center animate-fade-in">
      <h1 class="text-9xl font-bold text-primary-500 mb-4">404</h1>
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">Sayfa Bulunamadı</h2>
      <p class="text-gray-600 mb-8">
        Aradığınız sayfa mevcut değil veya taşınmış olabilir.
      </p>
      <button @click="goHome" class="btn-primary">
        Ana Sayfaya Dön
      </button>
    </div>
  </div>
</template>
