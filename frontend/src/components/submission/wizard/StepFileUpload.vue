<script setup lang="ts">
/**
 * TruEditor - Wizard Step 2: File Upload
 * =======================================
 * File upload area with drag-and-drop support.
 * Note: Full S3 integration will be in Phase 8.
 */

import { ref, computed } from 'vue'
import { FILE_TYPES, type FileType, type ManuscriptFile } from '@/types/submission'

interface UploadedFile {
  id: string
  name: string
  size: number
  type: FileType
  progress: number
  status: 'uploading' | 'completed' | 'error'
  errorMessage?: string
}

interface Props {
  /** Uploaded files */
  files?: ManuscriptFile[]
}

const props = withDefaults(defineProps<Props>(), {
  files: () => [],
})

const emit = defineEmits<{
  upload: [file: File, type: FileType]
  remove: [fileId: string]
  reorder: [fileIds: string[]]
}>()

const isDragging = ref(false)
const uploadedFiles = ref<UploadedFile[]>([])
const selectedFileType = ref<FileType>('main_text')

/**
 * Format file size
 */
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

/**
 * Get file extension icon
 */
function getFileIcon(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || ''
  
  const icons: Record<string, string> = {
    pdf: 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    doc: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    docx: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    jpg: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
    png: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
  }
  
  return icons[ext] ?? icons['doc'] ?? ''
}

/**
 * Handle file drop
 */
function handleDrop(event: DragEvent): void {
  isDragging.value = false
  
  const files = event.dataTransfer?.files
  if (!files || files.length === 0) return
  
  Array.from(files).forEach(file => {
    addFile(file)
  })
}

/**
 * Handle file input change
 */
function handleFileInput(event: Event): void {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (!files) return
  
  Array.from(files).forEach(file => {
    addFile(file)
  })
  
  input.value = ''
}

/**
 * Add file to upload list (simulated)
 */
function addFile(file: File): void {
  // Validate file type
  const allowedExtensions = ['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'xlsx', 'xls']
  const ext = file.name.split('.').pop()?.toLowerCase()
  
  if (!ext || !allowedExtensions.includes(ext)) {
    uploadedFiles.value.push({
      id: crypto.randomUUID(),
      name: file.name,
      size: file.size,
      type: selectedFileType.value,
      progress: 0,
      status: 'error',
      errorMessage: 'File type not allowed',
    })
    return
  }
  
  // Check file size (50MB max)
  if (file.size > 50 * 1024 * 1024) {
    uploadedFiles.value.push({
      id: crypto.randomUUID(),
      name: file.name,
      size: file.size,
      type: selectedFileType.value,
      progress: 0,
      status: 'error',
      errorMessage: 'File size exceeds 50MB limit',
    })
    return
  }
  
  // Simulate upload
  const uploadFile: UploadedFile = {
    id: crypto.randomUUID(),
    name: file.name,
    size: file.size,
    type: selectedFileType.value,
    progress: 0,
    status: 'uploading',
  }
  
  uploadedFiles.value.push(uploadFile)
  
  // Simulate upload progress
  const interval = setInterval(() => {
    const fileIndex = uploadedFiles.value.findIndex(f => f.id === uploadFile.id)
    if (fileIndex === -1) {
      clearInterval(interval)
      return
    }
    
    const currentFile = uploadedFiles.value[fileIndex]
    if (!currentFile) {
      clearInterval(interval)
      return
    }
    
    currentFile.progress += Math.random() * 30
    
    if (currentFile.progress >= 100) {
      currentFile.progress = 100
      currentFile.status = 'completed'
      clearInterval(interval)
      emit('upload', file, selectedFileType.value)
    }
  }, 200)
}

/**
 * Remove file
 */
function removeFile(fileId: string): void {
  uploadedFiles.value = uploadedFiles.value.filter(f => f.id !== fileId)
  emit('remove', fileId)
}

/**
 * Get file type color
 */
function getTypeColor(type: FileType): string {
  const colors: Record<FileType, string> = {
    main_text: 'bg-blue-100 text-blue-700',
    cover_letter: 'bg-purple-100 text-purple-700',
    title_page: 'bg-indigo-100 text-indigo-700',
    abstract: 'bg-cyan-100 text-cyan-700',
    tables: 'bg-green-100 text-green-700',
    figures: 'bg-amber-100 text-amber-700',
    supplementary: 'bg-gray-100 text-gray-700',
    ethics_approval: 'bg-rose-100 text-rose-700',
    copyright: 'bg-slate-100 text-slate-700',
    revision: 'bg-orange-100 text-orange-700',
    revision_notes: 'bg-teal-100 text-teal-700',
    other: 'bg-gray-100 text-gray-600',
  }
  return colors[type]
}

const hasMainText = computed(() => 
  uploadedFiles.value.some(f => f.type === 'main_text' && f.status === 'completed')
)
</script>

<template>
  <div class="step-file-upload">
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Upload Files</h3>
      <p class="mt-1 text-sm text-gray-500">
        Upload your manuscript and supporting documents. Main text document is required.
      </p>
    </div>

    <!-- File Type Selector -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        File Type
      </label>
      <select 
        v-model="selectedFileType"
        class="input-field"
      >
        <option 
          v-for="(typeInfo, typeKey) in FILE_TYPES" 
          :key="typeKey" 
          :value="typeKey"
        >
          {{ typeInfo.label }} {{ typeInfo.required ? '*' : '' }}
        </option>
      </select>
    </div>

    <!-- Drop Zone -->
    <div
      class="drop-zone"
      :class="{ 'dragging': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <input
        type="file"
        multiple
        accept=".doc,.docx,.pdf,.jpg,.jpeg,.png,.tiff,.tif,.xlsx,.xls"
        class="hidden"
        id="fileInput"
        @change="handleFileInput"
      />
      
      <label for="fileInput" class="cursor-pointer">
        <div class="flex flex-col items-center">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          
          <p class="text-base font-medium text-gray-700 mb-1">
            Drop files here or <span class="text-primary-600">browse</span>
          </p>
          <p class="text-sm text-gray-500">
            DOC, DOCX, PDF, JPG, PNG, TIFF, XLS, XLSX (Max 50MB)
          </p>
        </div>
      </label>
    </div>

    <!-- Uploaded Files List -->
    <div v-if="uploadedFiles.length > 0" class="mt-6 space-y-3">
      <h4 class="text-sm font-medium text-gray-700">Uploaded Files ({{ uploadedFiles.length }})</h4>
      
      <div
        v-for="file in uploadedFiles"
        :key="file.id"
        class="file-item"
        :class="{ 'error': file.status === 'error' }"
      >
        <div class="flex items-center gap-3">
          <!-- File Icon -->
          <div class="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="getFileIcon(file.name)" />
            </svg>
          </div>
          
          <!-- File Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
              <span 
                class="px-2 py-0.5 text-xs font-medium rounded-full"
                :class="getTypeColor(file.type)"
              >
                {{ FILE_TYPES[file.type].label }}
              </span>
            </div>
            <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
            
            <!-- Progress Bar -->
            <div v-if="file.status === 'uploading'" class="mt-2">
              <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-primary-500 transition-all duration-300"
                  :style="{ width: `${file.progress}%` }"
                />
              </div>
            </div>
            
            <!-- Error Message -->
            <p v-if="file.status === 'error'" class="text-xs text-red-600 mt-1">
              {{ file.errorMessage }}
            </p>
          </div>
          
          <!-- Status/Actions -->
          <div class="flex-shrink-0">
            <svg 
              v-if="file.status === 'completed'" 
              class="w-5 h-5 text-green-500" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            
            <button
              v-else-if="file.status !== 'uploading'"
              @click="removeFile(file.id)"
              class="p-1 text-gray-400 hover:text-red-500 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <div v-else class="animate-spin">
              <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Validation Message -->
    <div v-if="!hasMainText" class="mt-6 flex items-center gap-2 text-amber-600">
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-sm font-medium">Main text document is required to continue</span>
    </div>

    <!-- Info Box -->
    <div class="mt-6 p-4 bg-blue-50 rounded-xl">
      <div class="flex gap-3">
        <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="text-sm text-blue-700">
          <p class="font-medium mb-1">File Requirements</p>
          <ul class="list-disc list-inside space-y-0.5 text-blue-600">
            <li>Main text should be in DOC, DOCX, or PDF format</li>
            <li>Tables and figures should be uploaded separately</li>
            <li>All author information should be removed for blind review</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 0.75rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.2s ease;
}

.drop-zone:hover {
  border-color: var(--color-primary-400, #5a87be);
  background-color: rgba(30, 58, 95, 0.025);
}

.drop-zone.dragging {
  border-color: var(--color-primary-500, #1e3a5f);
  background-color: rgba(30, 58, 95, 0.05);
}

.file-item {
  padding: 0.75rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.file-item.error {
  border-color: #fecaca;
  background-color: #fef2f2;
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
</style>
