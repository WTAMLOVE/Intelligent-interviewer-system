<template>
  <div class="resume-manager">
    <!-- 页面头部 -->
    <div class="resume-header">
      <div class="header-content">
        <div class="header-title">
          <h2>简历管理</h2>
          <p>管理您的个人简历，每个面试者只能拥有一份简历</p>
        </div>
        <div class="header-actions">
          <el-button 
            v-if="!hasResume"
            type="primary" 
            @click="openEditDialog" 
            size="large"
            class="create-btn"
          >
            <template #icon>
              <el-icon><Plus /></el-icon>
            </template>
            创建简历
          </el-button>
          <template v-else>
            <el-button 
              type="primary" 
              size="large"
              @click="openEditDialog"
            >
              <template #icon>
                <el-icon><Edit /></el-icon>
              </template>
              编辑简历
            </el-button>
            <el-button 
              type="danger" 
              size="large"
              :loading="deleteLoading"
              @click="handleDeleteResume"
            >
              <template #icon>
                <el-icon><Delete /></el-icon>
              </template>
              删除简历
            </el-button>
          </template>
        </div>
      </div>
    </div>

    <div class="resume-content card">
      <!-- 简历内容展示区 -->
      <div class="resume-display-container">
        <div v-if="!hasResume" class="empty-state">
          <div class="empty-icon">
            <el-icon size="64"><Document /></el-icon>
          </div>
          <h3 class="empty-title">暂无简历</h3>
          <p class="empty-description">您还没有创建简历，点击上方"创建简历"按钮开始创建</p>
        </div>

        <div v-else class="resume-display">
          <div class="resume-card">
            <div class="resume-card-header">
              <div class="card-title">
                <h3>我的简历</h3>
                <div class="card-meta">
                  <span class="meta-item">创建时间：{{ formatDate(resume.created_at) }}</span>
                  <span class="meta-item">更新时间：{{ formatDate(resume.updated_at) }}</span>
                </div>
              </div>
            </div>
            
            <div class="resume-card-body">
              <div class="resume-content-preview">
                <pre class="resume-text">{{ resume.content || '简历内容为空' }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <el-dialog
      v-model="editDialogVisible"
      :title="hasResume ? '编辑简历' : '创建简历'"
      width="800px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="edit-dialog-content">
        <el-form :model="editForm" ref="editFormRef" label-width="0px">
          <el-form-item required>
            <el-input
              v-model="editForm.content"
              type="textarea"
              :rows="20"
              placeholder="请输入您的个人简历内容..."
              maxlength="5000"
              show-word-limit
              resize="none"
            />
          </el-form-item>
        </el-form>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeEditDialog">取消</el-button>
          <el-button 
            type="primary" 
            :loading="saveLoading"
            @click="handleSaveResume"
          >
            {{ hasResume ? '更新简历' : '保存简历' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Edit, Delete, Check, Plus } from '@element-plus/icons-vue'
import { resumeAPI } from '../api/resumes.js'

// 响应式数据
const resume = ref(null)
const saveLoading = ref(false)
const deleteLoading = ref(false)
const editDialogVisible = ref(false)
const editFormRef = ref(null)

// 编辑表单数据
const editForm = reactive({
  content: ''
})

// 计算属性
const hasResume = computed(() => resume.value !== null)

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
// 加载简历数据
const loadResume = async () => {
  try {
    const response = await resumeAPI.getMyResume()
    if (response.data && response.data.data) {
      resume.value = response.data.data
    } else {
      resume.value = null
    }
  } catch (error) {
    ElMessage.error('加载简历失败: ' + (error.response?.data?.message || error.message))
  }
}

// 打开编辑弹窗
const openEditDialog = () => {
  editForm.content = resume.value ? resume.value.content : ''
  editDialogVisible.value = true
}

// 关闭编辑弹窗
const closeEditDialog = () => {
  editDialogVisible.value = false
  editForm.content = ''
}

// 保存简历
const handleSaveResume = async () => {
  try {
    // 添加二次确认
    const action = hasResume.value ? '更新' : '创建'
    await ElMessageBox.confirm(
      `确定要${action}简历吗？`,
      `${action}简历确认`,
      {
        confirmButtonText: `确定${action}`,
        cancelButtonText: '取消',
        type: 'info',
      }
    )

    saveLoading.value = true
    const response = await resumeAPI.saveMyResume(editForm.content || '')
    resume.value = response.data.data
    ElMessage.success(response.data.message || '简历保存成功')
    
    // 关闭弹窗
    closeEditDialog()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('保存简历失败: ' + (error.response?.data?.message || error.message))
    }
  } finally {
    saveLoading.value = false
  }
}

// 删除简历
const handleDeleteResume = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除您的简历吗？此操作不可恢复。',
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    deleteLoading.value = true
    await resumeAPI.deleteMyResume()
    
    resume.value = null
    ElMessage.success('简历删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除简历失败: ' + (error.response?.data?.message || error.message))
    }
  } finally {
    deleteLoading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadResume()
})
</script>

<style scoped>
.resume-manager {
  height: 100%;
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
}

/* 页面头部样式 */
.resume-header {
  padding: var(--spacing-lg) 0;
  border-bottom: 1px solid var(--border-primary);
  background: var(--bg-primary);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.header-title h2 {
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-2xl);
  font-weight: 600;
}

.header-title p {
  color: var(--text-secondary);
  margin: 0;
  font-size: var(--font-size-base);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

/* 卡片布局 */
.card {
  flex: 1;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  margin-top: var(--spacing-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.resume-content {
  padding: var(--spacing-lg);
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* 简历展示容器 */
.resume-display-container {
  flex: 1;
  overflow: auto;
  min-height: 0;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl);
  text-align: center;
  height: 400px;
}

.empty-icon {
  margin-bottom: var(--spacing-lg);
  color: var(--gray-300);
}

.empty-title {
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: 600;
  margin: 0 0 var(--spacing-sm) 0;
}

.empty-description {
  color: var(--text-secondary);
  font-size: var(--font-size-base);
  line-height: 1.6;
  margin: 0 0 var(--spacing-xl) 0;
  max-width: 400px;
}

/* 简历卡片样式 */
.resume-display {
  height: 100%;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.resume-card {
  background: var(--card-bg);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  height: 100%;
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.resume-card-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-primary);
  background: var(--bg-secondary);
}

.card-title h3 {
  color: var(--text-primary);
  font-size: var(--font-size-lg);
  font-weight: 600;
  margin: 0 0 var(--spacing-sm) 0;
}

.card-meta {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.meta-item {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.resume-card-body {
  padding: var(--spacing-lg);
  flex: 1;
  overflow: hidden;
}

.resume-content-preview {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  height: 100%;
  overflow: hidden;
}

.resume-text {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  font-size: var(--font-size-sm);
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  margin: 0;
  padding: var(--spacing-lg);
  background: var(--card-bg);
  height: 100%;
  overflow: auto;
  border: none;
  min-height: 300px;
}

/* 编辑弹窗样式 */
.edit-dialog-content {
  padding: var(--spacing-xs) 0;
}

.edit-dialog-content :deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--text-primary);
  font-size: var(--font-size-base);
}

.edit-dialog-content :deep(.el-textarea__inner) {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
  font-size: var(--font-size-sm);
  line-height: 1.6;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-primary);
  padding: var(--spacing-md);
  transition: var(--transition-base);
}

.edit-dialog-content :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}

.edit-dialog-content :deep(.el-textarea .el-input__count) {
  background: rgba(255, 255, 255, 0.9);
  border-radius: var(--radius-sm);
  padding: 2px var(--spacing-xs);
  font-size: var(--font-size-xs);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
}

/* 按钮样式优化 - 与岗位管理保持一致 */
:deep(.el-button) {
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: var(--transition-base);
}

:deep(.el-button--primary) {
  background: var(--primary-500);
  border-color: var(--primary-500);
}

:deep(.el-button--primary:hover) {
  background: var(--primary-600);
  border-color: var(--primary-600);
}

:deep(.el-button--danger) {
  background: var(--error);
  border-color: var(--error);
}

:deep(.el-button--danger:hover) {
  background: #dc2626;
  border-color: #dc2626;
}

/* 标签样式 */
:deep(.el-tag) {
  border-radius: var(--radius-sm);
  font-weight: 500;
  padding: var(--spacing-xs) var(--spacing-sm);
}

:deep(.el-tag--success) {
  background: var(--success);
  border-color: var(--success);
  color: var(--text-inverse);
}

/* 弹窗样式 */
:deep(.el-dialog) {
  border-radius: var(--radius-lg);
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background: var(--bg-secondary);
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--border-primary);
}

:deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: var(--spacing-xl);
}

:deep(.el-dialog__footer) {
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-primary);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }

  .header-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 768px) {
  .resume-content {
    padding: var(--spacing-lg);
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .empty-state {
    padding: var(--spacing-xl);
    height: 300px;
  }

  .resume-card-header {
    padding: var(--spacing-md);
  }

  .resume-card-body {
    padding: var(--spacing-md);
  }

  .card-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  :deep(.el-dialog) {
    width: 95% !important;
    margin: 0 auto;
  }

  :deep(.el-dialog__body) {
    padding: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .resume-content {
    padding: var(--spacing-md);
  }

  .header-title h2 {
    font-size: var(--font-size-xl);
  }

  .empty-title {
    font-size: var(--font-size-lg);
  }
}
</style>