<script setup lang="ts">
/**
 * TruEditor - Author Dashboard
 * ============================
 * Modern dashboard displaying author's submissions and their statuses.
 * 
 * Developer: Abdullah Dogan
 */
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isVisible = ref(false)
const isMobileMenuOpen = ref(false)

// Mock data - will be replaced with API calls
const stats = ref({
  draft: 2,
  submitted: 1,
  underReview: 3,
  accepted: 5,
})

const recentSubmissions = ref([
  {
    id: 1,
    title: 'AI-Assisted Academic Text Analysis',
    status: 'draft',
    statusText: 'Draft',
    updatedAt: '2026-01-10',
    type: 'Research Article',
  },
  {
    id: 2,
    title: 'Natural Language Processing with Machine Learning',
    status: 'submitted',
    statusText: 'Submitted',
    updatedAt: '2026-01-08',
    type: 'Review',
  },
  {
    id: 3,
    title: 'Deep Learning Approaches: A Comprehensive Survey',
    status: 'under_review',
    statusText: 'Under Review',
    updatedAt: '2026-01-05',
    type: 'Research Article',
  },
])

const totalSubmissions = computed(() => 
  stats.value.draft + stats.value.submitted + stats.value.underReview + stats.value.accepted
)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})

function startNewSubmission() {
  router.push('/submissions/new')
}

function viewSubmission(id: number) {
  router.push(`/submissions/${id}`)
}

function logout() {
  authStore.logout()
  router.push('/')
}

// Status badge styles
type StatusStyle = { bg: string; text: string; dot: string }

function getStatusStyles(status: string): StatusStyle {
  const defaultStyle: StatusStyle = { bg: 'bg-gray-100', text: 'text-gray-700', dot: 'bg-gray-400' }
  const styles: Record<string, StatusStyle> = {
    draft: defaultStyle,
    submitted: { bg: 'bg-blue-50', text: 'text-blue-700', dot: 'bg-blue-500' },
    under_review: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-500' },
    accepted: { bg: 'bg-emerald-50', text: 'text-emerald-700', dot: 'bg-emerald-500' },
    rejected: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-500' },
  }
  return styles[status] || defaultStyle
}

// Greeting based on time
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-gradient-to-r from-primary-600 via-primary-500 to-primary-600 shadow-lg sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16 sm:h-20">
          <!-- Logo -->
          <RouterLink to="/dashboard" class="flex items-center gap-2 sm:gap-3 group">
            <div class="relative">
              <div class="w-9 h-9 sm:w-11 sm:h-11 bg-white rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
                <span class="text-primary-500 font-bold text-lg sm:text-xl">T</span>
              </div>
              <div class="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-primary-500"></div>
            </div>
            <div class="hidden sm:block">
              <span class="text-xl font-bold text-white tracking-tight">TruEditor</span>
              <p class="text-xs text-white/60 -mt-0.5">Dashboard</p>
            </div>
          </RouterLink>

          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center gap-1">
            <RouterLink 
              to="/dashboard" 
              class="px-4 py-2 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition-all font-medium"
            >
              Dashboard
            </RouterLink>
            <RouterLink 
              to="/submissions" 
              class="px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
            >
              Submissions
            </RouterLink>
            <RouterLink 
              to="/profile" 
              class="px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
            >
              Profile
            </RouterLink>
          </nav>

          <!-- User menu -->
          <div class="flex items-center gap-2 sm:gap-4">
            <div class="hidden sm:block text-right">
              <p class="text-sm font-semibold text-white">{{ authStore.fullName }}</p>
              <a 
                :href="authStore.orcidUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs text-orcid hover:text-orcid-light transition-colors flex items-center justify-end gap-1"
              >
                <svg class="w-3 h-3" viewBox="0 0 256 256" fill="currentColor">
                  <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0z"/>
                </svg>
                {{ authStore.orcidId }}
              </a>
            </div>
            
            <button 
              @click="logout"
              class="hidden sm:flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white text-sm font-medium transition-all"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>

            <!-- Mobile menu button -->
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="md:hidden p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all"
            >
              <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <div 
          v-show="isMobileMenuOpen"
          class="md:hidden pb-4 border-t border-white/10 mt-2 pt-4"
        >
          <nav class="flex flex-col gap-1">
            <RouterLink 
              to="/dashboard" 
              class="px-4 py-2.5 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition-all font-medium"
              @click="isMobileMenuOpen = false"
            >
              Dashboard
            </RouterLink>
            <RouterLink 
              to="/submissions" 
              class="px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
              @click="isMobileMenuOpen = false"
            >
              Submissions
            </RouterLink>
            <RouterLink 
              to="/profile" 
              class="px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
              @click="isMobileMenuOpen = false"
            >
              Profile
            </RouterLink>
            <button 
              @click="logout"
              class="flex items-center gap-2 px-4 py-2.5 text-red-300 hover:text-red-200 hover:bg-white/10 rounded-lg transition-all text-left"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <!-- Welcome Section -->
      <div 
        class="mb-6 sm:mb-8 transition-all duration-700"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-1">
          {{ greeting }}, {{ authStore.fullName?.split(' ')[0] || 'Author' }}! 👋
        </h1>
        <p class="text-gray-500 text-sm sm:text-base">
          Here's what's happening with your submissions.
        </p>
      </div>

      <!-- Stats Cards -->
      <div 
        class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8 transition-all duration-700 delay-100"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <div class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group">
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-gray-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </div>
            <span class="text-xs font-medium text-gray-400 bg-gray-50 px-2 py-1 rounded-full">Draft</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-gray-800">{{ stats.draft }}</div>
          <div class="text-xs sm:text-sm text-gray-500">Manuscripts</div>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group">
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-blue-50 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </div>
            <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">Submitted</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-blue-600">{{ stats.submitted }}</div>
          <div class="text-xs sm:text-sm text-gray-500">Awaiting Review</div>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group">
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-amber-50 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <span class="text-xs font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-full">In Review</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-amber-600">{{ stats.underReview }}</div>
          <div class="text-xs sm:text-sm text-gray-500">Being Reviewed</div>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group">
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-emerald-50 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">Accepted</span>
          </div>
          <div class="text-2xl sm:text-3xl font-bold text-emerald-600">{{ stats.accepted }}</div>
          <div class="text-xs sm:text-sm text-gray-500">Published</div>
        </div>
      </div>

      <!-- Quick Actions & New Submission -->
      <div 
        class="grid lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8 transition-all duration-700 delay-200"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <!-- New Submission CTA -->
        <div class="lg:col-span-2 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-5 sm:p-8 text-white relative overflow-hidden">
          <!-- Background decoration -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-32 translate-x-32"></div>
          <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-24 -translate-x-24"></div>
          
          <div class="relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div>
                <h2 class="text-xl sm:text-2xl font-bold mb-2">Ready to Submit?</h2>
                <p class="text-white/80 text-sm sm:text-base max-w-md">
                  Start a new manuscript submission with our guided wizard. It only takes a few minutes.
                </p>
              </div>
              <div class="hidden sm:flex w-14 h-14 bg-white/20 rounded-2xl items-center justify-center">
                <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
            </div>
            
            <button 
              @click="startNewSubmission"
              class="mt-2 sm:mt-4 px-6 sm:px-8 py-3 sm:py-4 bg-white text-primary-600 font-bold text-sm sm:text-base rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-300 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Start New Submission
            </button>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="bg-white rounded-2xl p-5 sm:p-6 shadow-sm border border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Overview
          </h3>
          
          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-500">Total Submissions</span>
                <span class="font-semibold text-gray-800">{{ totalSubmissions }}</span>
              </div>
              <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-primary-500 to-primary-400 rounded-full"
                  :style="{ width: '100%' }"
                ></div>
              </div>
            </div>
            
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="text-gray-500">Acceptance Rate</span>
                <span class="font-semibold text-emerald-600">{{ totalSubmissions ? Math.round((stats.accepted / totalSubmissions) * 100) : 0 }}%</span>
              </div>
              <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-emerald-500 to-emerald-400 rounded-full transition-all duration-500"
                  :style="{ width: `${totalSubmissions ? (stats.accepted / totalSubmissions) * 100 : 0}%` }"
                ></div>
              </div>
            </div>

            <div class="pt-3 border-t border-gray-100">
              <RouterLink 
                to="/submissions" 
                class="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1 group"
              >
                View all submissions
                <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Submissions -->
      <div 
        class="transition-all duration-700 delay-300"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg sm:text-xl font-bold text-gray-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Recent Submissions
          </h2>
          <RouterLink 
            to="/submissions" 
            class="text-sm text-primary-600 hover:text-primary-700 font-medium hidden sm:flex items-center gap-1 group"
          >
            View all
            <svg class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </RouterLink>
        </div>
        
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="divide-y divide-gray-100">
            <div 
              v-for="submission in recentSubmissions"
              :key="submission.id"
              @click="viewSubmission(submission.id)"
              class="p-4 sm:p-5 hover:bg-gray-50 cursor-pointer transition-all duration-200 flex items-center justify-between gap-4 group"
            >
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-800 truncate group-hover:text-primary-600 transition-colors text-sm sm:text-base">
                  {{ submission.title }}
                </h3>
                <div class="flex flex-wrap items-center gap-2 sm:gap-3 mt-1.5 text-xs sm:text-sm text-gray-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    {{ submission.type }}
                  </span>
                  <span class="hidden sm:inline">•</span>
                  <span class="flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ submission.updatedAt }}
                  </span>
                </div>
              </div>
              <div class="flex items-center gap-2 sm:gap-3">
                <span 
                  :class="[
                    'inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full text-xs font-semibold',
                    getStatusStyles(submission.status).bg,
                    getStatusStyles(submission.status).text
                  ]"
                >
                  <span 
                    :class="['w-1.5 h-1.5 rounded-full', getStatusStyles(submission.status).dot]"
                  ></span>
                  <span class="hidden sm:inline">{{ submission.statusText }}</span>
                </span>
                <svg 
                  class="w-5 h-5 text-gray-300 group-hover:text-primary-500 group-hover:translate-x-1 transition-all"
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div 
            v-if="recentSubmissions.length === 0"
            class="text-center py-12 sm:py-16"
          >
            <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">No submissions yet</h3>
            <p class="text-gray-500 mb-6 max-w-sm mx-auto">
              Start by submitting your first manuscript to begin your publishing journey.
            </p>
            <button 
              @click="startNewSubmission" 
              class="px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl shadow-lg shadow-primary-500/30 hover:shadow-xl transition-all"
            >
              Start New Submission
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-200 py-6 mt-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 bg-primary-100 rounded flex items-center justify-center">
              <span class="text-primary-600 font-bold text-xs">T</span>
            </div>
            <span>TruEditor © 2026</span>
          </div>
          <p>Developed by Abdullah Dogan</p>
        </div>
      </div>
    </footer>
  </div>
</template>
