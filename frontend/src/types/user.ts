/**
 * TruEditor - User Types
 * ======================
 */

export interface User {
  id: string
  orcid_id: string
  email: string | null
  full_name: string
  given_name: string
  family_name: string
  institution: string
  department: string
  is_reviewer: boolean
  is_editor: boolean
  is_active: boolean
  date_joined: string
  last_login: string | null
  last_orcid_sync: string | null
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface ORCIDLoginResponse {
  authorization_url: string
}
