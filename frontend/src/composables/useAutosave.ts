/**
 * TruEditor - Auto-save Composable
 * ==================================
 * Debounced auto-save functionality for forms.
 */

import { ref, watch, onUnmounted, type Ref, type WatchSource } from 'vue'

export interface UseAutosaveOptions {
  /** Debounce delay in milliseconds */
  delay?: number
  /** Auto-save interval in milliseconds (0 to disable) */
  interval?: number
  /** Callback when save starts */
  onSaveStart?: () => void
  /** Callback when save completes */
  onSaveComplete?: () => void
  /** Callback on save error */
  onSaveError?: (error: Error) => void
}

export interface UseAutosaveReturn {
  /** Whether currently saving */
  isSaving: Ref<boolean>
  /** Last saved timestamp */
  lastSavedAt: Ref<Date | null>
  /** Error message if save failed */
  error: Ref<string | null>
  /** Whether there are unsaved changes */
  isDirty: Ref<boolean>
  /** Save status text */
  statusText: Ref<string>
  /** Manually trigger save */
  save: () => Promise<void>
  /** Reset dirty state */
  resetDirty: () => void
  /** Cancel pending save */
  cancel: () => void
}

/**
 * Auto-save composable
 * 
 * @param data - Reactive data to watch for changes
 * @param saveFn - Function to call when saving
 * @param options - Configuration options
 */
export function useAutosave<T>(
  data: WatchSource<T>,
  saveFn: () => Promise<void>,
  options: UseAutosaveOptions = {}
): UseAutosaveReturn {
  const {
    delay = 2000,
    interval = 30000,
    onSaveStart,
    onSaveComplete,
    onSaveError,
  } = options

  // State
  const isSaving = ref(false)
  const lastSavedAt = ref<Date | null>(null)
  const error = ref<string | null>(null)
  const isDirty = ref(false)

  // Timers
  let debounceTimer: ReturnType<typeof setTimeout> | null = null
  let intervalTimer: ReturnType<typeof setInterval> | null = null

  // Computed status text
  const statusText = ref('Not saved')

  function updateStatusText(): void {
    if (isSaving.value) {
      statusText.value = 'Saving...'
    } else if (error.value) {
      statusText.value = 'Save failed'
    } else if (lastSavedAt.value) {
      const now = new Date()
      const diff = now.getTime() - lastSavedAt.value.getTime()
      
      if (diff < 10000) {
        statusText.value = 'Saved just now'
      } else if (diff < 60000) {
        statusText.value = 'Saved a moment ago'
      } else {
        const minutes = Math.floor(diff / 60000)
        statusText.value = `Saved ${minutes} minute${minutes > 1 ? 's' : ''} ago`
      }
    } else {
      statusText.value = isDirty.value ? 'Unsaved changes' : 'Not saved'
    }
  }

  /**
   * Perform save
   */
  async function save(): Promise<void> {
    if (isSaving.value) return

    isSaving.value = true
    error.value = null
    updateStatusText()
    onSaveStart?.()

    try {
      await saveFn()
      lastSavedAt.value = new Date()
      isDirty.value = false
      onSaveComplete?.()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Save failed'
      onSaveError?.(err instanceof Error ? err : new Error('Save failed'))
    } finally {
      isSaving.value = false
      updateStatusText()
    }
  }

  /**
   * Debounced save
   */
  function debouncedSave(): void {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
    }

    debounceTimer = setTimeout(() => {
      if (isDirty.value) {
        save()
      }
    }, delay)
  }

  /**
   * Reset dirty state
   */
  function resetDirty(): void {
    isDirty.value = false
    updateStatusText()
  }

  /**
   * Cancel pending save
   */
  function cancel(): void {
    if (debounceTimer) {
      clearTimeout(debounceTimer)
      debounceTimer = null
    }
  }

  // Watch for data changes
  watch(
    data,
    () => {
      isDirty.value = true
      updateStatusText()
      debouncedSave()
    },
    { deep: true }
  )

  // Set up interval save
  if (interval > 0) {
    intervalTimer = setInterval(() => {
      if (isDirty.value && !isSaving.value) {
        save()
      }
    }, interval)
  }

  // Update status text periodically
  const statusTimer = setInterval(updateStatusText, 10000)

  // Cleanup
  onUnmounted(() => {
    cancel()
    if (intervalTimer) {
      clearInterval(intervalTimer)
    }
    clearInterval(statusTimer)
  })

  return {
    isSaving,
    lastSavedAt,
    error,
    isDirty,
    statusText,
    save,
    resetDirty,
    cancel,
  }
}

export default useAutosave
