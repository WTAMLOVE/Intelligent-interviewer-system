<template>
  <div class="auth-header">
    <div class="auth-header-content">
      <div class="user-info" v-if="user">
        <div class="user-avatar">
          <el-icon><Avatar /></el-icon>
        </div>
        <div class="user-details">
          <span class="user-name">{{ user.username }}</span>
          <span class="user-role">{{ getRoleText(user.role) }}</span>
        </div>
      </div>
      
      <div class="auth-actions">
        <el-dropdown v-if="user" trigger="click">
          <el-button type="text" class="user-menu-btn">
            <el-icon><Setting /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goToProfile">
                <el-icon><User /></el-icon>
                个人资料
              </el-dropdown-item>
              <el-dropdown-item @click="goToSettings">
                <el-icon><Setting /></el-icon>
                设置
              </el-dropdown-item>
              <el-dropdown-item divided @click="onLogout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { ElMessage } from 'element-plus'
import { 
  Avatar, 
  Setting, 
  User, 
  SwitchButton 
} from '@element-plus/icons-vue'

import { computed } from 'vue'
const router = useRouter()
const auth = useAuthStore()

auth.loadFromStorage()
const user = computed(() => auth.user)

function getRoleText(role) {
  const roleMap = {
    'admin': '管理员',
    'interviewer': '面试官',
    'interviewee': '面试者'
  }
  return roleMap[role] || role
}

function goToProfile() {
  ElMessage.info('个人资料功能开发中...')
}

function goToSettings() {
  ElMessage.info('设置功能开发中...')
}

function onLogout() {
  auth.logout()
  ElMessage.success('已成功退出登录')
  router.push('/login')
}
</script>

<style scoped>
.auth-header {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-primary);
  padding: var(--spacing-sm) 0;
  backdrop-filter: blur(10px);
}

.auth-header-content {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--spacing-md);
  padding: 0 var(--spacing-lg);
  max-width: 1400px;
  margin: 0 auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary-100);
  color: var(--primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.user-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.2;
}

.user-role {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: 1.2;
}

.auth-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.user-menu-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  padding: 0;
  color: var(--text-secondary);
  border: 1px solid var(--border-primary);
}

.user-menu-btn:hover {
  color: var(--primary-600);
  border-color: var(--primary-200);
  background: var(--primary-50);
}

.logout-btn {
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
}

/* Element Plus 样式覆盖 */
:deep(.el-dropdown-menu) {
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--card-shadow-lg);
  padding: var(--spacing-xs);
}

:deep(.el-dropdown-menu__item) {
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

:deep(.el-dropdown-menu__item:hover) {
  background: var(--bg-secondary);
  color: var(--primary-600);
}

:deep(.el-dropdown-menu__item.is-divided) {
  border-top: 1px solid var(--border-primary);
  margin-top: var(--spacing-xs);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-header-content {
    padding: 0 var(--spacing-md);
  }
  
  .user-details {
    display: none;
  }
  
  .user-info {
    padding: var(--spacing-xs);
    background: transparent;
  }
}

@media (max-width: 480px) {
  .auth-header-content {
    padding: 0 var(--spacing-sm);
    gap: var(--spacing-sm);
  }
  
  .logout-btn span {
    display: none;
  }
  
  .logout-btn {
    width: 32px;
    padding: var(--spacing-xs);
  }
}
</style>
