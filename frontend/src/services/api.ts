/**
 * TruEditor - Axios API Service
 * ==============================
 */

import axios, { type AxiosInstance, type AxiosError } from 'axios'

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance
export const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // For refresh token cookies
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`📤 ${config.method?.toUpperCase()} ${config.url}`)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`📥 ${response.status} ${response.config.url}`)
    }
    return response
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as any

    // Log error in development
    if (import.meta.env.DEV) {
      console.error(`❌ ${error.response?.status} ${originalRequest?.url}`, error.response?.data)
    }

    // Handle 401 - Unauthorized (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh token
        const response = await api.post('/auth/token/refresh/')
        const newAccessToken = response.data.access

        // Update authorization header
        api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`

        // Retry original request
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// API response type
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: {
    code: string
    message: string
    details?: Array<{ field: string; message: string }>
  }
}

// Helper functions
export async function get<T>(url: string): Promise<ApiResponse<T>> {
  const response = await api.get(url)
  return response.data
}

export async function post<T>(url: string, data?: any): Promise<ApiResponse<T>> {
  const response = await api.post(url, data)
  return response.data
}

export async function put<T>(url: string, data?: any): Promise<ApiResponse<T>> {
  const response = await api.put(url, data)
  return response.data
}

export async function patch<T>(url: string, data?: any): Promise<ApiResponse<T>> {
  const response = await api.patch(url, data)
  return response.data
}

export async function del<T>(url: string): Promise<ApiResponse<T>> {
  const response = await api.delete(url)
  return response.data
}
