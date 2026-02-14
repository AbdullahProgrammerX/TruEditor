<script setup lang="ts">
/**
 * TruEditor - Wizard Step 4: Authors
 * ====================================
 * Author management with drag-and-drop reordering.
 */

import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { COUNTRIES } from '@/types/user'
import type { AuthorInput } from '@/types/submission'

// Local form type with all fields required for form binding
interface AuthorFormData {
  given_name: string
  family_name: string
  email: string
  orcid_id: string
  institution: string
  department: string
  country: string
  city: string
  is_corresponding: boolean
  contribution: string
  order?: number
  user?: string | null
}

interface Props {
  /** Authors list */
  authors?: AuthorInput[]
}

const props = withDefaults(defineProps<Props>(), {
  authors: () => [],
})

const emit = defineEmits<{
  'update:authors': [value: AuthorInput[]]
}>()

const authStore = useAuthStore()
const localAuthors = ref<AuthorFormData[]>([...props.authors.map(a => ({
  given_name: a.given_name || '',
  family_name: a.family_name || '',
  email: a.email || '',
  orcid_id: a.orcid_id || '',
  institution: a.institution || '',
  department: a.department || '',
  country: a.country || '',
  city: a.city || '',
  is_corresponding: a.is_corresponding || false,
  contribution: a.contribution || '',
  order: a.order,
  user: a.user,
}))])
const showModal = ref(false)
const editingIndex = ref<number | null>(null)

// Form state
const authorForm = ref<AuthorFormData>({
  given_name: '',
  family_name: '',
  email: '',
  orcid_id: '',
  institution: '',
  department: '',
  country: '',
  city: '',
  is_corresponding: false,
  contribution: '',
})

// Watch and emit changes
watch(localAuthors, (val) => {
  emit('update:authors', val as AuthorInput[])
}, { deep: true })

// Computed
const hasCorresponding = computed(() => 
  localAuthors.value.some(a => a.is_corresponding)
)

const isFormValid = computed(() => {
  const f = authorForm.value
  return f.given_name.trim() && 
         f.family_name.trim() && 
         f.email.trim() && 
         f.institution.trim()
})

/**
 * Open modal for new author
 */
function openAddModal(): void {
  editingIndex.value = null
  authorForm.value = {
    given_name: '',
    family_name: '',
    email: '',
    orcid_id: '',
    institution: '',
    department: '',
    country: '',
    city: '',
    is_corresponding: !hasCorresponding.value,
    contribution: '',
  }
  showModal.value = true
}

/**
 * Add current user as author.
 * Fetches fresh profile if needed and uses full_name fallback for given/family.
 */
async function addSelfAsAuthor(): Promise<void> {
  if (!authStore.user) return

  let user = authStore.user
  if (!(user.given_name || '').trim() || !(user.family_name || '').trim() || !(user.institution || '').trim()) {
    await authStore.fetchProfile()
    user = authStore.user
    if (!user) return
  }

  let given = (user.given_name || '').trim()
  let family = (user.family_name || '').trim()
  if (!given || !family) {
    const parts = (user.full_name || '').trim().split(/\s+/).filter(Boolean)
    given = given || parts[0] || 'Author'
    family = family || (parts.slice(1).join(' ') || parts[0] || 'Name')
  }

  const email = (user.email || '').trim()
  if (!email) {
    ;(window as any).toast?.('error', 'Please add your email in Profile first.')
    return
  }

  const institution = (user.institution || '').trim()
  if (!institution) {
    ;(window as any).toast?.('error', 'Please add your institution in Profile first.')
    return
  }

  const newAuthor: AuthorFormData = {
    given_name: given,
    family_name: family,
    email,
    orcid_id: user.orcid_id || '',
    institution,
    department: user.department || '',
    country: user.country || '',
    city: user.city || '',
    is_corresponding: !hasCorresponding.value,
    contribution: '',
    order: localAuthors.value.length + 1,
  }

  localAuthors.value.push(newAuthor)
}

/**
 * Open modal for editing
 */
function openEditModal(index: number): void {
  const author = localAuthors.value[index]
  if (!author) return
  
  editingIndex.value = index
  authorForm.value = { ...author }
  showModal.value = true
}

/**
 * Save author (add or update)
 */
function saveAuthor(): void {
  if (!isFormValid.value) return
  
  const author: AuthorFormData = {
    ...authorForm.value,
    order: editingIndex.value !== null 
      ? (localAuthors.value[editingIndex.value]?.order ?? localAuthors.value.length + 1)
      : localAuthors.value.length + 1,
  }
  
  // If setting as corresponding, unset others
  if (author.is_corresponding) {
    localAuthors.value.forEach(a => a.is_corresponding = false)
  }
  
  if (editingIndex.value !== null && localAuthors.value[editingIndex.value]) {
    localAuthors.value[editingIndex.value] = author
  } else if (editingIndex.value === null) {
    localAuthors.value.push(author)
  }
  
  closeModal()
}

/**
 * Remove author
 */
function removeAuthor(index: number): void {
  localAuthors.value.splice(index, 1)
  // Reorder
  localAuthors.value.forEach((a, i) => a.order = i + 1)
}

/**
 * Move author up
 */
function moveUp(index: number): void {
  if (index === 0) return
  const current = localAuthors.value[index]
  const previous = localAuthors.value[index - 1]
  if (!current || !previous) return
  
  localAuthors.value[index] = previous
  localAuthors.value[index - 1] = current
  // Update order
  localAuthors.value.forEach((a, i) => a.order = i + 1)
}

/**
 * Move author down
 */
function moveDown(index: number): void {
  if (index === localAuthors.value.length - 1) return
  const current = localAuthors.value[index]
  const next = localAuthors.value[index + 1]
  if (!current || !next) return
  
  localAuthors.value[index] = next
  localAuthors.value[index + 1] = current
  // Update order
  localAuthors.value.forEach((a, i) => a.order = i + 1)
}

/**
 * Set as corresponding author
 */
function setCorresponding(index: number): void {
  localAuthors.value.forEach((a, i) => {
    a.is_corresponding = i === index
  })
}

/**
 * Close modal
 */
function closeModal(): void {
  showModal.value = false
  editingIndex.value = null
}

/**
 * Check if user is already added
 */
const isUserAdded = computed(() => {
  if (!authStore.user) return false
  return localAuthors.value.some(a => a.orcid_id === authStore.user?.orcid_id)
})
</script>

<template>
  <div class="step-authors">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Authors</h3>
      <p class="mt-1 text-sm text-gray-500">
        Add all authors of the manuscript. Use drag handles to reorder.
      </p>
    </div>

    <!-- Quick Add Self -->
    <div v-if="!isUserAdded" class="mb-6 p-4 bg-primary-50 rounded-xl border border-primary-100">
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-primary-900">Add yourself as an author</p>
          <p class="text-sm text-primary-700">
            {{ authStore.fullName }} ({{ authStore.orcidId }})
          </p>
        </div>
        <button
          @click="addSelfAsAuthor"
          class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
        >
          Add Me
        </button>
      </div>
    </div>

    <!-- Authors List -->
    <div v-if="localAuthors.length > 0" class="space-y-3 mb-6">
      <div
        v-for="(author, index) in localAuthors"
        :key="index"
        class="author-card"
      >
        <div class="flex items-start gap-4">
          <!-- Order Badge -->
          <div class="flex flex-col items-center gap-1">
            <span class="w-8 h-8 flex items-center justify-center bg-gray-100 text-gray-600 rounded-full font-semibold text-sm">
              {{ index + 1 }}
            </span>
            <div class="flex flex-col gap-0.5">
              <button
                @click="moveUp(index)"
                :disabled="index === 0"
                class="p-0.5 text-gray-400 hover:text-gray-600 disabled:opacity-30"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
              </button>
              <button
                @click="moveDown(index)"
                :disabled="index === localAuthors.length - 1"
                class="p-0.5 text-gray-400 hover:text-gray-600 disabled:opacity-30"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Author Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <h4 class="font-medium text-gray-900">
                {{ author.given_name }} {{ author.family_name }}
              </h4>
              <span 
                v-if="author.is_corresponding"
                class="px-2 py-0.5 bg-accent-100 text-accent-700 text-xs font-medium rounded-full"
              >
                Corresponding
              </span>
            </div>
            <p class="text-sm text-gray-500">{{ author.email }}</p>
            <p class="text-sm text-gray-500">
              {{ [author.department, author.institution, author.country].filter(Boolean).join(', ') }}
            </p>
            <p v-if="author.orcid_id" class="text-sm text-orcid-500 mt-1">
              ORCID: {{ author.orcid_id }}
            </p>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center gap-2">
            <button
              v-if="!author.is_corresponding"
              @click="setCorresponding(index)"
              class="p-2 text-gray-400 hover:text-accent-500 hover:bg-accent-50 rounded-lg transition-colors"
              title="Set as corresponding author"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </button>
            <button
              @click="openEditModal(index)"
              class="p-2 text-gray-400 hover:text-primary-500 hover:bg-primary-50 rounded-lg transition-colors"
              title="Edit"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              @click="removeAuthor(index)"
              class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              title="Remove"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8 bg-gray-50 rounded-xl mb-6">
      <svg class="w-12 h-12 mx-auto text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <p class="text-gray-600 font-medium">No authors added yet</p>
      <p class="text-sm text-gray-500">Add at least one author to continue</p>
    </div>

    <!-- Add Author Button -->
    <button
      @click="openAddModal"
      class="w-full py-3 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 hover:border-primary-400 hover:text-primary-600 hover:bg-primary-50 transition-all flex items-center justify-center gap-2"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      Add Author
    </button>

    <!-- Validation Messages -->
    <div v-if="localAuthors.length === 0" class="mt-4 flex items-center gap-2 text-amber-600">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-sm font-medium">At least one author is required</span>
    </div>
    
    <div v-else-if="!hasCorresponding" class="mt-4 flex items-center gap-2 text-amber-600">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-sm font-medium">Please designate a corresponding author</span>
    </div>

    <!-- Author Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/50" @click="closeModal" />
          
          <!-- Modal Content -->
          <div class="relative bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div class="sticky top-0 bg-white px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">
                {{ editingIndex !== null ? 'Edit Author' : 'Add Author' }}
              </h3>
              <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div class="p-6 space-y-4">
              <!-- Name -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    First Name <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="authorForm.given_name"
                    type="text"
                    class="input-field"
                    placeholder="First name"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Last Name <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="authorForm.family_name"
                    type="text"
                    class="input-field"
                    placeholder="Last name"
                  />
                </div>
              </div>
              
              <!-- Email -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Email <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="authorForm.email"
                  type="email"
                  class="input-field"
                  placeholder="author@institution.edu"
                />
              </div>
              
              <!-- ORCID -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  ORCID ID
                </label>
                <input
                  v-model="authorForm.orcid_id"
                  type="text"
                  class="input-field"
                  placeholder="0000-0000-0000-0000"
                />
              </div>
              
              <!-- Institution -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Institution <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="authorForm.institution"
                  type="text"
                  class="input-field"
                  placeholder="University or organization"
                />
              </div>
              
              <!-- Department -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Department
                </label>
                <input
                  v-model="authorForm.department"
                  type="text"
                  class="input-field"
                  placeholder="Department or division"
                />
              </div>
              
              <!-- Location -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Country
                  </label>
                  <select v-model="authorForm.country" class="input-field">
                    <option value="">Select country</option>
                    <option v-for="country in COUNTRIES" :key="country" :value="country">
                      {{ country }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    City
                  </label>
                  <input
                    v-model="authorForm.city"
                    type="text"
                    class="input-field"
                    placeholder="City"
                  />
                </div>
              </div>
              
              <!-- Corresponding Author -->
              <div>
                <label class="flex items-center gap-2 cursor-pointer">
                  <input
                    v-model="authorForm.is_corresponding"
                    type="checkbox"
                    class="w-4 h-4 text-primary-500 rounded border-gray-300 focus:ring-primary-500"
                  />
                  <span class="text-sm font-medium text-gray-700">Corresponding Author</span>
                </label>
                <p class="mt-1 text-xs text-gray-500 ml-6">
                  The corresponding author handles all communication with the journal.
                </p>
              </div>
            </div>
            
            <!-- Modal Footer -->
            <div class="sticky bottom-0 bg-gray-50 px-6 py-4 border-t border-gray-100 flex items-center justify-end gap-3">
              <button
                @click="closeModal"
                class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                @click="saveAuthor"
                :disabled="!isFormValid"
                class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ editingIndex !== null ? 'Save Changes' : 'Add Author' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.author-card {
  padding: 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
}

.author-card:hover {
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.input-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  transition: box-shadow 0.2s ease;
}

.input-field:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary-500, #1e3a5f);
  border-color: var(--color-primary-500, #1e3a5f);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.2s ease;
}

.modal-enter-from .relative {
  transform: scale(0.95);
}

.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>
