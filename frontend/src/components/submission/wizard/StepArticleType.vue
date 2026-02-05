<script setup lang="ts">
/**
 * TruEditor - Wizard Step 1: Article Type Selection
 * ==================================================
 * Radio button group for selecting manuscript article type.
 */

import { computed } from 'vue'
import { ARTICLE_TYPES, type ArticleType } from '@/types/submission'

interface Props {
  /** Selected article type */
  modelValue: ArticleType | undefined
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: ArticleType]
}>()

const selectedType = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value as ArticleType)
})

// Article type icons
const typeIcons: Record<ArticleType, string> = {
  research: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z',
  review: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
  case_report: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  short_communication: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  letter: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
  editorial: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z',
  other: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
}
</script>

<template>
  <div class="step-article-type">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Select Article Type</h3>
      <p class="mt-1 text-sm text-gray-500">
        Choose the type that best describes your manuscript. This helps editors assign appropriate reviewers.
      </p>
    </div>

    <div class="grid gap-4">
      <label
        v-for="(typeInfo, typeKey) in ARTICLE_TYPES"
        :key="typeKey"
        class="article-type-option"
        :class="{ 'selected': selectedType === typeKey }"
      >
        <input
          v-model="selectedType"
          type="radio"
          name="articleType"
          :value="typeKey"
          class="sr-only"
        />
        
        <div class="flex items-start gap-4">
          <!-- Icon -->
          <div 
            class="flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-colors"
            :class="selectedType === typeKey ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-400'"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" :d="typeIcons[typeKey as ArticleType]" />
            </svg>
          </div>
          
          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <span 
                class="font-medium transition-colors"
                :class="selectedType === typeKey ? 'text-primary-700' : 'text-gray-900'"
              >
                {{ typeInfo.label }}
              </span>
              
              <!-- Check indicator -->
              <div 
                class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all"
                :class="selectedType === typeKey 
                  ? 'border-primary-500 bg-primary-500' 
                  : 'border-gray-300'"
              >
                <svg 
                  v-if="selectedType === typeKey"
                  class="w-3 h-3 text-white" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke="currentColor"
                  stroke-width="3"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            
            <p class="mt-1 text-sm text-gray-500">
              {{ typeInfo.description }}
            </p>
          </div>
        </div>
      </label>
    </div>

    <!-- Validation Message -->
    <div v-if="!selectedType" class="mt-6 flex items-center gap-2 text-amber-600">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-sm font-medium">Please select an article type to continue</span>
    </div>
  </div>
</template>

<style scoped>
.article-type-option {
  position: relative;
  padding: 1rem;
  background-color: white;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.article-type-option:hover {
  border-color: #d1d5db;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.article-type-option.selected {
  border-color: var(--color-primary-500, #1e3a5f);
  background-color: rgba(30, 58, 95, 0.05);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
</style>
