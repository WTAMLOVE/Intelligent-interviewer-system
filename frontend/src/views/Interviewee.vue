<template>
  <div class="interviewee-page">
    <aside class="sidebar">
      <el-menu 
        :default-active="activeMenu" 
        class="sidebar-menu"
        @select="handleMenuSelect"
      >
        <el-menu-item index="resume">简历管理</el-menu-item>
        <el-menu-item index="interviews">面试清单</el-menu-item>
      </el-menu>
    </aside>

    <section class="main-content">
      <!-- 根据选中的菜单显示不同内容 -->
      <ResumeManager v-if="activeMenu === 'resume'" />
      <IntervieweeInterviewManager v-else-if="activeMenu === 'interviews'" />
      <div v-else class="placeholder-content">
        <h3>选择左侧菜单项查看内容</h3>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ResumeManager from '../components/ResumeManager.vue'
import IntervieweeInterviewManager from '../components/IntervieweeInterviewManager.vue'

// 当前激活的菜单项
const activeMenu = ref('resume')

// 处理菜单选择
function handleMenuSelect(index) {
  activeMenu.value = index
}
</script>

<style scoped>
.interviewee-page {
  display: flex;
  height: calc(100vh - 120px);
  min-height: 600px;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  min-width: 220px;
  max-width: 220px;
  border-right: 1px solid var(--border-primary);
  padding: var(--spacing-md);
  background: var(--card-bg);
  box-sizing: border-box;
  flex-shrink: 0;
}

.sidebar-menu {
  border-right: none;
  background: transparent;
}

.sidebar-menu .el-menu-item {
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xs);
  transition: all 0.3s ease;
}

.sidebar-menu .el-menu-item:hover {
  background: var(--primary-50);
  color: var(--primary-600);
}

.sidebar-menu .el-menu-item.is-active {
  background: var(--primary-100);
  color: var(--primary-700);
  font-weight: 500;
}

.main-content {
  flex: 1;
  min-width: 0;
  max-width: calc(100vw - 220px);
  width: calc(100vw - 220px);
  padding: var(--spacing-md);
  background: var(--bg-primary);
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

.placeholder-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .interviewee-page {
    flex-direction: column;
    height: auto;
    min-height: calc(100vh - 120px);
  }

  .sidebar {
    width: 100%;
    max-width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border-primary);
  }

  .main-content {
    max-width: 100%;
    width: 100%;
    padding: var(--spacing-sm);
  }

  .sidebar-menu {
    display: flex;
    overflow-x: auto;
  }

  .sidebar-menu .el-menu-item {
    white-space: nowrap;
    margin-bottom: 0;
    margin-right: var(--spacing-xs);
  }
}
</style>

