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
const saveError = ref<string | null>(null)

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

// Auto-save timer
let autosaveTimer: ReturnType<typeof setInterval> | null = null

const steps = [
  { id: 1, title: 'Article Type' },
  { id: 2, title: 'Files' },
  { id: 3, title: 'Article Info' },
  { id: 4, title: 'Authors' },
  { id: 5, title: 'Additional' },
  { id: 6, title: 'Review' },
]

// ============================================
// COMPUTED
// ============================================

const progressPercentage = computed(() => ((currentStep.value - 1) / (totalSteps - 1)) * 100)

const submissionId = computed(() => submissionStore.currentSubmission?.id)

const canGoNext = computed(() => {
  switch (currentStep.value) {
    case 1: return !!articleType.value
    case 2: return true // Files optional for draft
    case 3: return title.value.trim().length > 0 && abstract.value.trim().length > 0 && keywords.value.length >= 3
    case 4: return authors.value.length > 0 && authors.value.some(a => a.is_corresponding)
    case 5: return true
    case 6: return true
    default: return false
  }
})

const isDirty = computed(() => {
  return articleType.value !== undefined || title.value !== '' || abstract.value !== '' || authors.value.length > 0
})

// ============================================
// DRAFT MANAGEMENT
// ============================================

/**
 * Ensure a draft submission exists.
 * Returns true if draft exists (or was created), false if creation failed.
 */
async function ensureDraftExists(): Promise<boolean> {
  if (submissionStore.currentSubmission) return true

  try {
    await submissionStore.createSubmission({
      title: title.value || 'Untitled',
      article_type: articleType.value,
      wizard_step: currentStep.value,
      wizard_data: getWizardData(),
    })
    lastSavedAt.value = new Date().toISOString()
    saveError.value = null
    return true
  } catch (err: any) {
    console.error('Failed to create draft:', err)
    saveError.value = err.response?.data?.error?.message || 'Could not save draft. Please check your connection.'
    return false
  }
}

// ============================================
// FILE MANAGEMENT
// ============================================

async function fetchSubmissionFiles(): Promise<void> {
  const sid = submissionStore.currentSubmission?.id
  if (!sid) return
  try {
    const response = await api.get(`/files/?submission_id=${sid}`)
    uploadedFiles.value = response.data.data || []
  } catch {
    // Non-blocking
  }
}

function onFilesChanged(files: ManuscriptFile[]): void {
  uploadedFiles.value = files
}

// ============================================
// NAVIGATION
// ============================================

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

async function goNext(): Promise<void> {
  if (currentStep.value >= totalSteps || !canGoNext.value) return

  // Create draft before file upload step
  if (currentStep.value === 1 && !submissionStore.currentSubmission) {
    const created = await ensureDraftExists()
    if (!created) {
      // Show error but still advance - file upload shows appropriate message per file
      ;(window as any).toast?.('error', saveError.value || 'Could not save draft. You can still continue.')
    }
  }

  currentStep.value++

  // Fetch files when entering review step
  if (currentStep.value === 6) {
    await fetchSubmissionFiles()
  }

  // Save progress in background (don't block navigation)
  saveProgressQuiet()
}

function goToStep(step: number): void {
  if (step <= currentStep.value || step === currentStep.value + 1) {
    currentStep.value = step
    if (step === 6) {
      fetchSubmissionFiles()
    }
  }
}

// ============================================
// SAVE / AUTO-SAVE
// ============================================

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
 * Save progress (shows saving indicator)
 */
async function saveProgress(): Promise<void> {
  if (isSaving.value) return
  isSaving.value = true
  saveError.value = null

  try {
    if (!submissionStore.currentSubmission) {
      await submissionStore.createSubmission({
        title: title.value || 'Untitled',
        article_type: articleType.value,
        wizard_step: currentStep.value,
        wizard_data: getWizardData(),
      })
    } else {
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
    saveError.value = null
  } catch (error: any) {
    console.error('Save failed:', error)
    saveError.value = 'Save failed'
  } finally {
    isSaving.value = false
  }
}

/**
 * Save progress quietly (no UI indicator, for background saves)
 */
async function saveProgressQuiet(): Promise<void> {
  try {
    if (!submissionStore.currentSubmission) {
      await submissionStore.createSubmission({
        title: title.value || 'Untitled',
        article_type: articleType.value,
        wizard_step: currentStep.value,
        wizard_data: getWizardData(),
      })
    } else {
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
  } catch {
    // Silent
  }
}

// ============================================
// SUBMIT
// ============================================

async function handleSubmit(): Promise<void> {
  try {
    if (!submissionStore.currentSubmission) {
      await saveProgress()
    }

    if (!submissionStore.currentSubmission) {
      ;(window as any).toast?.('error', 'Could not create submission. Please try again.')
      return
    }

    const sid = submissionStore.currentSubmission.id

    // Save all submission fields first
    await saveProgress()

    // Delete existing server-side authors (handles re-submit / retry gracefully)
    const existingAuthors = submissionStore.currentSubmission?.authors || []
    for (const existing of existingAuthors) {
      try {
        await submissionStore.removeAuthor(sid, existing.id)
      } catch {
        // Continue even if individual deletion fails
      }
    }

    // Add authors from wizard with clean data (no user field, explicit order)
    for (let i = 0; i < authors.value.length; i++) {
      const a = authors.value[i]
      if (!a) continue
      await submissionStore.addAuthor(sid, {
        given_name: a.given_name,
        family_name: a.family_name,
        email: a.email,
        institution: a.institution,
        orcid_id: a.orcid_id || '',
        department: a.department || '',
        country: a.country || '',
        city: a.city || '',
        order: i + 1,
        is_corresponding: a.is_corresponding || false,
        contribution: a.contribution || '',
      })
    }

    await submissionStore.submitForReview(sid)

    ;(window as any).toast?.('success', 'Manuscript submitted successfully!')
    router.push('/dashboard')
  } catch (error: any) {
    const msg = error.response?.data?.error?.message || error.message || 'Submission failed'
    ;(window as any).toast?.('error', msg)
  }
}

// ============================================
// UTILITY
// ============================================

function formatLastSaved(): string {
  if (!lastSavedAt.value) return ''
  return new Date(lastSavedAt.value).toLocaleTimeString()
}

// ============================================
// LIFECYCLE
// ============================================

onMounted(() => {
  autosaveTimer = setInterval(() => {
    if (isDirty.value && submissionStore.currentSubmission) {
      saveProgressQuiet()
    }
  }, 30000)
})

onBeforeUnmount(() => {
  if (autosaveTimer) clearInterval(autosaveTimer)
})

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
    <!-- Header (no transitions, fixed position) -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="goBack" class="flex items-center gap-2 text-gray-600 hover:text-gray-900">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <h1 class="text-lg font-semibold text-gray-800">New Manuscript Submission</h1>
          <div class="flex items-center gap-2 text-sm text-gray-500 min-w-[100px] justify-end">
            <template v-if="isSaving">
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              <span>Saving...</span>
            </template>
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
        <div class="h-1 bg-gray-100 rounded-full overflow-hidden">
          <div
            class="h-full bg-primary-500"
            :style="{ width: `${progressPercentage}%`, transition: 'width 0.3s ease' }"
          />
        </div>

        <div class="py-4 flex items-center justify-between">
          <button
            v-for="step in steps"
            :key="step.id"
            @click="goToStep(step.id)"
            :disabled="step.id > currentStep + 1"
            class="flex flex-col items-center gap-1 group"
            :class="{ 'cursor-not-allowed opacity-50': step.id > currentStep + 1 }"
          >
            <div
              class="flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium"
              :class="[
                step.id < currentStep ? 'bg-accent-500 text-white' :
                step.id === currentStep ? 'bg-primary-500 text-white ring-4 ring-primary-100' :
                'bg-gray-100 text-gray-400'
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

    <!-- Step Content (NO transition wrapper - prevents layout shifts) -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8">
        <StepArticleType
          v-if="currentStep === 1"
          v-model="articleType"
        />

        <StepFileUpload
          v-else-if="currentStep === 2"
          :submissionId="submissionId"
          @filesChanged="onFilesChanged"
        />

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

        <StepAuthors
          v-else-if="currentStep === 4"
          v-model:authors="authors"
        />

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
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between mt-6">
        <button
          @click="goBack"
          class="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50"
        >
          {{ currentStep === 1 ? 'Cancel' : 'Previous' }}
        </button>

        <button
          v-if="currentStep < totalSteps"
          @click="goNext"
          :disabled="!canGoNext"
          class="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </main>
  </div>
</template>
