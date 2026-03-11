/**
 * TruEditor - useFileUpload Composable
 * ======================================
 * Handles real file uploads to the backend API with progress tracking.
 */

import { ref, computed } from 'vue'
import { api } from '@/services/api'
import type { FileType, ManuscriptFile } from '@/types/submission'

export interface ExtractedMetadata {
  extracted: boolean
  title?: string | null
  abstract?: string | null
  keywords?: string[]
}

export interface UploadingFile {
  /** Client-side tracking ID */
  id: string
  /** Original file name */
  name: string
  /** File size in bytes */
  size: number
  /** File type category */
  fileType: FileType
  /** Upload progress 0-100 */
  progress: number
  /** Upload status */
  status: 'uploading' | 'completed' | 'error'
  /** Error message if failed */
  errorMessage?: string
  /** Server-side file record after successful upload */
  serverFile?: ManuscriptFile
}

// Allowed extensions
const ALLOWED_EXTENSIONS = ['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'xlsx', 'xls']
const MAX_FILE_SIZE = 50 * 1024 * 1024 // 50MB

export function useFileUpload(submissionId: () => string | undefined) {
  const uploadingFiles = ref<UploadingFile[]>([])
  const serverFiles = ref<ManuscriptFile[]>([])
  const isLoadingFiles = ref(false)

  /**
   * Total count of files (server + uploading)
   */
  const totalFiles = computed(() =>
    serverFiles.value.length + uploadingFiles.value.filter(f => f.status === 'uploading').length
  )

  /**
   * Has any file currently uploading
   */
  const isUploading = computed(() =>
    uploadingFiles.value.some(f => f.status === 'uploading')
  )

  /**
   * Validate file before upload
   */
  function validateFile(file: File): { valid: boolean; error?: string } {
    const ext = file.name.split('.').pop()?.toLowerCase() || ''

    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      return { valid: false, error: `File type .${ext} is not allowed. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}` }
    }

    if (file.size > MAX_FILE_SIZE) {
      return { valid: false, error: 'File size exceeds 50MB limit.' }
    }

    return { valid: true }
  }

  /**
   * Format file size to human-readable string
   */
  function formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }

  /**
   * Fetch existing files for the submission from the server
   */
  async function fetchFiles(): Promise<void> {
    const sid = submissionId()
    if (!sid) return

    isLoadingFiles.value = true
    try {
      const response = await api.get(`/files/?submission_id=${sid}`)
      serverFiles.value = response.data.data || []
    } catch (err) {
      console.error('Failed to fetch files:', err)
    } finally {
      isLoadingFiles.value = false
    }
  }

  /**
   * Upload a single file to the server
   */
  async function uploadFile(file: File, fileType: FileType): Promise<void> {
    const sid = submissionId()
    if (!sid) {
      uploadingFiles.value.push({
        id: crypto.randomUUID(),
        name: file.name,
        size: file.size,
        fileType,
        progress: 0,
        status: 'error',
        errorMessage: 'Draft could not be created. Please go back, select an article type, and try again.',
      })
      return
    }

    // Validate
    const validation = validateFile(file)
    if (!validation.valid) {
      uploadingFiles.value.push({
        id: crypto.randomUUID(),
        name: file.name,
        size: file.size,
        fileType,
        progress: 0,
        status: 'error',
        errorMessage: validation.error,
      })
      return
    }

    // Create tracking entry
    const trackingId = crypto.randomUUID()
    const entry: UploadingFile = {
      id: trackingId,
      name: file.name,
      size: file.size,
      fileType,
      progress: 0,
      status: 'uploading',
    }
    uploadingFiles.value.push(entry)

    // Build FormData
    const formData = new FormData()
    formData.append('file', file)
    formData.append('file_type', fileType)

    try {
      const response = await api.post(`/files/?submission_id=${sid}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const idx = uploadingFiles.value.findIndex(f => f.id === trackingId)
          const item = idx !== -1 ? uploadingFiles.value[idx] : undefined
          if (item && progressEvent.total) {
            item.progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            )
          }
        },
      })

      // Mark as completed
      const idx = uploadingFiles.value.findIndex(f => f.id === trackingId)
      const completedItem = idx !== -1 ? uploadingFiles.value[idx] : undefined
      if (completedItem) {
        completedItem.status = 'completed'
        completedItem.progress = 100
        completedItem.serverFile = response.data.data
      }

      // Add to server files list
      if (response.data.data) {
        serverFiles.value.push(response.data.data)
      }

      // Remove completed entry immediately to avoid duplicate display
      uploadingFiles.value = uploadingFiles.value.filter(f => f.id !== trackingId)

      // Auto-extract metadata for main_text or revision files
      if (
        (fileType === 'main_text' || fileType === 'revision') &&
        response.data.data?.id
      ) {
        extractMetadata(response.data.data.id).catch(() => {})
      }
    } catch (err: any) {
      const idx = uploadingFiles.value.findIndex(f => f.id === trackingId)
      const errorItem = idx !== -1 ? uploadingFiles.value[idx] : undefined
      if (errorItem) {
        errorItem.status = 'error'
        errorItem.errorMessage =
          err.response?.data?.error?.message || 'Upload failed. Please try again.'
      }
    }
  }

  /**
   * Upload multiple files
   */
  async function uploadFiles(files: File[], fileType: FileType): Promise<void> {
    for (const file of files) {
      await uploadFile(file, fileType)
    }
  }

  /**
   * Remove (soft delete) a file on the server
   */
  async function removeFile(fileId: string): Promise<void> {
    try {
      await api.delete(`/files/${fileId}/`)
      serverFiles.value = serverFiles.value.filter(f => f.id !== fileId)
    } catch (err: any) {
      console.error('Failed to remove file:', err)
      throw err
    }
  }

  /**
   * Remove an uploading/error entry from the local list
   */
  function dismissUploadEntry(trackingId: string): void {
    uploadingFiles.value = uploadingFiles.value.filter(f => f.id !== trackingId)
  }

  /**
   * Get presigned download URL for a file
   */
  async function getDownloadUrl(fileId: string): Promise<string | null> {
    try {
      const response = await api.get(`/files/${fileId}/presigned_url/`)
      return response.data.data?.download_url || null
    } catch (err) {
      console.error('Failed to get download URL:', err)
      return null
    }
  }

  const lastExtractedMetadata = ref<ExtractedMetadata | null>(null)

  /**
   * Extract metadata (title, abstract, keywords) from a file
   */
  async function extractMetadata(fileId: string): Promise<ExtractedMetadata | null> {
    try {
      const response = await api.post<{ data: ExtractedMetadata }>(`/files/${fileId}/extract_metadata/`)
      const data = response.data.data
      if (data?.extracted) {
        lastExtractedMetadata.value = data
        return data
      }
    } catch {
      // Silently fail — metadata extraction is best-effort
    }
    return null
  }

  /**
   * Reorder files
   */
  async function reorderFiles(fileIds: string[]): Promise<void> {
    if (fileIds.length === 0) return

    try {
      // Use the first file's endpoint for reorder
      await api.post(`/files/${fileIds[0]}/reorder/`, { file_ids: fileIds })
      // Refetch to get updated order
      await fetchFiles()
    } catch (err) {
      console.error('Failed to reorder files:', err)
    }
  }

  return {
    // State
    uploadingFiles,
    serverFiles,
    isLoadingFiles,
    lastExtractedMetadata,

    // Computed
    totalFiles,
    isUploading,

    // Methods
    validateFile,
    formatFileSize,
    fetchFiles,
    uploadFile,
    uploadFiles,
    removeFile,
    dismissUploadEntry,
    getDownloadUrl,
    reorderFiles,
    extractMetadata,
  }
}
