/**
 * TruEditor - Submission Store (Pinia)
 * =====================================
 * State management for manuscript submissions and wizard.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'
import type {
  Submission,
  SubmissionListItem,
  SubmissionCreateInput,
  SubmissionUpdateInput,
  SubmissionFilters,
  SubmissionStats,
  SubmissionStatus,
  WizardData,
  Author,
  AuthorInput,
} from '@/types/submission'

export const useSubmissionStore = defineStore('submission', () => {
  // ============================================
  // STATE
  // ============================================
  
  // List state
  const submissions = ref<SubmissionListItem[]>([])
  const totalCount = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const filters = ref<SubmissionFilters>({})
  
  // Current submission state
  const currentSubmission = ref<Submission | null>(null)
  
  // Loading states
  const isLoading = ref(false)
  const isLoadingDetail = ref(false)
  const isSaving = ref(false)
  
  // Error state
  const error = ref<string | null>(null)
  
  // Wizard state
  const wizardStep = ref(1)
  const wizardData = ref<WizardData>({})
  const isDirty = ref(false)
  const lastSavedAt = ref<string | null>(null)
  
  // ============================================
  // GETTERS
  // ============================================
  
  /**
   * Submission statistics
   */
  const stats = computed<SubmissionStats>(() => {
    const all = submissions.value
    return {
      total: totalCount.value,
      draft: all.filter(s => s.status === 'draft').length,
      submitted: all.filter(s => s.status === 'submitted').length,
      under_review: all.filter(s => s.status === 'under_review').length,
      revision_required: all.filter(s => s.status === 'revision_required').length,
      accepted: all.filter(s => s.status === 'accepted').length,
      rejected: all.filter(s => s.status === 'rejected').length,
      published: all.filter(s => s.status === 'published').length,
    }
  })
  
  /**
   * Draft submissions count
   */
  const draftCount = computed(() => submissions.value.filter(s => s.status === 'draft').length)
  
  /**
   * Submitted submissions count
   */
  const submittedCount = computed(() => submissions.value.filter(s => s.status === 'submitted').length)
  
  /**
   * Revision required count
   */
  const revisionCount = computed(() => submissions.value.filter(s => s.status === 'revision_required').length)
  
  /**
   * Accepted count
   */
  const acceptedCount = computed(() => submissions.value.filter(s => s.status === 'accepted').length)
  
  /**
   * Filter submissions by status
   */
  const byStatus = computed(() => (status: SubmissionStatus) => {
    return submissions.value.filter(s => s.status === status)
  })
  
  /**
   * Has next page
   */
  const hasNextPage = computed(() => {
    return currentPage.value * pageSize.value < totalCount.value
  })
  
  /**
   * Has previous page
   */
  const hasPrevPage = computed(() => currentPage.value > 1)
  
  /**
   * Total pages
   */
  const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))
  
  /**
   * Current submission is editable
   */
  const isEditable = computed(() => currentSubmission.value?.is_editable ?? false)
  
  /**
   * Wizard progress percentage
   */
  const wizardProgress = computed(() => ((wizardStep.value - 1) / 5) * 100)
  
  // ============================================
  // ACTIONS - List Operations
  // ============================================
  
  /**
   * Fetch submissions list with filters
   */
  async function fetchSubmissions(newFilters?: SubmissionFilters): Promise<void> {
    isLoading.value = true
    error.value = null
    
    if (newFilters) {
      filters.value = { ...filters.value, ...newFilters }
    }
    
    try {
      const params = new URLSearchParams()
      
      if (filters.value.status) params.append('status', filters.value.status)
      if (filters.value.article_type) params.append('article_type', filters.value.article_type)
      if (filters.value.search) params.append('search', filters.value.search)
      if (filters.value.ordering) params.append('ordering', filters.value.ordering)
      
      params.append('page', String(currentPage.value))
      params.append('page_size', String(pageSize.value))
      
      const response = await api.get(`/submissions/?${params.toString()}`)
      
      // Handle both wrapped ({success, data: {count, results}}) and
      // unwrapped ({count, results}) response formats
      const payload = response.data?.data ?? response.data
      submissions.value = payload.results ?? []
      totalCount.value = payload.count ?? 0
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to load submissions'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Set current page and fetch
   */
  async function setPage(page: number): Promise<void> {
    currentPage.value = page
    await fetchSubmissions()
  }
  
  /**
   * Set page size and fetch
   */
  async function setPageSize(size: number): Promise<void> {
    pageSize.value = size
    currentPage.value = 1
    await fetchSubmissions()
  }
  
  /**
   * Filter by status
   */
  async function filterByStatus(status: SubmissionStatus | undefined): Promise<void> {
    currentPage.value = 1
    await fetchSubmissions({ status })
  }
  
  /**
   * Search submissions
   */
  async function search(query: string): Promise<void> {
    currentPage.value = 1
    await fetchSubmissions({ search: query })
  }
  
  /**
   * Clear filters
   */
  async function clearFilters(): Promise<void> {
    filters.value = {}
    currentPage.value = 1
    await fetchSubmissions()
  }
  
  // ============================================
  // ACTIONS - CRUD Operations
  // ============================================
  
  /**
   * Fetch single submission detail
   */
  async function fetchSubmission(id: string): Promise<Submission> {
    isLoadingDetail.value = true
    error.value = null
    
    try {
      const response = await api.get<{ data: Submission }>(`/submissions/${id}/`)
      currentSubmission.value = response.data.data
      
      // Sync wizard state
      wizardStep.value = response.data.data.wizard_step
      wizardData.value = response.data.data.wizard_data || {}
      isDirty.value = false
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to load submission'
      throw err
    } finally {
      isLoadingDetail.value = false
    }
  }
  
  /**
   * Create new submission (draft)
   */
  async function createSubmission(data: SubmissionCreateInput = {}): Promise<Submission> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.post<{ data: Submission }>('/submissions/', data)
      currentSubmission.value = response.data.data
      
      // Initialize wizard
      wizardStep.value = 1
      wizardData.value = {}
      isDirty.value = false
      
      // Add to list if exists
      if (submissions.value.length > 0) {
        await fetchSubmissions()
      }
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to create submission'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Update submission
   */
  async function updateSubmission(id: string, data: SubmissionUpdateInput): Promise<Submission> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.patch<{ data: Submission }>(`/submissions/${id}/`, data)
      currentSubmission.value = response.data.data
      isDirty.value = false
      lastSavedAt.value = new Date().toISOString()
      
      // Update in list
      const index = submissions.value.findIndex(s => s.id === id)
      if (index !== -1) {
        const existingItem = submissions.value[index]
        if (existingItem) {
          submissions.value[index] = {
            ...existingItem,
            title: response.data.data.title,
            article_type: response.data.data.article_type,
            status: response.data.data.status,
            status_display: response.data.data.status_display,
            updated_at: response.data.data.updated_at,
          }
        }
      }
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to update submission'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Delete submission (only drafts)
   */
  async function deleteSubmission(id: string): Promise<void> {
    isSaving.value = true
    error.value = null
    
    try {
      await api.delete(`/submissions/${id}/`)
      
      // Remove from list
      submissions.value = submissions.value.filter(s => s.id !== id)
      totalCount.value--
      
      // Clear current if it was deleted
      if (currentSubmission.value?.id === id) {
        currentSubmission.value = null
      }
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to delete submission'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  // ============================================
  // ACTIONS - Submission Actions
  // ============================================
  
  /**
   * Submit for review
   */
  async function submitForReview(id: string): Promise<Submission> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.post<{ data: Submission }>(`/submissions/${id}/submit/`, {
        confirm: true
      })
      currentSubmission.value = response.data.data
      
      // Update in list
      await fetchSubmissions()
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to submit'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Withdraw submission
   */
  async function withdraw(id: string): Promise<Submission> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.post<{ data: Submission }>(`/submissions/${id}/withdraw/`)
      currentSubmission.value = response.data.data
      
      // Update in list
      await fetchSubmissions()
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to withdraw'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Submit a revision
   */
  async function submitRevision(id: string, revisionResponse: string): Promise<Submission> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.post<{ data: Submission }>(`/submissions/${id}/submit_revision/`, {
        revision_response: revisionResponse
      })
      currentSubmission.value = response.data.data
      await fetchSubmissions()
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to submit revision'
      throw err
    } finally {
      isSaving.value = false
    }
  }

  // ============================================
  // ACTIONS - Author Operations
  // ============================================
  
  /**
   * Add author to submission
   */
  async function addAuthor(submissionId: string, author: AuthorInput): Promise<Author> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.post<{ data: Author }>(
        `/submissions/${submissionId}/authors/`,
        author
      )
      
      // Add to current submission if loaded
      if (currentSubmission.value?.id === submissionId) {
        currentSubmission.value.authors.push(response.data.data)
      }
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to add author'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Update author
   */
  async function updateAuthor(
    submissionId: string, 
    authorId: string, 
    data: Partial<AuthorInput>
  ): Promise<Author> {
    isSaving.value = true
    error.value = null
    
    try {
      const response = await api.patch<{ data: Author }>(
        `/submissions/${submissionId}/authors/${authorId}/`,
        data
      )
      
      // Update in current submission
      if (currentSubmission.value?.id === submissionId) {
        const index = currentSubmission.value.authors.findIndex(a => a.id === authorId)
        if (index !== -1) {
          currentSubmission.value.authors[index] = response.data.data
        }
      }
      
      return response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to update author'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Remove author
   */
  async function removeAuthor(submissionId: string, authorId: string): Promise<void> {
    isSaving.value = true
    error.value = null
    
    try {
      await api.delete(`/submissions/${submissionId}/authors/${authorId}/`)
      
      // Remove from current submission
      if (currentSubmission.value?.id === submissionId) {
        currentSubmission.value.authors = currentSubmission.value.authors.filter(
          a => a.id !== authorId
        )
      }
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to remove author'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  /**
   * Reorder authors
   */
  async function reorderAuthors(submissionId: string, authorIds: string[]): Promise<void> {
    isSaving.value = true
    error.value = null
    
    try {
      await api.post(`/submissions/${submissionId}/authors/reorder/`, {
        author_ids: authorIds
      })
      
      // Refetch to get updated order
      if (currentSubmission.value?.id === submissionId) {
        await fetchSubmission(submissionId)
      }
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to reorder authors'
      throw err
    } finally {
      isSaving.value = false
    }
  }
  
  // ============================================
  // ACTIONS - Wizard Operations
  // ============================================
  
  /**
   * Set wizard step
   */
  function setWizardStep(step: number): void {
    if (step >= 1 && step <= 6) {
      wizardStep.value = step
    }
  }
  
  /**
   * Go to next wizard step
   */
  function nextStep(): void {
    if (wizardStep.value < 6) {
      wizardStep.value++
    }
  }
  
  /**
   * Go to previous wizard step
   */
  function prevStep(): void {
    if (wizardStep.value > 1) {
      wizardStep.value--
    }
  }
  
  /**
   * Update wizard data
   */
  function updateWizardData(data: Partial<WizardData>): void {
    wizardData.value = { ...wizardData.value, ...data }
    isDirty.value = true
  }
  
  /**
   * Save wizard progress (autosave)
   */
  async function saveWizardProgress(): Promise<void> {
    if (!currentSubmission.value || !isDirty.value) return
    
    try {
      await updateSubmission(currentSubmission.value.id, {
        wizard_step: wizardStep.value,
        wizard_data: {
          ...wizardData.value,
          last_saved_at: new Date().toISOString()
        }
      })
    } catch {
      // Silently fail for autosave
    }
  }
  
  /**
   * Reset wizard state
   */
  function resetWizard(): void {
    wizardStep.value = 1
    wizardData.value = {}
    isDirty.value = false
    lastSavedAt.value = null
    currentSubmission.value = null
  }
  
  // ============================================
  // ACTIONS - Utility
  // ============================================
  
  /**
   * Clear error
   */
  function clearError(): void {
    error.value = null
  }
  
  /**
   * Reset store
   */
  function $reset(): void {
    submissions.value = []
    totalCount.value = 0
    currentPage.value = 1
    filters.value = {}
    currentSubmission.value = null
    isLoading.value = false
    isLoadingDetail.value = false
    isSaving.value = false
    error.value = null
    resetWizard()
  }
  
  return {
    // State
    submissions,
    totalCount,
    currentPage,
    pageSize,
    filters,
    currentSubmission,
    isLoading,
    isLoadingDetail,
    isSaving,
    error,
    wizardStep,
    wizardData,
    isDirty,
    lastSavedAt,
    
    // Getters
    stats,
    draftCount,
    submittedCount,
    revisionCount,
    acceptedCount,
    byStatus,
    hasNextPage,
    hasPrevPage,
    totalPages,
    isEditable,
    wizardProgress,
    
    // List Actions
    fetchSubmissions,
    setPage,
    setPageSize,
    filterByStatus,
    search,
    clearFilters,
    
    // CRUD Actions
    fetchSubmission,
    createSubmission,
    updateSubmission,
    deleteSubmission,
    
    // Submission Actions
    submitForReview,
    withdraw,
    submitRevision,

    // Author Actions
    addAuthor,
    updateAuthor,
    removeAuthor,
    reorderAuthors,
    
    // Wizard Actions
    setWizardStep,
    nextStep,
    prevStep,
    updateWizardData,
    saveWizardProgress,
    resetWizard,
    
    // Utility
    clearError,
    $reset,
  }
})
