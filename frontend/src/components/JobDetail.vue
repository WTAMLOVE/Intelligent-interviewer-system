<template>
  <el-dialog 
    :model-value="visible" 
    title="岗位详情" 
    width="600px"
    class="job-detail-dialog"
    @update:model-value="$emit('update:visible', $event)"
  >
    <div v-if="jobData" class="job-detail-content">
      <div class="detail-header">
        <h3 class="detail-title">{{ jobData.job_title }}</h3>
      </div>
      
      <div class="detail-body">
        <div class="detail-section">
          <label class="detail-label">岗位描述</label>
          <div class="detail-value">
            <p class="description-text">{{ jobData.description || '暂无描述' }}</p>
          </div>
        </div>
        
        <div class="detail-section">
          <label class="detail-label">技能要求</label>
          <div class="detail-value">
            <div class="skills-grid">
              <el-tag 
                v-for="(skill, idx) in (jobData.skills || [])" 
                :key="idx" 
                class="skill-tag-large"
                type="info"
              >
                {{ skill }}
              </el-tag>
              <span v-if="!jobData.skills || jobData.skills.length === 0" class="no-skills">
                暂无技能要求
              </span>
            </div>
          </div>
        </div>

        <div class="detail-section" v-if="jobData.created_at">
          <label class="detail-label">创建时间</label>
          <div class="detail-value">
            <span class="created-time">{{ formatDate(jobData.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="$emit('update:visible', false)">关闭</el-button>
        <el-button type="primary" @click="$emit('edit', jobData)">编辑岗位</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  jobData: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['update:visible', 'edit'])

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.job-detail-dialog {
  border-radius: var(--radius-lg);
}

.job-detail-content {
  padding: var(--spacing-md) 0;
}

.detail-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: var(--spacing-2xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-primary);
}

.detail-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.detail-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.detail-label {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-primary);
}

.description-text {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.6;
  white-space: pre-wrap;
}

.skills-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.skill-tag-large {
  font-size: var(--font-size-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
}

.no-skills {
  color: var(--text-tertiary);
  font-style: italic;
  font-size: var(--font-size-sm);
}

.created-time {
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}

/* Element Plus 样式覆盖 */
:deep(.el-dialog__header) {
  padding: var(--spacing-lg) var(--spacing-xl);
  border-bottom: 1px solid var(--border-primary);
}

:deep(.el-dialog__body) {
  padding: var(--spacing-xl);
}

:deep(.el-dialog__footer) {
  padding: var(--spacing-lg) var(--spacing-xl);
  border-top: 1px solid var(--border-primary);
}
</style>