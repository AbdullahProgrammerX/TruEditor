/**
 * TruEditor - User Types
 * ======================
 * TypeScript types for user-related data.
 */

/**
 * Academic title options
 */
export type AcademicTitle = 
  | '' 
  | 'prof' 
  | 'assoc_prof' 
  | 'asst_prof' 
  | 'dr' 
  | 'lecturer' 
  | 'researcher' 
  | 'phd_student' 
  | 'msc_student' 
  | 'other'

/**
 * Academic title display names
 */
export const ACADEMIC_TITLES: Record<AcademicTitle, string> = {
  '': 'Select',
  'prof': 'Professor',
  'assoc_prof': 'Associate Professor',
  'asst_prof': 'Assistant Professor',
  'dr': 'Doctor',
  'lecturer': 'Lecturer',
  'researcher': 'Researcher',
  'phd_student': 'PhD Student',
  'msc_student': 'MSc Student',
  'other': 'Other',
}

/**
 * User model - Full user data from API
 */
export interface User {
  // Primary
  id: string
  
  // ORCID Information
  orcid_id: string
  orcid_url: string
  last_orcid_sync: string | null
  
  // Personal Information
  email: string | null
  full_name: string
  given_name: string
  family_name: string
  display_name: string
  
  // Contact Information
  phone: string
  country: string
  city: string
  address: string
  
  // Academic Information
  title: AcademicTitle
  institution: string
  department: string
  expertise_areas: string[]
  bio: string
  website: string
  
  // Roles
  is_reviewer: boolean
  is_editor: boolean
  is_chief_editor: boolean
  reviewer_interests: string[]
  
  // Status
  is_active: boolean
  email_verified: boolean
  profile_completed: boolean
  
  // Timestamps
  date_joined: string
  last_login: string | null
}

/**
 * User profile update - Editable fields only
 */
export interface UserProfileUpdate {
  // Personal
  email?: string
  full_name?: string
  given_name?: string
  family_name?: string
  
  // Contact
  phone?: string
  country?: string
  city?: string
  address?: string
  
  // Academic
  title?: AcademicTitle
  institution?: string
  department?: string
  expertise_areas?: string[]
  bio?: string
  website?: string
  
  // Reviewer
  reviewer_interests?: string[]
}

/**
 * Minimal user data for nested relations
 */
export interface UserMinimal {
  id: string
  orcid_id: string
  orcid_url: string
  full_name: string
  email: string | null
  institution: string
}

/**
 * Authentication response
 */
export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

/**
 * ORCID login URL response
 */
export interface ORCIDLoginResponse {
  authorization_url: string
}

/**
 * Country list for dropdown
 */
export const COUNTRIES = [
  'Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Armenia', 'Australia', 
  'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 
  'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria', 'Canada', 
  'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 
  'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 
  'El Salvador', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Georgia', 
  'Germany', 'Ghana', 'Greece', 'Guatemala', 'Honduras', 'Hong Kong', 
  'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 
  'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 
  'Kuwait', 'Latvia', 'Lebanon', 'Libya', 'Lithuania', 'Luxembourg', 
  'Malaysia', 'Malta', 'Mexico', 'Moldova', 'Morocco', 'Netherlands', 
  'New Zealand', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 
  'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 
  'Portugal', 'Qatar', 'Romania', 'Russia', 'Saudi Arabia', 'Serbia', 
  'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 
  'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 
  'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates', 
  'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 
  'Vietnam', 'Yemen'
] as const

export type Country = typeof COUNTRIES[number]
