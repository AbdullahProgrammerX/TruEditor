<script setup lang="ts">
/**
 * TruEditor - Author Dashboard
 * ============================
 * Modern dashboard displaying author's submissions and their statuses.
 * Uses submission store for real data.
 */
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSubmissionStore } from '@/stores/submission'
import SubmissionTable from '@/components/submission/SubmissionTable.vue'

const router = useRouter()
const authStore = useAuthStore()
const submissionStore = useSubmissionStore()

const isVisible = ref(false)
const isMobileMenuOpen = ref(false)
const showWelcomeBanner = ref(false)
const showProfileReminder = ref(false)

// Stats from submission store
const stats = computed(() => ({
  draft: submissionStore.draftCount,
  submitted: submissionStore.submittedCount,
  underReview: submissionStore.byStatus('under_review').length,
  accepted: submissionStore.acceptedCount,
}))

const totalSubmissions = computed(() => submissionStore.totalCount)

onMounted(async () => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)

  if (authStore.isNewUser) {
    showWelcomeBanner.value = true
    authStore.isNewUser = false
  }

  if (!authStore.profileCompleted) {
    showProfileReminder.value = true
  }

  await submissionStore.fetchSubmissions()
})

function startNewSubmission() {
  router.push('/submissions/new')
}

function viewSubmission(id: string) {
  router.push(`/submissions/${id}`)
}

function goToSubmissions(status?: string) {
  router.push({ path: '/submissions', query: status ? { status } : {} })
}

function handlePageChange(page: number) {
  submissionStore.setPage(page)
}

function handleDeleteSubmission(id: string) {
  if (confirm('Are you sure you want to delete this draft?')) {
    submissionStore.deleteSubmission(id)
  }
}

function logout() {
  authStore.logout()
  router.push('/')
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
            <img src="/logo-icon.png" alt="TruEditor" class="brand-logo brand-logo--header brand-logo--on-dark group-hover:opacity-90 transition-opacity" />
            <div class="hidden sm:block">
              <span class="text-xl font-bold text-white tracking-tight">Tru<span class="text-white/70">Editor</span></span>
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
      <!-- Welcome Banner (new users) -->
      <Transition name="banner">
        <div 
          v-if="showWelcomeBanner"
          class="mb-6 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl p-5 sm:p-6 text-white relative overflow-hidden"
        >
          <button 
            @click="showWelcomeBanner = false"
            class="absolute top-3 right-3 p-1.5 rounded-lg hover:bg-white/20 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center flex-shrink-0">
              <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
            </div>
            <div>
              <h2 class="text-lg sm:text-xl font-bold">Welcome to TruEditor!</h2>
              <p class="text-white/85 text-sm mt-1">
                Your account has been created successfully. Start by completing your profile, then submit your first manuscript.
              </p>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Profile Completion Reminder -->
      <Transition name="banner">
        <div 
          v-if="showProfileReminder && !showWelcomeBanner"
          class="mb-6 bg-amber-50 border border-amber-200 rounded-2xl p-5 sm:p-6 relative"
        >
          <button 
            @click="showProfileReminder = false"
            class="absolute top-3 right-3 p-1.5 rounded-lg text-amber-400 hover:text-amber-600 hover:bg-amber-100 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-6 h-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
            <div class="flex-1">
              <h3 class="font-semibold text-amber-800">Complete Your Profile</h3>
              <p class="text-amber-700 text-sm mt-0.5">
                Your profile is incomplete. A complete profile is required before submitting manuscripts.
              </p>
            </div>
            <RouterLink 
              to="/profile"
              class="flex-shrink-0 px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-semibold text-sm rounded-xl transition-colors"
            >
              Complete Profile
            </RouterLink>
          </div>
        </div>
      </Transition>

      <!-- Welcome Section -->
      <div 
        class="mb-6 sm:mb-8 transition-all duration-700"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-1">
          {{ greeting }}, {{ authStore.fullName?.split(' ')[0] || 'Author' }}
        </h1>
        <p class="text-gray-500 text-sm sm:text-base">
          Here's what's happening with your submissions.
        </p>
      </div>

      <!-- Stats Cards (clickable when count > 0) -->
      <div 
        class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8 transition-all duration-700 delay-100"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <button
          @click="stats.draft > 0 ? goToSubmissions('draft') : null"
          class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group text-left"
          :class="{ 'cursor-pointer': stats.draft > 0, 'cursor-default': stats.draft === 0 }"
        >
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
        </button>

        <button
          @click="stats.submitted > 0 ? goToSubmissions('submitted') : null"
          class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group text-left"
          :class="{ 'cursor-pointer': stats.submitted > 0, 'cursor-default': stats.submitted === 0 }"
        >
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
        </button>

        <button
          @click="stats.underReview > 0 ? goToSubmissions('under_review') : null"
          class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group text-left"
          :class="{ 'cursor-pointer': stats.underReview > 0, 'cursor-default': stats.underReview === 0 }"
        >
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
        </button>

        <button
          @click="stats.accepted > 0 ? goToSubmissions('accepted') : null"
          class="bg-white rounded-2xl p-4 sm:p-6 shadow-sm hover:shadow-md transition-all border border-gray-100 group text-left"
          :class="{ 'cursor-pointer': stats.accepted > 0, 'cursor-default': stats.accepted === 0 }"
        >
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
        </button>
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

      <!-- Submissions Table -->
      <div 
        class="transition-all duration-700 delay-300"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg sm:text-xl font-bold text-gray-800 flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            My Submissions
          </h2>
        </div>

        <SubmissionTable
          :items="submissionStore.submissions"
          :loading="submissionStore.isLoading"
          :current-page="submissionStore.currentPage"
          :total-pages="submissionStore.totalPages"
          empty-message="No submissions yet. Start your first manuscript."
          @page-change="handlePageChange"
          @delete="handleDeleteSubmission"
          @view="viewSubmission"
          @edit="viewSubmission"
        />
      </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-200 py-6 mt-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <div class="flex items-center gap-2">
            <img src="/logo-icon.png" alt="TruEditor" class="brand-logo brand-logo--footer brand-logo--on-light" />
            <span>TruEditor © 2026</span>
          </div>
          <p>Developed by Abdullah Dogan</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.banner-enter-active,
.banner-leave-active {
  transition: all 0.4s ease;
}
.banner-enter-from,
.banner-leave-to {
  opacity: 0;
  max-height: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
  overflow: hidden;
}
</style>
