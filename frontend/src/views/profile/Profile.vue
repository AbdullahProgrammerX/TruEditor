<script setup lang="ts">
/**
 * TruEditor - User Profile Page
 * ==============================
 * Displays and manages user profile information with modern design.
 * 
 * Developer: Abdullah Dogan
 */
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ACADEMIC_TITLES, COUNTRIES, type UserProfileUpdate, type AcademicTitle } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// Animation
const isVisible = ref(false)

// Edit mode state
const isEditing = ref(false)
const isSaving = ref(false)
const saveError = ref<string | null>(null)
const saveSuccess = ref(false)

// Form data
const formData = reactive<UserProfileUpdate>({
  email: '',
  full_name: '',
  given_name: '',
  family_name: '',
  phone: '',
  country: '',
  city: '',
  address: '',
  title: '',
  institution: '',
  department: '',
  expertise_areas: [],
  bio: '',
  website: '',
})

const newExpertise = ref('')

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})

function initForm() {
  if (authStore.user) {
    formData.email = authStore.user.email || ''
    formData.full_name = authStore.user.full_name || ''
    formData.given_name = authStore.user.given_name || ''
    formData.family_name = authStore.user.family_name || ''
    formData.phone = authStore.user.phone || ''
    formData.country = authStore.user.country || ''
    formData.city = authStore.user.city || ''
    formData.address = authStore.user.address || ''
    formData.title = authStore.user.title || ''
    formData.institution = authStore.user.institution || ''
    formData.department = authStore.user.department || ''
    formData.expertise_areas = [...(authStore.user.expertise_areas || [])]
    formData.bio = authStore.user.bio || ''
    formData.website = authStore.user.website || ''
  }
}

function startEditing() {
  initForm()
  isEditing.value = true
  saveError.value = null
  saveSuccess.value = false
}

function cancelEditing() {
  isEditing.value = false
  saveError.value = null
}

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

async function saveProfile() {
  isSaving.value = true
  saveError.value = null
  saveSuccess.value = false

  try {
    await authStore.updateProfile(formData)
    isEditing.value = false
    saveSuccess.value = true
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (err: any) {
    saveError.value = err.response?.data?.error?.message || 'Failed to save profile'
  } finally {
    isSaving.value = false
  }
}

async function syncOrcid() {
  try {
    await authStore.syncORCIDProfile()
    saveSuccess.value = true
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch {
    saveError.value = 'Failed to sync ORCID profile'
  }
}

const titleOptions = computed(() => Object.entries(ACADEMIC_TITLES))
const bioCharCount = computed(() => formData.bio?.length || 0)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-gradient-to-r from-primary-600 via-primary-500 to-primary-600 shadow-lg sticky top-0 z-40">
      <div class="max-w-5xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between h-16">
          <button 
            @click="router.push('/dashboard')" 
            class="flex items-center gap-2 text-white/80 hover:text-white transition-colors group"
          >
            <svg class="w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span class="hidden sm:inline">Dashboard</span>
          </button>
          <h1 class="text-lg font-semibold text-white">Profile Settings</h1>
          <div class="w-24"></div>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <!-- Success Message -->
      <div 
        v-if="saveSuccess" 
        class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-700 flex items-center gap-3 transition-all duration-300"
        :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'"
      >
        <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="font-medium">Profile updated successfully!</span>
      </div>

      <!-- Error Message -->
      <div 
        v-if="saveError" 
        class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-center gap-3"
      >
        <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ saveError }}
      </div>

      <!-- Profile Card -->
      <div 
        class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden transition-all duration-700"
        :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'"
      >
        <!-- Header with Avatar -->
        <div class="bg-gradient-to-r from-primary-500 to-primary-600 px-4 sm:px-8 py-6 sm:py-8">
          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-4 sm:gap-6">
            <!-- Avatar -->
            <div class="w-20 h-20 sm:w-24 sm:h-24 bg-white rounded-2xl flex items-center justify-center text-primary-500 text-3xl sm:text-4xl font-bold shadow-lg">
              {{ authStore.fullName?.charAt(0) || 'U' }}
            </div>
            
            <div class="text-center sm:text-left flex-1">
              <h2 class="text-xl sm:text-2xl font-bold text-white mb-1">{{ authStore.fullName }}</h2>
              <a 
                :href="authStore.orcidUrl"
                target="_blank"
                class="inline-flex items-center gap-1.5 text-white/80 hover:text-white transition-colors text-sm"
              >
                <svg class="w-4 h-4 text-[#a6ce39]" viewBox="0 0 256 256">
                  <path fill="currentColor" d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128S57.3 0 128 0s128 57.3 128 128"/>
                </svg>
                {{ authStore.orcidId }}
              </a>
              <p v-if="!authStore.profileCompleted" class="text-amber-300 text-sm mt-2 flex items-center justify-center sm:justify-start gap-1">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Please complete your profile
              </p>
            </div>

            <!-- Edit Button -->
            <button 
              v-if="!isEditing"
              @click="startEditing"
              class="px-5 py-2.5 bg-white text-primary-600 font-semibold rounded-xl shadow hover:shadow-lg hover:scale-105 transition-all flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <span class="hidden sm:inline">Edit Profile</span>
            </button>
          </div>
        </div>

        <div class="p-4 sm:p-8">
          <!-- View Mode -->
          <div v-if="!isEditing" class="space-y-8">
            <!-- Personal Information -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100 flex items-center gap-2">
                <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Personal Information
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Full Name</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.full_name || '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Email</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.email || '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Title</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.title ? ACADEMIC_TITLES[authStore.user.title as AcademicTitle] : '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Phone</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.phone || '—' }}</p>
                </div>
              </div>
            </section>

            <!-- Academic Information -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100 flex items-center gap-2">
                <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                </svg>
                Academic Information
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Institution</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.institution || '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Department</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.department || '—' }}</p>
                </div>
                <div class="sm:col-span-2 bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Expertise Areas</label>
                  <div v-if="authStore.user?.expertise_areas?.length" class="flex flex-wrap gap-2">
                    <span 
                      v-for="area in authStore.user.expertise_areas" 
                      :key="area"
                      class="px-3 py-1.5 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
                    >
                      {{ area }}
                    </span>
                  </div>
                  <p v-else class="text-gray-400">No expertise areas specified</p>
                </div>
                <div class="sm:col-span-2 bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Biography</label>
                  <p class="text-gray-800 whitespace-pre-wrap">{{ authStore.user?.bio || '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Website</label>
                  <a 
                    v-if="authStore.user?.website" 
                    :href="authStore.user.website" 
                    target="_blank"
                    class="text-primary-600 hover:text-primary-700 hover:underline font-medium"
                  >
                    {{ authStore.user.website }}
                  </a>
                  <p v-else class="text-gray-400">—</p>
                </div>
              </div>
            </section>

            <!-- Location -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100 flex items-center gap-2">
                <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Location
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Country</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.country || '—' }}</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4">
                  <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">City</label>
                  <p class="text-gray-800 font-medium">{{ authStore.user?.city || '—' }}</p>
                </div>
              </div>
            </section>

            <!-- ORCID Sync -->
            <section class="pt-6 border-t border-gray-100">
              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-gray-50 rounded-xl p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-[#a6ce39]/10 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-[#a6ce39]" viewBox="0 0 256 256" fill="currentColor">
                      <path d="M128 0C57.307 0 0 57.307 0 128s57.307 128 128 128 128-57.307 128-128S198.693 0 128 0z"/>
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-gray-800">ORCID Sync</p>
                    <p class="text-xs text-gray-500">
                      Last synced: {{ authStore.user?.last_orcid_sync ? new Date(authStore.user.last_orcid_sync).toLocaleString() : 'Never' }}
                    </p>
                  </div>
                </div>
                <button 
                  @click="syncOrcid" 
                  :disabled="authStore.isLoading"
                  class="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  <svg v-if="authStore.isLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  {{ authStore.isLoading ? 'Syncing...' : 'Sync from ORCID' }}
                </button>
              </div>
            </section>
          </div>

          <!-- Edit Mode -->
          <form v-else @submit.prevent="saveProfile" class="space-y-8">
            <!-- Personal Information -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100">Personal Information</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="full_name">Full Name</label>
                  <input 
                    id="full_name"
                    v-model="formData.full_name"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="Enter your full name"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="email">Email <span class="text-red-500">*</span></label>
                  <input 
                    id="email"
                    v-model="formData.email"
                    type="email"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="Enter your email"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="title">Academic Title</label>
                  <select id="title" v-model="formData.title" class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all bg-white">
                    <option value="">Select title</option>
                    <option v-for="[value, label] in titleOptions" :key="value" :value="value">
                      {{ label }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="phone">Phone</label>
                  <input 
                    id="phone"
                    v-model="formData.phone"
                    type="tel"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="+90 555 123 4567"
                  />
                </div>
              </div>
            </section>

            <!-- Academic Information -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100">Academic Information</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="institution">Institution <span class="text-red-500">*</span></label>
                  <input 
                    id="institution"
                    v-model="formData.institution"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="Enter your institution"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="department">Department</label>
                  <input 
                    id="department"
                    v-model="formData.department"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="Enter your department"
                  />
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Expertise Areas <span class="text-gray-400 font-normal">(max 10)</span></label>
                  <div class="flex gap-2 mb-3">
                    <input 
                      v-model="newExpertise"
                      type="text"
                      class="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                      placeholder="Add expertise area"
                      @keypress.enter.prevent="addExpertise"
                    />
                    <button 
                      type="button"
                      @click="addExpertise"
                      :disabled="!newExpertise.trim() || (formData.expertise_areas?.length ?? 0) >= 10"
                      class="px-5 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
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
                      <button type="button" @click="removeExpertise(index)" class="hover:text-red-600 transition-colors">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </span>
                  </div>
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="bio">Biography <span class="text-gray-400 font-normal">({{ bioCharCount }}/1000)</span></label>
                  <textarea 
                    id="bio"
                    v-model="formData.bio"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all resize-none"
                    placeholder="Write a short biography..."
                    maxlength="1000"
                    rows="4"
                  ></textarea>
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="website">Website</label>
                  <input 
                    id="website"
                    v-model="formData.website"
                    type="url"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="https://example.com"
                  />
                </div>
              </div>
            </section>

            <!-- Location -->
            <section>
              <h3 class="text-lg font-bold text-gray-800 mb-4 pb-2 border-b border-gray-100">Location</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="country">Country</label>
                  <select id="country" v-model="formData.country" class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all bg-white">
                    <option value="">Select country</option>
                    <option v-for="country in COUNTRIES" :key="country" :value="country">
                      {{ country }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2" for="city">City</label>
                  <input 
                    id="city"
                    v-model="formData.city"
                    type="text"
                    class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all"
                    placeholder="Enter your city"
                  />
                </div>
              </div>
            </section>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row justify-end gap-3 pt-6 border-t border-gray-100">
              <button 
                type="button"
                @click="cancelEditing"
                :disabled="isSaving"
                class="px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-gray-100 font-semibold rounded-xl transition-all order-2 sm:order-1"
              >
                Cancel
              </button>
              <button 
                type="submit"
                :disabled="isSaving"
                class="px-8 py-3 bg-primary-500 hover:bg-primary-600 text-white font-semibold rounded-xl shadow-lg shadow-primary-500/30 hover:shadow-xl transition-all flex items-center justify-center gap-2 order-1 sm:order-2 disabled:opacity-50"
              >
                <svg v-if="isSaving" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>
