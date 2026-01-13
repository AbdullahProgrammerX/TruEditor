/**
 * TruEditor - Vue Router Configuration
 * =====================================
 * Handles routing with authentication and profile completion guards.
 */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy-loaded views
const LandingPage = () => import('@/views/LandingPage.vue')
const LoginPage = () => import('@/views/auth/LoginPage.vue')
const ORCIDCallback = () => import('@/views/auth/ORCIDCallback.vue')
const CompleteProfile = () => import('@/views/profile/CompleteProfile.vue')
const Dashboard = () => import('@/views/dashboard/Dashboard.vue')
const NewSubmission = () => import('@/views/submission/NewSubmission.vue')
const SubmissionDetail = () => import('@/views/submission/SubmissionDetail.vue')
const Profile = () => import('@/views/profile/Profile.vue')
const NotFound = () => import('@/views/NotFound.vue')

/**
 * Route meta types:
 * - requiresAuth: Route requires user to be logged in
 * - requiresProfile: Route requires profile to be complete
 * - guestOnly: Route is only for non-authenticated users
 * - allowIncompleteProfile: Allows access even if profile is incomplete
 */
const routes: RouteRecordRaw[] = [
  // ================================
  // PUBLIC ROUTES
  // ================================
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { requiresAuth: false, guestOnly: true }
  },
  {
    path: '/auth/orcid/callback',
    name: 'orcid-callback',
    component: ORCIDCallback,
    meta: { requiresAuth: false }
  },

  // ================================
  // PROFILE COMPLETION (Auth required, incomplete profile allowed)
  // ================================
  {
    path: '/complete-profile',
    name: 'complete-profile',
    component: CompleteProfile,
    meta: { 
      requiresAuth: true,
      allowIncompleteProfile: true  // This is the only route that allows incomplete profile
    }
  },

  // ================================
  // PROTECTED ROUTES (Auth + Complete Profile required)
  // ================================
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { 
      requiresAuth: true,
      requiresProfile: true 
    }
  },
  {
    path: '/submissions/new',
    name: 'new-submission',
    component: NewSubmission,
    meta: { 
      requiresAuth: true,
      requiresProfile: true 
    }
  },
  {
    path: '/submissions/:id',
    name: 'submission-detail',
    component: SubmissionDetail,
    meta: { 
      requiresAuth: true,
      requiresProfile: true 
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { 
      requiresAuth: true,
      requiresProfile: true 
    }
  },

  // ================================
  // 404
  // ================================
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  }
})

// ================================
// NAVIGATION GUARDS
// ================================
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  const requiresAuth = to.meta.requiresAuth
  const requiresProfile = to.meta.requiresProfile
  const guestOnly = to.meta.guestOnly
  const allowIncompleteProfile = to.meta.allowIncompleteProfile

  // Check authentication status
  const isAuthenticated = authStore.isAuthenticated
  const isProfileComplete = authStore.profileCompleted

  // CASE 1: Guest-only routes (login page, etc.)
  if (guestOnly && isAuthenticated) {
    // Already logged in, redirect based on profile status
    if (isProfileComplete) {
      next({ name: 'dashboard' })
    } else {
      next({ name: 'complete-profile' })
    }
    return
  }

  // CASE 2: Protected routes requiring authentication
  if (requiresAuth && !isAuthenticated) {
    // Not logged in, redirect to login
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // CASE 3: Routes requiring profile completion
  if (requiresProfile && isAuthenticated && !isProfileComplete) {
    // Profile not complete, redirect to complete-profile
    // Unless the route explicitly allows incomplete profiles
    if (!allowIncompleteProfile) {
      next({ name: 'complete-profile' })
      return
    }
  }

  // CASE 4: Complete-profile page when profile is already complete
  if (to.name === 'complete-profile' && isAuthenticated && isProfileComplete) {
    // Profile already complete, redirect to dashboard
    next({ name: 'dashboard' })
    return
  }

  // All checks passed
  next()
})

export default router
