/**
 * TruEditor - Submission Types
 * ============================
 * TypeScript types for submissions, authors, and files.
 */

import type { UserMinimal } from './user'

// ============================================
// ENUMS & CONSTANTS
// ============================================

/**
 * Submission status values
 */
export type SubmissionStatus = 
  | 'draft'
  | 'submitted'
  | 'under_review'
  | 'revision_required'
  | 'revision_submitted'
  | 'accepted'
  | 'rejected'
  | 'withdrawn'
  | 'published'

/**
 * Submission status display names
 */
export const SUBMISSION_STATUS: Record<SubmissionStatus, { label: string; color: string; bgColor: string }> = {
  draft: { label: 'Draft', color: 'text-gray-600', bgColor: 'bg-gray-100' },
  submitted: { label: 'Submitted', color: 'text-blue-600', bgColor: 'bg-blue-100' },
  under_review: { label: 'Under Review', color: 'text-purple-600', bgColor: 'bg-purple-100' },
  revision_required: { label: 'Revision Required', color: 'text-orange-600', bgColor: 'bg-orange-100' },
  revision_submitted: { label: 'Revision Submitted', color: 'text-indigo-600', bgColor: 'bg-indigo-100' },
  accepted: { label: 'Accepted', color: 'text-green-600', bgColor: 'bg-green-100' },
  rejected: { label: 'Rejected', color: 'text-red-600', bgColor: 'bg-red-100' },
  withdrawn: { label: 'Withdrawn', color: 'text-gray-500', bgColor: 'bg-gray-100' },
  published: { label: 'Published', color: 'text-emerald-600', bgColor: 'bg-emerald-100' },
}

/**
 * Article type values
 */
export type ArticleType = 
  | 'research'
  | 'review'
  | 'case_report'
  | 'short_communication'
  | 'letter'
  | 'editorial'
  | 'other'

/**
 * Article type display names
 */
export const ARTICLE_TYPES: Record<ArticleType, { label: string; description: string }> = {
  research: { 
    label: 'Research Article', 
    description: 'Original research with methodology, results, and conclusions' 
  },
  review: { 
    label: 'Review Article', 
    description: 'Comprehensive review of existing literature on a topic' 
  },
  case_report: { 
    label: 'Case Report', 
    description: 'Detailed report of a specific clinical case' 
  },
  short_communication: { 
    label: 'Short Communication', 
    description: 'Brief report of significant findings' 
  },
  letter: { 
    label: 'Letter to the Editor', 
    description: 'Commentary or response to published articles' 
  },
  editorial: { 
    label: 'Editorial', 
    description: 'Opinion piece or commentary by editors' 
  },
  other: { 
    label: 'Other', 
    description: 'Other type of manuscript' 
  },
}

/**
 * Manuscript file types
 */
export type FileType = 
  | 'main_text'
  | 'cover_letter'
  | 'title_page'
  | 'abstract'
  | 'tables'
  | 'figures'
  | 'supplementary'
  | 'ethics_approval'
  | 'copyright'
  | 'revision'
  | 'revision_notes'
  | 'other'

/**
 * File type display names
 */
export const FILE_TYPES: Record<FileType, { label: string; required: boolean; description: string }> = {
  main_text: { label: 'Main Text', required: true, description: 'Main manuscript document' },
  cover_letter: { label: 'Cover Letter', required: false, description: 'Letter to the editor' },
  title_page: { label: 'Title Page', required: false, description: 'Separate title page' },
  abstract: { label: 'Abstract', required: false, description: 'Separate abstract file' },
  tables: { label: 'Tables', required: false, description: 'Tables and data' },
  figures: { label: 'Figures', required: false, description: 'Figures and images' },
  supplementary: { label: 'Supplementary Files', required: false, description: 'Additional materials' },
  ethics_approval: { label: 'Ethics Approval', required: false, description: 'Ethics committee approval' },
  copyright: { label: 'Copyright Form', required: false, description: 'Copyright transfer agreement' },
  revision: { label: 'Revision File', required: false, description: 'Revised manuscript' },
  revision_notes: { label: 'Revision Notes', required: false, description: 'Response to reviewers' },
  other: { label: 'Other', required: false, description: 'Other documents' },
}

/**
 * Language options
 */
export type Language = 'en' | 'tr'

export const LANGUAGES: Record<Language, string> = {
  en: 'English',
  tr: 'Turkish',
}

// ============================================
// INTERFACES
// ============================================

/**
 * Author information
 */
export interface Author {
  id: string
  user?: UserMinimal | null
  orcid_id: string
  given_name: string
  family_name: string
  full_name: string
  email: string
  institution: string
  department: string
  country: string
  city: string
  affiliation: string
  order: number
  is_corresponding: boolean
  contribution: string
  created_at: string
}

/**
 * Author create/update input
 */
export interface AuthorInput {
  user?: string | null
  orcid_id?: string
  given_name: string
  family_name: string
  email: string
  institution: string
  department?: string
  country?: string
  city?: string
  order?: number
  is_corresponding?: boolean
  contribution?: string
}

/**
 * Manuscript file information
 */
export interface ManuscriptFile {
  id: string
  submission: string
  uploaded_by?: UserMinimal | null
  file: string
  file_type: FileType
  file_type_display: string
  original_filename: string
  file_size: number
  file_size_human: string
  mime_type: string
  description: string
  caption: string
  order: number
  revision_number: number
  is_active: boolean
  is_primary: boolean
  is_image: boolean
  is_document: boolean
  download_url: string | null
  created_at: string
  updated_at: string
}

/**
 * Status history entry
 */
export interface StatusHistoryEntry {
  id: string
  from_status: SubmissionStatus
  to_status: SubmissionStatus
  from_status_display: string
  to_status_display: string
  changed_by: string | null
  changed_by_name: string
  notes: string
  created_at: string
}

/**
 * Corresponding author summary
 */
export interface CorrespondingAuthor {
  name: string
  email: string
  orcid_id: string
}

/**
 * Submission list item (for dashboard)
 */
export interface SubmissionListItem {
  id: string
  manuscript_id: string | null
  title: string
  article_type: ArticleType
  status: SubmissionStatus
  status_display: string
  submitter: UserMinimal
  author_count: number
  file_count: number
  corresponding_author: CorrespondingAuthor | null
  created_at: string
  updated_at: string
  submitted_at: string | null
}

/**
 * Full submission detail
 */
export interface Submission {
  // Primary
  id: string
  manuscript_id: string | null
  
  // Status
  status: SubmissionStatus
  status_display: string
  is_editable: boolean
  can_be_withdrawn: boolean
  
  // Submission Info
  submitter: UserMinimal
  article_type: ArticleType
  article_type_display: string
  language: Language
  
  // Manuscript Info
  title: string
  title_en: string
  abstract: string
  abstract_en: string
  keywords: string[]
  keywords_en: string[]
  
  // Cover Letter & Ethics
  cover_letter: string
  ethics_statement: string
  ethics_approval_number: string
  conflict_of_interest: string
  funding_statement: string
  
  // Wizard Progress
  wizard_step: number
  wizard_data: WizardData
  
  // Revision Info
  revision_number: number
  revision_notes: string
  revision_deadline: string | null
  
  // Editor Assignment
  assigned_editor: UserMinimal | null
  editor_notes: string
  editor_decision: string
  editor_decision_date: string | null
  
  // Relations
  authors: Author[]
  files: ManuscriptFile[]
  status_history: StatusHistoryEntry[]
  author_count: number
  file_count: number
  
  // Timestamps
  created_at: string
  updated_at: string
  submitted_at: string | null
  accepted_at: string | null
  published_at: string | null
}

/**
 * Submission create input
 */
export interface SubmissionCreateInput {
  title?: string
  title_en?: string
  abstract?: string
  abstract_en?: string
  keywords?: string[]
  keywords_en?: string[]
  article_type?: ArticleType
  language?: Language
  cover_letter?: string
  ethics_statement?: string
  ethics_approval_number?: string
  conflict_of_interest?: string
  funding_statement?: string
  wizard_step?: number
  wizard_data?: WizardData
}

/**
 * Submission update input (same as create for now)
 */
export type SubmissionUpdateInput = SubmissionCreateInput

// ============================================
// WIZARD TYPES
// ============================================

/**
 * Wizard data stored in submission
 */
export interface WizardData {
  // Step 1: Article Type
  article_type?: ArticleType
  
  // Step 2: Files (temporary file IDs)
  uploaded_files?: string[]
  
  // Step 3: Article Info
  title?: string
  title_en?: string
  abstract?: string
  abstract_en?: string
  keywords?: string[]
  keywords_en?: string[]
  
  // Step 4: Authors
  authors?: AuthorInput[]
  
  // Step 5: Additional Info
  cover_letter?: string
  ethics_statement?: string
  ethics_approval_number?: string
  conflict_of_interest?: string
  funding_statement?: string
  suggested_reviewers?: SuggestedReviewer[]
  opposed_reviewers?: OpposedReviewer[]
  editor_comments?: string
  
  // Step 6: Confirmation
  confirmed?: boolean
  
  // Metadata
  last_saved_at?: string
}

/**
 * Suggested reviewer
 */
export interface SuggestedReviewer {
  name: string
  email: string
  institution: string
  reason?: string
}

/**
 * Opposed reviewer
 */
export interface OpposedReviewer {
  name: string
  email?: string
  reason: string
}

// ============================================
// API RESPONSE TYPES
// ============================================

/**
 * Paginated list response
 */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/**
 * Submission list filters
 */
export interface SubmissionFilters {
  status?: SubmissionStatus
  article_type?: ArticleType
  search?: string
  ordering?: string
  page?: number
  page_size?: number
}

/**
 * Submission statistics for dashboard
 */
export interface SubmissionStats {
  total: number
  draft: number
  submitted: number
  under_review: number
  revision_required: number
  accepted: number
  rejected: number
  published: number
}
