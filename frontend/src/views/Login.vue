<template>
  <div class="auth-form-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <h1>欢迎回来</h1>
        <p class="subtitle">登录您的智能面试官账户</p>
      </div>
      
      <div class="auth-form">
        <el-form 
          :model="form" 
          @submit.prevent="onSubmit" 
          :rules="rules" 
          ref="formRef"
          @keyup.enter="onSubmit"
        >
          <div class="form-group">
            <label class="form-label">用户名</label>
            <el-form-item prop="username">
              <el-input 
                v-model="form.username" 
                placeholder="请输入用户名"
                size="large"
                prefix-icon="User"
                @keyup.enter="onSubmit"
              />
            </el-form-item>
          </div>
          
          <div class="form-group">
            <label class="form-label">密码</label>
            <el-form-item prop="password">
              <el-input 
                type="password" 
                v-model="form.password" 
                placeholder="请输入密码"
                size="large"
                prefix-icon="Lock"
                show-password
                @keyup.enter="onSubmit"
              />
            </el-form-item>
          </div>
          
          <div class="form-actions">
            <el-button 
              type="primary" 
              @click="onSubmit" 
              :loading="isLoading"
              size="large"
              style="width: 100%; margin-bottom: 16px;"
            >
              {{ isLoading ? '登录中...' : '登录' }}
            </el-button>
            
            <div class="auth-links">
              <span>还没有账户？</span>
              <el-button type="text" @click="goRegister" class="link-button">
                立即注册
              </el-button>
            </div>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const formRef = ref()
const isLoading = ref(false)
const form = reactive({ username: '', password: '' })

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ]
}

async function onSubmit() {
  if (!formRef.value || isLoading.value) return
  
  try {
    await formRef.value.validate()
    isLoading.value = true
    
    const res = await login(form)
    const auth = useAuthStore()
    auth.setToken(res.data.access_token)
    auth.setUser(res.data.user)
    
    ElMessage.success('登录成功！')
    router.push('/')
  } catch (err) {
    if (err.errors) return // 表单验证错误
    
    const msg = err?.response?.data?.message || '用户名或密码错误'
    ElMessage.error(msg)
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function goRegister() {
  router.push('/register')
}
</script>

<style scoped>
.auth-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.auth-header h1 {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
}

.auth-form {
  width: 100%;
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.form-actions {
  margin-top: var(--spacing-xl);
}

.auth-links {
  text-align: center;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.link-button {
  color: var(--primary-600);
  font-weight: 500;
  padding: 0;
  margin-left: var(--spacing-xs);
}

.link-button:hover {
  color: var(--primary-700);
}

/* Element Plus 样式覆盖 */
:deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--border-primary);
  transition: all var(--transition-fast);
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--border-secondary);
}

:deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--primary-500), 0 0 0 3px rgba(14, 165, 233, 0.1);
}

:deep(.el-button--primary) {
  background: var(--primary-600);
  border-color: var(--primary-600);
  border-radius: var(--radius-md);
  font-weight: 500;
}

:deep(.el-button--primary:hover) {
  background: var(--primary-700);
  border-color: var(--primary-700);
}

:deep(.el-form-item__error) {
  color: var(--error);
  font-size: var(--font-size-xs);
}
</style>
