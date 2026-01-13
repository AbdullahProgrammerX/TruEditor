<script setup lang="ts">
/**
 * TruEditor - User Profile Page
 * ==============================
 * Displays and manages user profile information.
 */
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ACADEMIC_TITLES, COUNTRIES, type UserProfileUpdate, type AcademicTitle } from '@/types/user'

const router = useRouter()
const authStore = useAuthStore()

// Edit mode state
const isEditing = ref(false)
const isSaving = ref(false)
const saveError = ref<string | null>(null)
const saveSuccess = ref(false)

// Form data - reactive copy of user data
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

// Expertise area input
const newExpertise = ref('')

// Initialize form with user data
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

// Enter edit mode
function startEditing() {
  initForm()
  isEditing.value = true
  saveError.value = null
  saveSuccess.value = false
}

// Cancel editing
function cancelEditing() {
  isEditing.value = false
  saveError.value = null
}

// Add expertise area
function addExpertise() {
  const value = newExpertise.value.trim()
  if (value && formData.expertise_areas && formData.expertise_areas.length < 10) {
    if (!formData.expertise_areas.includes(value)) {
      formData.expertise_areas.push(value)
    }
    newExpertise.value = ''
  }
}

// Remove expertise area
function removeExpertise(index: number) {
  formData.expertise_areas?.splice(index, 1)
}

// Save profile
async function saveProfile() {
  isSaving.value = true
  saveError.value = null
  saveSuccess.value = false

  try {
    await authStore.updateProfile(formData)
    isEditing.value = false
    saveSuccess.value = true
    
    // Hide success message after 3 seconds
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (err: any) {
    saveError.value = err.response?.data?.error?.message || 'Failed to save profile'
  } finally {
    isSaving.value = false
  }
}

// Sync ORCID
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

// Computed values
const titleOptions = computed(() => Object.entries(ACADEMIC_TITLES))
const bioCharCount = computed(() => formData.bio?.length || 0)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="router.push('/dashboard')" class="btn-ghost">
            ← Dashboard
          </button>
          <h1 class="text-lg font-semibold text-gray-800">Profile</h1>
          <div class="w-20"></div>
        </div>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 py-8">
      <!-- Success Message -->
      <div v-if="saveSuccess" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
        ✓ Profile updated successfully
      </div>

      <!-- Error Message -->
      <div v-if="saveError" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
        {{ saveError }}
      </div>

      <!-- Profile Card -->
      <div class="card">
        <!-- Header with Avatar -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-6">
            <!-- Avatar -->
            <div class="w-20 h-20 bg-primary-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {{ authStore.fullName?.charAt(0) || 'U' }}
            </div>
            
            <div>
              <h2 class="text-2xl font-bold text-gray-800">{{ authStore.fullName }}</h2>
              <a 
                :href="authStore.orcidUrl"
                target="_blank"
                class="text-orcid hover:underline flex items-center gap-1"
              >
                <svg class="w-4 h-4" viewBox="0 0 256 256">
                  <path fill="#A6CE39" d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128S57.3 0 128 0s128 57.3 128 128"/>
                  <path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 57.7c-5.7 0-10.3-4.6-10.3-10.3s4.6-10.3 10.3-10.3s10.3 4.6 10.3 10.3s-4.6 10.3-10.3 10.3zM108.9 79.1h41.6c39.6 0 57 28.3 57 53.6c0 27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7v79.4z"/>
                </svg>
                {{ authStore.orcidId }}
              </a>
              <p v-if="!authStore.profileCompleted" class="text-sm text-amber-600 mt-1">
                ⚠ Please complete your profile
              </p>
            </div>
          </div>

          <!-- Edit Button -->
          <button 
            v-if="!isEditing"
            @click="startEditing"
            class="btn-primary"
          >
            Edit Profile
          </button>
        </div>

        <!-- View Mode -->
        <div v-if="!isEditing" class="space-y-8">
          <!-- Personal Information -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Personal Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label">Full Name</label>
                <p class="text-gray-800">{{ authStore.user?.full_name || 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">Email</label>
                <p class="text-gray-800">{{ authStore.user?.email || 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">Title</label>
                <p class="text-gray-800">{{ authStore.user?.title ? ACADEMIC_TITLES[authStore.user.title as AcademicTitle] : 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">Phone</label>
                <p class="text-gray-800">{{ authStore.user?.phone || 'Not specified' }}</p>
              </div>
            </div>
          </section>

          <!-- Academic Information -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Academic Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label">Institution</label>
                <p class="text-gray-800">{{ authStore.user?.institution || 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">Department</label>
                <p class="text-gray-800">{{ authStore.user?.department || 'Not specified' }}</p>
              </div>
              <div class="md:col-span-2">
                <label class="label">Expertise Areas</label>
                <div v-if="authStore.user?.expertise_areas?.length" class="flex flex-wrap gap-2">
                  <span 
                    v-for="area in authStore.user.expertise_areas" 
                    :key="area"
                    class="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                  >
                    {{ area }}
                  </span>
                </div>
                <p v-else class="text-gray-500">Not specified</p>
              </div>
              <div class="md:col-span-2">
                <label class="label">Biography</label>
                <p class="text-gray-800 whitespace-pre-wrap">{{ authStore.user?.bio || 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">Website</label>
                <a 
                  v-if="authStore.user?.website" 
                  :href="authStore.user.website" 
                  target="_blank"
                  class="text-primary-600 hover:underline"
                >
                  {{ authStore.user.website }}
                </a>
                <p v-else class="text-gray-500">Not specified</p>
              </div>
            </div>
          </section>

          <!-- Location -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Location</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label">Country</label>
                <p class="text-gray-800">{{ authStore.user?.country || 'Not specified' }}</p>
              </div>
              <div>
                <label class="label">City</label>
                <p class="text-gray-800">{{ authStore.user?.city || 'Not specified' }}</p>
              </div>
              <div class="md:col-span-2">
                <label class="label">Address</label>
                <p class="text-gray-800">{{ authStore.user?.address || 'Not specified' }}</p>
              </div>
            </div>
          </section>

          <!-- ORCID Sync -->
          <section class="pt-6 border-t">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-500">
                  Last synced: {{ authStore.user?.last_orcid_sync ? new Date(authStore.user.last_orcid_sync).toLocaleString() : 'Never' }}
                </p>
              </div>
              <button @click="syncOrcid" class="btn-outline" :disabled="authStore.isLoading">
                <span v-if="authStore.isLoading">Syncing...</span>
                <span v-else>Sync from ORCID</span>
              </button>
            </div>
          </section>
        </div>

        <!-- Edit Mode -->
        <form v-else @submit.prevent="saveProfile" class="space-y-8">
          <!-- Personal Information -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Personal Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label" for="given_name">First Name</label>
                <input 
                  id="given_name"
                  v-model="formData.given_name"
                  type="text"
                  class="input"
                  placeholder="Enter your first name"
                />
              </div>
              <div>
                <label class="label" for="family_name">Last Name</label>
                <input 
                  id="family_name"
                  v-model="formData.family_name"
                  type="text"
                  class="input"
                  placeholder="Enter your last name"
                />
              </div>
              <div>
                <label class="label" for="full_name">Full Name</label>
                <input 
                  id="full_name"
                  v-model="formData.full_name"
                  type="text"
                  class="input"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label class="label" for="email">Email *</label>
                <input 
                  id="email"
                  v-model="formData.email"
                  type="email"
                  class="input"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div>
                <label class="label" for="title">Academic Title</label>
                <select id="title" v-model="formData.title" class="input">
                  <option v-for="[value, label] in titleOptions" :key="value" :value="value">
                    {{ label }}
                  </option>
                </select>
              </div>
              <div>
                <label class="label" for="phone">Phone</label>
                <input 
                  id="phone"
                  v-model="formData.phone"
                  type="tel"
                  class="input"
                  placeholder="+90 555 123 4567"
                />
              </div>
            </div>
          </section>

          <!-- Academic Information -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Academic Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label" for="institution">Institution *</label>
                <input 
                  id="institution"
                  v-model="formData.institution"
                  type="text"
                  class="input"
                  placeholder="Enter your institution"
                  required
                />
              </div>
              <div>
                <label class="label" for="department">Department</label>
                <input 
                  id="department"
                  v-model="formData.department"
                  type="text"
                  class="input"
                  placeholder="Enter your department"
                />
              </div>
              <div class="md:col-span-2">
                <label class="label">Expertise Areas (max 10)</label>
                <div class="flex gap-2 mb-2">
                  <input 
                    v-model="newExpertise"
                    type="text"
                    class="input flex-1"
                    placeholder="Add expertise area"
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
                    <button type="button" @click="removeExpertise(index)" class="hover:text-red-600">
                      ×
                    </button>
                  </span>
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="label" for="bio">Biography ({{ bioCharCount }}/1000)</label>
                <textarea 
                  id="bio"
                  v-model="formData.bio"
                  class="input min-h-[120px]"
                  placeholder="Write a short biography..."
                  maxlength="1000"
                  rows="4"
                ></textarea>
              </div>
              <div class="md:col-span-2">
                <label class="label" for="website">Website</label>
                <input 
                  id="website"
                  v-model="formData.website"
                  type="url"
                  class="input"
                  placeholder="https://example.com"
                />
              </div>
            </div>
          </section>

          <!-- Location -->
          <section>
            <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-2 border-b">Location</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="label" for="country">Country</label>
                <select id="country" v-model="formData.country" class="input">
                  <option value="">Select country</option>
                  <option v-for="country in COUNTRIES" :key="country" :value="country">
                    {{ country }}
                  </option>
                </select>
              </div>
              <div>
                <label class="label" for="city">City</label>
                <input 
                  id="city"
                  v-model="formData.city"
                  type="text"
                  class="input"
                  placeholder="Enter your city"
                />
              </div>
              <div class="md:col-span-2">
                <label class="label" for="address">Address</label>
                <textarea 
                  id="address"
                  v-model="formData.address"
                  class="input"
                  placeholder="Enter your mailing address"
                  rows="2"
                ></textarea>
              </div>
            </div>
          </section>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-4 pt-6 border-t">
            <button 
              type="button"
              @click="cancelEditing"
              class="btn-ghost"
              :disabled="isSaving"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="btn-primary"
              :disabled="isSaving"
            >
              <span v-if="isSaving">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>
