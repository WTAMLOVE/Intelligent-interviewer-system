<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="page-title">欢迎来到智能面试官</h1>
      <p class="page-subtitle">您的智能面试助手，让面试更高效、更专业</p>
    </div>

    <div class="dashboard-grid">
      <!-- 快速操作卡片 -->
      <div class="card action-card">
        <div class="card-header">
          <h3>快速开始</h3>
        </div>
        <div class="card-body">
          <div class="action-buttons">
            <el-button 
              type="primary" 
              size="large"
              @click="$router.push('/admin')"
              class="action-btn"
            >
              <template #icon>
                <el-icon><Setting /></el-icon>
              </template>
              系统管理
            </el-button>
            
            <el-button 
              type="success" 
              size="large"
              @click="$router.push('/interviewer')"
              class="action-btn"
            >
              <template #icon>
                <el-icon><Avatar /></el-icon>
              </template>
              面试管理
            </el-button>
          </div>
        </div>
      </div>

      <!-- 统计信息卡片 -->
      <div class="card stats-card">
        <div class="card-header">
          <h3>数据概览</h3>
        </div>
        <div class="card-body">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon primary">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">156</div>
                <div class="stat-label">活跃用户</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon success">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">324</div>
                <div class="stat-label">面试题目</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon warning">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">89</div>
                <div class="stat-label">进行中面试</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon info">
                <el-icon><Trophy /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">2,341</div>
                <div class="stat-label">完成面试</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="card activity-card">
        <div class="card-header">
          <h3>最近活动</h3>
        </div>
        <div class="card-body">
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon">
                <el-icon><MessageBox /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">新增面试题目</div>
                <div class="activity-desc">添加了 "React Hooks 使用场景" 面试题</div>
                <div class="activity-time">2 小时前</div>
              </div>
            </div>
            
            <div class="activity-item">
              <div class="activity-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">用户注册</div>
                <div class="activity-desc">张三完成了账户注册</div>
                <div class="activity-time">4 小时前</div>
              </div>
            </div>
            
            <div class="activity-item">
              <div class="activity-icon">
                <el-icon><Check /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">面试完成</div>
                <div class="activity-desc">李四完成了前端开发岗位面试</div>
                <div class="activity-time">6 小时前</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能导航 -->
      <div class="card features-card">
        <div class="card-header">
          <h3>功能导航</h3>
        </div>
        <div class="card-body">
          <div class="features-grid">
            <router-link to="/interviewer" class="feature-item">
              <div class="feature-icon">
                <el-icon><Avatar /></el-icon>
              </div>
              <div class="feature-title">面试官模式</div>
              <div class="feature-desc">创建面试，管理候选人</div>
            </router-link>
            
            <router-link to="/interviewee" class="feature-item">
              <div class="feature-icon">
                <el-icon><UserFilled /></el-icon>
              </div>
              <div class="feature-title">面试者模式</div>
              <div class="feature-desc">参与面试，展示技能</div>
            </router-link>
            
            <router-link to="/admin" class="feature-item">
              <div class="feature-icon">
                <el-icon><Tools /></el-icon>
              </div>
              <div class="feature-title">系统设置</div>
              <div class="feature-desc">配置系统参数</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  DocumentAdd, 
  Setting, 
  User, 
  Document, 
  Clock, 
  Trophy, 
  MessageBox, 
  Check, 
  Avatar, 
  UserFilled, 
  Tools 
} from '@element-plus/icons-vue'
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.dashboard-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-xl);
}

/* 快速操作卡片 */
.action-card .card-body {
  padding: var(--spacing-xl);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-lg);
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 140px;
  height: 60px;
  font-size: var(--font-size-base);
  font-weight: 500;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.stat-icon.primary { background: var(--primary-500); }
.stat-icon.success { background: var(--success); }
.stat-icon.warning { background: var(--warning); }
.stat-icon.info { background: var(--info); }

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.activity-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.activity-item:hover {
  background: var(--bg-tertiary);
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--primary-100);
  color: var(--primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.activity-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.activity-time {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* 功能导航 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  background: var(--bg-secondary);
  text-decoration: none;
  color: var(--text-primary);
  transition: all var(--transition-fast);
  gap: var(--spacing-sm);
}

.feature-item:hover {
  background: var(--bg-tertiary);
  transform: translateY(-2px);
  box-shadow: var(--card-shadow);
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--primary-100);
  color: var(--primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.feature-title {
  font-weight: 500;
  font-size: var(--font-size-sm);
}

.feature-desc {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .action-btn {
    min-width: 100%;
  }
  
  .stat-item {
    padding: var(--spacing-sm);
  }
  
  .feature-item {
    padding: var(--spacing-md);
  }
}
</style>
