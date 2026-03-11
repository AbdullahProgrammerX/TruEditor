<script setup lang="ts">
/**
 * TruEditor - Submission Detail Page
 * ====================================
 * Full submission detail view with status timeline,
 * manuscript info, authors, files, and action buttons.
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSubmissionStore } from '@/stores/submission'
import StatusTimeline from '@/components/submission/StatusTimeline.vue'
import {
  SUBMISSION_STATUS,
  ARTICLE_TYPES,
  FILE_TYPES,
  LANGUAGES,
} from '@/types/submission'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const submissionStore = useSubmissionStore()

const submissionId = route.params.id as string
const isLoading = ref(true)
const error = ref<string | null>(null)
const activeTab = ref<'overview' | 'files' | 'authors' | 'correspondence' | 'additional'>('overview')
const showWithdrawConfirm = ref(false)
const isWithdrawing = ref(false)
const isMobileMenuOpen = ref(false)
const isGeneratingPdf = ref(false)
const pdfUrl = ref<string | null>(null)
const newMessageBody = ref('')
const newMessageSubject = ref('')
const isSendingMessage = ref(false)

const submission = computed(() => submissionStore.currentSubmission)

const statusInfo = computed(() => {
  if (!submission.value) return null
  return SUBMISSION_STATUS[submission.value.status]
})

const articleTypeInfo = computed(() => {
  if (!submission.value) return null
  return ARTICLE_TYPES[submission.value.article_type]
})

const languageLabel = computed(() => {
  if (!submission.value) return ''
  return LANGUAGES[submission.value.language] || submission.value.language
})

const correspondingAuthor = computed(() => {
  return submission.value?.authors.find(a => a.is_corresponding) || null
})

const activeFiles = computed(() => {
  return submission.value?.files?.filter(f => f.is_active && f.file_type !== 'system_pdf') || []
})

const existingPdf = computed(() => {
  return submission.value?.files?.find(f => f.is_active && f.file_type === 'system_pdf') || null
})

const suggestedReviewers = computed(() => {
  return submission.value?.wizard_data?.suggested_reviewers || []
})

const opposedReviewers = computed(() => {
  return submission.value?.wizard_data?.opposed_reviewers || []
})

const editorComments = computed(() => {
  return submission.value?.wizard_data?.editor_comments || ''
})

const correspondenceMessages = computed(() => {
  return submission.value?.correspondence || []
})

const decisionLetter = computed(() => {
  return correspondenceMessages.value.find(m => m.message_type === 'decision_letter') || null
})

const unreadCount = computed(() => {
  return correspondenceMessages.value.filter(m => !m.is_read && m.message_type !== 'author_to_editor').length
})

onMounted(async () => {
  try {
    await submissionStore.fetchSubmission(submissionId)
  } catch {
    error.value = 'Failed to load submission details.'
  } finally {
    isLoading.value = false
  }
})

async function handleWithdraw() {
  if (!submission.value) return
  isWithdrawing.value = true
  try {
    await submissionStore.withdraw(submission.value.id)
    showWithdrawConfirm.value = false
    ;(window as any).toast?.('success', 'Submission withdrawn successfully.')
  } catch {
    ;(window as any).toast?.('error', 'Failed to withdraw submission.')
  } finally {
    isWithdrawing.value = false
  }
}

async function handleDelete() {
  if (!submission.value) return
  if (!confirm('Are you sure you want to delete this draft? This cannot be undone.')) return
  try {
    await submissionStore.deleteSubmission(submission.value.id)
    ;(window as any).toast?.('success', 'Draft deleted.')
    router.push('/submissions')
  } catch {
    ;(window as any).toast?.('error', 'Failed to delete draft.')
  }
}

async function handleGeneratePdf() {
  if (!submission.value) return
  isGeneratingPdf.value = true
  pdfUrl.value = null
  try {
    const { api } = await import('@/services/api')
    const response = await api.post(`/submissions/${submission.value.id}/build_pdf/`)
    const data = response.data?.data
    if (data?.download_url) {
      pdfUrl.value = data.download_url
      ;(window as any).toast?.('success', 'PDF generated successfully.')
      // Refetch to update files list
      await submissionStore.fetchSubmission(submission.value.id)
    }
  } catch {
    ;(window as any).toast?.('error', 'PDF generation failed. Please try again.')
  } finally {
    isGeneratingPdf.value = false
  }
}

async function handleViewPdf() {
  if (pdfUrl.value) {
    window.open(pdfUrl.value, '_blank')
    return
  }
  if (existingPdf.value) {
    await downloadFile(existingPdf.value.id)
    return
  }
}

async function downloadFile(fileId: string) {
  try {
    const response = await (await import('@/services/api')).api.get(`/files/${fileId}/presigned_url/`)
    const url = response.data?.data?.url || response.data?.url
    if (url) {
      window.open(url, '_blank')
    }
  } catch {
    ;(window as any).toast?.('error', 'Failed to get download link.')
  }
}

async function handleSendMessage() {
  if (!submission.value || !newMessageBody.value.trim()) return
  isSendingMessage.value = true
  try {
    await submissionStore.sendCorrespondence(
      submission.value.id,
      newMessageBody.value.trim(),
      newMessageSubject.value.trim() || undefined,
    )
    newMessageBody.value = ''
    newMessageSubject.value = ''
    ;(window as any).toast?.('success', 'Message sent successfully.')
  } catch {
    ;(window as any).toast?.('error', 'Failed to send message.')
  } finally {
    isSendingMessage.value = false
  }
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function formatDateTime(dateStr: string | null): string {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function getFileIcon(mimeType: string): string {
  if (mimeType.includes('pdf')) return '📄'
  if (mimeType.includes('word') || mimeType.includes('document')) return '📝'
  if (mimeType.includes('image')) return '🖼️'
  if (mimeType.includes('spreadsheet') || mimeType.includes('excel')) return '📊'
  return '📎'
}

function logout() {
  authStore.logout()
  router.push('/')
}

const tabs = [
  { id: 'overview' as const, label: 'Overview', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
  { id: 'files' as const, label: 'Files', icon: 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z' },
  { id: 'authors' as const, label: 'Authors', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z' },
  { id: 'correspondence' as const, label: 'Messages', icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { id: 'additional' as const, label: 'Details', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
]
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
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
              <p class="text-xs text-white/60 -mt-0.5">Submission Detail</p>
            </div>
          </RouterLink>

          <nav class="hidden md:flex items-center gap-1">
            <RouterLink to="/dashboard" class="px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all">Dashboard</RouterLink>
            <RouterLink to="/submissions" class="px-4 py-2 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition-all font-medium">Submissions</RouterLink>
            <RouterLink to="/profile" class="px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-all">Profile</RouterLink>
          </nav>

          <div class="flex items-center gap-2 sm:gap-4">
            <div class="hidden sm:block text-right">
              <p class="text-sm font-semibold text-white">{{ authStore.fullName }}</p>
            </div>
            <button @click="logout" class="hidden sm:flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white text-sm font-medium transition-all">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
              Logout
            </button>
            <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="md:hidden p-2 text-white/80 hover:text-white rounded-lg hover:bg-white/10">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
          </div>
        </div>
        <!-- Mobile menu -->
        <div v-if="isMobileMenuOpen" class="md:hidden pb-4 border-t border-white/10 mt-2 pt-3 space-y-1">
          <RouterLink to="/dashboard" class="block px-4 py-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg">Dashboard</RouterLink>
          <RouterLink to="/submissions" class="block px-4 py-2 text-white hover:bg-white/10 rounded-lg font-medium">Submissions</RouterLink>
          <RouterLink to="/profile" class="block px-4 py-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg">Profile</RouterLink>
          <button @click="logout" class="w-full text-left px-4 py-2 text-white/80 hover:text-white hover:bg-white/10 rounded-lg">Logout</button>
        </div>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <div class="animate-pulse space-y-6">
        <div class="h-8 bg-gray-200 rounded w-1/3"></div>
        <div class="h-4 bg-gray-200 rounded w-1/4"></div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-4">
            <div class="h-40 bg-gray-200 rounded-xl"></div>
            <div class="h-60 bg-gray-200 rounded-xl"></div>
          </div>
          <div class="h-80 bg-gray-200 rounded-xl"></div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-5xl mx-auto px-4 sm:px-6 py-12">
      <div class="bg-white rounded-2xl shadow-sm border border-red-200 p-8 text-center">
        <div class="text-5xl mb-4">⚠️</div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">Could not load submission</h2>
        <p class="text-gray-600 mb-6">{{ error }}</p>
        <button @click="router.push('/submissions')" class="px-6 py-2.5 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium">
          Back to Submissions
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main v-else-if="submission" class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <!-- Back link & Title bar -->
      <div class="mb-6">
        <button @click="router.push('/submissions')" class="text-sm text-gray-500 hover:text-primary-600 transition-colors mb-3 flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          Back to Submissions
        </button>
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div class="min-w-0">
            <div class="flex items-center gap-3 flex-wrap mb-1">
              <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 break-words">{{ submission.title || 'Untitled Submission' }}</h1>
            </div>
            <div class="flex items-center gap-3 text-sm text-gray-500 flex-wrap">
              <span v-if="submission.manuscript_id" class="font-mono font-semibold text-primary-600">{{ submission.manuscript_id }}</span>
              <span v-else class="font-mono text-gray-400">DRAFT</span>
              <span class="text-gray-300">|</span>
              <span>{{ articleTypeInfo?.label }}</span>
              <span class="text-gray-300">|</span>
              <span>{{ languageLabel }}</span>
            </div>
          </div>
          <!-- Status Badge -->
          <div v-if="statusInfo" class="flex-shrink-0">
            <span :class="[statusInfo.bgColor, statusInfo.color]" class="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold">
              {{ submission.status_display }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left: Tabs & Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Tabs -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="flex border-b border-gray-100">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'flex-1 flex items-center justify-center gap-2 px-4 py-3.5 text-sm font-medium transition-all border-b-2',
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600 bg-primary-50/30'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                ]"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="tab.icon" /></svg>
                <span class="hidden sm:inline">{{ tab.label }}</span>
                <span v-if="tab.id === 'correspondence' && unreadCount > 0" class="w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">{{ unreadCount }}</span>
              </button>
            </div>

            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="p-6 space-y-6">
              <!-- Abstract -->
              <div v-if="submission.abstract">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Abstract</h3>
                <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ submission.abstract }}</p>
              </div>
              <div v-if="submission.abstract_en && submission.language === 'tr'">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Abstract (English)</h3>
                <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ submission.abstract_en }}</p>
              </div>

              <!-- Title (English) -->
              <div v-if="submission.title_en && submission.language === 'tr'">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">English Title</h3>
                <p class="text-gray-700">{{ submission.title_en }}</p>
              </div>

              <!-- Keywords -->
              <div v-if="submission.keywords?.length">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Keywords</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="kw in submission.keywords" :key="kw" class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">{{ kw }}</span>
                </div>
              </div>
              <div v-if="submission.keywords_en?.length && submission.language === 'tr'">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Keywords (English)</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="kw in submission.keywords_en" :key="kw" class="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">{{ kw }}</span>
                </div>
              </div>

              <!-- Quick Stats -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <p class="text-2xl font-bold text-gray-800">{{ submission.author_count }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">Authors</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <p class="text-2xl font-bold text-gray-800">{{ activeFiles.length }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">Files</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <p class="text-2xl font-bold text-gray-800">{{ submission.revision_number }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">Revisions</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <p class="text-sm font-semibold text-gray-800">{{ formatDate(submission.submitted_at || submission.created_at) }}</p>
                  <p class="text-xs text-gray-500 mt-0.5">{{ submission.submitted_at ? 'Submitted' : 'Created' }}</p>
                </div>
              </div>
            </div>

            <!-- Files Tab -->
            <div v-if="activeTab === 'files'" class="p-6">
              <div v-if="activeFiles.length === 0" class="text-center py-8 text-gray-500">
                <div class="text-4xl mb-2">📁</div>
                <p>No files uploaded yet.</p>
              </div>
              <div v-else class="space-y-3">
                <div
                  v-for="file in activeFiles"
                  :key="file.id"
                  class="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors group"
                >
                  <div class="flex items-center gap-3 min-w-0">
                    <span class="text-2xl flex-shrink-0">{{ getFileIcon(file.mime_type) }}</span>
                    <div class="min-w-0">
                      <p class="text-sm font-medium text-gray-800 truncate">{{ file.original_filename }}</p>
                      <div class="flex items-center gap-2 text-xs text-gray-500">
                        <span class="px-1.5 py-0.5 bg-white rounded text-gray-600 font-medium">{{ FILE_TYPES[file.file_type]?.label || file.file_type }}</span>
                        <span>{{ file.file_size_human }}</span>
                        <span>{{ formatDate(file.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  <button
                    @click="downloadFile(file.id)"
                    class="flex-shrink-0 p-2 text-gray-400 hover:text-primary-600 hover:bg-white rounded-lg transition-all opacity-60 group-hover:opacity-100"
                    title="Download"
                  >
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Authors Tab -->
            <div v-if="activeTab === 'authors'" class="p-6">
              <div v-if="!submission.authors?.length" class="text-center py-8 text-gray-500">
                <div class="text-4xl mb-2">👤</div>
                <p>No authors added yet.</p>
              </div>
              <div v-else class="space-y-3">
                <div
                  v-for="author in submission.authors"
                  :key="author.id"
                  class="p-4 bg-gray-50 rounded-xl"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold" :class="author.is_corresponding ? 'bg-primary-100 text-primary-700' : 'bg-gray-200 text-gray-600'">
                        {{ author.order }}
                      </div>
                      <div>
                        <div class="flex items-center gap-2">
                          <p class="font-semibold text-gray-800">{{ author.full_name }}</p>
                          <span v-if="author.is_corresponding" class="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full font-medium">Corresponding</span>
                        </div>
                        <p class="text-sm text-gray-600">{{ author.affiliation }}</p>
                        <div class="flex items-center gap-3 mt-1 text-xs text-gray-500">
                          <a :href="'mailto:' + author.email" class="hover:text-primary-600 transition-colors">{{ author.email }}</a>
                          <span v-if="author.orcid_id" class="text-green-600">ORCID: {{ author.orcid_id }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <p v-if="author.contribution" class="text-xs text-gray-500 mt-2 pl-13"><span class="font-medium">Contribution:</span> {{ author.contribution }}</p>
                </div>
              </div>
            </div>

            <!-- Correspondence Tab -->
            <div v-if="activeTab === 'correspondence'" class="p-6 space-y-5">
              <!-- Decision Letter (if exists, show first) -->
              <div v-if="decisionLetter" class="border-2 border-emerald-200 bg-emerald-50 rounded-xl p-5">
                <div class="flex items-center gap-2 mb-3">
                  <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                  <div>
                    <p class="font-bold text-emerald-800">Decision Letter</p>
                    <p class="text-xs text-emerald-600">{{ formatDateTime(decisionLetter.created_at) }}</p>
                  </div>
                </div>
                <p v-if="decisionLetter.subject" class="font-semibold text-emerald-900 mb-2">{{ decisionLetter.subject }}</p>
                <div class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">{{ decisionLetter.body }}</div>
              </div>

              <!-- Message thread -->
              <div v-if="correspondenceMessages.length === 0 && !decisionLetter" class="text-center py-10 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                <p class="font-medium">No messages yet</p>
                <p class="text-sm mt-1">Send a message to the editor using the form below.</p>
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="msg in correspondenceMessages.filter(m => m.message_type !== 'decision_letter')"
                  :key="msg.id"
                  class="rounded-xl p-4"
                  :class="[
                    msg.message_type === 'author_to_editor'
                      ? 'bg-primary-50 border border-primary-100 ml-6'
                      : msg.message_type === 'system'
                        ? 'bg-gray-50 border border-gray-100'
                        : 'bg-blue-50 border border-blue-100 mr-6'
                  ]"
                >
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div
                        class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
                        :class="msg.message_type === 'author_to_editor' ? 'bg-primary-200 text-primary-700' : 'bg-blue-200 text-blue-700'"
                      >
                        {{ msg.sender_name?.charAt(0) || '?' }}
                      </div>
                      <div>
                        <p class="text-sm font-semibold" :class="msg.message_type === 'author_to_editor' ? 'text-primary-800' : 'text-blue-800'">
                          {{ msg.sender_name }}
                        </p>
                        <p class="text-xs text-gray-500">{{ msg.message_type_display }}</p>
                      </div>
                    </div>
                    <span class="text-xs text-gray-400">{{ formatDateTime(msg.created_at) }}</span>
                  </div>
                  <p v-if="msg.subject" class="text-sm font-semibold text-gray-800 mb-1">{{ msg.subject }}</p>
                  <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">{{ msg.body }}</p>
                </div>
              </div>

              <!-- Send Message Form (only for non-draft) -->
              <div v-if="submission.status !== 'draft'" class="border-t border-gray-200 pt-5">
                <h4 class="text-sm font-semibold text-gray-700 mb-3">Send Message to Editor</h4>
                <div class="space-y-3">
                  <input
                    v-model="newMessageSubject"
                    type="text"
                    placeholder="Subject (optional)"
                    class="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10 transition-all"
                  />
                  <textarea
                    v-model="newMessageBody"
                    rows="4"
                    placeholder="Write your message..."
                    class="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10 transition-all resize-none"
                  ></textarea>
                  <div class="flex justify-end">
                    <button
                      @click="handleSendMessage"
                      :disabled="!newMessageBody.trim() || isSendingMessage"
                      class="px-6 py-2.5 bg-primary-500 hover:bg-primary-600 text-white font-semibold text-sm rounded-xl shadow-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      <svg v-if="!isSendingMessage" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
                      <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                      {{ isSendingMessage ? 'Sending...' : 'Send Message' }}
                    </button>
                  </div>
                </div>
              </div>
              <p v-else class="text-sm text-gray-400 text-center">Submit your manuscript before sending messages to the editor.</p>
            </div>

            <!-- Additional Details Tab -->
            <div v-if="activeTab === 'additional'" class="p-6 space-y-5">
              <div v-if="submission.cover_letter">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Cover Letter</h3>
                <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-line bg-gray-50 rounded-lg p-4">{{ submission.cover_letter }}</p>
              </div>

              <div v-if="submission.ethics_statement || submission.ethics_approval_number">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Ethics Statement</h3>
                <div class="bg-gray-50 rounded-lg p-4 text-sm space-y-1">
                  <p v-if="submission.ethics_approval_number" class="text-gray-700"><span class="font-medium">Approval #:</span> {{ submission.ethics_approval_number }}</p>
                  <p v-if="submission.ethics_statement" class="text-gray-700 whitespace-pre-line">{{ submission.ethics_statement }}</p>
                </div>
              </div>

              <div v-if="submission.conflict_of_interest">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Conflict of Interest</h3>
                <p class="text-gray-700 text-sm bg-gray-50 rounded-lg p-4 whitespace-pre-line">{{ submission.conflict_of_interest }}</p>
              </div>

              <div v-if="submission.funding_statement">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Funding</h3>
                <p class="text-gray-700 text-sm bg-gray-50 rounded-lg p-4 whitespace-pre-line">{{ submission.funding_statement }}</p>
              </div>

              <div v-if="suggestedReviewers.length">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Suggested Reviewers</h3>
                <div class="space-y-2">
                  <div v-for="(rev, i) in suggestedReviewers" :key="i" class="bg-gray-50 rounded-lg p-3 text-sm">
                    <p class="font-medium text-gray-800">{{ rev.name }}</p>
                    <p class="text-gray-600">{{ rev.email }} &middot; {{ rev.institution }}</p>
                    <p v-if="rev.reason" class="text-gray-500 text-xs mt-1">{{ rev.reason }}</p>
                  </div>
                </div>
              </div>

              <div v-if="opposedReviewers.length">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Opposed Reviewers</h3>
                <div class="space-y-2">
                  <div v-for="(rev, i) in opposedReviewers" :key="i" class="bg-red-50 rounded-lg p-3 text-sm">
                    <p class="font-medium text-gray-800">{{ rev.name }}</p>
                    <p v-if="rev.email" class="text-gray-600">{{ rev.email }}</p>
                    <p v-if="rev.reason" class="text-gray-500 text-xs mt-1">{{ rev.reason }}</p>
                  </div>
                </div>
              </div>

              <div v-if="editorComments">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Comments to Editor</h3>
                <p class="text-gray-700 text-sm bg-yellow-50 rounded-lg p-4 whitespace-pre-line border border-yellow-100">{{ editorComments }}</p>
              </div>

              <!-- Revision Info -->
              <div v-if="submission.revision_notes || submission.revision_response">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Revision Information</h3>
                
                <div v-if="submission.revision_notes" class="bg-orange-50 rounded-lg p-4 text-sm border border-orange-100 mb-3">
                  <p class="text-xs font-semibold text-orange-600 mb-1">Editor's Request (Revision #{{ submission.revision_number }})</p>
                  <p class="text-gray-700 whitespace-pre-line">{{ submission.revision_notes }}</p>
                  <p v-if="submission.revision_deadline" class="text-orange-600 text-xs mt-2 font-medium">Deadline: {{ formatDate(submission.revision_deadline) }}</p>
                </div>

                <div v-if="submission.revision_response" class="bg-purple-50 rounded-lg p-4 text-sm border border-purple-100">
                  <p class="text-xs font-semibold text-purple-600 mb-1">Author's Response</p>
                  <p class="text-gray-700 whitespace-pre-line">{{ submission.revision_response }}</p>
                  <p v-if="submission.revision_submitted_at" class="text-purple-600 text-xs mt-2 font-medium">Submitted: {{ formatDate(submission.revision_submitted_at) }}</p>
                </div>
              </div>

              <div v-if="!submission.cover_letter && !submission.ethics_statement && !submission.conflict_of_interest && !submission.funding_statement && !suggestedReviewers.length && !opposedReviewers.length && !editorComments && !submission.revision_notes" class="text-center py-8 text-gray-500">
                <div class="text-4xl mb-2">📋</div>
                <p>No additional details provided.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Sidebar -->
        <div class="space-y-6">
          <!-- Actions -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Actions</h3>
            <div class="space-y-2.5">
              <!-- Generate PDF -->
              <button
                @click="handleGeneratePdf"
                :disabled="isGeneratingPdf"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors font-medium text-sm disabled:opacity-50"
              >
                <svg v-if="!isGeneratingPdf" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                {{ isGeneratingPdf ? 'Generating PDF...' : existingPdf ? 'Regenerate PDF' : 'Generate PDF' }}
              </button>

              <!-- View/Download PDF -->
              <button
                v-if="existingPdf || pdfUrl"
                @click="handleViewPdf"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-colors font-medium text-sm"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                View / Download PDF
              </button>

              <!-- Submit Revision (revision_required) -->
              <button
                v-if="submission.status === 'revision_required'"
                @click="router.push(`/submissions/${submission.id}/revise`)"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors font-medium text-sm"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                Submit Revision
              </button>

              <!-- Edit (draft only now) -->
              <button
                v-if="submission.status === 'draft'"
                @click="router.push(`/submissions/new?edit=${submission.id}`)"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-primary-50 text-primary-700 rounded-lg hover:bg-primary-100 transition-colors font-medium text-sm"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                Edit Submission
              </button>

              <!-- Withdraw (submitted / under_review / revision_required) -->
              <button
                v-if="submission.can_be_withdrawn && submission.status !== 'draft'"
                @click="showWithdrawConfirm = true"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors font-medium text-sm"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" /></svg>
                Withdraw Submission
              </button>

              <!-- Delete (draft only) -->
              <button
                v-if="submission.status === 'draft'"
                @click="handleDelete"
                class="w-full flex items-center gap-3 px-4 py-2.5 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors font-medium text-sm"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                Delete Draft
              </button>

              <!-- No actions available -->
              <p v-if="!submission.is_editable && (!submission.can_be_withdrawn || submission.status === 'draft') && submission.status !== 'draft'" class="text-sm text-gray-500 text-center py-2">
                No actions available for this status.
              </p>
            </div>
          </div>

          <!-- Submission Info -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Submission Info</h3>
            <dl class="space-y-3 text-sm">
              <div class="flex justify-between">
                <dt class="text-gray-500">Created</dt>
                <dd class="text-gray-800 font-medium">{{ formatDate(submission.created_at) }}</dd>
              </div>
              <div v-if="submission.submitted_at" class="flex justify-between">
                <dt class="text-gray-500">Submitted</dt>
                <dd class="text-gray-800 font-medium">{{ formatDate(submission.submitted_at) }}</dd>
              </div>
              <div v-if="submission.accepted_at" class="flex justify-between">
                <dt class="text-gray-500">Accepted</dt>
                <dd class="text-green-700 font-medium">{{ formatDate(submission.accepted_at) }}</dd>
              </div>
              <div v-if="submission.published_at" class="flex justify-between">
                <dt class="text-gray-500">Published</dt>
                <dd class="text-emerald-700 font-medium">{{ formatDate(submission.published_at) }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-500">Last Updated</dt>
                <dd class="text-gray-800">{{ formatDateTime(submission.updated_at) }}</dd>
              </div>
              <div v-if="correspondingAuthor" class="flex justify-between">
                <dt class="text-gray-500">Corresponding</dt>
                <dd class="text-gray-800 text-right">{{ correspondingAuthor.full_name }}</dd>
              </div>
              <div v-if="submission.assigned_editor" class="flex justify-between">
                <dt class="text-gray-500">Editor</dt>
                <dd class="text-gray-800">{{ submission.assigned_editor.full_name }}</dd>
              </div>
              <div v-if="submission.editor_decision" class="flex justify-between">
                <dt class="text-gray-500">Decision</dt>
                <dd class="font-semibold" :class="submission.editor_decision === 'accept' ? 'text-green-700' : submission.editor_decision === 'reject' ? 'text-red-700' : 'text-orange-700'">
                  {{ submission.editor_decision.replace('_', ' ') }}
                </dd>
              </div>
            </dl>
          </div>

          <!-- Status Timeline -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Status Timeline</h3>
            <StatusTimeline
              :history="submission.status_history || []"
              :current-status="submission.status"
              :created-at="submission.created_at"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- Withdraw Confirmation Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showWithdrawConfirm" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50" @click.self="showWithdrawConfirm = false">
          <div class="bg-white rounded-2xl shadow-xl max-w-md w-full p-6">
            <div class="text-center">
              <div class="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" /></svg>
              </div>
              <h3 class="text-lg font-bold text-gray-900 mb-2">Withdraw Submission?</h3>
              <p class="text-gray-600 text-sm mb-6">
                Are you sure you want to withdraw <strong>{{ submission?.manuscript_id || 'this submission' }}</strong>?
                This action can be reversed by contacting the editorial office.
              </p>
              <div class="flex gap-3">
                <button
                  @click="showWithdrawConfirm = false"
                  class="flex-1 px-4 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm"
                >
                  Cancel
                </button>
                <button
                  @click="handleWithdraw"
                  :disabled="isWithdrawing"
                  class="flex-1 px-4 py-2.5 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors font-medium text-sm disabled:opacity-50"
                >
                  {{ isWithdrawing ? 'Withdrawing...' : 'Yes, Withdraw' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.pl-13 {
  padding-left: 3.25rem;
}
</style>
