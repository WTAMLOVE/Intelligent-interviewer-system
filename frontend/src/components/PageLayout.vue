<template>
  <div class="page-root">
    <AuthHeader />
    <div v-if="isAuthLayout" class="auth-layout">
      <!-- 认证页面使用全屏布局 -->
      <slot />
    </div>
    <div v-else class="page-layout">
      <div class="page-container">
        <div class="page-card card">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AuthHeader from './AuthHeader.vue'

const route = useRoute()
const isAuthLayout = route.meta && route.meta.layout === 'auth'
</script>

<style scoped>
.page-root { 
  min-height: 100vh; 
  background: linear-gradient(135deg, var(--primary-50) 0%, var(--gray-50) 100%);
}

.auth-layout {
  min-height: calc(100vh - 60px);
}

.page-layout { 
  display: flex; 
  align-items: flex-start; 
  justify-content: center; 
  padding: var(--spacing-xl);
  min-height: calc(100vh - 60px);
}

.page-container {
  width: 100%;
  max-width: 1200px;
}

.page-card { 
  width: 100%; 
  background: var(--card-bg); 
  border-radius: var(--radius-lg); 
  box-shadow: var(--card-shadow-lg); 
  padding: var(--spacing-2xl);
  border: 1px solid var(--card-border);
  backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
  .page-layout {
    padding: var(--spacing-md);
  }
  
  .page-card {
    padding: var(--spacing-lg);
  }
}

@media (max-width: 480px) {
  .page-layout {
    padding: var(--spacing-sm);
  }
  
  .page-card {
    padding: var(--spacing-md);
  }
}
</style>
