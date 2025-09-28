<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h1 class="page-title">系统管理</h1>
      <p class="page-subtitle">管理系统设置、用户和数据</p>
    </div>

    <div class="admin-grid">
      <!-- 系统概览 -->
      <div class="card overview-card">
        <div class="card-header">
          <h3>系统概览</h3>
          <el-tag type="success">系统正常</el-tag>
        </div>
        <div class="card-body">
          <div class="overview-stats">
            <div class="overview-item">
              <div class="overview-label">服务器状态</div>
              <div class="overview-value status-success">正常运行</div>
            </div>
            <div class="overview-item">
              <div class="overview-label">数据库连接</div>
              <div class="overview-value status-success">连接正常</div>
            </div>
            <div class="overview-item">
              <div class="overview-label">内存使用</div>
              <div class="overview-value">68%</div>
            </div>
            <div class="overview-item">
              <div class="overview-label">磁盘空间</div>
              <div class="overview-value">42%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 用户管理 -->
      <div class="card users-card">
        <div class="card-header">
          <h3>用户管理</h3>
          <el-button type="primary" size="small">
            <template #icon>
              <el-icon><Plus /></el-icon>
            </template>
            新增用户
          </el-button>
        </div>
        <div class="card-body">
          <div class="user-stats">
            <div class="user-stat">
              <span class="stat-number">1,234</span>
              <span class="stat-label">总用户数</span>
            </div>
            <div class="user-stat">
              <span class="stat-number">892</span>
              <span class="stat-label">活跃用户</span>
            </div>
            <div class="user-stat">
              <span class="stat-number">156</span>
              <span class="stat-label">新注册</span>
            </div>
          </div>
          <div class="quick-actions">
            <el-button size="small" @click="manageUsers">管理用户</el-button>
            <el-button size="small" @click="viewReports">查看报告</el-button>
          </div>
        </div>
      </div>

      <!-- 数据统计 -->
      <div class="card analytics-card">
        <div class="card-header">
          <h3>数据分析</h3>
        </div>
        <div class="card-body">
          <div class="chart-placeholder">
            <div class="chart-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <p>面试数据统计图表</p>
            <small>展示最近30天的面试趋势</small>
          </div>
        </div>
      </div>

      <!-- 面试管理 -->
      <div class="card interview-management-card">
        <div class="card-header">
          <h3>面试管理</h3>
          <el-button type="primary" size="small" @click="manageInterviews">
            <template #icon>
              <el-icon><Management /></el-icon>
            </template>
            管理面试
          </el-button>
        </div>
        <div class="card-body">
          <div class="interview-stats">
            <div class="interview-stat">
              <span class="stat-number">{{ interviewStats.total || 0 }}</span>
              <span class="stat-label">总面试数</span>
            </div>
            <div class="interview-stat">
              <span class="stat-number">{{ interviewStats.active || 0 }}</span>
              <span class="stat-label">进行中</span>
            </div>
            <div class="interview-stat">
              <span class="stat-number">{{ interviewStats.completed || 0 }}</span>
              <span class="stat-label">已完成</span>
            </div>
          </div>
          <div class="quick-actions">
            <el-button size="small" @click="manageInterviews">管理面试</el-button>
            <el-button size="small" @click="cleanupData" type="warning">清理数据</el-button>
          </div>
        </div>
      </div>

      <!-- 快速操作 */
      <div class="card actions-card">
        <div class="card-header">
          <h3>快速操作</h3>
        </div>
        <div class="card-body">
          <div class="action-list">
            <div class="action-item" @click="backupData">
              <div class="action-icon">
                <el-icon><Download /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">数据备份</div>
                <div class="action-desc">备份系统数据</div>
              </div>
            </div>
            
            <div class="action-item" @click="systemLogs">
              <div class="action-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">系统日志</div>
                <div class="action-desc">查看系统运行日志</div>
              </div>
            </div>
            
            <div class="action-item" @click="systemSettings">
              <div class="action-icon">
                <el-icon><Setting /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">系统设置</div>
                <div class="action-desc">配置系统参数</div>
              </div>
            </div>
            
            <div class="action-item" @click="securityAudit">
              <div class="action-icon">
                <el-icon><Lock /></el-icon>
              </div>
              <div class="action-content">
                <div class="action-title">安全审计</div>
                <div class="action-desc">系统安全检查</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="card recent-activity-card">
        <div class="card-header">
          <h3>最近活动</h3>
          <el-button type="text" size="small">查看全部</el-button>
        </div>
        <div class="card-body">
          <div class="activity-timeline">
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <div class="timeline-title">用户张三注册账户</div>
                <div class="timeline-time">2小时前</div>
              </div>
            </div>
            
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <div class="timeline-title">系统自动备份完成</div>
                <div class="timeline-time">4小时前</div>
              </div>
            </div>
            
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <div class="timeline-title">面试题库更新</div>
                <div class="timeline-time">6小时前</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统信息 -->
      <div class="card system-info-card">
        <div class="card-header">
          <h3>系统信息</h3>
        </div>
        <div class="card-body">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span class="info-value">v2.1.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">Python版本</span>
              <span class="info-value">3.11.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">数据库</span>
              <span class="info-value">PostgreSQL 14</span>
            </div>
            <div class="info-item">
              <span class="info-label">启动时间</span>
              <span class="info-value">2025-09-19 08:00:00</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 面试管理对话框 -->
    <el-dialog
      v-model="interviewManagementVisible"
      title="面试管理"
      width="90%"
      :close-on-click-modal="false"
    >
      <div class="interview-management">
        <div class="management-header">
          <div class="header-left">
            <h3>面试记录管理</h3>
            <p>管理系统中的所有面试记录，支持批量删除</p>
          </div>
          <div class="header-right">
            <el-button @click="loadInterviews" :loading="loading">
              <template #icon>
                <el-icon><Refresh /></el-icon>
              </template>
              刷新
            </el-button>
            <el-button 
              type="danger" 
              :disabled="selectedInterviews.length === 0"
              @click="batchDelete"
            >
              <template #icon>
                <el-icon><Delete /></el-icon>
              </template>
              批量删除 ({{ selectedInterviews.length }})
            </el-button>
          </div>
        </div>

        <div class="management-filters">
          <el-form :model="filters" inline>
            <el-form-item label="状态筛选">
              <el-select v-model="filters.status" placeholder="选择状态" clearable style="width: 150px;">
                <el-option label="草稿" value="draft" />
                <el-option label="已分配" value="assigned" />
                <el-option label="进行中" value="in_progress" />
                <el-option label="待评价" value="pending_evaluation" />
                <el-option label="已完成" value="completed" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键词">
              <el-input 
                v-model="filters.keyword" 
                placeholder="搜索面试标题或面试者"
                style="width: 200px;"
                clearable
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchInterviews">搜索</el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="management-table">
          <el-table 
            :data="interviews" 
            v-loading="loading"
            @selection-change="handleSelectionChange"
            stripe
            border
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="title" label="面试标题" min-width="200" />
            <el-table-column label="岗位" min-width="150">
              <template #default="{ row }">
                {{ row.job_requirement?.job_title || '未知岗位' }}
              </template>
            </el-table-column>
            <el-table-column label="面试者" min-width="120">
              <template #default="{ row }">
                {{ row.interviewee?.username || '未分配' }}
              </template>
            </el-table-column>
            <el-table-column label="面试官" min-width="120">
              <template #default="{ row }">
                {{ row.interviewer?.username || '未知' }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="题目数量" width="100">
              <template #default="{ row }">
                {{ row.question_count || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="viewInterview(row)"
                >
                  查看
                </el-button>
                <el-popconfirm
                  title="确定删除这个面试记录吗？将同时删除相关的题目和评价！"
                  @confirm="deleteInterview(row.id)"
                >
                  <template #reference>
                    <el-button type="danger" size="small">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>

          <div class="table-pagination">
            <el-pagination
              v-model:current-page="pagination.page"
              v-model:page-size="pagination.size"
              :total="pagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadInterviews"
              @current-change="loadInterviews"
            />
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, 
  TrendCharts, 
  Download, 
  Document, 
  Setting, 
  Lock,
  Management,
  Refresh,
  Delete
} from '@element-plus/icons-vue'
import { interviewApi, INTERVIEW_STATUS_LABELS } from '../api/interviews.js'

// 面试管理相关数据
const interviewManagementVisible = ref(false)
const interviews = ref([])
const selectedInterviews = ref([])
const loading = ref(false)
const interviewStats = ref({
  total: 0,
  active: 0,
  completed: 0
})

// 筛选和分页
const filters = ref({
  status: '',
  keyword: ''
})

const pagination = ref({
  page: 1,
  size: 20,
  total: 0
})

function manageUsers() {
  ElMessage.info('用户管理功能开发中...')
}

function viewReports() {
  ElMessage.info('报告功能开发中...')
}

function backupData() {
  ElMessage.success('数据备份已启动')
}

function systemLogs() {
  ElMessage.info('系统日志功能开发中...')
}

function systemSettings() {
  ElMessage.info('系统设置功能开发中...')
}

function securityAudit() {
  ElMessage.info('安全审计功能开发中...')
}

// 面试管理方法
function manageInterviews() {
  interviewManagementVisible.value = true
  loadInterviews()
}

// 加载面试列表
async function loadInterviews() {
  try {
    loading.value = true
    const params = {
      page: pagination.value.page,
      per_page: pagination.value.size,
      status: filters.value.status,
      keyword: filters.value.keyword
    }
    
    const response = await interviewApi.getInterviews(params)
    interviews.value = response.data.data || response.data.interviews || []
    pagination.value.total = response.data.total || interviews.value.length
    
    // 更新统计信息
    updateInterviewStats()
  } catch (error) {
    console.error('加载面试列表失败:', error)
    ElMessage.error('加载面试列表失败')
  } finally {
    loading.value = false
  }
}

// 更新面试统计信息
function updateInterviewStats() {
  interviewStats.value = {
    total: interviews.value.length,
    active: interviews.value.filter(i => ['assigned', 'in_progress'].includes(i.status)).length,
    completed: interviews.value.filter(i => i.status === 'completed').length
  }
}

// 搜索面试
function searchInterviews() {
  pagination.value.page = 1
  loadInterviews()
}

// 处理选择变化
function handleSelectionChange(selection) {
  selectedInterviews.value = selection
}

// 查看面试详情
function viewInterview(interview) {
  ElMessage.info(`查看面试: ${interview.title}`)
  // TODO: 这里可以集成面试详情组件
}

// 删除单个面试
async function deleteInterview(interviewId) {
  try {
    await interviewApi.deleteInterview(interviewId)
    ElMessage.success('面试记录删除成功')
    loadInterviews()
  } catch (error) {
    console.error('删除面试失败:', error)
    ElMessage.error(error.response?.data?.message || '删除面试失败')
  }
}

// 批量删除面试
async function batchDelete() {
  if (selectedInterviews.value.length === 0) {
    ElMessage.warning('请选择要删除的面试记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedInterviews.value.length} 个面试记录吗？\n删除后将无法恢复，相关的题目和评价也会被删除！`,
      '批量删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        dangerouslyUseHTMLString: true
      }
    )
    
    loading.value = true
    const deletePromises = selectedInterviews.value.map(interview => 
      interviewApi.deleteInterview(interview.id)
    )
    
    await Promise.all(deletePromises)
    ElMessage.success(`成功删除 ${selectedInterviews.value.length} 个面试记录`)
    selectedInterviews.value = []
    loadInterviews()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 清理数据
async function cleanupData() {
  try {
    await ElMessageBox.confirm(
      '此操作将清理已完成超过30天的面试记录，确定继续吗？',
      '数据清理确认',
      {
        confirmButtonText: '确定清理',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.success('数据清理任务已启动')
    // TODO: 实现数据清理逻辑
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('数据清理失败')
    }
  }
}

// 获取状态标签
function getStatusLabel(status) {
  return INTERVIEW_STATUS_LABELS[status] || status
}

// 获取状态类型
function getStatusType(status) {
  const typeMap = {
    'draft': 'info',
    'assigned': 'warning',
    'in_progress': 'primary',
    'pending_evaluation': 'warning',
    'completed': 'success'
  }
  return typeMap[status] || 'info'
}

// 格式化日期时间
function formatDateTime(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 组件挂载时加载统计数据
onMounted(async () => {
  // 加载面试统计数据 - 不需要打开对话框，只获取基本统计
  try {
    const response = await interviewApi.getInterviews({ per_page: 1 }) // 只获取1条记录用于统计
    const allInterviews = response.data.data || response.data.interviews || []
    
    // 这里可以调用一个专门的统计API，现在先用简单统计
    interviewStats.value = {
      total: response.data.total || 0,
      active: 0, // 需要专门的统计API
      completed: 0 // 需要专门的统计API
    }
  } catch (error) {
    console.error('加载面试统计失败:', error)
  }
})
</script>

<style scoped>
.admin-panel {
  width: 100%;
}

.admin-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-xl);
}

/* 系统概览卡片 */
.overview-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.overview-item {
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.overview-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.overview-value {
  font-weight: 600;
  color: var(--text-primary);
}

.status-success {
  color: var(--success);
}

/* 用户管理卡片 */
.users-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: var(--spacing-lg);
}

.user-stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--primary-600);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.quick-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
}

/* 数据分析卡片 */
.chart-placeholder {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.chart-icon {
  font-size: 48px;
  color: var(--primary-400);
  margin-bottom: var(--spacing-md);
}

.chart-placeholder p {
  margin: 0 0 var(--spacing-sm) 0;
  font-weight: 500;
  color: var(--text-primary);
}

.chart-placeholder small {
  color: var(--text-secondary);
}

/* 快速操作卡片 */
.action-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.action-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-item:hover {
  background: var(--bg-tertiary);
  transform: translateX(4px);
}

.action-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--primary-100);
  color: var(--primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-content {
  flex: 1;
}

.action-title {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.action-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* 活动时间线 */
.recent-activity-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 20px;
  width: 1px;
  height: calc(100% + var(--spacing-lg));
  background: var(--border-primary);
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary-500);
  flex-shrink: 0;
  margin-top: 4px;
}

.timeline-content {
  flex: 1;
}

.timeline-title {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.timeline-time {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* 系统信息 */
.info-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--border-primary);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.info-value {
  color: var(--text-primary);
  font-weight: 500;
  font-size: var(--font-size-sm);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .overview-stats {
    grid-template-columns: 1fr;
  }
  
  .user-stats {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .quick-actions {
    flex-direction: column;
  }
}

/* 面试管理样式 */
.interview-management {
  padding: 0;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.header-left h3 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 18px;
}

.header-left p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 12px;
}

.management-filters {
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 6px;
}

.management-table {
  border-radius: 6px;
  overflow: hidden;
}

.table-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 面试统计样式 */
.interview-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 16px;
}

.interview-stat {
  text-align: center;
}

.interview-stat .stat-number {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 4px;
}

.interview-stat .stat-label {
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .management-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .header-right {
    justify-content: flex-start;
  }
  
  .management-filters .el-form {
    flex-direction: column;
  }
  
  .management-filters .el-form-item {
    margin-bottom: 16px;
  }
}
</style>
