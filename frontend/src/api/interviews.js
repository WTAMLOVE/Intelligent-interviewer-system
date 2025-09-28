import api from './index'

// 面试管理相关API
export const interviewApi = {
    // 获取面试列表
  getInterviews(params = {}) {
    return api.get('/interviews/', { params })
  },

  // 创建面试
  createInterview(data) {
    return api.post('/interviews/', data)
  },

  // 获取面试详情
  getInterview(id) {
    return api.get(`/interviews/${id}`)
  },

  // 更新面试
  updateInterview(id, data) {
    return api.put(`/interviews/${id}`, data)
  },

  // 删除面试
  deleteInterview(id) {
    return api.delete(`/interviews/${id}`)
  },

  // 分配面试给面试者
  assignInterview(id) {
    return api.post(`/interviews/${id}/assign`)
  },

  // 更新面试状态
  updateInterviewStatus(id, status) {
    return api.put(`/interviews/${id}/status`, { status })
  },

  // 开始面试
  startInterview(id) {
    return api.post(`/interviews/${id}/start`)
  },

  // 完成面试
  completeInterview(id) {
    return api.post(`/interviews/${id}/complete`)
  },

  // 获取面试题目
  getInterviewQuestions(interviewId) {
    return api.get(`/interviews/${interviewId}/questions`)
  },

  // 添加面试题目
  addQuestion(interviewId, data) {
    return api.post(`/interviews/${interviewId}/questions`, data)
  },

  // 更新题目
  updateQuestion(questionId, data) {
    return api.put(`/interviews/questions/${questionId}`, data)
  },

  // 删除题目
  deleteQuestion(questionId) {
    return api.delete(`/interviews/questions/${questionId}`)
  },

  // 提交答案
  submitAnswer(questionId, answer) {
    return api.post(`/interviews/questions/${questionId}/answer`, { answer })
  },

    // 为题目评分
  scoreQuestion(questionId, score, comments = '') {
    return api.post(`/interviews/questions/${questionId}/score`, { score, comments })
  },

  // 获取面试评价
  getEvaluation(interviewId) {
    return api.get(`/interviews/${interviewId}/evaluation`)
  },

  // 创建面试评价
  createEvaluation(interviewId, data) {
    return api.post(`/interviews/${interviewId}/evaluation`, data)
  },

  // 更新面试评价
  updateEvaluation(evaluationId, data) {
    return api.put(`/interviews/evaluation/${evaluationId}`, data)
  },

  // 获取我的面试列表（面试者）
  getMyInterviews(params = {}) {
    return api.get('/interviews/my-interviews', { params })
  },

  // 开始面试
  startInterview(id) {
    return api.post(`/interviews/${id}/start`)
  },

  // 完成面试
  completeInterview(id) {
    return api.post(`/interviews/${id}/complete`)
  }
}

// 面试状态常量
export const INTERVIEW_STATUS = {
  DRAFT: 'draft',           // 草稿
  ASSIGNED: 'assigned',     // 已分配
  IN_PROGRESS: 'in_progress', // 进行中
  PENDING_EVALUATION: 'pending_evaluation', // 待评价
  COMPLETED: 'completed',   // 已完成
  EVALUATED: 'evaluated'    // 已评价（保留兼容性）
}

// 面试状态标签映射
export const INTERVIEW_STATUS_LABELS = {
  [INTERVIEW_STATUS.DRAFT]: '草稿',
  [INTERVIEW_STATUS.ASSIGNED]: '已分配',
  [INTERVIEW_STATUS.IN_PROGRESS]: '进行中',
  [INTERVIEW_STATUS.PENDING_EVALUATION]: '待评价',
  [INTERVIEW_STATUS.COMPLETED]: '已完成',
  [INTERVIEW_STATUS.EVALUATED]: '已评价'
}

// 题目类型常量
export const QUESTION_TYPES = {
  SINGLE_CHOICE: 'single_choice',     // 单选题
  MULTIPLE_CHOICE: 'multiple_choice', // 多选题
  TEXT: 'text',                       // 文本题
  CODE: 'code'                        // 代码题
}

// 题目类型标签映射
export const QUESTION_TYPE_LABELS = {
  [QUESTION_TYPES.SINGLE_CHOICE]: '单选题',
  [QUESTION_TYPES.MULTIPLE_CHOICE]: '多选题',
  [QUESTION_TYPES.TEXT]: '文本题',
  [QUESTION_TYPES.CODE]: '代码题'
}

export default interviewApi