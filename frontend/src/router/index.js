import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Admin from '../views/Admin.vue'
import Interviewer from '../views/Interviewer.vue'
import Interviewee from '../views/Interviewee.vue'
import { useAuthStore } from '../store/auth'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: Admin, meta: { requiresAuth: true, roles: ['admin'] } },
  { path: '/interviewer', component: Interviewer, meta: { requiresAuth: true, roles: ['interviewer'] } },
  { path: '/interviewee', component: Interviewee, meta: { requiresAuth: true, roles: ['interviewee'] } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// navigation guard: redirect root based on auth state/role
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  auth.loadFromStorage()
  
  // 检查token有效性
  const tokenValid = auth.checkTokenValidity()
  
  // Helper function to get user's home page based on role
  const getUserHomePage = (userRole) => {
    if (userRole === 'admin') return '/admin'
    if (userRole === 'interviewer') return '/interviewer'
    return '/interviewee'
  }

  // Redirect authenticated users away from auth pages
  if (tokenValid && auth.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
    return next(getUserHomePage(auth.userRole))
  }

  // Handle root path redirection
  if (to.path === '/') {
    if (!tokenValid || !auth.isAuthenticated) return next('/login')
    return next(getUserHomePage(auth.userRole))
  }

  // require auth for all routes except login/register
  if (to.path !== '/login' && to.path !== '/register') {
    if (!tokenValid || !auth.isAuthenticated) return next('/login')
  }

  // role-based access
  const roles = to.meta && to.meta.roles
  if (roles && roles.length > 0) {
    if (!tokenValid || !auth.isAuthenticated || !roles.includes(auth.userRole)) {
      return next('/login')
    }
  }

  next()
})

export default router
