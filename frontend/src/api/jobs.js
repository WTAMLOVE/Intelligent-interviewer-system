import api from './index'

const base = '/jobs'

export async function listJobs() {
  const res = await api.get(base + '/')
  return res.data
}

export async function getJob(id) {
  const res = await api.get(base + `/${id}`)
  return res.data
}

export async function createJob(payload) {
  const res = await api.post(base + '/', payload)
  return res.data
}

export async function updateJob(id, payload) {
  const res = await api.put(base + `/${id}`, payload)
  return res.data
}

export async function deleteJob(id) {
  const res = await api.delete(base + `/${id}`)
  return res.data
}
