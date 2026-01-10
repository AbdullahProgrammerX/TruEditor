<script setup lang="ts">
/**
 * TruEditor - User Profile Page
 * ==============================
 */
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
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
          <h1 class="text-lg font-semibold text-gray-800">Profil</h1>
          <div class="w-20"></div>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 py-8">
      <div class="card">
        <div class="flex items-center gap-6 mb-8">
          <!-- Avatar -->
          <div class="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
            {{ authStore.fullName?.charAt(0) || 'U' }}
          </div>
          
          <div>
            <h2 class="text-2xl font-bold text-gray-800">{{ authStore.fullName }}</h2>
            <a 
              :href="authStore.orcidUrl"
              target="_blank"
              class="text-orcid hover:underline"
            >
              {{ authStore.orcidId }}
            </a>
          </div>
        </div>

        <div class="space-y-4">
          <div>
            <label class="label">Email</label>
            <p class="text-gray-800">{{ authStore.user?.email || 'Belirtilmemiş' }}</p>
          </div>
          
          <div>
            <label class="label">Kurum</label>
            <p class="text-gray-800">{{ authStore.user?.institution || 'Belirtilmemiş' }}</p>
          </div>
          
          <div>
            <label class="label">Departman</label>
            <p class="text-gray-800">{{ authStore.user?.department || 'Belirtilmemiş' }}</p>
          </div>
        </div>

        <div class="mt-8 pt-8 border-t">
          <button class="btn-outline">
            ORCID Profilini Senkronize Et
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
