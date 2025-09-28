<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑题目' : '添加题目'"
    width="800px"
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
      <el-form-item label="题目类型" prop="question_type">
        <el-select
          v-model="form.question_type"
          placeholder="请选择题目类型"
          style="width: 100%"
          @change="handleTypeChange"
        >
          <el-option
            v-for="(label, value) in QUESTION_TYPE_LABELS"
            :key="value"
            :label="label"
            :value="value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="题目内容" prop="question_text">
        <el-input
          v-model="form.question_text"
          type="textarea"
          placeholder="请输入题目内容"
          :rows="4"
          maxlength="2000"
          show-word-limit
        />
      </el-form-item>

      <!-- 选择题选项 -->
      <el-form-item 
        v-if="isChoiceQuestion" 
        label="选项" 
        prop="options"
      >
        <div class="options-container">
          <div
            v-for="(option, index) in form.options"
            :key="index"
            class="option-item"
          >
            <el-input
              v-model="form.options[index]"
              :placeholder="`选项 ${String.fromCharCode(65 + index)}`"
              style="flex: 1"
            />
            <el-button
              v-if="form.options.length > 2"
              type="danger"
              size="small"
              @click="removeOption(index)"
            >
              删除
            </el-button>
          </div>
          <el-button
            v-if="form.options.length < 8"
            type="primary"
            size="small"
            @click="addOption"
          >
            添加选项
          </el-button>
        </div>
      </el-form-item>

      <el-form-item label="参考答案" prop="reference_answer">
        <el-input
          v-if="!isChoiceQuestion"
          v-model="form.reference_answer"
          type="textarea"
          placeholder="请输入参考答案"
          :rows="3"
          maxlength="1000"
          show-word-limit
        />
        <el-checkbox-group
          v-else-if="form.question_type === 'multiple_choice'"
          v-model="form.correct_options"
        >
          <el-checkbox
            v-for="(option, index) in form.options"
            :key="index"
            :label="index"
          >
            {{ String.fromCharCode(65 + index) }}. {{ option }}
          </el-checkbox>
        </el-checkbox-group>
        <el-radio-group
          v-else
          v-model="form.correct_option"
        >
          <el-radio
            v-for="(option, index) in form.options"
            :key="index"
            :label="index"
          >
            {{ String.fromCharCode(65 + index) }}. {{ option }}
          </el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="分值" prop="score">
        <el-input-number
          v-model="form.score"
          :min="1"
          :max="100"
          :step="1"
          controls-position="right"
          style="width: 200px"
        />
        <span class="input-suffix">分</span>
      </el-form-item>

      <el-form-item label="题目顺序" prop="order_index">
        <el-input-number
          v-model="form.order_index"
          :min="1"
          :max="100"
          :step="1"
          controls-position="right"
          style="width: 200px"
        />
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
          {{ isEdit ? '更新' : '添加' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { interviewApi, QUESTION_TYPE_LABELS } from '../api/interviews'

// Props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  question: {
    type: Object,
    default: null
  },
  interviewId: {
    type: Number,
    required: true
  }
})

// Emits
const emit = defineEmits(['update:visible', 'success'])

// 响应式数据
const formRef = ref()
const submitting = ref(false)

// 表单数据
const form = reactive({
  question_type: 'text',
  question_text: '',
  options: ['', ''],
  reference_answer: '',
  correct_option: null,
  correct_options: [],
  score: 10,
  order_index: 1
})

// 表单验证规则
const rules = {
  question_type: [
    { required: true, message: '请选择题目类型', trigger: 'change' }
  ],
  question_text: [
    { required: true, message: '请输入题目内容', trigger: 'blur' },
    { min: 5, max: 2000, message: '题目内容长度应在 5 到 2000 个字符', trigger: 'blur' }
  ],
  options: [
    {
      validator: (rule, value, callback) => {
        if (isChoiceQuestion.value) {
          const validOptions = value.filter(opt => opt.trim())
          if (validOptions.length < 2) {
            callback(new Error('至少需要2个选项'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  reference_answer: [
    { required: true, message: '请输入参考答案', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (form.question_type === 'single_choice' && form.correct_option === null) {
          callback(new Error('请选择正确答案'))
        } else if (form.question_type === 'multiple_choice' && form.correct_options.length === 0) {
          callback(new Error('请选择正确答案'))
        } else if (!isChoiceQuestion.value && !value.trim()) {
          callback(new Error('请输入参考答案'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  score: [
    { required: true, message: '请输入分值', trigger: 'blur' },
    { type: 'number', min: 1, max: 100, message: '分值应在 1 到 100 分之间', trigger: 'blur' }
  ],
  order_index: [
    { required: true, message: '请输入题目顺序', trigger: 'blur' },
    { type: 'number', min: 1, max: 100, message: '顺序应在 1 到 100 之间', trigger: 'blur' }
  ]
}

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEdit = computed(() => !!props.question)

const isChoiceQuestion = computed(() => {
  return ['single_choice', 'multiple_choice'].includes(form.question_type)
})

// 监听题目数据变化
watch(() => props.question, (newQuestion) => {
  if (newQuestion) {
    // 编辑模式，填充表单数据
    Object.assign(form, {
      question_type: newQuestion.question_type || 'text',
      question_text: newQuestion.question_text || '',
      options: newQuestion.options || ['', ''],
      reference_answer: newQuestion.reference_answer || '',
      correct_option: newQuestion.correct_option != null ? newQuestion.correct_option : null,
      correct_options: newQuestion.correct_options || [],
      score: newQuestion.score || 10,
      order_index: newQuestion.order_index || 1
    })
  } else {
    // 创建模式，重置表单
    resetForm()
  }
}, { immediate: true })

// 题目类型变化处理
function handleTypeChange() {
  if (isChoiceQuestion.value && form.options.length < 2) {
    form.options = ['', '']
  }
  form.correct_option = null
  form.correct_options = []
  form.reference_answer = ''
}

// 添加选项
function addOption() {
  if (form.options.length < 8) {
    form.options.push('')
  }
}

// 删除选项
function removeOption(index) {
  if (form.options.length > 2) {
    form.options.splice(index, 1)
    
    // 调整正确答案
    if (form.question_type === 'single_choice' && form.correct_option === index) {
      form.correct_option = null
    } else if (form.question_type === 'single_choice' && form.correct_option > index) {
      form.correct_option--
    }
    
    if (form.question_type === 'multiple_choice') {
      form.correct_options = form.correct_options
        .filter(opt => opt !== index)
        .map(opt => opt > index ? opt - 1 : opt)
    }
  }
}

// 重置表单
function resetForm() {
  Object.assign(form, {
    question_type: 'text',
    question_text: '',
    options: ['', ''],
    reference_answer: '',
    correct_option: null,
    correct_options: [],
    score: 10,
    order_index: 1
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

  // 构建提交数据
  const submitData = {
    question_type: form.question_type,
    question_text: form.question_text,
    score: form.score,
    order_index: form.order_index
  }

  // 根据题目类型处理答案
  if (isChoiceQuestion.value) {
    submitData.options = form.options.filter(opt => opt.trim())
    
    if (form.question_type === 'single_choice') {
      submitData.correct_option = form.correct_option
      submitData.reference_answer = submitData.options[form.correct_option] || ''
    } else {
      submitData.correct_options = form.correct_options
      submitData.reference_answer = form.correct_options
        .map(idx => submitData.options[idx])
        .join(', ')
    }
  } else {
    submitData.reference_answer = form.reference_answer
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      // 更新题目
      await interviewApi.updateQuestion(props.question.id, submitData)
      ElMessage.success('题目更新成功')
    } else {
      // 添加题目
      await interviewApi.addQuestion(props.interviewId, submitData)
      ElMessage.success('题目添加成功')
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
</script>

<style scoped>
.options-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.option-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
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

:deep(.el-checkbox-group) {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}
</style>