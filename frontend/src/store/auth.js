import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({ token: null, user: null }),
  getters: {
    isAuthenticated: (state) => !!(state.token && state.user),
    userRole: (state) => state.user?.role || null
  },
  actions: {
    setToken(t) { this.token = t; localStorage.setItem('token', t) },
    setUser(u) { this.user = u; localStorage.setItem('user', JSON.stringify(u)) },
    loadFromStorage() {
      const t = localStorage.getItem('token')
      const u = localStorage.getItem('user')
      if (t) this.token = t
      if (u) this.user = JSON.parse(u)
    },
    logout() { 
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    // 检查token是否过期
    checkTokenValidity() {
      if (!this.token) return false
      
      try {
        // 简单的JWT解析（不验证签名，仅检查过期时间）
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        const currentTime = Math.floor(Date.now() / 1000)
        
        if (payload.exp && payload.exp < currentTime) {
          // token已过期
          this.logout()
          return false
        }
        
        return true
      } catch (error) {
        // token格式错误
        this.logout()
        return false
      }
    }
  }
})
