/**
 * TruEditor - Auth Store (Pinia)
 * ===============================
 * ORCID-based authentication state management.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'
import type { User, UserProfileUpdate } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const fullName = computed(() => user.value?.full_name || user.value?.orcid_id || '')
  const orcidId = computed(() => user.value?.orcid_id || '')
  const orcidUrl = computed(() => user.value?.orcid_url || '')
  const profileCompleted = computed(() => user.value?.profile_completed || false)

  // Actions
  
  /**
   * Get ORCID login URL
   */
  async function getORCIDLoginUrl(): Promise<string> {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/auth/orcid/login/')
      return response.data.data.authorization_url
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Could not connect to ORCID'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Handle ORCID callback - exchange OAuth code for token
   */
  async function handleORCIDCallback(code: string): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/orcid/callback/', { code })
      const data = response.data.data

      // Save token and user info
      accessToken.value = data.access_token
      user.value = data.user

      // Add token to API instance
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`

    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout
   */
  async function logout(): Promise<void> {
    isLoading.value = true

    try {
      await api.post('/auth/logout/')
    } catch {
      // Logout error doesn't matter, still clear state
    } finally {
      // Clear state
      user.value = null
      accessToken.value = null
      delete api.defaults.headers.common['Authorization']
      isLoading.value = false
    }
  }

  /**
   * Fetch profile information
   */
  async function fetchProfile(): Promise<void> {
    if (!accessToken.value) return

    isLoading.value = true
    error.value = null

    try {
      const response = await api.get('/auth/profile/')
      user.value = response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Could not load profile'
      
      // If token is invalid, logout
      if (err.response?.status === 401) {
        await logout()
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Refresh token
   */
  async function refreshToken(): Promise<boolean> {
    try {
      const response = await api.post('/auth/token/refresh/')
      accessToken.value = response.data.access
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      return true
    } catch {
      await logout()
      return false
    }
  }

  /**
   * Update user profile
   */
  async function updateProfile(profileData: UserProfileUpdate): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.patch('/auth/profile/', profileData)
      user.value = response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Failed to update profile'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Sync ORCID profile
   */
  async function syncORCIDProfile(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/orcid/sync/')
      user.value = response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Sync failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Initialize auth on app start
   */
  function initAuth(): void {
    if (accessToken.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
      fetchProfile()
    }
  }

  return {
    // State
    user,
    accessToken,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    fullName,
    orcidId,
    orcidUrl,
    profileCompleted,
    
    // Actions
    getORCIDLoginUrl,
    handleORCIDCallback,
    logout,
    fetchProfile,
    updateProfile,
    refreshToken,
    syncORCIDProfile,
    initAuth,
  }
}, {
  persist: {
    key: 'trueditor-auth',
    pick: ['accessToken', 'user'],
  }
})
