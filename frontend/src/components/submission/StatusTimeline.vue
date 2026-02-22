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
