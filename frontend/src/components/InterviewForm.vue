<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑面试' : '创建面试'"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="right"
    >
      <el-form-item label="面试标题" prop="title">
        <el-input
          v-model="form.title"
          placeholder="请输入面试标题"
          maxlength="255"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="面试描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          placeholder="请输入面试描述"
          :rows="4"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="关联岗位" prop="job_requirement_id">
        <el-select
          v-model="form.job_requirement_id"
          placeholder="请选择关联岗位"
          filterable
          style="width: 100%"
          :loading="jobsLoading"
        >
          <el-option
            v-for="job in jobList"
            :key="job.id"
            :label="job.job_title"
            :value="job.id"
          >
            <div class="job-option">
              <div class="job-title">{{ job.job_title }}</div>
              <div class="job-description">{{ job.description || '暂无描述' }}</div>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="面试者" prop="interviewee_id">
        <el-select
          v-model="form.interviewee_id"
          placeholder="请选择面试者（可留空后续分配）"
          filterable
          clearable
          style="width: 100%"
          :loading="usersLoading"
        >
          <el-option
            v-for="user in intervieweeList"
            :key="user.id"
            :label="user.username"
            :value="user.id"
          >
            <div class="user-option">
              <div class="user-name">{{ user.username }}</div>
              <div class="user-email">{{ user.email }}</div>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="面试题数量" prop="question_count">
        <el-input-number
          v-model="form.question_count"
          :min="1"
          :max="50"
          :step="1"
          controls-position="right"
          style="width: 200px"
        />
        <span class="input-suffix">题</span>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          type="primary"
          @click="handleSubmit"
          :loading="submitting"
        >
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { interviewApi } from '../api/interviews'
import { listJobs } from '../api/jobs'
import { userAPI } from '../api/users'

// Props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  interview: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:visible', 'success'])

// 响应式数据
const formRef = ref()
const submitting = ref(false)
const jobsLoading = ref(false)
const usersLoading = ref(false)
const jobList = ref([])
const intervieweeList = ref([])

// 表单数据
const form = reactive({
  title: '',
  description: '',
  job_requirement_id: null,
  interviewee_id: null,
  question_count: 5
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入面试标题', trigger: 'blur' },
    { min: 2, max: 255, message: '标题长度应在 2 到 255 个字符', trigger: 'blur' }
  ],
  description: [
    { max: 1000, message: '描述长度不能超过 1000 个字符', trigger: 'blur' }
  ],
  job_requirement_id: [
    { required: true, message: '请选择关联岗位', trigger: 'change' }
  ],
  question_count: [
    { required: true, message: '请输入面试题数量', trigger: 'blur' },
    { type: 'number', min: 1, max: 50, message: '题数应在 1 到 50 题之间', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEdit = computed(() => !!props.interview)

// 监听面试数据变化
watch(() => props.interview, (newInterview) => {
  if (newInterview) {
    // 编辑模式，填充表单数据
    Object.assign(form, {
      title: newInterview.title || '',
      description: newInterview.description || '',
      job_requirement_id: newInterview.job_requirement_id || null,
      interviewee_id: newInterview.interviewee_id || null,
      question_count: newInterview.question_count || 5
    })
  } else {
    // 创建模式，重置表单
    resetForm()
  }
}, { immediate: true })

// 加载岗位列表
async function loadJobs() {
  jobsLoading.value = true
  try {
    const response = await listJobs()
    // 后端直接返回JobRequirement对象列表
    jobList.value = response || []
  } catch (error) {
    console.error('加载岗位列表失败:', error)
    ElMessage.error('加载岗位列表失败')
  } finally {
    jobsLoading.value = false
  }
}

// 加载面试者列表
async function loadInterviewees() {
  usersLoading.value = true
  try {
    const response = await userAPI.getInterviewees()
    intervieweeList.value = response.data.users || []
  } catch (error) {
    console.error('加载面试者列表失败:', error)
    ElMessage.error('加载面试者列表失败')
  } finally {
    usersLoading.value = false
  }
}

// 重置表单
function resetForm() {
  Object.assign(form, {
    title: '',
    description: '',
    job_requirement_id: null,
    interviewee_id: null,
    question_count: 5
  })
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

// 处理提交
async function handleSubmit() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (error) {
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      // 更新面试
      await interviewApi.updateInterview(props.interview.id, form)
      ElMessage.success('面试更新成功')
    } else {
      // 创建面试
      await interviewApi.createInterview(form)
      ElMessage.success('面试创建成功')
    }
    
    emit('success')
  } catch (error) {
    console.error('操作失败:', error)
    const message = error.response?.data?.message || '操作失败'
    ElMessage.error(message)
  } finally {
    submitting.value = false
  }
}

// 处理关闭
function handleClose() {
  resetForm()
  dialogVisible.value = false
}

// 生命周期
onMounted(() => {
  loadJobs()
  loadInterviewees()
})
</script>

<style scoped>
.job-option, .user-option {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.job-title, .user-name {
  font-weight: 500;
  color: var(--text-primary);
}

.job-description, .user-email {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.input-suffix {
  margin-left: var(--spacing-sm);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input-number) {
  width: 100%;
}

:deep(.el-textarea__inner) {
  resize: vertical;
}
</style>