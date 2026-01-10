<script setup lang="ts">
/**
 * TruEditor - Submission Detail Page
 * ====================================
 * (Placeholder - Faz 5'te detaylandırılacak)
 */
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const submissionId = route.params.id
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="router.push('/dashboard')" class="btn-ghost">
            ← Dashboard
          </button>
          <h1 class="text-lg font-semibold text-gray-800">Gönderim Detayı</h1>
          <div class="w-20"></div>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 py-8">
      <div class="card text-center py-12">
        <div class="text-5xl mb-4">📄</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Gönderim #{{ submissionId }}</h2>
        <p class="text-gray-600">Bu sayfa Faz 5'te geliştirilecek.</p>
      </div>
    </main>
  </div>
</template>
