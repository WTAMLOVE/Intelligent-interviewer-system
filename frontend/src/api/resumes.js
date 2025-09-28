import api from './index.js'

// 简历相关API
export const resumeAPI = {
  // 获取我的简历
  getMyResume() {
    return api.get('/resumes/my')
  },

  // 创建或更新我的简历
  saveMyResume(content) {
    return api.post('/resumes/my', { content })
  },

  // 删除我的简历
  deleteMyResume() {
    return api.delete('/resumes/my')
  },

  // 获取指定用户的简历（面试官和管理员使用）
  getUserResume(userId) {
    return api.get(`/resumes/user/${userId}`)
  }
}