<script setup lang="ts">
/**
 * TruEditor - Submissions List Page
 * ==================================
 * Full-page submissions list with status filter.
 * Used by /submissions route and linked from Dashboard.
 */
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSubmissionStore } from '@/stores/submission'
import SubmissionTable from '@/components/submission/SubmissionTable.vue'
import type { SubmissionStatus } from '@/types/submission'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const submissionStore = useSubmissionStore()

const isMobileMenuOpen = ref(false)

const statusFilter = ref<SubmissionStatus | undefined>(
  (route.query.status as SubmissionStatus) || undefined
)

const statusTabs = [
  { value: undefined as SubmissionStatus | undefined, label: 'All' },
  { value: 'draft' as SubmissionStatus, label: 'Draft' },
  { value: 'submitted' as SubmissionStatus, label: 'Submitted' },
  { value: 'under_review' as SubmissionStatus, label: 'In Review' },
  { value: 'revision_required' as SubmissionStatus, label: 'Revision' },
  { value: 'accepted' as SubmissionStatus, label: 'Accepted' },
  { value: 'rejected' as SubmissionStatus, label: 'Rejected' },
]

async function fetchWithFilter() {
  await submissionStore.filterByStatus(statusFilter.value)
}

onMounted(async () => {
  statusFilter.value = (route.query.status as SubmissionStatus) || undefined
  await fetchWithFilter()
})

watch(
  () => route.query.status,
  (newStatus) => {
    statusFilter.value = (newStatus as SubmissionStatus) || undefined
    fetchWithFilter()
  }
)

function setFilter(status: SubmissionStatus | undefined) {
  statusFilter.value = status
  router.replace({
    path: '/submissions',
    query: status ? { status } : {},
  })
  fetchWithFilter()
}

function startNewSubmission() {
  router.push('/submissions/new')
}

function viewSubmission(id: string) {
  router.push(`/submissions/${id}`)
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
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header (same as Dashboard) -->
    <header class="bg-gradient-to-r from-primary-600 via-primary-500 to-primary-600 shadow-lg sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16 sm:h-20">
          <RouterLink to="/dashboard" class="flex items-center gap-2 sm:gap-3 group">
            <div class="relative">
              <div class="w-9 h-9 sm:w-11 sm:h-11 bg-white rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
                <span class="text-primary-500 font-bold text-lg sm:text-xl">T</span>
              </div>
              <div class="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-primary-500"></div>
            </div>
            <div class="hidden sm:block">
              <span class="text-xl font-bold text-white tracking-tight">TruEditor</span>
              <p class="text-xs text-white/60 -mt-0.5">Submissions</p>
            </div>
          </RouterLink>

          <nav class="hidden md:flex items-center gap-1">
            <RouterLink
              to="/dashboard"
              class="px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all"
            >
              Dashboard
            </RouterLink>
            <RouterLink
              to="/submissions"
              class="px-4 py-2 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition-all font-medium"
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

        <div v-show="isMobileMenuOpen" class="md:hidden pb-4 border-t border-white/10 mt-2 pt-4">
          <nav class="flex flex-col gap-1">
            <RouterLink to="/dashboard" class="px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all" @click="isMobileMenuOpen = false">
              Dashboard
            </RouterLink>
            <RouterLink to="/submissions" class="px-4 py-2.5 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition-all font-medium" @click="isMobileMenuOpen = false">
              Submissions
            </RouterLink>
            <RouterLink to="/profile" class="px-4 py-2.5 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all" @click="isMobileMenuOpen = false">
              Profile
            </RouterLink>
            <button @click="logout" class="flex items-center gap-2 px-4 py-2.5 text-red-300 hover:text-red-200 hover:bg-white/10 rounded-lg transition-all text-left">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </nav>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <h1 class="text-2xl font-bold text-gray-800">My Submissions</h1>
        <button
          @click="startNewSubmission"
          class="inline-flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors font-medium"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Submission
        </button>
      </div>

      <!-- Status filter tabs -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button
          v-for="tab in statusTabs"
          :key="tab.label"
          @click="setFilter(tab.value)"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="statusFilter === tab.value
            ? 'bg-primary-500 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'"
        >
          {{ tab.label }}
        </button>
      </div>

      <SubmissionTable
        :items="submissionStore.submissions"
        :loading="submissionStore.isLoading"
        :current-page="submissionStore.currentPage"
        :total-pages="submissionStore.totalPages"
        empty-message="No submissions found. Start your first manuscript."
        @page-change="handlePageChange"
        @delete="handleDeleteSubmission"
        @view="viewSubmission"
        @edit="viewSubmission"
      />
    </main>
  </div>
</template>
