<script setup lang="ts">
/**
 * TruEditor - Wizard Step 6: Review & Submit
 * ============================================
 * Final review of all submission data before submitting.
 */

import { ref, computed } from 'vue'
import { ARTICLE_TYPES, type ArticleType, type AuthorInput, type ManuscriptFile } from '@/types/submission'

interface Props {
  /** Article type */
  articleType?: ArticleType
  /** Title */
  title?: string
  /** Abstract */
  abstract?: string
  /** Keywords */
  keywords?: string[]
  /** Authors */
  authors?: AuthorInput[]
  /** Files (for display) */
  files?: ManuscriptFile[]
  /** Cover letter */
  coverLetter?: string
  /** Ethics statement */
  ethicsStatement?: string
  /** Conflict of interest */
  conflictOfInterest?: string
  /** Funding statement */
  fundingStatement?: string
  /** Is submission valid */
  isValid?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  articleType: 'research',
  title: '',
  abstract: '',
  keywords: () => [],
  authors: () => [],
  files: () => [],
  coverLetter: '',
  ethicsStatement: '',
  conflictOfInterest: '',
  fundingStatement: '',
  isValid: false,
})

const emit = defineEmits<{
  submit: []
  goToStep: [step: number]
}>()

const confirmed = ref(false)
const isSubmitting = ref(false)

// Computed
const correspondingAuthor = computed(() => 
  props.authors.find(a => a.is_corresponding)
)

const hasRequiredFields = computed(() => {
  return props.articleType && 
         props.title && 
         props.abstract && 
         props.keywords.length >= 3 &&
         props.authors.length > 0 &&
         props.authors.some(a => a.is_corresponding)
})

/**
 * Handle submit
 */
async function handleSubmit(): Promise<void> {
  if (!confirmed.value || !hasRequiredFields.value) return
  
  isSubmitting.value = true
  emit('submit')
}

/**
 * Truncate text
 */
function truncate(text: string, length: number): string {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}
</script>

<template>
  <div class="step-review-submit">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Review & Submit</h3>
      <p class="mt-1 text-sm text-gray-500">
        Please review your submission details before submitting.
      </p>
    </div>

    <!-- Summary Cards -->
    <div class="space-y-4">
      <!-- Article Type Card -->
      <div class="review-card">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900">Article Type</h4>
          <button
            @click="emit('goToStep', 1)"
            class="text-sm text-primary-600 hover:text-primary-700"
          >
            Edit
          </button>
        </div>
        <p class="text-gray-700">{{ ARTICLE_TYPES[articleType]?.label || articleType }}</p>
      </div>

      <!-- Manuscript Info Card -->
      <div class="review-card">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900">Manuscript Information</h4>
          <button
            @click="emit('goToStep', 3)"
            class="text-sm text-primary-600 hover:text-primary-700"
          >
            Edit
          </button>
        </div>
        
        <div class="space-y-3">
          <div>
            <span class="text-sm text-gray-500">Title</span>
            <p class="text-gray-900 font-medium">{{ title || 'Not provided' }}</p>
          </div>
          
          <div>
            <span class="text-sm text-gray-500">Abstract</span>
            <p class="text-gray-700 text-sm">{{ truncate(abstract, 300) || 'Not provided' }}</p>
          </div>
          
          <div>
            <span class="text-sm text-gray-500">Keywords</span>
            <div class="flex flex-wrap gap-1 mt-1">
              <span
                v-for="keyword in keywords"
                :key="keyword"
                class="px-2 py-0.5 bg-gray-100 text-gray-700 text-sm rounded-full"
              >
                {{ keyword }}
              </span>
              <span v-if="keywords.length === 0" class="text-gray-400 text-sm">Not provided</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Files Card -->
      <div class="review-card">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900">Files</h4>
          <button
            @click="emit('goToStep', 2)"
            class="text-sm text-primary-600 hover:text-primary-700"
          >
            Edit
          </button>
        </div>
        
        <div v-if="files.length > 0" class="space-y-2">
          <div
            v-for="file in files"
            :key="file.id"
            class="flex items-center gap-3 p-2 bg-gray-50 rounded-lg"
          >
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ file.original_filename }}</p>
              <p class="text-xs text-gray-500">{{ file.file_type_display }} - {{ file.file_size_human }}</p>
            </div>
          </div>
        </div>
        <p v-else class="text-gray-400 text-sm">No files uploaded</p>
      </div>

      <!-- Authors Card -->
      <div class="review-card">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900">Authors ({{ authors.length }})</h4>
          <button
            @click="emit('goToStep', 4)"
            class="text-sm text-primary-600 hover:text-primary-700"
          >
            Edit
          </button>
        </div>
        
        <div v-if="authors.length > 0" class="space-y-2">
          <div
            v-for="(author, index) in authors"
            :key="index"
            class="flex items-center gap-3"
          >
            <span class="w-6 h-6 flex items-center justify-center bg-gray-100 text-gray-600 rounded-full text-xs font-medium">
              {{ index + 1 }}
            </span>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">
                {{ author.given_name }} {{ author.family_name }}
                <span v-if="author.is_corresponding" class="ml-1 text-xs text-accent-600">(Corresponding)</span>
              </p>
              <p class="text-xs text-gray-500">{{ author.institution }}</p>
            </div>
          </div>
        </div>
        <p v-else class="text-gray-400 text-sm">No authors added</p>
      </div>

      <!-- Additional Info Card -->
      <div class="review-card">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-medium text-gray-900">Additional Information</h4>
          <button
            @click="emit('goToStep', 5)"
            class="text-sm text-primary-600 hover:text-primary-700"
          >
            Edit
          </button>
        </div>
        
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-500">Cover Letter</span>
            <p class="text-gray-700">{{ coverLetter ? 'Provided' : 'Not provided' }}</p>
          </div>
          <div>
            <span class="text-gray-500">Ethics Statement</span>
            <p class="text-gray-700">{{ ethicsStatement ? 'Provided' : 'Not provided' }}</p>
          </div>
          <div>
            <span class="text-gray-500">Conflict of Interest</span>
            <p class="text-gray-700">{{ conflictOfInterest ? 'Declared' : 'Not declared' }}</p>
          </div>
          <div>
            <span class="text-gray-500">Funding</span>
            <p class="text-gray-700">{{ fundingStatement ? 'Provided' : 'Not provided' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Validation Summary -->
    <div v-if="!hasRequiredFields" class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl">
      <div class="flex gap-3">
        <svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h5 class="font-medium text-amber-800">Missing required information</h5>
          <ul class="mt-2 text-sm text-amber-700 space-y-1">
            <li v-if="!title">- Title is required</li>
            <li v-if="!abstract">- Abstract is required</li>
            <li v-if="keywords.length < 3">- At least 3 keywords are required</li>
            <li v-if="authors.length === 0">- At least one author is required</li>
            <li v-if="!correspondingAuthor">- A corresponding author must be designated</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Confirmation -->
    <div class="mt-6 p-4 bg-gray-50 rounded-xl">
      <label class="flex items-start gap-3 cursor-pointer">
        <input
          v-model="confirmed"
          type="checkbox"
          :disabled="!hasRequiredFields"
          class="mt-1 w-4 h-4 text-primary-500 rounded border-gray-300 focus:ring-primary-500 disabled:opacity-50"
        />
        <span class="text-sm text-gray-700">
          I confirm that all information provided is accurate and complete. I understand that this submission 
          will be reviewed by the editorial team and I may be contacted for revisions or additional information.
        </span>
      </label>
    </div>

    <!-- Submit Button -->
    <div class="mt-6">
      <button
        @click="handleSubmit"
        :disabled="!confirmed || !hasRequiredFields || isSubmitting"
        class="w-full py-4 bg-accent-500 text-white font-semibold rounded-xl hover:bg-accent-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
      >
        <svg v-if="isSubmitting" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        {{ isSubmitting ? 'Submitting...' : 'Submit Manuscript' }}
      </button>
      
      <p class="mt-3 text-center text-xs text-gray-500">
        By submitting, you agree to the journal's submission guidelines and policies.
      </p>
    </div>
  </div>
</template>

<style scoped>
.review-card {
  padding: 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
}
</style>
