import { createRouter, createWebHistory } from 'vue-router'

// Stores
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { public: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true, guestOnly: true },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/Signup.vue'),
    meta: { public: true, guestOnly: true },
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPassword.vue'),
    meta: { public: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/work-orders',
    name: 'WorkOrders',
    component: () => import('../views/WorkOrders.vue'),
    meta: { requiresAuth: true },
    // All roles can access, but data is filtered per role in the component
  },
  {
    path: '/work-orders/new',
    name: 'CreateWorkOrder',
    component: () => import('../views/CreateWorkOrder.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin', 'supervisor'] },
  },
  {
    path: '/work-orders/:id',
    name: 'WorkOrderDetail',
    component: () => import('../views/WorkOrderDetail.vue'),
    meta: { requiresAuth: true },
    // All roles can view details, but technicians can only view their own (enforced in component)
  },
  {
    path: '/work-orders/:id/edit',
    name: 'EditWorkOrder',
    component: () => import('../views/EditWorkOrder.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin', 'supervisor'] },
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/activity-log',
    name: 'ActivityLog',
    component: () => import('../views/ActivityLog.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notfound',
    component: () => import('../views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check if route is guest-only (like login page when already logged in)
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  // Check role-based access
  if (to.meta.allowedRoles && authStore.isAuthenticated) {
    const userRole = authStore.userRole
    if (!to.meta.allowedRoles.includes(userRole)) {
      // Redirect unauthorized roles back to dashboard
      next('/dashboard')
      return
    }
  }

  next()
})

export default router
