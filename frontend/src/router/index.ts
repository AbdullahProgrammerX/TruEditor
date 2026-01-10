/**
 * TruEditor - Vue Router Configuration
 * =====================================
 */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy-loaded views
const LandingPage = () => import('@/views/LandingPage.vue')
const LoginPage = () => import('@/views/auth/LoginPage.vue')
const ORCIDCallback = () => import('@/views/auth/ORCIDCallback.vue')
const Dashboard = () => import('@/views/dashboard/Dashboard.vue')
const NewSubmission = () => import('@/views/submission/NewSubmission.vue')
const SubmissionDetail = () => import('@/views/submission/SubmissionDetail.vue')
const Profile = () => import('@/views/profile/Profile.vue')
const NotFound = () => import('@/views/NotFound.vue')

const routes: RouteRecordRaw[] = [
  // Public routes
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

  // Protected routes (requires authentication)
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/submissions/new',
    name: 'new-submission',
    component: NewSubmission,
    meta: { requiresAuth: true }
  },
  {
    path: '/submissions/:id',
    name: 'submission-detail',
    component: SubmissionDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
    meta: { requiresAuth: true }
  },

  // 404
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

// Navigation guards
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const guestOnly = to.meta.guestOnly

  // Check if user is authenticated
  const isAuthenticated = authStore.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if not authenticated
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (guestOnly && isAuthenticated) {
    // Redirect to dashboard if already logged in
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
