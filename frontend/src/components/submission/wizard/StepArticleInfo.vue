<script setup lang="ts">
/**
 * TruEditor - Wizard Step 3: Article Information
 * ================================================
 * Title, abstract, and keywords input form.
 */

import { ref, computed, watch } from 'vue'
import { LANGUAGES, type Language } from '@/types/submission'

interface Props {
  /** Title */
  title?: string
  /** English title */
  titleEn?: string
  /** Abstract */
  abstract?: string
  /** English abstract */
  abstractEn?: string
  /** Keywords */
  keywords?: string[]
  /** English keywords */
  keywordsEn?: string[]
  /** Language */
  language?: Language
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  titleEn: '',
  abstract: '',
  abstractEn: '',
  keywords: () => [],
  keywordsEn: () => [],
  language: 'en',
})

const emit = defineEmits<{
  'update:title': [value: string]
  'update:titleEn': [value: string]
  'update:abstract': [value: string]
  'update:abstractEn': [value: string]
  'update:keywords': [value: string[]]
  'update:keywordsEn': [value: string[]]
  'update:language': [value: Language]
}>()

// Local state
const localTitle = ref(props.title)
const localTitleEn = ref(props.titleEn)
const localAbstract = ref(props.abstract)
const localAbstractEn = ref(props.abstractEn)
const localKeywords = ref<string[]>([...props.keywords])
const localKeywordsEn = ref<string[]>([...props.keywordsEn])
const localLanguage = ref(props.language)

const keywordInput = ref('')
const keywordInputEn = ref('')

// Constants
const MAX_ABSTRACT_LENGTH = 5000
const MIN_KEYWORDS = 3
const MAX_KEYWORDS = 10

// Computed
const abstractLength = computed(() => localAbstract.value.length)
const abstractEnLength = computed(() => localAbstractEn.value.length)
const showEnglishFields = computed(() => localLanguage.value === 'tr')

// Watchers for emitting updates
watch(localTitle, (val) => emit('update:title', val))
watch(localTitleEn, (val) => emit('update:titleEn', val))
watch(localAbstract, (val) => emit('update:abstract', val))
watch(localAbstractEn, (val) => emit('update:abstractEn', val))
watch(localKeywords, (val) => emit('update:keywords', val), { deep: true })
watch(localKeywordsEn, (val) => emit('update:keywordsEn', val), { deep: true })
watch(localLanguage, (val) => emit('update:language', val))

/**
 * Add keyword
 */
function addKeyword(isEnglish = false): void {
  const input = isEnglish ? keywordInputEn : keywordInput
  const keywords = isEnglish ? localKeywordsEn : localKeywords
  
  const keyword = input.value.trim()
  if (!keyword) return
  if (keywords.value.length >= MAX_KEYWORDS) return
  if (keywords.value.includes(keyword)) return
  
  keywords.value.push(keyword)
  input.value = ''
}

/**
 * Remove keyword
 */
function removeKeyword(index: number, isEnglish = false): void {
  const keywords = isEnglish ? localKeywordsEn : localKeywords
  keywords.value.splice(index, 1)
}

/**
 * Handle keyword input keydown
 */
function handleKeywordKeydown(event: KeyboardEvent, isEnglish = false): void {
  if (event.key === 'Enter' || event.key === ',') {
    event.preventDefault()
    addKeyword(isEnglish)
  }
}

// Validation
const isTitleValid = computed(() => localTitle.value.trim().length > 0)
const isAbstractValid = computed(() => 
  localAbstract.value.trim().length > 0 && 
  localAbstract.value.length <= MAX_ABSTRACT_LENGTH
)
const isKeywordsValid = computed(() => 
  localKeywords.value.length >= MIN_KEYWORDS && 
  localKeywords.value.length <= MAX_KEYWORDS
)

// Expose validation for parent component
defineExpose({
  isValid: computed(() => isTitleValid.value && isAbstractValid.value && isKeywordsValid.value)
})
</script>

<template>
  <div class="step-article-info">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Article Information</h3>
      <p class="mt-1 text-sm text-gray-500">
        Provide the title, abstract, and keywords for your manuscript.
      </p>
    </div>

    <!-- Language Selector -->
    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Manuscript Language
      </label>
      <div class="flex gap-3">
        <label 
          v-for="(langLabel, langKey) in LANGUAGES" 
          :key="langKey"
          class="flex items-center gap-2 px-4 py-2 border rounded-lg cursor-pointer transition-all"
          :class="localLanguage === langKey 
            ? 'border-primary-500 bg-primary-50 text-primary-700' 
            : 'border-gray-200 hover:border-gray-300'"
        >
          <input 
            v-model="localLanguage" 
            type="radio" 
            :value="langKey" 
            class="sr-only" 
          />
          {{ langLabel }}
        </label>
      </div>
    </div>

    <div class="space-y-6">
      <!-- Title -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Title <span class="text-red-500">*</span>
        </label>
        <input
          v-model="localTitle"
          type="text"
          class="input-field"
          :class="{ 'error': !isTitleValid && localTitle.length > 0 }"
          placeholder="Enter the title of your manuscript"
        />
        <p v-if="!isTitleValid && localTitle.length > 0" class="mt-1 text-sm text-red-500">
          Title is required
        </p>
      </div>

      <!-- English Title (if Turkish manuscript) -->
      <div v-if="showEnglishFields">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          English Title
        </label>
        <input
          v-model="localTitleEn"
          type="text"
          class="input-field"
          placeholder="Enter the English title (optional)"
        />
      </div>

      <!-- Abstract -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Abstract <span class="text-red-500">*</span>
        </label>
        <textarea
          v-model="localAbstract"
          rows="6"
          class="input-field resize-none"
          :class="{ 'error': abstractLength > MAX_ABSTRACT_LENGTH }"
          placeholder="Enter your manuscript abstract (max 5000 characters)"
        />
        <div class="flex justify-between mt-1">
          <p 
            v-if="abstractLength > MAX_ABSTRACT_LENGTH" 
            class="text-sm text-red-500"
          >
            Abstract exceeds maximum length
          </p>
          <span v-else />
          <span 
            class="text-sm"
            :class="abstractLength > MAX_ABSTRACT_LENGTH ? 'text-red-500' : 'text-gray-500'"
          >
            {{ abstractLength }} / {{ MAX_ABSTRACT_LENGTH }}
          </span>
        </div>
      </div>

      <!-- English Abstract (if Turkish manuscript) -->
      <div v-if="showEnglishFields">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          English Abstract
        </label>
        <textarea
          v-model="localAbstractEn"
          rows="6"
          class="input-field resize-none"
          :class="{ 'error': abstractEnLength > MAX_ABSTRACT_LENGTH }"
          placeholder="Enter the English abstract (optional)"
        />
        <div class="flex justify-end mt-1">
          <span 
            class="text-sm"
            :class="abstractEnLength > MAX_ABSTRACT_LENGTH ? 'text-red-500' : 'text-gray-500'"
          >
            {{ abstractEnLength }} / {{ MAX_ABSTRACT_LENGTH }}
          </span>
        </div>
      </div>

      <!-- Keywords -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Keywords <span class="text-red-500">*</span>
          <span class="font-normal text-gray-500">({{ MIN_KEYWORDS }}-{{ MAX_KEYWORDS }} keywords)</span>
        </label>
        
        <!-- Keyword Tags -->
        <div class="flex flex-wrap gap-2 mb-2" v-if="localKeywords.length > 0">
          <span
            v-for="(keyword, index) in localKeywords"
            :key="index"
            class="keyword-tag"
          >
            {{ keyword }}
            <button 
              @click="removeKeyword(index)"
              class="ml-1 hover:text-red-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>
        
        <!-- Keyword Input -->
        <div class="flex gap-2">
          <input
            v-model="keywordInput"
            type="text"
            class="input-field flex-1"
            placeholder="Type a keyword and press Enter"
            :disabled="localKeywords.length >= MAX_KEYWORDS"
            @keydown="handleKeywordKeydown($event, false)"
          />
          <button
            @click="addKeyword(false)"
            :disabled="localKeywords.length >= MAX_KEYWORDS || !keywordInput.trim()"
            class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Add
          </button>
        </div>
        
        <p 
          v-if="localKeywords.length < MIN_KEYWORDS" 
          class="mt-1 text-sm text-amber-600"
        >
          Please add at least {{ MIN_KEYWORDS }} keywords ({{ MIN_KEYWORDS - localKeywords.length }} more needed)
        </p>
      </div>

      <!-- English Keywords (if Turkish manuscript) -->
      <div v-if="showEnglishFields">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          English Keywords
          <span class="font-normal text-gray-500">(optional)</span>
        </label>
        
        <!-- Keyword Tags -->
        <div class="flex flex-wrap gap-2 mb-2" v-if="localKeywordsEn.length > 0">
          <span
            v-for="(keyword, index) in localKeywordsEn"
            :key="index"
            class="keyword-tag"
          >
            {{ keyword }}
            <button 
              @click="removeKeyword(index, true)"
              class="ml-1 hover:text-red-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </span>
        </div>
        
        <!-- Keyword Input -->
        <div class="flex gap-2">
          <input
            v-model="keywordInputEn"
            type="text"
            class="input-field flex-1"
            placeholder="Type an English keyword and press Enter"
            :disabled="localKeywordsEn.length >= MAX_KEYWORDS"
            @keydown="handleKeywordKeydown($event, true)"
          />
          <button
            @click="addKeyword(true)"
            :disabled="localKeywordsEn.length >= MAX_KEYWORDS || !keywordInputEn.trim()"
            class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Add
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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

.input-field.error {
  border-color: #fca5a5;
}

.input-field.error:focus {
  box-shadow: 0 0 0 2px #ef4444;
  border-color: #ef4444;
}

.keyword-tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background-color: rgba(30, 58, 95, 0.1);
  color: var(--color-primary-700, #152b47);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}
</style>
