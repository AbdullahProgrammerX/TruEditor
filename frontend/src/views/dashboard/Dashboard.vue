<script setup lang="ts">
/**
 * TruEditor - Author Dashboard
 * ============================
 * Displays author's submissions and their statuses.
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isVisible = ref(false)

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

// Status badge colors
function getStatusColor(status: string) {
  const colors: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-800',
    submitted: 'bg-blue-100 text-blue-800',
    under_review: 'bg-yellow-100 text-yellow-800',
    accepted: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <RouterLink to="/dashboard" class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary-500 rounded-xl flex items-center justify-center">
              <span class="text-white font-bold text-xl">T</span>
            </div>
            <span class="text-xl font-bold text-gray-800">TruEditor</span>
          </RouterLink>

          <!-- User menu -->
          <div class="flex items-center gap-4">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-medium text-gray-800">{{ authStore.fullName }}</p>
              <a 
                :href="authStore.orcidUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs text-orcid hover:underline"
              >
                {{ authStore.orcidId }}
              </a>
            </div>
            <button 
              @click="logout"
              class="btn-ghost text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- Welcome Section -->
      <div 
        class="mb-8 transform transition-all duration-700"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <h1 class="text-3xl font-bold text-gray-800 mb-2">
          Welcome, {{ authStore.fullName?.split(' ')[0] || 'Author' }}!
        </h1>
        <p class="text-gray-600">
          Track your submissions and submit new manuscripts here.
        </p>
      </div>

      <!-- Stats Cards -->
      <div 
        class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8 transform transition-all duration-700 delay-100"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <div class="card text-center hover:border-gray-200 border border-transparent">
          <div class="text-3xl font-bold text-gray-800 mb-1">{{ stats.draft }}</div>
          <div class="text-sm text-gray-500">Drafts</div>
        </div>
        <div class="card text-center hover:border-blue-200 border border-transparent">
          <div class="text-3xl font-bold text-blue-600 mb-1">{{ stats.submitted }}</div>
          <div class="text-sm text-gray-500">Submitted</div>
        </div>
        <div class="card text-center hover:border-yellow-200 border border-transparent">
          <div class="text-3xl font-bold text-yellow-600 mb-1">{{ stats.underReview }}</div>
          <div class="text-sm text-gray-500">Under Review</div>
        </div>
        <div class="card text-center hover:border-green-200 border border-transparent">
          <div class="text-3xl font-bold text-green-600 mb-1">{{ stats.accepted }}</div>
          <div class="text-sm text-gray-500">Accepted</div>
        </div>
      </div>

      <!-- Actions -->
      <div 
        class="mb-8 transform transition-all duration-700 delay-200"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <button 
          @click="startNewSubmission"
          class="btn-primary text-lg px-8 py-4 shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all"
        >
          <span class="mr-2">+</span>
          Start New Submission
        </button>
      </div>

      <!-- Recent Submissions -->
      <div 
        class="transform transition-all duration-700 delay-300"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'"
      >
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Recent Submissions</h2>
        
        <div class="bg-white rounded-xl shadow-card overflow-hidden">
          <div class="divide-y divide-gray-100">
            <div 
              v-for="submission in recentSubmissions"
              :key="submission.id"
              @click="viewSubmission(submission.id)"
              class="p-4 hover:bg-gray-50 cursor-pointer transition-colors flex items-center justify-between group"
            >
              <div class="flex-1 min-w-0">
                <h3 class="font-medium text-gray-800 truncate group-hover:text-primary-600 transition-colors">
                  {{ submission.title }}
                </h3>
                <div class="flex items-center gap-3 mt-1 text-sm text-gray-500">
                  <span>{{ submission.type }}</span>
                  <span>•</span>
                  <span>{{ submission.updatedAt }}</span>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span :class="['badge', getStatusColor(submission.status)]">
                  {{ submission.statusText }}
                </span>
                <svg 
                  class="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors"
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div 
          v-if="recentSubmissions.length === 0"
          class="text-center py-12"
        >
          <div class="text-5xl mb-4">📝</div>
          <h3 class="text-lg font-medium text-gray-800 mb-2">No submissions yet</h3>
          <p class="text-gray-600 mb-4">Start by submitting your first manuscript</p>
          <button @click="startNewSubmission" class="btn-primary">
            Start New Submission
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
