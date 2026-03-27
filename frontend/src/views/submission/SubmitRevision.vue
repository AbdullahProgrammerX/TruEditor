<script setup lang="ts">
/**
 * TruEditor - Submit Revision Page
 * ==================================
 * Allows authors to upload revised files, respond to reviewer
 * comments, and submit their revision.
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSubmissionStore } from '@/stores/submission'
import { useFileUpload } from '@/composables/useFileUpload'
import { SUBMISSION_STATUS, FILE_TYPES } from '@/types/submission'
import type { FileType } from '@/types/submission'

const route = useRoute()
const router = useRouter()
const submissionStore = useSubmissionStore()

const submissionId = route.params.id as string
const isLoading = ref(true)
const error = ref<string | null>(null)
const revisionResponse = ref('')
const isSubmitting = ref(false)
const showSubmitConfirm = ref(false)
const selectedFileType = ref<FileType>('revision')
const isDragging = ref(false)

const submission = computed(() => submissionStore.currentSubmission)

const statusInfo = computed(() => {
  if (!submission.value) return null
  return SUBMISSION_STATUS[submission.value.status]
})

const {
  uploadingFiles,
  serverFiles,
  isLoadingFiles,
  isUploading,
  formatFileSize,
  fetchFiles,
  uploadFile,
  removeFile,
  dismissUploadEntry,
  getDownloadUrl,
} = useFileUpload(() => submissionId)

const revisionFileTypes: { key: FileType; label: string }[] = [
  { key: 'revision', label: 'Revised Manuscript' },
  { key: 'revision_notes', label: 'Revision Notes / Response Letter' },
  { key: 'main_text', label: 'Main Text (Replacement)' },
  { key: 'figures', label: 'Figures' },
  { key: 'tables', label: 'Tables' },
  { key: 'supplementary', label: 'Supplementary Material' },
  { key: 'other', label: 'Other' },
]

const revisionFiles = computed(() =>
  serverFiles.value.filter(f =>
    f.revision_number === (submission.value?.revision_number ?? 0)
  )
)

const previousFiles = computed(() =>
  serverFiles.value.filter(f =>
    f.revision_number < (submission.value?.revision_number ?? 0) &&
    f.file_type !== 'system_pdf'
  )
)

const allDisplayFiles = computed(() => {
  const uploading = uploadingFiles.value.map(f => ({
    id: f.id,
    name: f.name,
    size: f.size,
    fileType: f.fileType,
    progress: f.progress,
    status: f.status as string,
    errorMessage: f.errorMessage,
  }))

  const server = revisionFiles.value.map(f => ({
    id: f.id,
    name: f.original_filename,
    size: f.file_size,
    fileType: f.file_type,
    progress: 100,
    status: 'server',
    errorMessage: undefined,
  }))

  return [...uploading, ...server]
})

const daysLeft = computed(() => {
  if (!submission.value?.revision_deadline) return null
  const deadline = new Date(submission.value.revision_deadline)
  const now = new Date()
  const diff = Math.ceil((deadline.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  return diff
})

const canSubmit = computed(() =>
  revisionResponse.value.trim().length > 20 &&
  revisionFiles.value.length > 0 &&
  !isUploading.value
)

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

function handleDrop(event: DragEvent): void {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (!files || files.length === 0) return
  Array.from(files).forEach(file => uploadFile(file, selectedFileType.value))
}

function handleFileInput(event: Event): void {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (!files) return
  Array.from(files).forEach(file => uploadFile(file, selectedFileType.value))
  input.value = ''
}

async function handleRemoveFile(fileId: string, fileStatus: string): Promise<void> {
  if (fileStatus === 'error') {
    dismissUploadEntry(fileId)
    return
  }
  if (fileStatus === 'server') {
    try {
      await removeFile(fileId)
      ;(window as any).toast?.('success', 'File removed.')
    } catch {
      ;(window as any).toast?.('error', 'Could not remove file.')
    }
  }
}

async function handleDownload(fileId: string, filename: string): Promise<void> {
  const url = await getDownloadUrl(fileId)
  if (url) {
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.target = '_blank'
    a.click()
  }
}

function getTypeLabel(ft: string): string {
  return FILE_TYPES[ft as FileType]?.label || ft
}

function getTypeColor(ft: string): string {
  const colors: Record<string, string> = {
    revision: 'bg-purple-100 text-purple-700',
    revision_notes: 'bg-pink-100 text-pink-700',
    main_text: 'bg-blue-100 text-blue-700',
    figures: 'bg-green-100 text-green-700',
    tables: 'bg-yellow-100 text-yellow-700',
    supplementary: 'bg-teal-100 text-teal-700',
    other: 'bg-gray-100 text-gray-700',
  }
  return colors[ft] || 'bg-gray-100 text-gray-600'
}

async function handleSubmitRevision(): Promise<void> {
  if (!canSubmit.value) return
  showSubmitConfirm.value = false
  isSubmitting.value = true

  try {
    await submissionStore.submitRevision(submissionId, revisionResponse.value)
    ;(window as any).toast?.('success', 'Revision submitted successfully!')
    router.push(`/submissions/${submissionId}`)
  } catch {
    ;(window as any).toast?.('error', 'Failed to submit revision. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  try {
    await submissionStore.fetchSubmission(submissionId)

    if (submission.value?.status !== 'revision_required') {
      ;(window as any).toast?.('warning', 'This submission is not awaiting a revision.')
      router.push(`/submissions/${submissionId}`)
      return
    }

    revisionResponse.value = submission.value.revision_response || ''
    await fetchFiles()
  } catch {
    error.value = 'Failed to load submission'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <router-link to="/dashboard" class="flex items-center gap-2">
            <img src="/logo-icon.png" alt="TruEditor" class="brand-logo brand-logo--header-sm brand-logo--on-light" />
            <span class="text-lg font-semibold text-gray-900">Tru<span class="text-primary-400">Editor</span></span>
          </router-link>
          <nav class="hidden md:flex items-center gap-6">
            <router-link to="/dashboard" class="text-sm text-gray-600 hover:text-primary-600 transition-colors">Dashboard</router-link>
            <router-link to="/submissions" class="text-sm text-gray-600 hover:text-primary-600 transition-colors">Submissions</router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="isLoading" class="max-w-5xl mx-auto px-4 py-16">
      <div class="animate-pulse space-y-6">
        <div class="h-8 bg-gray-200 rounded w-1/3"></div>
        <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        <div class="h-64 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="max-w-5xl mx-auto px-4 py-16 text-center">
      <p class="text-red-600 text-lg">{{ error }}</p>
      <button @click="router.push('/submissions')" class="mt-4 text-primary-600 hover:underline">Back to Submissions</button>
    </div>

    <!-- Main Content -->
    <div v-else-if="submission" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Back Link -->
      <button
        @click="router.push(`/submissions/${submissionId}`)"
        class="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 mb-6 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        Back to Submission Detail
      </button>

      <!-- Title -->
      <div class="mb-8">
        <div class="flex flex-wrap items-center gap-3 mb-2">
          <h1 class="text-2xl font-bold text-gray-900">Submit Revision</h1>
          <span class="text-sm font-mono text-gray-400">{{ submission.manuscript_id }}</span>
          <span v-if="statusInfo" :class="[statusInfo.bgColor, statusInfo.color]" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
            Revision #{{ submission.revision_number }}
          </span>
        </div>
        <p class="text-gray-600">{{ submission.title || 'Untitled Manuscript' }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Content -->
        <div class="lg:col-span-2 space-y-8">

          <!-- Editor Notes Card -->
          <div class="bg-white rounded-xl shadow-sm border border-orange-200 overflow-hidden">
            <div class="bg-orange-50 px-6 py-4 border-b border-orange-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                <h2 class="text-lg font-semibold text-orange-800">Editor's Revision Request</h2>
              </div>
            </div>
            <div class="px-6 py-5">
              <p class="text-gray-700 whitespace-pre-line leading-relaxed">{{ submission.revision_notes || 'No specific notes provided.' }}</p>
              <div v-if="submission.revision_deadline" class="mt-4 flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                <span class="text-gray-500">Deadline: <strong class="text-gray-700">{{ formatDate(submission.revision_deadline) }}</strong></span>
                <span v-if="daysLeft !== null" :class="daysLeft <= 3 ? 'text-red-600 font-semibold' : daysLeft <= 7 ? 'text-orange-600' : 'text-green-600'">
                  ({{ daysLeft > 0 ? `${daysLeft} days left` : 'Overdue' }})
                </span>
              </div>
            </div>
          </div>

          <!-- Response to Reviewers -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Response to Reviewers</h2>
              <p class="text-sm text-gray-500 mt-1">Explain how you addressed each reviewer comment. Be specific and reference the changes you made.</p>
            </div>
            <div class="p-6">
              <textarea
                v-model="revisionResponse"
                rows="10"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-y"
                placeholder="Dear Editor and Reviewers,&#10;&#10;Thank you for the constructive feedback. Below I address each point raised:&#10;&#10;Reviewer 1, Comment 1: ...&#10;Our response: ...&#10;&#10;Reviewer 2, Comment 1: ...&#10;Our response: ..."
              ></textarea>
              <p class="mt-2 text-xs text-gray-400">
                Minimum 20 characters required. {{ revisionResponse.length }} characters entered.
              </p>
            </div>
          </div>

          <!-- File Upload -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Upload Revised Files</h2>
              <p class="text-sm text-gray-500 mt-1">Upload your revised manuscript and any supporting documents.</p>
            </div>
            <div class="p-6">
              <!-- File Type Selector -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">File Type</label>
                <select v-model="selectedFileType" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                  <option v-for="ft in revisionFileTypes" :key="ft.key" :value="ft.key">{{ ft.label }}</option>
                </select>
              </div>

              <!-- Drop Zone -->
              <div
                class="border-2 border-dashed rounded-xl p-8 text-center transition-colors"
                :class="isDragging ? 'border-primary-400 bg-primary-50' : 'border-gray-300 hover:border-primary-300'"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
              >
                <input type="file" multiple accept=".doc,.docx,.pdf,.jpg,.jpeg,.png,.tiff,.tif,.xlsx,.xls" class="hidden" id="revisionFileInput" @change="handleFileInput" />
                <label for="revisionFileInput" class="cursor-pointer">
                  <div class="flex flex-col items-center">
                    <div class="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center mb-3">
                      <svg class="w-7 h-7 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
                    </div>
                    <p class="text-sm font-medium text-gray-700 mb-1">Drop files here or <span class="text-primary-600">browse</span></p>
                    <p class="text-xs text-gray-500">DOC, DOCX, PDF, JPG, PNG, TIFF, XLS, XLSX (Max 50MB)</p>
                  </div>
                </label>
              </div>

              <!-- Loading -->
              <div v-if="isLoadingFiles" class="mt-4 flex items-center justify-center gap-2 py-4">
                <div class="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                <span class="text-sm text-gray-500">Loading files...</span>
              </div>

              <!-- Current Revision Files -->
              <div v-if="allDisplayFiles.length > 0" class="mt-6">
                <h4 class="text-sm font-medium text-gray-700 mb-3">Revision #{{ submission.revision_number }} Files</h4>
                <div class="space-y-2">
                  <div
                    v-for="file in allDisplayFiles"
                    :key="file.id"
                    class="flex items-center justify-between px-4 py-3 rounded-lg border border-gray-200 bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <div class="flex items-center gap-3 min-w-0 flex-1">
                      <svg class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                      <div class="min-w-0">
                        <p class="text-sm font-medium text-gray-800 truncate">{{ file.name }}</p>
                        <div class="flex items-center gap-2 mt-0.5">
                          <span :class="getTypeColor(file.fileType)" class="text-xs px-1.5 py-0.5 rounded font-medium">{{ getTypeLabel(file.fileType) }}</span>
                          <span class="text-xs text-gray-400">{{ formatFileSize(file.size) }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Upload progress -->
                    <div v-if="file.status === 'uploading'" class="flex items-center gap-2">
                      <div class="w-20 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div class="h-full bg-primary-500 rounded-full transition-all" :style="{ width: file.progress + '%' }"></div>
                      </div>
                      <span class="text-xs text-gray-500">{{ file.progress }}%</span>
                    </div>

                    <!-- Error -->
                    <div v-else-if="file.status === 'error'" class="flex items-center gap-2">
                      <span class="text-xs text-red-500">{{ file.errorMessage }}</span>
                      <button @click="handleRemoveFile(file.id, file.status)" class="text-gray-400 hover:text-red-500">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                      </button>
                    </div>

                    <!-- Server file actions -->
                    <div v-else class="flex items-center gap-1">
                      <button @click="handleDownload(file.id, file.name)" class="p-1.5 text-gray-400 hover:text-primary-600 rounded" title="Download">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                      </button>
                      <button @click="handleRemoveFile(file.id, file.status)" class="p-1.5 text-gray-400 hover:text-red-500 rounded" title="Remove">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Previous Revision Files (read-only) -->
          <div v-if="previousFiles.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100">
              <h2 class="text-lg font-semibold text-gray-900">Previous Files</h2>
              <p class="text-sm text-gray-500 mt-1">Files from earlier revisions (read-only)</p>
            </div>
            <div class="p-6 space-y-2">
              <div
                v-for="file in previousFiles"
                :key="file.id"
                class="flex items-center justify-between px-4 py-3 rounded-lg border border-gray-100 bg-gray-50/50"
              >
                <div class="flex items-center gap-3 min-w-0 flex-1">
                  <svg class="w-5 h-5 text-gray-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                  <div class="min-w-0">
                    <p class="text-sm text-gray-600 truncate">{{ file.original_filename }}</p>
                    <div class="flex items-center gap-2 mt-0.5">
                      <span class="text-xs text-gray-400">Rev #{{ file.revision_number }}</span>
                      <span class="text-xs text-gray-400">{{ formatFileSize(file.file_size) }}</span>
                    </div>
                  </div>
                </div>
                <button @click="handleDownload(file.id, file.original_filename)" class="p-1.5 text-gray-400 hover:text-primary-600 rounded" title="Download">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- Right Sidebar -->
        <div class="space-y-6">

          <!-- Submit Action Card -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100">
              <h3 class="text-sm font-semibold text-gray-900">Actions</h3>
            </div>
            <div class="p-6 space-y-3">
              <button
                @click="showSubmitConfirm = true"
                :disabled="!canSubmit || isSubmitting"
                class="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-primary-600 text-white text-sm font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg v-if="isSubmitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>
                {{ isSubmitting ? 'Submitting...' : 'Submit Revision' }}
              </button>

              <button
                @click="router.push(`/submissions/${submissionId}`)"
                class="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
            </div>

            <!-- Checklist -->
            <div class="px-6 pb-6">
              <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Checklist</h4>
              <div class="space-y-2">
                <div class="flex items-center gap-2 text-sm">
                  <div :class="revisionResponse.trim().length > 20 ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'" class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <span :class="revisionResponse.trim().length > 20 ? 'text-gray-700' : 'text-gray-400'">Response to reviewers</span>
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <div :class="revisionFiles.length > 0 ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'" class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <span :class="revisionFiles.length > 0 ? 'text-gray-700' : 'text-gray-400'">Revised files uploaded</span>
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <div :class="!isUploading ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'" class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                  </div>
                  <span :class="!isUploading ? 'text-gray-700' : 'text-yellow-600'">{{ isUploading ? 'Uploads in progress...' : 'All uploads complete' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Revision Info -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100">
              <h3 class="text-sm font-semibold text-gray-900">Revision Info</h3>
            </div>
            <div class="px-6 py-4 space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Revision</span>
                <span class="font-medium text-gray-800">#{{ submission.revision_number }}</span>
              </div>
              <div v-if="submission.revision_deadline" class="flex justify-between">
                <span class="text-gray-500">Deadline</span>
                <span class="font-medium" :class="daysLeft !== null && daysLeft <= 3 ? 'text-red-600' : 'text-gray-800'">{{ formatDate(submission.revision_deadline) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Files (this revision)</span>
                <span class="font-medium text-gray-800">{{ revisionFiles.length }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Previous files</span>
                <span class="font-medium text-gray-800">{{ previousFiles.length }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Submit Confirmation Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showSubmitConfirm" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40" @click="showSubmitConfirm = false"></div>
          <div class="relative bg-white rounded-2xl shadow-xl max-w-md w-full p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Submit Revision?</h3>
            <p class="text-sm text-gray-600 mb-6">
              You are about to submit <strong>Revision #{{ submission?.revision_number }}</strong> with
              <strong>{{ revisionFiles.length }}</strong> file(s). This action cannot be undone.
            </p>
            <div class="flex gap-3">
              <button
                @click="showSubmitConfirm = false"
                class="flex-1 px-4 py-2.5 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                @click="handleSubmitRevision"
                :disabled="isSubmitting"
                class="flex-1 px-4 py-2.5 bg-primary-600 text-white text-sm font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
              >
                {{ isSubmitting ? 'Submitting...' : 'Confirm & Submit' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
