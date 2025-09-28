<template>
  <el-dialog
    v-model="dialogVisible"
    :title="interview?.title || '面试详情'"
    width="90%"
    top="5vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div class="interview-detail" v-loading="loading">
      <el-tabs v-model="activeTab" type="border-card" class="detail-tabs">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <div class="basic-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="面试标题">
                {{ interview?.title }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getStatusType(interview?.status)" size="small">
                  {{ INTERVIEW_STATUS_LABELS[interview?.status] }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="关联岗位">
                {{ interview?.job_requirement?.job_title || '未设置' }}
              </el-descriptions-item>
              <el-descriptions-item label="题目数量">
                {{ interview?.question_count }}题
              </el-descriptions-item>
              <el-descriptions-item label="面试者">
                <span v-if="interview?.interviewee">
                  {{ interview.interviewee.username }} ({{ interview.interviewee.email }})
                </span>
                <el-tag v-else type="info" size="small">未分配</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="面试官">
                {{ interview?.interviewer?.username || '未知' }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                {{ formatDateTime(interview?.created_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="开始时间">
                {{ formatDateTime(interview?.started_at) || '未开始' }}
              </el-descriptions-item>
              <el-descriptions-item label="完成时间">
                {{ formatDateTime(interview?.completed_at) || '未完成' }}
              </el-descriptions-item>
              <el-descriptions-item label="描述" :span="2">
                {{ interview?.description || '无描述' }}
              </el-descriptions-item>
            </el-descriptions>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button
                v-if="interview?.status === 'draft' && !interview?.interviewee_id"
                type="primary"
                @click="showAssignDialog"
              >
                分配面试者
              </el-button>
              <el-button
                v-if="interview?.status === 'completed'"
                type="success"
                @click="activeTab = 'evaluation'"
              >
                评价面试
              </el-button>
            </div>
          </div>
        </el-tab-pane>

        <!-- 题目管理 -->
        <el-tab-pane label="题目管理" name="questions">
          <div class="questions-section">
            <div class="questions-header">
              <h4>面试题目</h4>
              <el-button
                v-if="interview?.status === 'draft'"
                type="primary"
                @click="showQuestionDialog"
              >
                <template #icon>
                  <el-icon><Plus /></el-icon>
                </template>
                添加题目
              </el-button>
            </div>

            <div class="questions-list">
              <el-card
                v-for="(question, index) in questions"
                :key="question.id"
                class="question-card"
                shadow="hover"
              >
                <div class="question-header">
                  <div class="question-info">
                    <span class="question-number">第{{ index + 1 }}题</span>
                    <el-tag :type="getQuestionTypeColor(question.question_type)" size="small">
                      {{ QUESTION_TYPE_LABELS[question.question_type] }}
                    </el-tag>
                    <span class="question-score">{{ question.score }}分</span>
                  </div>
                  <div class="question-actions" v-if="interview?.status === 'draft'">
                    <el-button
                      type="primary"
                      size="small"
                      @click="editQuestion(question)"
                    >
                      编辑
                    </el-button>
                    <el-popconfirm
                      title="确定删除这道题目吗？"
                      @confirm="deleteQuestion(question.id)"
                    >
                      <template #reference>
                        <el-button type="danger" size="small">删除</el-button>
                      </template>
                    </el-popconfirm>
                  </div>
                </div>

                <div class="question-content">
                  <div class="question-text">{{ question.question_text }}</div>
                  
                  <!-- 选择题选项 -->
                  <div v-if="question.options && question.options.length" class="question-options">
                    <div v-for="(option, idx) in question.options" :key="idx" class="option-item">
                      {{ String.fromCharCode(65 + idx) }}. {{ option }}
                    </div>
                  </div>

                  <!-- 参考答案 -->
                  <div v-if="question.reference_answer" class="reference-answer">
                    <strong>参考答案：</strong>{{ question.reference_answer }}
                  </div>

                  <!-- 面试者答案 -->
                  <div v-if="question.candidate_answer" class="candidate-answer">
                    <strong>面试者答案：</strong>{{ question.candidate_answer }}
                  </div>

                  <!-- 评分 -->
                  <div v-if="question.actual_score !== null" class="question-score-section">
                    <el-rate
                      :model-value="question.actual_score"
                      :max="question.score"
                      disabled
                      show-score
                      text-color="#ff9900"
                    />
                    <div v-if="question.comments" class="score-comments">
                      <strong>评语：</strong>{{ question.comments }}
                    </div>
                  </div>
                </div>
              </el-card>

              <div v-if="!questions.length" class="empty-questions">
                <el-empty description="暂无题目" />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 面试评价 -->
        <el-tab-pane label="面试评价" name="evaluation">
          <div class="evaluation-section">
            <!-- 已有评价时显示评价内容或编辑表单 -->
            <div v-if="evaluation && !isEditingEvaluation" class="evaluation-content">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="总分">
                  {{ evaluation.total_score }} / {{ evaluation.max_score }}
                  ({{ Math.round(evaluation.total_score / evaluation.max_score * 100) }}%)
                </el-descriptions-item>
                <el-descriptions-item label="面试结果">
                  <el-tag :type="evaluation.is_passed ? 'success' : 'danger'">
                    {{ evaluation.is_passed ? '通过' : '未通过' }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="评价时间">
                  {{ formatDateTime(evaluation.evaluated_at) }}
                </el-descriptions-item>
                <el-descriptions-item label="评价者">
                  {{ evaluation.evaluator?.username }}
                </el-descriptions-item>
                <el-descriptions-item label="总体评价" :span="2">
                  {{ evaluation.overall_comments || '无评价' }}
                </el-descriptions-item>
                <el-descriptions-item label="决定原因" :span="2">
                  {{ evaluation.decision_reason || '无说明' }}
                </el-descriptions-item>
                <el-descriptions-item label="综合建议" :span="2">
                  {{ evaluation.recommendations || '无建议' }}
                </el-descriptions-item>
              </el-descriptions>

              <!-- 技能评分 -->
              <div v-if="evaluation.skill_ratings" class="skill-ratings">
                <h4>技能评分</h4>
                <div class="skills-grid">
                  <div
                    v-for="(rating, skill) in evaluation.skill_ratings"
                    :key="skill"
                    class="skill-item"
                  >
                    <span class="skill-name">{{ skill }}</span>
                    <el-rate :model-value="rating" disabled show-score />
                  </div>
                </div>
              </div>

              <!-- 如果评价未完成，显示编辑按钮 -->
              <div v-if="!evaluation.is_finalized" class="evaluation-actions" style="margin-top: 20px;">
                <el-button type="warning" @click="editEvaluation">
                  编辑评价
                </el-button>
              </div>
            </div>

            <!-- 编辑评价表单 -->
            <div v-else-if="evaluation && isEditingEvaluation" class="evaluation-form">
              <el-form ref="evaluationFormRef" :model="evaluationForm" label-width="120px">
                <el-form-item label="总体评价" required>
                  <el-input
                    v-model="evaluationForm.overall_comments"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入对候选人的总体评价..."
                    maxlength="500"
                    show-word-limit
                  />
                </el-form-item>
                
                <el-form-item label="面试结果" required>
                  <el-radio-group v-model="evaluationForm.is_passed">
                    <el-radio :label="true">通过</el-radio>
                    <el-radio :label="false">未通过</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="决定原因">
                  <el-input
                    v-model="evaluationForm.decision_reason"
                    type="textarea"
                    :rows="3"
                    placeholder="请说明通过或未通过的原因..."
                    maxlength="300"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item label="综合建议">
                  <el-input
                    v-model="evaluationForm.recommendations"
                    type="textarea"
                    :rows="3"
                    placeholder="请提供针对候选人的建议..."
                    maxlength="300"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item label="总分">
                  <el-input-number
                    v-model="evaluationForm.total_score"
                    :min="0"
                    :max="evaluationForm.max_score"
                    style="width: 150px;"
                  />
                  <span style="margin-left: 10px;">/ {{ evaluationForm.max_score }}</span>
                </el-form-item>

                <el-form-item>
                  <el-button @click="cancelEditEvaluation">
                    取消
                  </el-button>
                  <el-button type="success" @click="saveEvaluationEdit" :loading="evaluationLoading">
                    保存评价
                  </el-button>
                  <el-button type="primary" @click="completeEvaluationEdit" :loading="evaluationLoading">
                    完成评价
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 待评价状态：显示评价表单 -->
            <div v-else-if="interview?.status === 'pending_evaluation'" class="evaluation-form">
              <el-form ref="evaluationFormRef" :model="evaluationForm" label-width="120px" :disabled="evaluation?.is_finalized">
                <el-form-item label="总体评价" required>
                  <el-input
                    v-model="evaluationForm.overall_comments"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入对候选人的总体评价..."
                    maxlength="500"
                    show-word-limit
                    :disabled="evaluation?.is_finalized"
                  />
                </el-form-item>
                
                <el-form-item label="面试结果" required>
                  <el-radio-group v-model="evaluationForm.is_passed" :disabled="evaluation?.is_finalized">
                    <el-radio :label="true">通过</el-radio>
                    <el-radio :label="false">未通过</el-radio>
                  </el-radio-group>
                </el-form-item>

                <el-form-item label="决定原因">
                  <el-input
                    v-model="evaluationForm.decision_reason"
                    type="textarea"
                    :rows="3"
                    placeholder="请说明通过或未通过的原因..."
                    maxlength="300"
                    show-word-limit
                    :disabled="evaluation?.is_finalized"
                  />
                </el-form-item>

                <el-form-item label="综合建议">
                  <el-input
                    v-model="evaluationForm.recommendations"
                    type="textarea"
                    :rows="3"
                    placeholder="请提供针对候选人的建议..."
                    maxlength="300"
                    show-word-limit
                    :disabled="evaluation?.is_finalized"
                  />
                </el-form-item>

                <el-form-item label="总分">
                  <el-input-number
                    v-model="evaluationForm.total_score"
                    :min="0"
                    :max="evaluationForm.max_score"
                    style="width: 150px;"
                    :disabled="evaluation?.is_finalized"
                  />
                  <span style="margin-left: 10px;">/ {{ evaluationForm.max_score }}</span>
                </el-form-item>

                <el-form-item v-if="!evaluation?.is_finalized">
                  <el-button type="success" @click="saveEvaluation" :loading="evaluationLoading">
                    保存评价
                  </el-button>
                  <el-button type="primary" @click="completeEvaluation" :loading="evaluationLoading">
                    完成评价
                  </el-button>
                </el-form-item>

                <el-alert v-if="evaluation?.is_finalized" 
                  title="评价已完成，不可再次修改" 
                  type="info" 
                  :closable="false" 
                  style="margin-top: 10px;"
                />
              </el-form>
            </div>

            <!-- 其他状态：显示相应提示信息 -->
            <div v-else class="evaluation-unavailable">
              <el-alert
                v-if="interview?.status === 'draft'"
                title="面试尚未开始"
                type="info"
                :closable="false"
              />
              <el-alert
                v-else-if="interview?.status === 'assigned'"
                title="面试尚未开始"
                type="info"
                :closable="false"
              />
              <el-alert
                v-else-if="interview?.status === 'in_progress'"
                title="面试者正在进行面试，请等待完成"
                type="warning"
                :closable="false"
              />
              <el-alert
                v-else
                title="面试者还未完成面试"
                type="info"
                :closable="false"
              />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 分配面试者对话框 -->
    <el-dialog
      v-model="assignDialogVisible"
      title="分配面试者"
      width="400px"
      append-to-body
    >
      <el-form>
        <el-form-item label="选择面试者">
          <el-select
            v-model="selectedInterviewee"
            placeholder="请选择面试者"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="user in intervieweeList"
              :key="user.id"
              :label="user.username"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="assignDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAssign" :loading="assigning">
          分配
        </el-button>
      </template>
    </el-dialog>

    <!-- 题目编辑对话框 -->
    <QuestionForm
      v-model:visible="questionDialogVisible"
      :question="currentQuestion"
      :interview-id="props.interviewId"
      @success="handleQuestionSuccess"
    />
    
    <!-- 评价编辑对话框 -->
    <!-- TODO: 创建 EvaluationForm 组件 -->
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { 
  interviewApi, 
  INTERVIEW_STATUS_LABELS,
  QUESTION_TYPE_LABELS 
} from '../api/interviews'
import QuestionForm from './QuestionForm.vue'

// Props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  interviewId: {
    type: Number,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:visible', 'refresh'])

// 响应式数据
const loading = ref(false)
const interview = ref(null)
const questions = ref([])
const evaluation = ref(null)
const activeTab = ref('basic')

// 对话框状态
const assignDialogVisible = ref(false)
const questionDialogVisible = ref(false)
const evaluationDialogVisible = ref(false)
const currentQuestion = ref(null)

// 分配相关
const assigning = ref(false)
const selectedInterviewee = ref(null)
const intervieweeList = ref([])

// 评价相关
const evaluationLoading = ref(false)
const evaluationFormRef = ref(null)
const isEditingEvaluation = ref(false)
const evaluationForm = ref({
  overall_comments: '',
  is_passed: null,
  decision_reason: '',
  recommendations: '',
  total_score: 0,
  max_score: 100
})

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

// 监听面试ID变化
watch(() => props.interviewId, (newId) => {
  if (newId && props.visible) {
    loadInterviewDetail()
  }
}, { immediate: true })

// 监听弹窗可见性变化
watch(() => props.visible, (visible) => {
  if (visible && props.interviewId) {
    loadInterviewDetail()
  }
})

// 监听标签页切换
watch(activeTab, (newTab) => {
  if (newTab === 'evaluation' && props.interviewId && props.visible) {
    loadEvaluation()
  }
})

// 加载面试详情
async function loadInterviewDetail() {
  if (!props.interviewId) return

  loading.value = true
  try {
    // 加载面试基本信息
    const response = await interviewApi.getInterview(props.interviewId)
    console.log('面试详情API响应:', response) // 调试日志
    
    // 处理不同的响应格式
    if (response.data) {
      interview.value = response.data.data || response.data
    } else {
      interview.value = response
    }

    if (!interview.value) {
      throw new Error('未获取到面试数据')
    }

    // 加载题目列表
    await loadQuestions()

    // 加载评价信息（如果面试已完成或待评价）
    if (['pending_evaluation', 'completed'].includes(interview.value.status)) {
      await loadEvaluation()
    }
  } catch (error) {
    console.error('加载面试详情失败:', error)
    const message = error.response?.data?.message || '加载面试详情失败'
    ElMessage.error(message)
    
    // 404错误时关闭对话框
    if (error.response?.status === 404) {
      handleClose()
    }
  } finally {
    loading.value = false
  }
}

// 加载题目列表
async function loadQuestions() {
  if (!props.interviewId) return
  
  try {
    const response = await interviewApi.getInterviewQuestions(props.interviewId)
    console.log('题目列表API响应:', response) // 调试日志
    
    // 处理不同的响应格式
    if (response.data) {
      questions.value = response.data.data || response.data || []
    } else {
      questions.value = response || []
    }
  } catch (error) {
    console.error('加载题目列表失败:', error)
    questions.value = []
    // 如果不是权限问题，显示错误信息
    if (error.response?.status !== 403) {
      ElMessage.error('加载题目列表失败')
    }
  }
}

// 加载评价信息
async function loadEvaluation() {
  if (!props.interviewId) {
    console.log('没有面试ID，跳过加载评价')
    return
  }
  
  try {
    console.log('开始加载评价信息，面试ID:', props.interviewId)
    const response = await interviewApi.getEvaluation(props.interviewId)
    console.log('评价API响应:', response)
    
    if (response.data) {
      evaluation.value = response.data.data || response.data
      console.log('设置评价数据:', evaluation.value)
    }
  } catch (error) {
    console.error('加载评价信息失败:', error)
    if (error.response?.status === 404) {
      console.log('评价不存在，这是正常的')
      evaluation.value = null
    }
  }
}

// 显示分配对话框
function showAssignDialog() {
  // TODO: 加载面试者列表
  assignDialogVisible.value = true
}

// 处理分配
async function handleAssign() {
  if (!selectedInterviewee.value) {
    ElMessage.warning('请选择面试者')
    return
  }

  assigning.value = true
  try {
    await interviewApi.assignInterview(props.interviewId, selectedInterviewee.value)
    ElMessage.success('分配成功')
    assignDialogVisible.value = false
    await loadInterviewDetail()
    emit('refresh')
  } catch (error) {
    console.error('分配失败:', error)
    ElMessage.error('分配失败')
  } finally {
    assigning.value = false
  }
}

// 显示题目对话框
function showQuestionDialog() {
  currentQuestion.value = null
  questionDialogVisible.value = true
}

// 编辑题目
function editQuestion(question) {
  currentQuestion.value = { ...question }
  questionDialogVisible.value = true
}

// 删除题目
async function deleteQuestion(questionId) {
  try {
    await interviewApi.deleteQuestion(questionId)
    ElMessage.success('删除成功')
    await loadQuestions()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

// 题目操作成功回调
function handleQuestionSuccess() {
  questionDialogVisible.value = false
  loadQuestions()
}

// 编辑评价
function editEvaluation() {
  if (evaluation.value) {
    evaluationForm.value = {
      overall_comments: evaluation.value.overall_comments || '',
      is_passed: evaluation.value.is_passed,
      decision_reason: evaluation.value.decision_reason || '',
      recommendations: evaluation.value.recommendations || '',
      total_score: evaluation.value.total_score || 0,
      max_score: evaluation.value.max_score || 100
    };
    
    isEditingEvaluation.value = true;
  }
}

// 取消编辑评价
function cancelEditEvaluation() {
  isEditingEvaluation.value = false;
  // 重置表单
  evaluationForm.value = {
    overall_comments: '',
    is_passed: null,
    decision_reason: '',
    recommendations: '',
    total_score: 0,
    max_score: 100
  };
}

// 保存评价编辑（不完成）
async function saveEvaluationEdit() {
  if (!interview.value) return;
  
  try {
    evaluationLoading.value = true;
    
    const evaluationData = {
      ...evaluationForm.value,
      is_finalized: false  // 保存但不完成
    };
    
    if (evaluation.value && evaluation.value.id) {
      // 更新现有评价
      await interviewApi.updateEvaluation(evaluation.value.id, evaluationData);
    } else {
      // 创建新评价
      await interviewApi.createEvaluation(interview.value.id, evaluationData);
    }
    
    ElMessage.success('评价保存成功');
    isEditingEvaluation.value = false;
    await loadEvaluation();
  } catch (error) {
    console.error('保存评价失败:', error);
    ElMessage.error(error.response?.data?.message || '保存评价失败');
  } finally {
    evaluationLoading.value = false;
  }
}

// 完成评价编辑
async function completeEvaluationEdit() {
  if (!interview.value) return;
  
  // 验证必填字段
  if (!evaluationForm.value.overall_comments || evaluationForm.value.is_passed === null) {
    ElMessage.warning('请填写总体评价和面试结果');
    return;
  }
  
  try {
    evaluationLoading.value = true;
    
    const evaluationData = {
      ...evaluationForm.value,
      is_finalized: true,  // 完成评价
      complete_evaluation: true  // 同时完成面试，更新面试状态
    };
    
    if (evaluation.value && evaluation.value.id) {
      // 更新现有评价并完成
      await interviewApi.updateEvaluation(evaluation.value.id, evaluationData);
    } else {
      // 创建新评价并完成
      await interviewApi.createEvaluation(interview.value.id, evaluationData);
    }
    
    ElMessage.success('评价完成并提交成功');
    isEditingEvaluation.value = false;
    await loadEvaluation();
    await loadInterviewDetail(); // 重新加载面试状态
  } catch (error) {
    console.error('完成评价失败:', error);
    ElMessage.error(error.response?.data?.message || '完成评价失败');
  } finally {
    evaluationLoading.value = false;
  }
}

// 保存评价（不完成）
async function saveEvaluation() {
  try {
    evaluationLoading.value = true
    
    const evaluationData = {
      ...evaluationForm.value,
      complete_evaluation: false
    }

    if (evaluation.value) {
      // 更新现有评价
      await interviewApi.updateEvaluation(evaluation.value.id, evaluationData)
      ElMessage.success('评价已保存')
    } else {
      // 创建新评价
      await interviewApi.createEvaluation(props.interviewId, evaluationData)
      ElMessage.success('评价已保存')
    }

    await loadEvaluation()
  } catch (error) {
    console.error('保存评价失败:', error)
    const message = error.response?.data?.message || '保存评价失败'
    ElMessage.error(message)
  } finally {
    evaluationLoading.value = false
  }
}

// 完成评价
async function completeEvaluation() {
  // 验证必填字段
  if (!evaluationForm.value.overall_comments?.trim()) {
    ElMessage.error('请填写总体评价')
    return
  }
  
  if (evaluationForm.value.is_passed === null) {
    ElMessage.error('请选择面试结果')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确定要完成评价吗？完成后将无法修改评价内容。',
      '完成评价确认',
      {
        confirmButtonText: '确定完成',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    evaluationLoading.value = true
    
    const evaluationData = {
      ...evaluationForm.value,
      complete_evaluation: true
    }

    if (evaluation.value) {
      // 更新现有评价并完成
      await interviewApi.updateEvaluation(evaluation.value.id, evaluationData)
    } else {
      // 创建新评价并完成
      await interviewApi.createEvaluation(props.interviewId, evaluationData)
    }

    ElMessage.success('评价已完成')
    await loadEvaluation()
    await loadInterviewDetail() // 刷新面试状态
    emit('refresh') // 通知父组件刷新

  } catch (error) {
    if (error !== 'cancel') {
      console.error('完成评价失败:', error)
      const message = error.response?.data?.message || '完成评价失败'
      ElMessage.error(message)
    }
  } finally {
    evaluationLoading.value = false
  }
}

// 显示评价对话框（保留兼容性）
function showEvaluationDialog() {
  ElMessage.info('请在评价选项卡中进行评价')
}

// 评价操作成功回调（保留兼容性）
function handleEvaluationSuccess() {
  loadEvaluation()
  emit('refresh')
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

// 获取题目类型颜色
function getQuestionTypeColor(type) {
  const colorMap = {
    'single_choice': 'primary',
    'multiple_choice': 'success',
    'text': 'warning',
    'code': 'danger'
  }
  return colorMap[type] || ''
}

// 格式化日期时间
function formatDateTime(dateStr) {
  if (!dateStr) return null
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 处理关闭
function handleClose() {
  // 只重置活动标签页，保留数据以便下次快速显示
  activeTab.value = 'basic'
  dialogVisible.value = false
}
</script>

<style scoped>
.interview-detail {
  min-height: 600px;
}

.detail-tabs {
  height: 100%;
}

.basic-info {
  padding: var(--spacing-md);
}

.action-buttons {
  margin-top: var(--spacing-lg);
  text-align: center;
}

.questions-section {
  padding: var(--spacing-md);
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.questions-header h4 {
  margin: 0;
  color: var(--text-primary);
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.question-card {
  border: 1px solid var(--border-light);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.question-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.question-number {
  font-weight: 600;
  color: var(--primary-600);
}

.question-score {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.question-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.question-content {
  line-height: 1.6;
}

.question-text {
  font-size: var(--font-size-base);
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.question-options {
  margin: var(--spacing-md) 0;
  padding-left: var(--spacing-md);
}

.option-item {
  margin-bottom: var(--spacing-xs);
  color: var(--text-secondary);
}

.reference-answer,
.candidate-answer {
  margin: var(--spacing-md) 0;
  padding: var(--spacing-sm);
  background: var(--bg-light);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
}

.question-score-section {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-light);
}

.score-comments {
  margin-top: var(--spacing-sm);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.empty-questions {
  text-align: center;
  padding: var(--spacing-xl);
}

.evaluation-section {
  padding: var(--spacing-md);
}

.skill-ratings {
  margin-top: var(--spacing-lg);
}

.skill-ratings h4 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.skill-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm);
  background: var(--bg-light);
  border-radius: var(--radius-sm);
}

.skill-name {
  font-weight: 500;
  color: var(--text-primary);
}

.no-evaluation,
.evaluation-unavailable {
  text-align: center;
  padding: var(--spacing-xl);
}
</style>