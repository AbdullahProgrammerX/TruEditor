<script setup lang="ts">
/**
 * TruEditor - Wizard Step 5: Additional Information
 * ==================================================
 * Cover letter, ethics, funding, and reviewer suggestions.
 */

import { ref, watch } from 'vue'
import type { SuggestedReviewer, OpposedReviewer } from '@/types/submission'

interface Props {
  /** Cover letter */
  coverLetter?: string
  /** Ethics statement */
  ethicsStatement?: string
  /** Ethics approval number */
  ethicsApprovalNumber?: string
  /** Conflict of interest statement */
  conflictOfInterest?: string
  /** Funding statement */
  fundingStatement?: string
  /** Suggested reviewers */
  suggestedReviewers?: SuggestedReviewer[]
  /** Opposed reviewers */
  opposedReviewers?: OpposedReviewer[]
  /** Comments to editor */
  editorComments?: string
}

const props = withDefaults(defineProps<Props>(), {
  coverLetter: '',
  ethicsStatement: '',
  ethicsApprovalNumber: '',
  conflictOfInterest: '',
  fundingStatement: '',
  suggestedReviewers: () => [],
  opposedReviewers: () => [],
  editorComments: '',
})

const emit = defineEmits<{
  'update:coverLetter': [value: string]
  'update:ethicsStatement': [value: string]
  'update:ethicsApprovalNumber': [value: string]
  'update:conflictOfInterest': [value: string]
  'update:fundingStatement': [value: string]
  'update:suggestedReviewers': [value: SuggestedReviewer[]]
  'update:opposedReviewers': [value: OpposedReviewer[]]
  'update:editorComments': [value: string]
}>()

// Local state
const localCoverLetter = ref(props.coverLetter)
const localEthicsStatement = ref(props.ethicsStatement)
const localEthicsApprovalNumber = ref(props.ethicsApprovalNumber)
const localConflictOfInterest = ref(props.conflictOfInterest)
const localFundingStatement = ref(props.fundingStatement)
const localSuggestedReviewers = ref<SuggestedReviewer[]>([...props.suggestedReviewers])
const localOpposedReviewers = ref<OpposedReviewer[]>([...props.opposedReviewers])
const localEditorComments = ref(props.editorComments)

// Accordion state
const expandedSections = ref<string[]>(['cover-letter'])

// Watchers
watch(localCoverLetter, (val) => emit('update:coverLetter', val))
watch(localEthicsStatement, (val) => emit('update:ethicsStatement', val))
watch(localEthicsApprovalNumber, (val) => emit('update:ethicsApprovalNumber', val))
watch(localConflictOfInterest, (val) => emit('update:conflictOfInterest', val))
watch(localFundingStatement, (val) => emit('update:fundingStatement', val))
watch(localSuggestedReviewers, (val) => emit('update:suggestedReviewers', val), { deep: true })
watch(localOpposedReviewers, (val) => emit('update:opposedReviewers', val), { deep: true })
watch(localEditorComments, (val) => emit('update:editorComments', val))

/**
 * Toggle section
 */
function toggleSection(section: string): void {
  const index = expandedSections.value.indexOf(section)
  if (index === -1) {
    expandedSections.value.push(section)
  } else {
    expandedSections.value.splice(index, 1)
  }
}

/**
 * Add suggested reviewer
 */
function addSuggestedReviewer(): void {
  if (localSuggestedReviewers.value.length >= 3) return
  localSuggestedReviewers.value.push({
    name: '',
    email: '',
    institution: '',
    reason: '',
  })
}

/**
 * Remove suggested reviewer
 */
function removeSuggestedReviewer(index: number): void {
  localSuggestedReviewers.value.splice(index, 1)
}

/**
 * Add opposed reviewer
 */
function addOpposedReviewer(): void {
  if (localOpposedReviewers.value.length >= 3) return
  localOpposedReviewers.value.push({
    name: '',
    email: '',
    reason: '',
  })
}

/**
 * Remove opposed reviewer
 */
function removeOpposedReviewer(index: number): void {
  localOpposedReviewers.value.splice(index, 1)
}

/**
 * Check if section is expanded
 */
function isExpanded(section: string): boolean {
  return expandedSections.value.includes(section)
}
</script>

<template>
  <div class="step-additional-info">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Additional Information</h3>
      <p class="mt-1 text-sm text-gray-500">
        Provide supplementary information about your submission.
      </p>
    </div>

    <div class="space-y-4">
      <!-- Cover Letter Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('cover-letter')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <span class="font-medium text-gray-900">Cover Letter</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('cover-letter') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('cover-letter')" class="accordion-content">
          <textarea
            v-model="localCoverLetter"
            rows="6"
            class="input-field resize-none"
            placeholder="Write a cover letter to the editor explaining why your manuscript is suitable for publication..."
          />
          <p class="mt-2 text-xs text-gray-500">
            Explain the significance of your work and why it is a good fit for the journal.
          </p>
        </div>
      </div>

      <!-- Ethics Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('ethics')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span class="font-medium text-gray-900">Ethics Statement</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('ethics') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('ethics')" class="accordion-content space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Ethics Statement
            </label>
            <textarea
              v-model="localEthicsStatement"
              rows="4"
              class="input-field resize-none"
              placeholder="Describe ethical approvals obtained for this research..."
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Ethics Approval Number
            </label>
            <input
              v-model="localEthicsApprovalNumber"
              type="text"
              class="input-field"
              placeholder="e.g., IRB-2026-001"
            />
          </div>
        </div>
      </div>

      <!-- Conflict of Interest Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('conflict')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span class="font-medium text-gray-900">Conflict of Interest</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('conflict') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('conflict')" class="accordion-content">
          <textarea
            v-model="localConflictOfInterest"
            rows="4"
            class="input-field resize-none"
            placeholder="Declare any conflicts of interest or state 'The authors declare no conflict of interest'..."
          />
        </div>
      </div>

      <!-- Funding Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('funding')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="font-medium text-gray-900">Funding Statement</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('funding') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('funding')" class="accordion-content">
          <textarea
            v-model="localFundingStatement"
            rows="4"
            class="input-field resize-none"
            placeholder="List funding sources and grant numbers, or state 'This research received no external funding'..."
          />
        </div>
      </div>

      <!-- Suggested Reviewers Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('suggested')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span class="font-medium text-gray-900">Suggested Reviewers</span>
            <span class="text-xs text-gray-500">(optional, max 3)</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('suggested') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('suggested')" class="accordion-content space-y-4">
          <div 
            v-for="(reviewer, index) in localSuggestedReviewers" 
            :key="index"
            class="p-4 bg-gray-50 rounded-lg space-y-3"
          >
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-700">Reviewer {{ index + 1 }}</span>
              <button
                @click="removeSuggestedReviewer(index)"
                class="p-1 text-gray-400 hover:text-red-500"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <input
                v-model="reviewer.name"
                type="text"
                class="input-field-sm"
                placeholder="Name"
              />
              <input
                v-model="reviewer.email"
                type="email"
                class="input-field-sm"
                placeholder="Email"
              />
            </div>
            <input
              v-model="reviewer.institution"
              type="text"
              class="input-field-sm"
              placeholder="Institution"
            />
          </div>
          
          <button
            v-if="localSuggestedReviewers.length < 3"
            @click="addSuggestedReviewer"
            class="w-full py-2 border border-dashed border-gray-300 rounded-lg text-sm text-gray-500 hover:border-primary-400 hover:text-primary-600 transition-colors"
          >
            + Add Suggested Reviewer
          </button>
        </div>
      </div>

      <!-- Opposed Reviewers Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('opposed')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
            </svg>
            <span class="font-medium text-gray-900">Opposed Reviewers</span>
            <span class="text-xs text-gray-500">(optional, max 3)</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('opposed') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('opposed')" class="accordion-content space-y-4">
          <div 
            v-for="(reviewer, index) in localOpposedReviewers" 
            :key="index"
            class="p-4 bg-gray-50 rounded-lg space-y-3"
          >
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-700">Opposed {{ index + 1 }}</span>
              <button
                @click="removeOpposedReviewer(index)"
                class="p-1 text-gray-400 hover:text-red-500"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <input
              v-model="reviewer.name"
              type="text"
              class="input-field-sm"
              placeholder="Name"
            />
            <textarea
              v-model="reviewer.reason"
              rows="2"
              class="input-field-sm resize-none"
              placeholder="Reason for opposition (required)"
            />
          </div>
          
          <button
            v-if="localOpposedReviewers.length < 3"
            @click="addOpposedReviewer"
            class="w-full py-2 border border-dashed border-gray-300 rounded-lg text-sm text-gray-500 hover:border-primary-400 hover:text-primary-600 transition-colors"
          >
            + Add Opposed Reviewer
          </button>
        </div>
      </div>

      <!-- Comments to Editor Section -->
      <div class="accordion-section">
        <button
          @click="toggleSection('comments')"
          class="accordion-header"
        >
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
            </svg>
            <span class="font-medium text-gray-900">Comments to Editor</span>
            <span class="text-xs text-gray-500">(confidential)</span>
          </div>
          <svg 
            class="w-5 h-5 text-gray-400 transition-transform"
            :class="{ 'rotate-180': isExpanded('comments') }"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div v-show="isExpanded('comments')" class="accordion-content">
          <textarea
            v-model="localEditorComments"
            rows="4"
            class="input-field resize-none"
            placeholder="Any confidential comments for the editor (will not be shared with reviewers)..."
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.accordion-section {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  overflow: hidden;
}

.accordion-header {
  width: 100%;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: white;
  transition: background-color 0.2s ease;
}

.accordion-header:hover {
  background-color: #f9fafb;
}

.accordion-content {
  padding: 0.5rem 1rem 1rem;
}

.input-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  transition: box-shadow 0.2s ease;
}

.input-field:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary-500, #1e3a5f);
  border-color: var(--color-primary-500, #1e3a5f);
}

.input-field-sm {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: box-shadow 0.2s ease;
}

.input-field-sm:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary-500, #1e3a5f);
  border-color: var(--color-primary-500, #1e3a5f);
}
</style>
