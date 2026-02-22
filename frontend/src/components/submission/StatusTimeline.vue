<script setup lang="ts">
/**
 * TruEditor - Status Timeline Component
 * ======================================
 * Visual timeline of submission status changes.
 */
import { computed } from 'vue'
import { SUBMISSION_STATUS, type StatusHistoryEntry, type SubmissionStatus } from '@/types/submission'

const props = defineProps<{
  history: StatusHistoryEntry[]
  currentStatus: SubmissionStatus
  createdAt: string
}>()

const STATUS_ICONS: Record<string, string> = {
  draft: 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z',
  submitted: 'M12 19l9 2-9-18-9 18 9-2zm0 0v-8',
  under_review: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
  revision_required: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
  revision_submitted: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  accepted: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z',
  rejected: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
  withdrawn: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
  published: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
}

const DOT_COLORS: Record<string, string> = {
  draft: 'bg-gray-400',
  submitted: 'bg-blue-500',
  under_review: 'bg-purple-500',
  revision_required: 'bg-orange-500',
  revision_submitted: 'bg-indigo-500',
  accepted: 'bg-green-500',
  rejected: 'bg-red-500',
  withdrawn: 'bg-gray-500',
  published: 'bg-emerald-500',
}

interface TimelineItem {
  status: SubmissionStatus
  label: string
  date: string
  notes: string
  changedBy: string
  isFirst: boolean
  isCurrent: boolean
}

const timelineItems = computed<TimelineItem[]>(() => {
  const items: TimelineItem[] = []

  // Always add creation as first entry
  items.push({
    status: 'draft',
    label: 'Draft Created',
    date: props.createdAt,
    notes: '',
    changedBy: '',
    isFirst: true,
    isCurrent: props.history.length === 0,
  })

  // Add history entries (newest first from API, we reverse to oldest first)
  const sorted = [...props.history].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  )

  sorted.forEach((entry, i) => {
    items.push({
      status: entry.to_status,
      label: entry.to_status_display,
      date: entry.created_at,
      notes: entry.notes,
      changedBy: entry.changed_by_name,
      isFirst: false,
      isCurrent: i === sorted.length - 1,
    })
  })

  return items
})

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function formatTime(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="relative">
    <div v-if="timelineItems.length === 0" class="text-sm text-gray-500 text-center py-4">
      No status history available.
    </div>

    <div v-else class="space-y-0">
      <div
        v-for="(item, index) in timelineItems"
        :key="index"
        class="relative flex gap-3"
      >
        <!-- Line -->
        <div class="flex flex-col items-center">
          <div
            class="w-3 h-3 rounded-full flex-shrink-0 ring-2 ring-white"
            :class="[
              item.isCurrent ? DOT_COLORS[item.status] + ' ring-4 ring-opacity-20' : DOT_COLORS[item.status]
            ]"
          ></div>
          <div
            v-if="index < timelineItems.length - 1"
            class="w-0.5 flex-1 min-h-[2rem] bg-gray-200"
          ></div>
        </div>

        <!-- Content -->
        <div :class="['pb-5 -mt-0.5 min-w-0', index === timelineItems.length - 1 ? 'pb-0' : '']">
          <p class="text-sm font-semibold" :class="SUBMISSION_STATUS[item.status]?.color || 'text-gray-700'">
            {{ item.label }}
          </p>
          <p class="text-xs text-gray-500 mt-0.5">
            {{ formatDate(item.date) }} at {{ formatTime(item.date) }}
          </p>
          <p v-if="item.notes" class="text-xs text-gray-500 mt-1 italic">{{ item.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
