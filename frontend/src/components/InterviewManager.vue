<template>
  <div class="interview-manager">
    <!-- 头部操作栏 -->
    <div class="manager-header">
      <div class="header-left">
        <h3>面试管理</h3>
        <el-tag :type="getStatusType(statusFilter)" class="status-filter-tag" v-if="statusFilter">
          {{ INTERVIEW_STATUS_LABELS[statusFilter] }}
        </el-tag>
      </div>
      <div class="header-right">
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          clearable
          class="status-filter"
          @change="loadInterviews"
        >
          <el-option label="全部" value="" />
          <el-option
            v-for="(label, status) in INTERVIEW_STATUS_LABELS"
            :key="status"
            :label="label"
            :value="status"
          />
        </el-select>
        <el-button
          type="primary"
          @click="showCreateDialog"
          size="large"
          class="create-btn"
        >
          <template #icon>
            <el-icon><Plus /></el-icon>
          </template>
          创建面试
        </el-button>
      </div>
    </div>

    <!-- 面试列表 -->
    <div class="interview-list">
      <el-table
        :data="interviews"
        v-loading="loading"
        stripe
        class="interview-table"
      >
        <el-table-column prop="title" label="面试标题" min-width="200">
          <template #default="{ row }">
            <el-link @click="viewDetails(row)" :underline="false" class="interview-title">
              {{ row.title }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="job_requirement" label="关联岗位" min-width="150">
          <template #default="{ row }">
            <span v-if="row.job_requirement">{{ row.job_requirement.job_title }}</span>
            <span v-else class="text-secondary">未设置</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="interviewee" label="面试者" min-width="120">
          <template #default="{ row }">
            <span v-if="row.interviewee">{{ row.interviewee.username }}</span>
            <el-tag v-else type="info" size="small">未分配</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ INTERVIEW_STATUS_LABELS[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="question_count" label="题数" width="80" />
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <div class="operation-buttons">
              <el-button
                type="primary"
                size="small"
                @click="viewDetails(row)"
              >
                查看
              </el-button>
              <el-button
                v-if="row.status === 'draft'"
                type="warning"
                size="small"
                @click="editInterview(row)"
              >
                编辑
              </el-button>
              <el-button
                v-if="row.status === 'draft' && row.interviewee_id"
                type="success"
                size="small"
                @click="dispatchInterview(row)"
              >
                派发
              </el-button>
              <el-popconfirm
                title="确定删除这个面试吗？删除后将无法恢复！"
                confirm-button-text="确定删除"
                cancel-button-text="取消"
                confirm-button-type="danger"
                @confirm="deleteInterview(row.id)"
              >
                <template #reference>
                  <el-button
                    v-if="row.status === 'draft'"
                    type="danger"
                    size="small"
                  >
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>

        <!-- 空状态 -->
        <template #empty>
          <div class="empty-state">
            <el-empty 
              :image-size="120"
              :description="statusFilter ? '没有找到符合条件的面试' : '暂无面试数据'"
            >
              <template #image>
                <svg viewBox="0 0 64 64" style="width: 120px; height: 120px;">
                  <path d="M32 12c11 0 20 9 20 20s-9 20-20 20-20-9-20-20 9-20 20-20z" fill="none" stroke="#ddd" stroke-width="2"/>
                  <path d="M26 24h12v16H26z" fill="#f5f5f5" stroke="#ddd" stroke-width="1"/>
                  <circle cx="32" cy="28" r="2" fill="#999"/>
                  <path d="M28 36h8" stroke="#999" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </template>
              <el-button v-if="!statusFilter" type="primary" @click="showCreateDialog">
                创建第一个面试
              </el-button>
            </el-empty>
          </div>
        </template>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-container" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadInterviews"
        @current-change="loadInterviews"
      />
    </div>

    <!-- 创建/编辑面试对话框 -->
    <InterviewForm
      v-model:visible="formDialogVisible"
      :interview="currentInterview"
      @success="handleFormSuccess"
    />

    <!-- 面试详情对话框 -->
    <InterviewDetail
      v-model:visible="detailDialogVisible"
      :interview-id="currentInterviewId"
      @refresh="loadInterviews"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { interviewApi, INTERVIEW_STATUS_LABELS } from '../api/interviews'
import { useAuthStore } from '../store/auth'
import InterviewForm from './InterviewForm.vue'
import InterviewDetail from './InterviewDetail.vue'

// 获取用户信息
const auth = useAuthStore()
console.log('当前用户信息:', auth.user) // 调试日志

// 响应式数据
const loading = ref(false)
const interviews = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const statusFilter = ref('')

// 对话框状态
const formDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentInterview = ref(null)
const currentInterviewId = ref(null)

// 加载面试列表
async function loadInterviews() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      size: pageSize.value
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    const response = await interviewApi.getInterviews(params)
    
    // 处理不同的响应格式
    if (response.data) {
      interviews.value = response.data.data || response.data || []
      total.value = response.data.total || interviews.value.length
    } else {
      interviews.value = []
      total.value = 0
    }
  } catch (error) {
    console.error('加载面试列表失败:', error)
    const message = error.response?.data?.message || '加载面试列表失败'
    ElMessage.error(message)
    interviews.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 显示创建对话框
function showCreateDialog() {
  currentInterview.value = null
  formDialogVisible.value = true
}

// 编辑面试
function editInterview(interview) {
  currentInterview.value = { ...interview }
  formDialogVisible.value = true
}

// 查看详情
function viewDetails(interview) {
  if (!interview || !interview.id) {
    ElMessage.error('无效的面试数据')
    return
  }
  
  console.log('查看面试详情:', interview) // 调试日志
  currentInterviewId.value = interview.id
  detailDialogVisible.value = true
}

// 删除面试
async function deleteInterview(id) {
  try {
    const interview = interviews.value.find(item => item.id === id)
    if (!interview) {
      ElMessage.error('找不到要删除的面试')
      return
    }

    // 只有草稿状态的面试才能删除
    if (interview.status !== 'draft') {
      ElMessage.warning('只能删除草稿状态的面试')
      return
    }

    loading.value = true
    await interviewApi.deleteInterview(id)
    ElMessage.success('面试删除成功')
    
    // 如果当前页没有数据了，回到上一页
    if (interviews.value.length === 1 && currentPage.value > 1) {
      currentPage.value -= 1
    }
    
    await loadInterviews()
  } catch (error) {
    console.error('删除面试失败:', error)
    const message = error.response?.data?.message || '删除面试失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

// 派发面试
async function dispatchInterview(interview) {
  try {
    if (!interview.interviewee_id) {
      ElMessage.error('请先为面试分配面试者')
      return
    }

    loading.value = true
    await interviewApi.updateInterviewStatus(interview.id, 'assigned')
    ElMessage.success('面试派发成功，面试者现在可以查看该面试')
    await loadInterviews()
  } catch (error) {
    console.error('派发面试失败:', error)
    const message = error.response?.data?.message || '派发面试失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

// 表单成功回调
function handleFormSuccess() {
  formDialogVisible.value = false
  loadInterviews()
}

// 获取状态类型
function getStatusType(status) {
  const typeMap = {
    'draft': '',
    'assigned': 'warning',
    'in_progress': 'primary',
    'pending_evaluation': 'warning',
    'completed': 'success',
    'evaluated': 'info'
  }
  return typeMap[status] || ''
}

// 格式化日期时间
function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadInterviews()
})
</script>

<style scoped>
.interview-manager {
  padding: var(--spacing-md);
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.header-left h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: 600;
}

.status-filter-tag {
  font-size: var(--font-size-sm);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.status-filter {
  width: 150px;
}

.interview-list {
  flex: 1;
  overflow: auto;
}

.interview-table {
  width: 100%;
}

.interview-title {
  font-weight: 500;
  color: var(--primary-600);
}

.interview-title:hover {
  color: var(--primary-700);
}

.text-secondary {
  color: var(--text-tertiary);
  font-style: italic;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: var(--spacing-lg) 0;
  border-top: 1px solid var(--border-light);
  margin-top: var(--spacing-md);
}

.empty-state {
  padding: var(--spacing-xl) 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .manager-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: stretch;
  }

  .header-right {
    justify-content: space-between;
  }

  .status-filter {
    flex: 1;
  }
}

/* 操作按钮布局 */
.operation-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
}

.operation-buttons .el-button {
  margin: 0;
}

/* 确保按钮在移动端也能合理显示 */
@media (max-width: 768px) {
  .operation-buttons {
    flex-direction: column;
    gap: 4px;
    align-items: stretch;
  }
  
  .operation-buttons .el-button {
    font-size: 12px;
    padding: 4px 8px;
  }
}
</style>