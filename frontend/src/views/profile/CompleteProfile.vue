<script setup lang="ts">
/**
 * TruEditor - Complete Profile (Onboarding)
 * ==========================================
 * Guides new users to complete their profile after ORCID login.
 * Required fields must be filled before accessing the dashboard.
 * 
 * Developer: Abdullah Dogan
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ACADEMIC_TITLES, COUNTRIES, type UserProfileUpdate } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// Animation states
const isLoaded = ref(false)
const currentStep = ref(1)
const totalSteps = 3

// Form state
const isSaving = ref(false)
const saveError = ref<string | null>(null)

// Form data
const formData = reactive<UserProfileUpdate>({
  full_name: '',
  email: '',
  institution: '',
  title: '',
  department: '',
  phone: '',
  country: '',
  city: '',
  bio: '',
  website: '',
  expertise_areas: [],
})

// Expertise area input
const newExpertise = ref('')

// Initialize form with data from ORCID
onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
  }, 100)

  if (authStore.user) {
    formData.full_name = authStore.user.full_name || ''
    formData.email = authStore.user.email || ''
    formData.institution = authStore.user.institution || ''
    formData.title = authStore.user.title || ''
    formData.department = authStore.user.department || ''
    formData.phone = authStore.user.phone || ''
    formData.country = authStore.user.country || ''
    formData.city = authStore.user.city || ''
    formData.bio = authStore.user.bio || ''
    formData.website = authStore.user.website || ''
    formData.expertise_areas = [...(authStore.user.expertise_areas || [])]
  }
  
  if (authStore.profileCompleted) {
    router.push('/dashboard')
  }
})

// Validation
const step1Valid = computed(() => {
  return formData.full_name?.trim() && formData.email?.trim()
})

const step2Valid = computed(() => {
  return formData.institution?.trim()
})

const canProceed = computed(() => {
  if (currentStep.value === 1) return step1Valid.value
  if (currentStep.value === 2) return step2Valid.value
  return true
})

const allRequiredFilled = computed(() => {
  return step1Valid.value && step2Valid.value
})

// Navigation
function nextStep() {
  if (canProceed.value && currentStep.value < totalSteps) {
    currentStep.value++
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

function goToStep(step: number) {
  if (step <= currentStep.value) {
    currentStep.value = step
  }
}

// Expertise areas
function addExpertise() {
  const value = newExpertise.value.trim()
  if (value && formData.expertise_areas && formData.expertise_areas.length < 10) {
    if (!formData.expertise_areas.includes(value)) {
      formData.expertise_areas.push(value)
    }
    newExpertise.value = ''
  }
}

function removeExpertise(index: number) {
  formData.expertise_areas?.splice(index, 1)
}

// Submit
async function submitProfile() {
  if (!allRequiredFilled.value) {
    saveError.value = 'Please fill in all required fields'
    return
  }

  isSaving.value = true
  saveError.value = null

  try {
    await authStore.updateProfile(formData)
    router.push('/dashboard')
  } catch (err: any) {
    saveError.value = err.response?.data?.error?.message || 'Failed to save profile'
  } finally {
    isSaving.value = false
  }
}

// Computed
const titleOptions = computed(() => Object.entries(ACADEMIC_TITLES))
const bioCharCount = computed(() => formData.bio?.length || 0)
const progressPercentage = computed(() => (currentStep.value / totalSteps) * 100)

// Step info
const steps = [
  { id: 1, name: 'Basic Info', icon: 'user' },
  { id: 2, name: 'Academic', icon: 'academic' },
  { id: 3, name: 'Additional', icon: 'info' },
]
</script>

<template>
  <div class="min-h-screen bg-gradient-hero overflow-hidden">
    <!-- Animated Background Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjAyIi8+PC9nPjwvc3ZnPg==')] opacity-40"></div>
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
    </div>

    <div class="relative z-10 min-h-screen flex flex-col">
      <!-- Header -->
      <header 
        class="py-4 sm:py-6 px-4 sm:px-8 transition-all duration-700"
        :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-5'"
      >
        <div class="max-w-4xl mx-auto flex items-center justify-between">
          <div class="flex items-center gap-2 sm:gap-3">
            <div class="relative">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-white rounded-xl flex items-center justify-center shadow-lg shadow-white/20">
                <span class="text-primary-500 font-bold text-xl sm:text-2xl">T</span>
              </div>
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full border-2 border-slate-900"></div>
            </div>
            <div>
              <span class="text-xl sm:text-2xl font-bold text-white tracking-tight">TruEditor</span>
              <p class="text-xs text-white/50 -mt-1 hidden sm:block">Complete Your Profile</p>
            </div>
          </div>
          
          <div class="flex items-center gap-2 sm:gap-3">
            <div class="text-right hidden sm:block">
              <p class="text-white/90 text-sm font-medium">
                {{ authStore.user?.given_name || 'Researcher' }}
              </p>
              <p class="text-white/50 text-xs">Step {{ currentStep }} of {{ totalSteps }}</p>
            </div>
            <div class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center border border-white/20">
              <svg class="w-5 h-5 text-white/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 flex items-start sm:items-center justify-center px-4 py-6 sm:py-12">
        <div 
          class="w-full max-w-2xl transition-all duration-700 delay-200"
          :class="isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
        >
          <!-- Card -->
          <div class="bg-white/95 backdrop-blur-sm rounded-2xl sm:rounded-3xl shadow-2xl overflow-hidden">
            <!-- Progress Header -->
            <div class="bg-gradient-to-r from-primary-500 to-primary-600 px-4 sm:px-8 py-5 sm:py-6">
              <h1 class="text-xl sm:text-2xl font-bold text-white mb-1">Complete Your Profile</h1>
              <p class="text-white/80 text-sm sm:text-base">
                Fields marked with <span class="text-yellow-300 font-semibold">*</span> are required
              </p>
              
              <!-- Progress Bar -->
              <div class="mt-4 sm:mt-6">
                <div class="flex justify-between mb-2">
                  <span class="text-sm text-white/70">Progress</span>
                  <span class="text-sm text-white font-medium">{{ Math.round(progressPercentage) }}%</span>
                </div>
                <div class="h-2 bg-white/20 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-gradient-to-r from-emerald-400 to-emerald-500 transition-all duration-500 ease-out"
                    :style="{ width: `${progressPercentage}%` }"
                  ></div>
                </div>
              </div>

              <!-- Step Indicators -->
              <div class="flex justify-between mt-4 sm:mt-6">
                <button 
                  v-for="step in steps" 
                  :key="step.id"
                  @click="goToStep(step.id)"
                  :disabled="step.id > currentStep"
                  class="flex items-center gap-1.5 sm:gap-2 text-xs sm:text-sm transition-all duration-300 group"
                  :class="[
                    step.id === currentStep ? 'text-white' : 
                    step.id < currentStep ? 'text-emerald-300' : 'text-white/40'
                  ]"
                >
                  <span 
                    class="w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300"
                    :class="[
                      step.id === currentStep ? 'bg-white text-primary-600 shadow-lg' :
                      step.id < currentStep ? 'bg-emerald-400 text-white' : 'bg-white/20 text-white/50'
                    ]"
                  >
                    <svg v-if="step.id < currentStep" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                    </svg>
                    <span v-else>{{ step.id }}</span>
                  </span>
                  <span class="hidden sm:inline font-medium">{{ step.name }}</span>
                </button>
              </div>
            </div>

            <!-- Form Content -->
            <div class="px-4 sm:px-8 py-6 sm:py-8">
              <!-- Error Message -->
              <div 
                v-if="saveError" 
                class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center gap-3"
              >
                <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-sm">{{ saveError }}</span>
              </div>

              <!-- Step 1: Basic Information -->
              <div v-show="currentStep === 1" class="space-y-5">
                <div class="text-center mb-6">
                  <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                    <svg class="w-7 h-7 sm:w-8 sm:h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h2 class="text-lg sm:text-xl font-bold text-gray-800">Basic Information</h2>
                  <p class="text-gray-500 text-sm mt-1">Let's start with your basic details</p>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="full_name">
                    Full Name <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="full_name"
                    v-model="formData.full_name"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                    placeholder="e.g., Dr. John Smith"
                    required
                  />
                  <p class="text-xs text-gray-400 mt-1.5">This will be displayed on your submissions</p>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="email">
                    Email Address <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="email"
                    v-model="formData.email"
                    type="email"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                    placeholder="john.smith@university.edu"
                    required
                  />
                  <p class="text-xs text-gray-400 mt-1.5">We'll use this for important notifications</p>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="phone">
                    Phone <span class="text-gray-400 font-normal">(Optional)</span>
                  </label>
                  <input 
                    id="phone"
                    v-model="formData.phone"
                    type="tel"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                    placeholder="+1 555 123 4567"
                  />
                </div>
              </div>

              <!-- Step 2: Academic Information -->
              <div v-show="currentStep === 2" class="space-y-5">
                <div class="text-center mb-6">
                  <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                    <svg class="w-7 h-7 sm:w-8 sm:h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    </svg>
                  </div>
                  <h2 class="text-lg sm:text-xl font-bold text-gray-800">Academic Information</h2>
                  <p class="text-gray-500 text-sm mt-1">Tell us about your academic affiliation</p>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="institution">
                    Institution / University <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="institution"
                    v-model="formData.institution"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                    placeholder="e.g., Harvard University"
                    required
                  />
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="department">
                    Department <span class="text-gray-400 font-normal">(Optional)</span>
                  </label>
                  <input 
                    id="department"
                    v-model="formData.department"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                    placeholder="e.g., Department of Computer Science"
                  />
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2" for="title">
                      Academic Title <span class="text-gray-400 font-normal">(Optional)</span>
                    </label>
                    <select 
                      id="title" 
                      v-model="formData.title" 
                      class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200 bg-white"
                    >
                      <option value="">Select title</option>
                      <option v-for="[value, label] in titleOptions" :key="value" :value="value">
                        {{ label }}
                      </option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2" for="country">
                      Country <span class="text-gray-400 font-normal">(Optional)</span>
                    </label>
                    <select 
                      id="country" 
                      v-model="formData.country" 
                      class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200 bg-white"
                    >
                      <option value="">Select country</option>
                      <option v-for="country in COUNTRIES" :key="country" :value="country">
                        {{ country }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Step 3: Additional Information -->
              <div v-show="currentStep === 3" class="space-y-5">
                <div class="text-center mb-6">
                  <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gradient-to-br from-emerald-100 to-emerald-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                    <svg class="w-7 h-7 sm:w-8 sm:h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h2 class="text-lg sm:text-xl font-bold text-gray-800">Additional Information</h2>
                  <p class="text-gray-500 text-sm mt-1">Help others learn more about you (all optional)</p>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">
                    Expertise Areas <span class="text-gray-400 font-normal">(max 10)</span>
                  </label>
                  <div class="flex gap-2 mb-3">
                    <input 
                      v-model="newExpertise"
                      type="text"
                      class="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                      placeholder="e.g., Machine Learning"
                      @keypress.enter.prevent="addExpertise"
                    />
                    <button 
                      type="button"
                      @click="addExpertise"
                      :disabled="!newExpertise.trim() || (formData.expertise_areas?.length ?? 0) >= 10"
                      class="px-5 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Add
                    </button>
                  </div>
                  <div v-if="formData.expertise_areas?.length" class="flex flex-wrap gap-2">
                    <span 
                      v-for="(area, index) in formData.expertise_areas" 
                      :key="index"
                      class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
                    >
                      {{ area }}
                      <button 
                        type="button" 
                        @click="removeExpertise(index)" 
                        class="hover:text-red-600 transition-colors"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </span>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="bio">
                    Short Biography <span class="text-gray-400 font-normal">({{ bioCharCount }}/1000)</span>
                  </label>
                  <textarea 
                    id="bio"
                    v-model="formData.bio"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200 resize-none"
                    placeholder="Tell us about your research interests and background..."
                    maxlength="1000"
                    rows="3"
                  ></textarea>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2" for="website">
                      Personal Website
                    </label>
                    <input 
                      id="website"
                      v-model="formData.website"
                      type="url"
                      class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                      placeholder="https://yourwebsite.com"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2" for="city">
                      City
                    </label>
                    <input 
                      id="city"
                      v-model="formData.city"
                      type="text"
                      class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-200"
                      placeholder="e.g., Cambridge"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="px-4 sm:px-8 py-5 sm:py-6 bg-gray-50 border-t border-gray-100 flex flex-col sm:flex-row justify-between gap-3">
              <button 
                v-if="currentStep > 1"
                @click="prevStep"
                :disabled="isSaving"
                class="order-2 sm:order-1 px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-gray-100 font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
                Back
              </button>
              <div v-else class="hidden sm:block"></div>

              <div class="order-1 sm:order-2 flex flex-col sm:flex-row gap-3">
                <button 
                  v-if="currentStep < totalSteps"
                  @click="nextStep"
                  :disabled="!canProceed"
                  class="w-full sm:w-auto px-8 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl shadow-lg shadow-primary-500/30 hover:shadow-xl hover:shadow-primary-500/40 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
                >
                  Continue
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
                
                <button 
                  v-if="currentStep === totalSteps"
                  @click="submitProfile"
                  :disabled="!allRequiredFilled || isSaving"
                  class="w-full sm:w-auto px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-xl shadow-lg shadow-emerald-500/30 hover:shadow-xl hover:shadow-emerald-500/40 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
                >
                  <span v-if="isSaving" class="flex items-center gap-2">
                    <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Saving...
                  </span>
                  <span v-else class="flex items-center gap-2">
                    Complete Profile
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </span>
                </button>
              </div>
            </div>
          </div>

          <!-- Footer Note -->
          <p class="text-center text-white/40 text-sm mt-6 px-4">
            You can update these details anytime from your profile settings.
          </p>
        </div>
      </main>
    </div>
  </div>
</template>
