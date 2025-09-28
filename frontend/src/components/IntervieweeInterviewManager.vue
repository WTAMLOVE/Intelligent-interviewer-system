<template>
  <div class="interview-manager">
    <div class="interview-header">
      <div class="header-content">
        <div class="header-title">
          <h2>面试清单</h2>
          <p>查看分配给您的面试，完成面试题目</p>
        </div>
        <div class="header-actions">
          <el-select v-model="statusFilter" placeholder="筛选状态" size="large" style="width: 150px;">
            <el-option label="全部" value="" />
            <el-option label="已分配" value="assigned" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
          <el-button size="large" @click="loadInterviews" :loading="listLoading">
            刷新
          </el-button>
        </div>
      </div>
    </div>

    <div class="interview-content card">
      <div class="interview-grid">
        <!-- 面试列表 -->
        <div class="interview-list-section">
          <div class="section-header">
            <h3>我的面试</h3>
          </div>
          <div class="section-body">
            <el-loading v-loading="listLoading">
              <div v-if="interviews.length === 0" class="empty-state">
                <el-empty description="暂无面试安排" />
              </div>
              <div v-else class="interview-list">
                <div 
                  v-for="interview in interviews" 
                  :key="interview.id"
                  class="interview-item"
                  :class="{ active: selectedInterview?.id === interview.id }"
                  @click="selectInterview(interview)"
                >
                  <div class="interview-info">
                    <div class="interview-title">{{ interview.title }}</div>
                    <div class="interview-meta">
                      <el-tag :type="getStatusType(interview.status)" size="small">
                        {{ getStatusLabel(interview.status) }}
                      </el-tag>
                      <span class="interview-job">{{ interview.job_requirement?.job_title || '未知岗位' }}</span>
                    </div>
                    <div class="interview-desc" v-if="interview.description">
                      {{ interview.description }}
                    </div>
                  </div>
                  <div class="interview-actions">
                    <el-button 
                      v-if="interview.status === 'assigned'"
                      type="primary" 
                      size="small"
                      @click.stop="startInterview(interview)"
                    >
                      开始面试
                    </el-button>
                    <el-button
                      v-else-if="interview.status === 'in_progress'"
                      type="warning" 
                      size="small"
                      @click.stop="selectInterview(interview)"
                    >
                      继续答题
                    </el-button>
                    <!-- 已完成的面试显示评价结果 -->
                    <el-tag 
                      v-if="interview.status === 'completed' && interview.evaluation"
                      :type="interview.evaluation.is_passed ? 'success' : 'danger'"
                      size="small"
                    >
                      {{ interview.evaluation.is_passed ? '通过' : '未通过' }}
                    </el-tag>
                    <!-- 已完成但暂无评价结果 -->
                    <el-tag 
                      v-else-if="interview.status === 'completed'"
                      type="info" 
                      size="small"
                    >
                      待评价
                    </el-tag>
                    <el-button
                      v-if="interview.status === 'completed'"
                      type="primary"
                      size="small"
                      @click.stop="viewResult(interview)"
                      style="margin-left: 8px;"
                    >
                      查看结果
                    </el-button>
                  </div>
                </div>
              </div>
            </el-loading>
          </div>
        </div>

        <!-- 面试详情和答题区域 -->
        <div class="interview-detail-section" v-if="selectedInterview">
          <div class="section-header">
            <h3>{{ selectedInterview.title }}</h3>
            <div class="header-info">
              <el-tag :type="getStatusType(selectedInterview.status)" size="small">
                {{ getStatusLabel(selectedInterview.status) }}
              </el-tag>
              <span class="duration">题目数量: {{ selectedInterview.question_count }}题</span>
            </div>
          </div>
          <div class="section-body">
            <!-- 岗位要求 -->
            <div class="job-requirements" v-if="selectedInterview.job_requirement">
              <h4>岗位要求</h4>
              <div class="job-info">
                <div class="job-title">{{ selectedInterview.job_requirement.title }}</div>
                <div class="job-desc">{{ selectedInterview.job_requirement.description }}</div>
                <div class="job-skills" v-if="selectedInterview.job_requirement.required_skills">
                  <strong>技能要求：</strong>
                  <el-tag 
                    v-for="skill in selectedInterview.job_requirement.required_skills" 
                    :key="skill"
                    size="small"
                    class="skill-tag"
                  >
                    {{ skill }}
                  </el-tag>
                </div>
              </div>
            </div>

            <!-- 面试题目 -->
            <div class="questions-section" v-if="questions.length > 0">
              <div class="questions-header">
                <h4>面试题目</h4>
                <div class="progress-info">
                  已完成: {{ answeredQuestionsCount }} / {{ questions.length }}
                </div>
              </div>
              
              <div class="questions-list">
                <div 
                  v-for="(question, index) in questions" 
                  :key="question.id"
                  class="question-item"
                >
                  <div class="question-header">
                    <span class="question-number">题目 {{ index + 1 }}</span>
                    <el-tag size="small">{{ getQuestionTypeLabel(question.question_type) }}</el-tag>
                    <span class="question-score">{{ question.score }}分</span>
                  </div>
                  
                  <div class="question-content">
                    <div class="question-text">{{ question.question_text }}</div>
                    
                    <!-- 选择题选项 -->
                    <div v-if="question.options && question.options.length > 0" class="question-options">
                      <div 
                        v-for="(option, optionIndex) in question.options" 
                        :key="optionIndex"
                        class="option-item"
                      >
                        {{ String.fromCharCode(65 + optionIndex) }}. {{ option }}
                      </div>
                    </div>
                    
                    <!-- 答题区域 -->
                    <div class="answer-section">
                      <el-form-item :label="`题目${index + 1}答案:`">
                        <el-input
                          v-model="question.candidate_answer"
                          type="textarea"
                          :rows="4"
                          placeholder="请输入您的答案..."
                          :disabled="selectedInterview.status === 'completed'"
                          @blur="saveAnswer(question)"
                        />
                      </el-form-item>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 提交面试按钮 -->
              <div class="submit-section" v-if="selectedInterview && (selectedInterview.status === 'in_progress' || selectedInterview.status === 'assigned')">
                <!-- 未开始的面试显示开始按钮 -->
                <div v-if="selectedInterview.status === 'assigned'" class="start-section">
                  <el-button 
                    type="primary" 
                    size="large"
                    @click="startInterview(selectedInterview)"
                  >
                    开始面试
                  </el-button>
                  <p class="start-tip">点击开始面试后即可答题</p>
                </div>
                
                <!-- 进行中的面试显示保存和完成按钮 -->
                <div v-else-if="selectedInterview.status === 'in_progress'" class="action-buttons">
                  <el-button 
                    type="primary" 
                    size="large"
                    :loading="saveLoading"
                    @click="saveAllAnswers"
                  >
                    保存答案
                  </el-button>
                  <el-button 
                    type="success" 
                    size="large"
                    :disabled="!allQuestionsAnswered"
                    :loading="completeLoading"
                    @click="handleCompleteInterview"
                  >
                    完成面试
                  </el-button>
                </div>
                
                <p class="submit-tip" v-if="selectedInterview.status === 'in_progress' && !allQuestionsAnswered">
                  请完成所有题目后再提交面试
                </p>
                <p class="save-tip" v-if="selectedInterview.status === 'in_progress'">
                  提示：答案会在失去焦点时自动保存，您也可以点击"保存答案"手动保存所有已填写的答案
                </p>
              </div>
            </div>

            <!-- 加载题目 -->
            <el-loading v-loading="questionsLoading" v-else-if="questionsLoading">
              <div class="loading-placeholder">正在加载面试题目...</div>
            </el-loading>
          </div>
        </div>
      </div>
    </div>

    <!-- 面试结果查看对话框 -->
    <el-dialog
      v-model="resultDialogVisible"
      title="面试结果"
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="currentEvaluation" class="evaluation-result">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="面试结果">
            <el-tag :type="currentEvaluation.is_passed ? 'success' : 'danger'" size="large">
              {{ currentEvaluation.is_passed ? '通过' : '未通过' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="总分">
            {{ currentEvaluation.total_score }} / {{ currentEvaluation.max_score }}
            ({{ Math.round(currentEvaluation.total_score / currentEvaluation.max_score * 100) }}%)
          </el-descriptions-item>
          <el-descriptions-item label="评价时间">
            {{ formatDateTime(currentEvaluation.evaluated_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="面试官">
            {{ currentEvaluation.evaluator?.username || '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="总体评价" :span="2">
            <div class="evaluation-text">
              {{ currentEvaluation.overall_comments || '无评价' }}
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="决定原因" :span="2">
            <div class="evaluation-text">
              {{ currentEvaluation.decision_reason || '无说明' }}
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="综合建议" :span="2">
            <div class="evaluation-text">
              {{ currentEvaluation.recommendations || '无建议' }}
            </div>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 技能评分 -->
        <div v-if="currentEvaluation.skill_ratings" class="skill-ratings" style="margin-top: 20px;">
          <h4>技能评分</h4>
          <div class="skills-grid">
            <div
              v-for="(rating, skill) in currentEvaluation.skill_ratings"
              :key="skill"
              class="skill-item"
            >
              <span class="skill-name">{{ skill }}</span>
              <el-rate :model-value="rating" disabled show-score />
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="evaluationLoading" class="loading-evaluation">
        <el-loading text="正在加载评价结果..." />
      </div>
      
      <div v-else class="no-evaluation">
        <el-alert
          title="暂无评价结果"
          description="面试官还未完成评价，请耐心等待"
          type="info"
          :closable="false"
        />
      </div>

      <template #footer>
        <el-button @click="resultDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { interviewApi, INTERVIEW_STATUS_LABELS, QUESTION_TYPE_LABELS } from '../api/interviews.js'

// 响应式数据
const interviews = ref([])
const selectedInterview = ref(null)
const questions = ref([])
const statusFilter = ref('')
const listLoading = ref(false)
const questionsLoading = ref(false)
const completeLoading = ref(false)
const saveLoading = ref(false)

// 面试结果相关
const resultDialogVisible = ref(false)
const currentEvaluation = ref(null)
const evaluationLoading = ref(false)

// 计算属性
const answeredQuestionsCount = computed(() => {
  return questions.value.filter(q => q.candidate_answer && q.candidate_answer.trim()).length
})

const allQuestionsAnswered = computed(() => {
  return questions.value.length > 0 && answeredQuestionsCount.value === questions.value.length
})

// 加载面试列表
const loadInterviews = async () => {
  listLoading.value = true
  try {
    const params = statusFilter.value ? { status: statusFilter.value } : {}
    const response = await interviewApi.getMyInterviews(params)
    const interviewList = response.data.data || []
    
    // 为已完成的面试加载评价信息
    const interviewsWithEvaluation = await Promise.all(
      interviewList.map(async (interview) => {
        if (interview.status === 'completed') {
          try {
            const evaluationResponse = await interviewApi.getEvaluation(interview.id)
            interview.evaluation = evaluationResponse.data.data
          } catch (error) {
            // 如果评价不存在（404错误），这是正常的，表示还未评价
            if (error.response?.status !== 404) {
              console.error(`加载面试 ${interview.id} 的评价失败:`, error)
            }
            interview.evaluation = null
          }
        }
        return interview
      })
    )
    
    interviews.value = interviewsWithEvaluation
    
    // 如果当前选中的面试不在列表中，清空选择
    if (selectedInterview.value) {
      const found = interviews.value.find(i => i.id === selectedInterview.value.id)
      if (!found) {
        selectedInterview.value = null
        questions.value = []
      }
    }
  } catch (error) {
    ElMessage.error('加载面试列表失败: ' + (error.response?.data?.message || error.message))
  } finally {
    listLoading.value = false
  }
}

// 选择面试
const selectInterview = async (interview) => {
  selectedInterview.value = interview
  await loadQuestions(interview.id)
}

// 加载面试题目
const loadQuestions = async (interviewId) => {
  questionsLoading.value = true
  try {
    const response = await interviewApi.getInterviewQuestions(interviewId)
    questions.value = response.data.data || []
  } catch (error) {
    ElMessage.error('加载面试题目失败: ' + (error.response?.data?.message || error.message))
    questions.value = []
  } finally {
    questionsLoading.value = false
  }
}

// 开始面试
const startInterview = async (interview) => {
  try {
    await interviewApi.startInterview(interview.id)
    ElMessage.success('面试已开始，祝您面试顺利！')
    await loadInterviews() // 重新加载列表更新状态
    selectInterview(interview)
  } catch (error) {
    ElMessage.error('开始面试失败: ' + (error.response?.data?.message || error.message))
  }
}

// 保存答案
const saveAnswer = async (question) => {
  if (!question.candidate_answer || !question.candidate_answer.trim()) {
    return
  }
  
  try {
    await interviewApi.submitAnswer(question.id, question.candidate_answer.trim())
    // 不显示成功消息，避免过于频繁
  } catch (error) {
    ElMessage.error('保存答案失败: ' + (error.response?.data?.message || error.message))
  }
}

// 保存所有答案
const saveAllAnswers = async () => {
  try {
    saveLoading.value = true
    
    // 获取所有有答案的题目
    const questionsWithAnswers = questions.value.filter(q => 
      q.candidate_answer && q.candidate_answer.trim()
    )
    
    if (questionsWithAnswers.length === 0) {
      ElMessage.warning('没有需要保存的答案')
      return
    }
    
    // 批量保存所有答案
    const savePromises = questionsWithAnswers.map(question =>
      interviewApi.submitAnswer(question.id, question.candidate_answer.trim())
    )
    
    await Promise.all(savePromises)
    
    ElMessage.success(`已保存 ${questionsWithAnswers.length} 道题目的答案`)
    
  } catch (error) {
    console.error('批量保存答案失败:', error)
    ElMessage.error('保存答案失败: ' + (error.response?.data?.message || error.message))
  } finally {
    saveLoading.value = false
  }
}

// 完成面试
const handleCompleteInterview = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要完成面试吗？提交后将无法修改答案。',
      '完成面试确认',
      {
        confirmButtonText: '确定完成',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    completeLoading.value = true
    await interviewApi.completeInterview(selectedInterview.value.id)
    
    ElMessage.success('面试已完成，感谢您的参与！')
    await loadInterviews() // 重新加载列表更新状态
    
    // 更新当前选中面试的状态
    if (selectedInterview.value) {
      const updated = interviews.value.find(i => i.id === selectedInterview.value.id)
      if (updated) {
        selectedInterview.value = updated
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('完成面试失败: ' + (error.response?.data?.message || error.message))
    }
  } finally {
    completeLoading.value = false
  }
}

// 获取状态标签
const getStatusLabel = (status) => {
  return INTERVIEW_STATUS_LABELS[status] || status
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    'assigned': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'evaluated': 'primary'
  }
  return typeMap[status] || 'info'
}

// 获取题目类型标签
const getQuestionTypeLabel = (type) => {
  return QUESTION_TYPE_LABELS[type] || type
}

// 查看面试结果
const viewResult = async (interview) => {
  try {
    evaluationLoading.value = true
    resultDialogVisible.value = true
    currentEvaluation.value = null
    
    const response = await interviewApi.getEvaluation(interview.id)
    currentEvaluation.value = response.data.data
  } catch (error) {
    console.error('加载评价结果失败:', error)
    if (error.response?.status === 404) {
      // 评价不存在，显示暂无评价
      currentEvaluation.value = null
    } else {
      ElMessage.error('加载评价结果失败')
      resultDialogVisible.value = false
    }
  } finally {
    evaluationLoading.value = false
  }
}

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

// 监听状态筛选变化
watch(statusFilter, () => {
  loadInterviews()
})

// 组件挂载时加载数据
onMounted(() => {
  loadInterviews()
})
</script>

<style scoped>
.interview-manager {
  height: 100%;
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
}

.interview-header {
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
  font-size: var(--font-size-xl);
  font-weight: 600;
}

.header-title p {
  color: var(--text-secondary);
  margin: 0;
  font-size: var(--font-size-sm);
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

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

.interview-content {
  padding: var(--spacing-lg);
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.interview-grid {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: var(--spacing-xl);
  height: 100%;
  min-height: 0;
}

.interview-list-section,
.interview-detail-section {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.section-header {
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-primary);
  margin-bottom: var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.header-info {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.duration {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.section-body {
  flex: 1;
  overflow: auto;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
}

.interview-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.interview-item {
  padding: var(--spacing-md);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
}

.interview-item:hover {
  border-color: var(--primary-300);
  background: var(--primary-50);
}

.interview-item.active {
  border-color: var(--primary-500);
  background: var(--primary-100);
}

.interview-info {
  margin-bottom: var(--spacing-sm);
}

.interview-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.interview-meta {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.interview-job {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.interview-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.4;
}

.interview-actions {
  display: flex;
  justify-content: flex-end;
}

.job-requirements {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-primary);
}

.job-requirements h4 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-primary);
}

.job-title {
  font-weight: 600;
  font-size: var(--font-size-lg);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.job-desc {
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: var(--spacing-sm);
}

.job-skills {
  margin-top: var(--spacing-sm);
}

.skill-tag {
  margin-right: var(--spacing-xs);
  margin-bottom: var(--spacing-xs);
}

.questions-section {
  margin-top: var(--spacing-lg);
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

.progress-info {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.question-item {
  padding: var(--spacing-lg);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  background: var(--card-bg);
}

.question-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.question-number {
  font-weight: 600;
  color: var(--primary-600);
}

.question-score {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-left: auto;
}

.question-text {
  font-size: var(--font-size-md);
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.question-options {
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
}

.option-item {
  margin-bottom: var(--spacing-xs);
  color: var(--text-secondary);
}

.answer-section {
  margin-top: var(--spacing-md);
}

.submit-section {
  margin-top: var(--spacing-xl);
  text-align: center;
}

.start-section {
  text-align: center;
  margin-bottom: var(--spacing-md);
}

.start-tip {
  margin-top: var(--spacing-sm);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-bottom: var(--spacing-sm);
}

.submit-tip {
  margin-top: var(--spacing-sm);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.save-tip {
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  font-style: italic;
}

.loading-placeholder {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }

  .interview-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .interview-content {
    padding: var(--spacing-md);
  }

  .interview-grid {
    gap: var(--spacing-md);
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .action-buttons .el-button {
    width: 200px;
  }
}

@media (max-width: 480px) {
  .questions-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .question-header {
    flex-wrap: wrap;
  }
}

/* 评价结果样式 */
.evaluation-result {
  padding: 16px 0;
}

.evaluation-text {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #333;
}

.skill-ratings {
  margin-top: 20px;
}

.skill-ratings h4 {
  margin-bottom: 16px;
  color: #303133;
  font-size: 16px;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.skill-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.skill-name {
  font-weight: 500;
  color: #303133;
}

.loading-evaluation,
.no-evaluation {
  padding: 40px;
  text-align: center;
}
</style>