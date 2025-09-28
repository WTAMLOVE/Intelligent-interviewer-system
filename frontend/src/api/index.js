import axios from 'axios'
import router from '@/router'

const instance = axios.create({ baseURL: '/api' })

// attach token if exists
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    // 检查token有效性
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      if (payload.exp && payload.exp < currentTime) {
        // token已过期，清除并跳转登录
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
        return Promise.reject(new Error('登录已过期，请重新登录'))
      }
    } catch (error) {
      // token格式错误，清除并跳转登录
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
      return Promise.reject(new Error('登录凭证无效，请重新登录'))
    }
    
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

instance.interceptors.response.use(
  res => res,
  err => {
    console.log('API错误:', err.response || err) // 调试用
    
    // 处理401错误（token过期或无效）
    if (err.response && err.response.status === 401) {
      // 清除本地存储的认证信息
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // 跳转到登录页面
      router.push('/login')
      
      // 显示用户友好的错误信息
      const message = err.response.data?.message || '登录已过期，请重新登录'
      return Promise.reject(new Error(message))
    }
    
    // 处理JWT相关的500错误（可能是JWT过期导致的内部错误）
    if (err.response && err.response.status === 500) {
      const errorMessage = err.response.data?.message || err.message || ''
      
      // 检查是否是JWT相关错误
      if (errorMessage.includes('expired') || 
          errorMessage.includes('Signature has expired') ||
          errorMessage.includes('jwt') ||
          errorMessage.includes('token')) {
        
        // 清除本地存储的认证信息
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        
        // 跳转到登录页面
        router.push('/login')
        
        return Promise.reject(new Error('登录已过期，请重新登录'))
      }
    }
    
    return Promise.reject(err.response || err)
  }
)

export default instance
