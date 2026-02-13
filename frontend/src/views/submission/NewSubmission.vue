<script setup lang="ts">
/**
 * TruEditor - New Submission Wizard
 * ==================================
 * 6-step manuscript submission wizard.
 * Integrates all wizard step components with auto-save.
 */

import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import { useSubmissionStore } from '@/stores/submission'
import StepArticleType from '@/components/submission/wizard/StepArticleType.vue'
import StepFileUpload from '@/components/submission/wizard/StepFileUpload.vue'
import StepArticleInfo from '@/components/submission/wizard/StepArticleInfo.vue'
import StepAuthors from '@/components/submission/wizard/StepAuthors.vue'
import StepAdditionalInfo from '@/components/submission/wizard/StepAdditionalInfo.vue'
import StepReviewSubmit from '@/components/submission/wizard/StepReviewSubmit.vue'
import { api } from '@/services/api'
import type { ArticleType, Language, AuthorInput, ManuscriptFile, SuggestedReviewer, OpposedReviewer } from '@/types/submission'

const router = useRouter()
const submissionStore = useSubmissionStore()

// Wizard state
const currentStep = ref(1)
const totalSteps = 6
const isSaving = ref(false)
const lastSavedAt = ref<string | null>(null)

// Form data
const articleType = ref<ArticleType | undefined>(undefined)
const title = ref('')
const titleEn = ref('')
const abstract = ref('')
const abstractEn = ref('')
const keywords = ref<string[]>([])
const keywordsEn = ref<string[]>([])
const language = ref<Language>('en')
const authors = ref<AuthorInput[]>([])
const coverLetter = ref('')
const ethicsStatement = ref('')
const ethicsApprovalNumber = ref('')
const conflictOfInterest = ref('')
const fundingStatement = ref('')
const suggestedReviewers = ref<SuggestedReviewer[]>([])
const opposedReviewers = ref<OpposedReviewer[]>([])
const editorComments = ref('')

// Uploaded files (tracked at parent level so they persist across steps)
const uploadedFiles = ref<ManuscriptFile[]>([])

/**
 * Fetch files from server for the current submission
 */
async function fetchSubmissionFiles(): Promise<void> {
  const sid = submissionStore.currentSubmission?.id
  if (!sid) return
  
  try {
    const response = await api.get(`/files/?submission_id=${sid}`)
    uploadedFiles.value = response.data.data || []
  } catch (err) {
    console.error('Failed to fetch files:', err)
  }
}

/**
 * Handle files changed from StepFileUpload
 */
function onFilesChanged(files: ManuscriptFile[]): void {
  uploadedFiles.value = files
}

// Auto-save timer
let autosaveTimer: ReturnType<typeof setInterval> | null = null

const steps = [
  { id: 1, title: 'Article Type', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
  { id: 2, title: 'Files', icon: 'M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12' },
  { id: 3, title: 'Article Info', icon: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z' },
  { id: 4, title: 'Authors', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
  { id: 5, title: 'Additional', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
  { id: 6, title: 'Review', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
]

// Computed
const progressPercentage = computed(() => ((currentStep.value - 1) / (totalSteps - 1)) * 100)

/**
 * Ensure a draft submission exists (needed before file upload)
 */
async function ensureDraftExists(): Promise<void> {
  if (submissionStore.currentSubmission) return
  
  await submissionStore.createSubmission({
    title: title.value || 'Untitled',
    article_type: articleType.value,
    wizard_step: currentStep.value,
    wizard_data: getWizardData(),
  })
  lastSavedAt.value = new Date().toISOString()
}

const submissionId = computed(() => submissionStore.currentSubmission?.id)

const canGoNext = computed(() => {
  switch (currentStep.value) {
    case 1:
      return !!articleType.value
    case 2:
      return true // Files are optional for draft
    case 3:
      return title.value.trim().length > 0 && 
             abstract.value.trim().length > 0 && 
             keywords.value.length >= 3
    case 4:
      return authors.value.length > 0 && authors.value.some(a => a.is_corresponding)
    case 5:
      return true // Additional info is optional
    case 6:
      return true
    default:
      return false
  }
})

const isDirty = computed(() => {
  return articleType.value !== undefined ||
         title.value !== '' ||
         abstract.value !== '' ||
         authors.value.length > 0
})

/**
 * Go to previous step
 */
function goBack(): void {
  if (currentStep.value > 1) {
    currentStep.value--
  } else {
    if (isDirty.value) {
      if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
        router.push('/dashboard')
      }
    } else {
      router.push('/dashboard')
    }
  }
}

/**
 * Go to next step
 */
async function goNext(): Promise<void> {
  if (currentStep.value < totalSteps && canGoNext.value) {
    // Auto-create draft when moving to file upload step
    if (currentStep.value === 1) {
      await ensureDraftExists()
    }
    currentStep.value++
    // Fetch files from server when entering review step
    if (currentStep.value === 6) {
      await fetchSubmissionFiles()
    }
    saveProgress()
  }
}

/**
 * Go to specific step
 */
function goToStep(step: number): void {
  if (step <= currentStep.value || step === currentStep.value + 1) {
    currentStep.value = step
    // Fetch files from server when entering review step
    if (step === 6) {
      fetchSubmissionFiles()
    }
  }
}

/**
 * Save progress (auto-save)
 */
async function saveProgress(): Promise<void> {
  if (isSaving.value) return
  
  isSaving.value = true
  
  try {
    // If no submission exists, create one
    if (!submissionStore.currentSubmission) {
      await submissionStore.createSubmission({
        title: title.value || 'Untitled',
        article_type: articleType.value,
        wizard_step: currentStep.value,
        wizard_data: getWizardData(),
      })
    } else {
      // Update existing
      await submissionStore.updateSubmission(submissionStore.currentSubmission.id, {
        title: title.value,
        title_en: titleEn.value,
        abstract: abstract.value,
        abstract_en: abstractEn.value,
        keywords: keywords.value,
        keywords_en: keywordsEn.value,
        article_type: articleType.value,
        language: language.value,
        cover_letter: coverLetter.value,
        ethics_statement: ethicsStatement.value,
        ethics_approval_number: ethicsApprovalNumber.value,
        conflict_of_interest: conflictOfInterest.value,
        funding_statement: fundingStatement.value,
        wizard_step: currentStep.value,
        wizard_data: getWizardData(),
      })
    }
    
    lastSavedAt.value = new Date().toISOString()
  } catch (error) {
    console.error('Auto-save failed:', error)
  } finally {
    isSaving.value = false
  }
}

/**
 * Get wizard data object
 */
function getWizardData() {
  return {
    article_type: articleType.value,
    title: title.value,
    title_en: titleEn.value,
    abstract: abstract.value,
    abstract_en: abstractEn.value,
    keywords: keywords.value,
    keywords_en: keywordsEn.value,
    authors: authors.value,
    cover_letter: coverLetter.value,
    ethics_statement: ethicsStatement.value,
    ethics_approval_number: ethicsApprovalNumber.value,
    conflict_of_interest: conflictOfInterest.value,
    funding_statement: fundingStatement.value,
    suggested_reviewers: suggestedReviewers.value,
    opposed_reviewers: opposedReviewers.value,
    editor_comments: editorComments.value,
    last_saved_at: new Date().toISOString(),
  }
}

/**
 * Handle final submission
 */
async function handleSubmit(): Promise<void> {
  try {
    // Ensure submission exists
    if (!submissionStore.currentSubmission) {
      await saveProgress()
    }
    
    // Double check after save
    if (!submissionStore.currentSubmission) {
      ;(window as any).toast?.('error', 'Could not create submission. Please try again.')
      return
    }
    
    const sid = submissionStore.currentSubmission.id
    
    // Save all data first
    await saveProgress()
    
    // Add authors to submission
    for (const author of authors.value) {
      await submissionStore.addAuthor(sid, author)
    }
    
    // Submit for review
    await submissionStore.submitForReview(sid)
    
    // Show success and redirect
    ;(window as any).toast?.('success', 'Manuscript submitted successfully!')
    router.push('/dashboard')
  } catch (error: any) {
    ;(window as any).toast?.('error', error.message || 'Submission failed')
  }
}

/**
 * Format last saved time
 */
function formatLastSaved(): string {
  if (!lastSavedAt.value) return ''
  const date = new Date(lastSavedAt.value)
  return date.toLocaleTimeString()
}

// Lifecycle
onMounted(() => {
  // Start auto-save timer (every 30 seconds)
  autosaveTimer = setInterval(() => {
    if (isDirty.value) {
      saveProgress()
    }
  }, 30000)
})

onBeforeUnmount(() => {
  if (autosaveTimer) {
    clearInterval(autosaveTimer)
  }
})

// Route guard for unsaved changes
onBeforeRouteLeave((_to, _from, next) => {
  if (isDirty.value && !submissionStore.currentSubmission) {
    if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
      next()
    } else {
      next(false)
    }
  } else {
    next()
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="goBack" class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <h1 class="text-lg font-semibold text-gray-800">New Manuscript Submission</h1>
          <div class="flex items-center gap-2 text-sm text-gray-500">
            <span v-if="isSaving" class="flex items-center gap-1">
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Saving...
            </span>
            <span v-else-if="lastSavedAt" class="text-green-600">
              Saved {{ formatLastSaved() }}
            </span>
          </div>
        </div>
      </div>
    </header>

    <!-- Progress Bar -->
    <div class="bg-white border-b">
      <div class="max-w-4xl mx-auto px-6">
        <!-- Progress Line -->
        <div class="h-1 bg-gray-100 rounded-full overflow-hidden">
          <div 
            class="h-full bg-primary-500 transition-all duration-500 ease-out"
            :style="{ width: `${progressPercentage}%` }"
          />
        </div>
        
        <!-- Step Indicators -->
        <div class="py-4 flex items-center justify-between">
          <button
            v-for="step in steps"
            :key="step.id"
            @click="goToStep(step.id)"
            :disabled="step.id > currentStep + 1"
            class="flex flex-col items-center gap-1 group"
            :class="{ 'cursor-not-allowed': step.id > currentStep + 1 }"
          >
            <div 
              class="flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium transition-all"
              :class="[
                step.id < currentStep ? 'bg-accent-500 text-white' : 
                step.id === currentStep ? 'bg-primary-500 text-white ring-4 ring-primary-100' : 
                'bg-gray-100 text-gray-400 group-hover:bg-gray-200'
              ]"
            >
              <svg v-if="step.id < currentStep" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>{{ step.id }}</span>
            </div>
            <span 
              class="text-xs font-medium hidden sm:block"
              :class="step.id <= currentStep ? 'text-gray-800' : 'text-gray-400'"
            >
              {{ step.title }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Step Content -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">
        <!-- Step 1: Article Type -->
        <Transition name="fade" mode="out-in">
          <StepArticleType 
            v-if="currentStep === 1"
            v-model="articleType"
          />
          
          <!-- Step 2: File Upload -->
          <StepFileUpload 
            v-else-if="currentStep === 2"
            :submissionId="submissionId"
            @filesChanged="onFilesChanged"
          />
          
          <!-- Step 3: Article Info -->
          <StepArticleInfo 
            v-else-if="currentStep === 3"
            v-model:title="title"
            v-model:titleEn="titleEn"
            v-model:abstract="abstract"
            v-model:abstractEn="abstractEn"
            v-model:keywords="keywords"
            v-model:keywordsEn="keywordsEn"
            v-model:language="language"
          />
          
          <!-- Step 4: Authors -->
          <StepAuthors 
            v-else-if="currentStep === 4"
            v-model:authors="authors"
          />
          
          <!-- Step 5: Additional Info -->
          <StepAdditionalInfo 
            v-else-if="currentStep === 5"
            v-model:coverLetter="coverLetter"
            v-model:ethicsStatement="ethicsStatement"
            v-model:ethicsApprovalNumber="ethicsApprovalNumber"
            v-model:conflictOfInterest="conflictOfInterest"
            v-model:fundingStatement="fundingStatement"
            v-model:suggestedReviewers="suggestedReviewers"
            v-model:opposedReviewers="opposedReviewers"
            v-model:editorComments="editorComments"
          />
          
          <!-- Step 6: Review & Submit -->
          <StepReviewSubmit 
            v-else-if="currentStep === 6"
            :articleType="articleType"
            :title="title"
            :abstract="abstract"
            :keywords="keywords"
            :authors="authors"
            :files="uploadedFiles"
            :coverLetter="coverLetter"
            :ethicsStatement="ethicsStatement"
            :conflictOfInterest="conflictOfInterest"
            :fundingStatement="fundingStatement"
            @submit="handleSubmit"
            @goToStep="goToStep"
          />
        </Transition>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-6">
        <button 
          @click="goBack"
          class="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          {{ currentStep === 1 ? 'Cancel' : 'Previous' }}
        </button>
        
        <button 
          v-if="currentStep < totalSteps"
          @click="goNext"
          :disabled="!canGoNext"
          class="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
        >
          Next
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
