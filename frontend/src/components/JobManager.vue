<template>
  <div class="job-manager">
    <div class="job-header">
      <div class="header-content">
        <div class="header-title">
          <h2>岗位管理</h2>
          <p>管理和维护面试岗位信息</p>
        </div>
        <el-button 
          type="primary" 
          @click="showCreateDialog" 
          size="large"
          class="create-btn"
        >
          <template #icon>
            <el-icon><Plus /></el-icon>
          </template>
          新增岗位
        </el-button>
      </div>
    </div>

    <div class="job-content card">
      <div class="job-filters">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索岗位名称或技能..."
          style="width: 300px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <div class="job-table-container">
        <el-table 
          :data="filteredJobs" 
          class="job-table" 
          empty-text="暂无岗位数据"
          stripe
          v-loading="loading"
          style="width: 100%"
          :table-layout="'fixed'"
        >
          <el-table-column prop="job_title" label="岗位名称" width="160" sortable>
            <template #default="{ row }">
              <div class="job-title-cell">
                <div class="job-name">{{ row.job_title }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="description" label="岗位描述" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="job-description">
                {{ row.description || '暂无描述' }}
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="技能要求" width="240">
            <template #default="{ row }">
              <div class="skills-container">
                <el-tag 
                  v-for="(skill, idx) in (row.skills || []).slice(0, 3)" 
                  :key="idx" 
                  class="skill-tag"
                  size="small"
                  type="info"
                >
                  {{ skill }}
                </el-tag>
                <el-tag 
                  v-if="row.skills && row.skills.length > 3"
                  size="small"
                  type="info"
                  class="more-skills"
                >
                  +{{ row.skills.length - 3 }}
                </el-tag>
                <span v-if="!row.skills || row.skills.length === 0" class="no-skills">
                  暂无技能要求
                </span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button 
                  type="primary" 
                  size="small"
                  @click="showDetailDialog(row)"
                >
                  查看
                </el-button>
                <el-button 
                  type="warning" 
                  size="small"
                  @click="showEditDialog(row)"
                >
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  size="small"
                  @click="confirmDelete(row)"
                >
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 岗位详情对话框 -->
    <JobDetail
      v-model:visible="detailVisible"
      :job-data="currentJob"
      @edit="showEditDialog"
    />

    <!-- 新增/编辑岗位对话框 -->
    <JobForm
      v-model:visible="formVisible"
      :job-data="editingJob"
      :is-edit="isEdit"
      :loading="submitting"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, 
  Search
} from '@element-plus/icons-vue'
import { listJobs, createJob, getJob, updateJob, deleteJob } from '../api/jobs'
import JobDetail from './JobDetail.vue'
import JobForm from './JobForm.vue'

const jobs = ref([])
const loading = ref(false)
const submitting = ref(false)
const searchKeyword = ref('')

// 对话框状态
const detailVisible = ref(false)
const formVisible = ref(false)
const isEdit = ref(false)

// 当前数据
const currentJob = ref(null)
const editingJob = ref({})

// 计算属性 - 过滤后的岗位列表
const filteredJobs = computed(() => {
  if (!searchKeyword.value.trim()) {
    return jobs.value
  }
  
  const keyword = searchKeyword.value.toLowerCase()
  return jobs.value.filter(job => {
    const titleMatch = job.job_title?.toLowerCase().includes(keyword)
    const skillsMatch = job.skills?.some(skill => skill.toLowerCase().includes(keyword))
    const descMatch = job.description?.toLowerCase().includes(keyword)
    return titleMatch || skillsMatch || descMatch
  })
})

// 页面加载时获取数据
onMounted(() => {
  loadJobs()
})

// 加载岗位列表
async function loadJobs() {
  loading.value = true
  try {
    jobs.value = await listJobs()
  } catch (error) {
    ElMessage.error('获取岗位列表失败')
    console.error('Failed to load jobs:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
function handleSearch() {
  // 实时搜索，由计算属性处理
}

// 显示创建对话框
function showCreateDialog() {
  isEdit.value = false
  editingJob.value = {}
  formVisible.value = true
}

// 显示详情对话框
async function showDetailDialog(job) {
  try {
    const jobDetail = await getJob(job.id)
    currentJob.value = jobDetail
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('获取岗位详情失败')
    console.error('Failed to load job detail:', error)
  }
}

// 显示编辑对话框
function showEditDialog(job) {
  isEdit.value = true
  editingJob.value = { ...job }
  formVisible.value = true
}

// 处理表单提交
async function handleSubmit(formData) {
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateJob(editingJob.value.id, formData)
      ElMessage.success('岗位更新成功')
    } else {
      await createJob(formData)
      ElMessage.success('岗位创建成功')
    }
    
    formVisible.value = false
    await loadJobs()
  } catch (error) {
    console.error('Failed to save job:', error)
    
    if (error.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
    } else if (error.status === 403) {
      ElMessage.error('权限不足，只有管理员和面试官可以操作岗位')
    } else {
      const action = isEdit.value ? '更新' : '创建'
      ElMessage.error(`${action}岗位失败: ${error.data?.message || error.message || '未知错误'}`)
    }
  } finally {
    submitting.value = false
  }
}

// 处理取消操作
function handleCancel() {
  formVisible.value = false
  editingJob.value = {}
}

// 确认删除
async function confirmDelete(job) {
  try {
    await ElMessageBox.confirm(
      `确定要删除岗位"${job.job_title}"吗？此操作不可撤销。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await deleteJob(job.id)
    ElMessage.success('岗位删除成功')
    await loadJobs()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    
    console.error('Failed to delete job:', error)
    if (error.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
    } else if (error.status === 403) {
      ElMessage.error('权限不足，只有管理员和面试官可以删除岗位')
    } else {
      ElMessage.error('删除岗位失败: ' + (error.data?.message || error.message || '未知错误'))
    }
  }
}
</script>

<style scoped>
.job-manager {
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.job-header {
  margin-bottom: var(--spacing-xl);
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.header-title h2 {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.header-title p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
}

.create-btn {
  flex-shrink: 0;
  border-radius: var(--radius-md);
  font-weight: 500;
}

.job-content {
  padding: var(--spacing-xl);
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.job-filters {
  margin-bottom: var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  flex-shrink: 0;
}

.job-table-container {
  border-radius: var(--radius-md);
  overflow: hidden;
  max-width: 100%;
  flex: 1;
  min-height: 0;
}

.job-table {
  width: 100%;
  max-width: 100%;
  table-layout: fixed;
}

.job-title-cell {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.job-name {
  font-weight: 500;
  color: var(--text-primary);
}

.job-description {
  color: var(--text-secondary);
  line-height: 1.4;
  word-break: break-word;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  align-items: center;
  max-width: 100%;
  overflow: hidden;
}

.skill-tag {
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-skills {
  background: var(--gray-100);
  color: var(--text-secondary);
  border: 1px solid var(--border-primary);
  flex-shrink: 0;
}

.no-skills {
  color: var(--text-tertiary);
  font-size: var(--font-size-xs);
  font-style: italic;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
  align-items: center;
  flex-wrap: nowrap;
  max-width: 100%;
}

.action-buttons .el-button {
  flex-shrink: 0;
  min-width: 50px;
  padding: 6px 12px;
  font-size: var(--font-size-xs);
}

/* Element Plus 表格样式覆盖 */
:deep(.el-table) {
  border: 1px solid var(--border-primary);
  width: 100% !important;
  max-width: 100% !important;
  table-layout: fixed !important;
}

:deep(.el-table__header) {
  background: var(--bg-secondary);
}

:deep(.el-table th) {
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-weight: 500;
  border-bottom: 1px solid var(--border-primary);
  padding: 12px 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.el-table td) {
  border-bottom: 1px solid var(--border-primary);
  padding: 12px 8px;
  overflow: hidden;
}

:deep(.el-table__row:hover) {
  background: var(--bg-secondary);
}

:deep(.el-table__empty-text) {
  color: var(--text-tertiary);
}

:deep(.el-table__body-wrapper) {
  overflow-x: auto;
  max-width: 100%;
}

:deep(.el-table .cell) {
  word-break: break-word;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.el-table__fixed-right) {
  right: 0 !important;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }
  
  .job-filters {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }
  
  .job-filters .el-input {
    width: 100% !important;
  }
}

@media (max-width: 768px) {
  .job-content {
    padding: var(--spacing-lg);
  }
  
  .action-buttons {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .action-buttons .el-button {
    width: 100%;
    min-width: unset;
  }
  
  :deep(.el-table__body-wrapper) {
    overflow-x: auto;
  }
}

@media (max-width: 480px) {
  .job-content {
    padding: var(--spacing-md);
  }
  
  .header-title h2 {
    font-size: var(--font-size-xl);
  }
}
</style>