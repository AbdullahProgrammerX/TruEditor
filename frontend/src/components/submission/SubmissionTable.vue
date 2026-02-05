<script setup lang="ts">
/**
 * TruEditor - Submission Table Component
 * =======================================
 * Table component for displaying submission list in dashboard.
 * Features: Skeleton loading, status badges, staggered animations, pagination.
 */

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StatusBadge from '@/components/common/StatusBadge.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import type { SubmissionListItem } from '@/types/submission'

interface Props {
  /** Submission items to display */
  items: SubmissionListItem[]
  /** Loading state */
  loading?: boolean
  /** Current page */
  currentPage?: number
  /** Total pages */
  totalPages?: number
  /** Empty state message */
  emptyMessage?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  currentPage: 1,
  totalPages: 1,
  emptyMessage: 'No submissions found',
})

const emit = defineEmits<{
  pageChange: [page: number]
  delete: [id: string]
  view: [id: string]
  edit: [id: string]
}>()

const router = useRouter()
const activeDropdown = ref<string | null>(null)

/**
 * Format date for display
 */
function formatDate(dateStr: string | null): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date)
}

/**
 * Format relative time
 */
function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  if (days < 30) return `${Math.floor(days / 7)} weeks ago`
  if (days < 365) return `${Math.floor(days / 30)} months ago`
  return `${Math.floor(days / 365)} years ago`
}

/**
 * Toggle dropdown menu
 */
function toggleDropdown(id: string): void {
  activeDropdown.value = activeDropdown.value === id ? null : id
}

/**
 * Close dropdown on outside click
 */
function closeDropdown(): void {
  activeDropdown.value = null
}

/**
 * Handle view action
 */
function handleView(item: SubmissionListItem): void {
  closeDropdown()
  emit('view', item.id)
  router.push(`/submissions/${item.id}`)
}

/**
 * Handle edit action
 */
function handleEdit(item: SubmissionListItem): void {
  closeDropdown()
  emit('edit', item.id)
  router.push(`/submissions/${item.id}/edit`)
}

/**
 * Handle delete action
 */
function handleDelete(item: SubmissionListItem): void {
  closeDropdown()
  emit('delete', item.id)
}

/**
 * Check if item can be edited
 */
function canEdit(item: SubmissionListItem): boolean {
  return item.status === 'draft' || item.status === 'revision_required'
}

/**
 * Check if item can be deleted
 */
function canDelete(item: SubmissionListItem): boolean {
  return item.status === 'draft'
}

/**
 * Get stagger animation delay
 */
function getAnimationDelay(index: number): string {
  return `${index * 50}ms`
}
</script>

<template>
  <div class="submission-table">
    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div class="p-6">
        <SkeletonLoader type="table" :rows="5" />
      </div>
    </div>

    <!-- Empty State -->
    <div 
      v-else-if="items.length === 0" 
      class="bg-white rounded-xl border border-gray-100 p-12 text-center"
    >
      <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ emptyMessage }}</h3>
      <p class="text-gray-500 mb-6">Start by creating a new submission.</p>
      <router-link 
        to="/submissions/new" 
        class="inline-flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        New Submission
      </router-link>
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Manuscript
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Authors
              </th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Last Updated
              </th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr
              v-for="(item, index) in items"
              :key="item.id"
              class="group hover:bg-gray-50 transition-colors animate-fade-in-up"
              :style="{ animationDelay: getAnimationDelay(index) }"
            >
              <!-- Manuscript Info -->
              <td class="px-6 py-4">
                <div class="flex items-start gap-3">
                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-900 truncate max-w-md group-hover:text-primary-600 transition-colors">
                      {{ item.title || 'Untitled' }}
                    </p>
                    <div class="flex items-center gap-2 mt-1 text-sm text-gray-500">
                      <span v-if="item.manuscript_id" class="font-mono">
                        {{ item.manuscript_id }}
                      </span>
                      <span v-else class="italic">Draft</span>
                      <span class="text-gray-300">|</span>
                      <span>{{ item.article_type.replace('_', ' ') }}</span>
                    </div>
                  </div>
                </div>
              </td>

              <!-- Status -->
              <td class="px-6 py-4">
                <StatusBadge :status="item.status" :show-icon="true" />
              </td>

              <!-- Authors -->
              <td class="px-6 py-4">
                <div v-if="item.corresponding_author" class="text-sm">
                  <p class="text-gray-900">{{ item.corresponding_author.name }}</p>
                  <p class="text-gray-500">
                    {{ item.author_count > 1 ? `+${item.author_count - 1} more` : 'Sole author' }}
                  </p>
                </div>
                <span v-else class="text-sm text-gray-400 italic">No authors</span>
              </td>

              <!-- Last Updated -->
              <td class="px-6 py-4">
                <div class="text-sm">
                  <p class="text-gray-900">{{ formatRelativeTime(item.updated_at) }}</p>
                  <p class="text-gray-500">{{ formatDate(item.updated_at) }}</p>
                </div>
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 text-right">
                <div class="relative inline-block">
                  <button
                    @click="toggleDropdown(item.id)"
                    class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </button>

                  <!-- Dropdown Menu -->
                  <Transition
                    enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95"
                    enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100"
                    leave-to-class="transform opacity-0 scale-95"
                  >
                    <div
                      v-if="activeDropdown === item.id"
                      class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-10"
                      @click.away="closeDropdown"
                    >
                      <button
                        @click="handleView(item)"
                        class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Details
                      </button>

                      <button
                        v-if="canEdit(item)"
                        @click="handleEdit(item)"
                        class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                        Edit
                      </button>

                      <button
                        v-if="canDelete(item)"
                        @click="handleDelete(item)"
                        class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                      >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Delete
                      </button>
                    </div>
                  </Transition>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div 
        v-if="totalPages > 1" 
        class="px-6 py-4 border-t border-gray-100 flex items-center justify-between"
      >
        <p class="text-sm text-gray-500">
          Page {{ currentPage }} of {{ totalPages }}
        </p>
        <div class="flex items-center gap-2">
          <button
            :disabled="currentPage === 1"
            @click="emit('pageChange', currentPage - 1)"
            class="px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Previous
          </button>
          <button
            :disabled="currentPage === totalPages"
            @click="emit('pageChange', currentPage + 1)"
            class="px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
