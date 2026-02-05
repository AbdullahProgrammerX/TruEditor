<script setup lang="ts">
/**
 * TruEditor - Status Badge Component
 * ===================================
 * Colored badge for displaying submission status.
 */

import { computed } from 'vue'
import { SUBMISSION_STATUS, type SubmissionStatus } from '@/types/submission'

interface Props {
  /** Status value */
  status: SubmissionStatus
  /** Badge size */
  size?: 'sm' | 'md' | 'lg'
  /** Show status icon */
  showIcon?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showIcon: false,
})

const statusInfo = computed(() => SUBMISSION_STATUS[props.status])

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-0.5 text-xs'
    case 'lg':
      return 'px-4 py-1.5 text-sm'
    default:
      return 'px-2.5 py-1 text-xs'
  }
})

// Status icons
const statusIcons: Record<SubmissionStatus, string> = {
  draft: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z',
  submitted: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  under_review: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
  revision_required: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
  revision_submitted: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
  accepted: 'M5 13l4 4L19 7',
  rejected: 'M6 18L18 6M6 6l12 12',
  withdrawn: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
  published: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
}
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 font-medium rounded-full transition-all"
    :class="[statusInfo.bgColor, statusInfo.color, sizeClasses]"
  >
    <svg 
      v-if="showIcon" 
      class="w-3.5 h-3.5" 
      fill="none" 
      viewBox="0 0 24 24" 
      stroke="currentColor"
      stroke-width="2"
    >
      <path stroke-linecap="round" stroke-linejoin="round" :d="statusIcons[status]" />
    </svg>
    {{ statusInfo.label }}
  </span>
</template>
