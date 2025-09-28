import api from './index'

export const userAPI = {
  // 获取面试者列表
  async getInterviewees() {
    const response = await api.get('/users?role=interviewee')
    return {
      data: {
        users: response.data.data || []
      }
    }
  },

  // 获取所有用户
  async getAllUsers() {
    const response = await api.get('/users')
    return {
      data: {
        users: response.data.data || []
      }
    }
  },

  // 根据角色获取用户
  async getUsersByRole(role) {
    const response = await api.get(`/users?role=${role}`)
    return {
      data: {
        users: response.data.data || []
      }
    }
  }
}