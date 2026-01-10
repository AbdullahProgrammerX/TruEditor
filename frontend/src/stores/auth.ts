/**
 * TruEditor - Auth Store (Pinia)
 * ===============================
 * ORCID tabanlı kimlik doğrulama state yönetimi.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'
import type { User } from '@/types/user'

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
  const orcidUrl = computed(() => user.value ? `https://orcid.org/${user.value.orcid_id}` : '')

  // Actions
  
  /**
   * ORCID login URL'ini al
   */
  async function getORCIDLoginUrl(): Promise<string> {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/auth/orcid/login/')
      return response.data.data.authorization_url
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'ORCID bağlantısı kurulamadı'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * ORCID callback işlemi - OAuth code ile token al
   */
  async function handleORCIDCallback(code: string): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/orcid/callback/', { code })
      const data = response.data.data

      // Token ve kullanıcı bilgilerini kaydet
      accessToken.value = data.access_token
      user.value = data.user

      // API instance'a token'ı ekle
      api.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`

    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Giriş başarısız'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Çıkış yap
   */
  async function logout(): Promise<void> {
    isLoading.value = true

    try {
      await api.post('/auth/logout/')
    } catch {
      // Logout hatası önemli değil, yine de temizle
    } finally {
      // State'i temizle
      user.value = null
      accessToken.value = null
      delete api.defaults.headers.common['Authorization']
      isLoading.value = false
    }
  }

  /**
   * Profil bilgilerini getir
   */
  async function fetchProfile(): Promise<void> {
    if (!accessToken.value) return

    isLoading.value = true
    error.value = null

    try {
      const response = await api.get('/auth/profile/')
      user.value = response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Profil yüklenemedi'
      
      // Token geçersizse çıkış yap
      if (err.response?.status === 401) {
        await logout()
      }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Token'ı yenile
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
   * ORCID profilini senkronize et
   */
  async function syncORCIDProfile(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.post('/auth/orcid/sync/')
      user.value = response.data.data
    } catch (err: any) {
      error.value = err.response?.data?.error?.message || 'Senkronizasyon başarısız'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Uygulama başlatıldığında token'ı kontrol et
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
    
    // Actions
    getORCIDLoginUrl,
    handleORCIDCallback,
    logout,
    fetchProfile,
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
