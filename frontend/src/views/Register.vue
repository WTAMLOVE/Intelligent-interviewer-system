<template>
  <div class="auth-form-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <h1>创建账户</h1>
        <p class="subtitle">加入智能面试官，开启高效面试之旅</p>
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
            <label class="form-label">邮箱地址</label>
            <el-form-item prop="email">
              <el-input 
                v-model="form.email" 
                placeholder="请输入邮箱地址"
                size="large"
                prefix-icon="Message"
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
          
          <div class="form-group">
            <label class="form-label">选择角色</label>
            <el-form-item prop="role">
              <el-select 
                v-model="form.role" 
                placeholder="请选择您的角色"
                size="large"
                style="width: 100%"
              >
                <el-option 
                  label="面试官 - 发布职位，管理面试" 
                  value="interviewer"
                >
                  <div class="role-option">
                    <span class="role-title">面试官</span>
                    <span class="role-desc">发布职位，管理面试</span>
                  </div>
                </el-option>
                <el-option 
                  label="面试者 - 参与面试，展示技能" 
                  value="interviewee"
                >
                  <div class="role-option">
                    <span class="role-title">面试者</span>
                    <span class="role-desc">参与面试，展示技能</span>
                  </div>
                </el-option>
              </el-select>
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
              {{ isLoading ? '注册中...' : '立即注册' }}
            </el-button>
            
            <div class="auth-links">
              <span>已有账户？</span>
              <el-button type="text" @click="goLogin" class="link-button">
                立即登录
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
import { register } from '../api/auth'

const router = useRouter()
const formRef = ref()
const isLoading = ref(false)
const form = reactive({ 
  username: '', 
  email: '', 
  password: '', 
  role: 'interviewee' 
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

async function onSubmit() {
  if (!formRef.value || isLoading.value) return
  
  try {
    await formRef.value.validate()
    isLoading.value = true
    
    await register(form)
    
    ElMessage.success('注册成功！请登录您的账户')
    router.push('/login')
  } catch (err) {
    if (err.errors) return // 表单验证错误
    
    const msg = err?.response?.data?.message || '注册失败，请重试'
    ElMessage.error(msg)
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function goLogin() {
  router.push('/login')
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

.role-option {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.role-title {
  font-weight: 500;
  color: var(--text-primary);
}

.role-desc {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
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

:deep(.el-select .el-input__wrapper) {
  border-radius: var(--radius-md);
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
