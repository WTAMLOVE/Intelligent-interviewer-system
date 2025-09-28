<template>
  <el-dialog 
    :model-value="visible" 
    :title="isEdit ? '编辑岗位' : '新增岗位'" 
    width="600px"
    :before-close="handleClose"
    class="job-form-dialog"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form 
      :model="formData" 
      :rules="formRules"
      ref="formRef"
      label-width="100px" 
      class="job-form"
    >
      <el-form-item label="岗位名称" prop="job_title">
        <el-input 
          v-model="formData.job_title" 
          placeholder="请输入岗位名称"
          size="large"
        />
      </el-form-item>
      
      <el-form-item label="岗位描述" prop="description">
        <el-input 
          v-model="formData.description" 
          type="textarea" 
          :rows="4"
          placeholder="请详细描述岗位职责和要求"
          size="large"
        />
      </el-form-item>
      
      <el-form-item label="技能要求">
        <el-input 
          v-model="skillsInput" 
          placeholder="请输入技能要求，多个技能用逗号分隔，例如：Python, Flask, SQL"
          size="large"
          @input="updateSkillsPreview"
        />
        <div class="skills-preview" v-if="skillsPreview.length > 0">
          <span class="preview-label">技能预览：</span>
          <el-tag 
            v-for="(skill, idx) in skillsPreview" 
            :key="idx" 
            class="skill-preview-tag"
            size="small"
            closable
            @close="removeSkill(idx)"
          >
            {{ skill }}
          </el-tag>
        </div>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel" size="large">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleSubmit" 
          :loading="loading"
          size="large"
        >
          {{ loading ? (isEdit ? '更新中...' : '保存中...') : (isEdit ? '更新' : '保存') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  jobData: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'submit', 'cancel'])

const formRef = ref()
const skillsInput = ref('')
const skillsPreview = ref([])

const formData = ref({
  job_title: '',
  description: '',
  skills: []
})

const formRules = {
  job_title: [
    { required: true, message: '请输入岗位名称', trigger: 'blur' },
    { min: 2, max: 50, message: '岗位名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { max: 500, message: '描述不能超过 500 个字符', trigger: 'blur' }
  ]
}

// 监听外部传入的数据变化
watch(() => props.jobData, (newData) => {
  if (newData && Object.keys(newData).length > 0) {
    formData.value = { ...newData }
    skillsInput.value = (newData.skills || []).join(', ')
    updateSkillsPreview()
  }
}, { immediate: true, deep: true })

// 监听弹窗显示状态
watch(() => props.visible, (visible) => {
  if (visible && !props.isEdit) {
    resetForm()
  }
})

function resetForm() {
  formData.value = {
    job_title: '',
    description: '',
    skills: []
  }
  skillsInput.value = ''
  skillsPreview.value = []
  formRef.value?.resetFields()
}

function updateSkillsPreview() {
  const skills = skillsInput.value
    .split(',')
    .map(s => s.trim())
    .filter(Boolean)
  skillsPreview.value = skills
  formData.value.skills = skills
}

function removeSkill(index) {
  skillsPreview.value.splice(index, 1)
  skillsInput.value = skillsPreview.value.join(', ')
  formData.value.skills = skillsPreview.value
}

async function handleSubmit() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    updateSkillsPreview()
    emit('submit', formData.value)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

function handleCancel() {
  emit('cancel')
  resetForm()
}

function handleClose() {
  handleCancel()
}
</script>

<style scoped>
.job-form-dialog {
  border-radius: var(--radius-lg);
}

.job-form {
  padding: var(--spacing-md) 0;
}

.skills-preview {
  margin-top: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
}

.preview-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-right: var(--spacing-sm);
}

.skill-preview-tag {
  margin: var(--spacing-xs) var(--spacing-xs) var(--spacing-xs) 0;
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

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-primary);
}

:deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
}

:deep(.el-textarea__inner) {
  border-radius: var(--radius-md);
}
</style>