<script setup lang="ts">
/**
 * TruEditor - Complete Profile (Onboarding)
 * ==========================================
 * Guides new users to complete their profile after ORCID login.
 * Required fields must be filled before accessing the dashboard.
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ACADEMIC_TITLES, COUNTRIES, type UserProfileUpdate } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// Form state
const isSaving = ref(false)
const saveError = ref<string | null>(null)
const currentStep = ref(1)
const totalSteps = 3

// Form data
const formData = reactive<UserProfileUpdate>({
  // Step 1: Basic Info (Required)
  full_name: '',
  email: '',
  
  // Step 2: Academic Info (Required)
  institution: '',
  
  // Step 2: Academic Info (Optional)
  title: '',
  department: '',
  
  // Step 3: Additional Info (Optional)
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
  
  // If profile is already complete, redirect to dashboard
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
  // Can only go back or to current step
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
    
    // Redirect to dashboard on success
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
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-primary-900">
    <div class="min-h-screen flex flex-col">
      <!-- Header -->
      <header class="py-6 px-8">
        <div class="max-w-3xl mx-auto flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">T</span>
            </div>
            <span class="text-white font-semibold text-xl">TruEditor</span>
          </div>
          
          <div class="text-white/60 text-sm">
            Welcome, {{ authStore.user?.given_name || 'Researcher' }}!
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 flex items-center justify-center px-6 py-12">
        <div class="w-full max-w-2xl">
          <!-- Card -->
          <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <!-- Progress Header -->
            <div class="bg-primary-50 px-8 py-6">
              <h1 class="text-2xl font-bold text-gray-800 mb-2">Complete Your Profile</h1>
              <p class="text-gray-600">
                Please provide the following information to start using TruEditor.
                Fields marked with <span class="text-red-500">*</span> are required.
              </p>
              
              <!-- Progress Bar -->
              <div class="mt-6">
                <div class="flex justify-between mb-2">
                  <span class="text-sm text-gray-500">Step {{ currentStep }} of {{ totalSteps }}</span>
                  <span class="text-sm text-gray-500">{{ Math.round(progressPercentage) }}% complete</span>
                </div>
                <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-primary-500 transition-all duration-500"
                    :style="{ width: `${progressPercentage}%` }"
                  ></div>
                </div>
              </div>

              <!-- Step Indicators -->
              <div class="flex justify-between mt-4">
                <button 
                  v-for="step in totalSteps" 
                  :key="step"
                  @click="goToStep(step)"
                  :disabled="step > currentStep"
                  class="flex items-center gap-2 text-sm transition-colors"
                  :class="[
                    step === currentStep ? 'text-primary-600 font-medium' : 
                    step < currentStep ? 'text-green-600' : 'text-gray-400'
                  ]"
                >
                  <span 
                    class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium"
                    :class="[
                      step === currentStep ? 'bg-primary-500 text-white' :
                      step < currentStep ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500'
                    ]"
                  >
                    <span v-if="step < currentStep">✓</span>
                    <span v-else>{{ step }}</span>
                  </span>
                  <span class="hidden sm:inline">
                    {{ step === 1 ? 'Basic Info' : step === 2 ? 'Academic' : 'Additional' }}
                  </span>
                </button>
              </div>
            </div>

            <!-- Form Content -->
            <div class="px-8 py-6">
              <!-- Error Message -->
              <div v-if="saveError" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {{ saveError }}
              </div>

              <!-- Step 1: Basic Information -->
              <div v-show="currentStep === 1" class="space-y-6">
                <div class="text-center mb-8">
                  <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h2 class="text-xl font-semibold text-gray-800">Basic Information</h2>
                  <p class="text-gray-500 mt-1">Let's start with your basic details</p>
                </div>

                <div>
                  <label class="label" for="full_name">
                    Full Name <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="full_name"
                    v-model="formData.full_name"
                    type="text"
                    class="input"
                    placeholder="e.g., Dr. John Smith"
                    required
                  />
                  <p class="text-xs text-gray-400 mt-1">This will be displayed on your submissions</p>
                </div>

                <div>
                  <label class="label" for="email">
                    Email Address <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="email"
                    v-model="formData.email"
                    type="email"
                    class="input"
                    placeholder="john.smith@university.edu"
                    required
                  />
                  <p class="text-xs text-gray-400 mt-1">We'll use this for important notifications</p>
                </div>

                <div>
                  <label class="label" for="phone">Phone (Optional)</label>
                  <input 
                    id="phone"
                    v-model="formData.phone"
                    type="tel"
                    class="input"
                    placeholder="+1 555 123 4567"
                  />
                </div>
              </div>

              <!-- Step 2: Academic Information -->
              <div v-show="currentStep === 2" class="space-y-6">
                <div class="text-center mb-8">
                  <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    </svg>
                  </div>
                  <h2 class="text-xl font-semibold text-gray-800">Academic Information</h2>
                  <p class="text-gray-500 mt-1">Tell us about your academic affiliation</p>
                </div>

                <div>
                  <label class="label" for="institution">
                    Institution / University <span class="text-red-500">*</span>
                  </label>
                  <input 
                    id="institution"
                    v-model="formData.institution"
                    type="text"
                    class="input"
                    placeholder="e.g., Harvard University"
                    required
                  />
                </div>

                <div>
                  <label class="label" for="department">Department (Optional)</label>
                  <input 
                    id="department"
                    v-model="formData.department"
                    type="text"
                    class="input"
                    placeholder="e.g., Department of Computer Science"
                  />
                </div>

                <div>
                  <label class="label" for="title">Academic Title (Optional)</label>
                  <select id="title" v-model="formData.title" class="input">
                    <option v-for="[value, label] in titleOptions" :key="value" :value="value">
                      {{ label }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="label" for="country">Country (Optional)</label>
                  <select id="country" v-model="formData.country" class="input">
                    <option value="">Select country</option>
                    <option v-for="country in COUNTRIES" :key="country" :value="country">
                      {{ country }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Step 3: Additional Information -->
              <div v-show="currentStep === 3" class="space-y-6">
                <div class="text-center mb-8">
                  <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h2 class="text-xl font-semibold text-gray-800">Additional Information</h2>
                  <p class="text-gray-500 mt-1">Help others learn more about you (all optional)</p>
                </div>

                <div>
                  <label class="label">Expertise Areas (max 10)</label>
                  <div class="flex gap-2 mb-2">
                    <input 
                      v-model="newExpertise"
                      type="text"
                      class="input flex-1"
                      placeholder="e.g., Machine Learning, NLP"
                      @keypress.enter.prevent="addExpertise"
                    />
                    <button 
                      type="button"
                      @click="addExpertise"
                      class="btn-outline"
                      :disabled="!newExpertise.trim() || (formData.expertise_areas?.length ?? 0) >= 10"
                    >
                      Add
                    </button>
                  </div>
                  <div v-if="formData.expertise_areas?.length" class="flex flex-wrap gap-2">
                    <span 
                      v-for="(area, index) in formData.expertise_areas" 
                      :key="index"
                      class="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center gap-1"
                    >
                      {{ area }}
                      <button type="button" @click="removeExpertise(index)" class="hover:text-red-600">×</button>
                    </span>
                  </div>
                </div>

                <div>
                  <label class="label" for="bio">Short Biography ({{ bioCharCount }}/1000)</label>
                  <textarea 
                    id="bio"
                    v-model="formData.bio"
                    class="input min-h-[100px]"
                    placeholder="Tell us about your research interests and background..."
                    maxlength="1000"
                    rows="3"
                  ></textarea>
                </div>

                <div>
                  <label class="label" for="website">Personal Website</label>
                  <input 
                    id="website"
                    v-model="formData.website"
                    type="url"
                    class="input"
                    placeholder="https://yourwebsite.com"
                  />
                </div>

                <div>
                  <label class="label" for="city">City</label>
                  <input 
                    id="city"
                    v-model="formData.city"
                    type="text"
                    class="input"
                    placeholder="e.g., Cambridge"
                  />
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="px-8 py-6 bg-gray-50 border-t flex justify-between">
              <button 
                v-if="currentStep > 1"
                @click="prevStep"
                class="btn-ghost"
                :disabled="isSaving"
              >
                ← Back
              </button>
              <div v-else></div>

              <div class="flex gap-3">
                <button 
                  v-if="currentStep < totalSteps"
                  @click="nextStep"
                  class="btn-primary"
                  :disabled="!canProceed"
                >
                  Continue →
                </button>
                
                <button 
                  v-if="currentStep === totalSteps"
                  @click="submitProfile"
                  class="btn-primary"
                  :disabled="!allRequiredFilled || isSaving"
                >
                  <span v-if="isSaving">Saving...</span>
                  <span v-else>Complete Profile ✓</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Skip Note -->
          <p class="text-center text-white/50 text-sm mt-6">
            You can update these details anytime from your profile settings.
          </p>
        </div>
      </main>
    </div>
  </div>
</template>
