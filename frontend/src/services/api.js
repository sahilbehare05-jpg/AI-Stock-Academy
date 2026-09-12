import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('asa_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('asa_token')
      localStorage.removeItem('asa_user')
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  me: () => api.get('/api/auth/me'),
}
export const stocksAPI = {
  getStock: (symbol, period = '1mo', interval = '1d') =>
    api.get(
      `/api/stocks/${encodeURIComponent(symbol)}?period=${period}&interval=${interval}`
    ),
}
export const predictionAPI = {
  predict: (symbol) =>
    api.get(`/api/prediction/${encodeURIComponent(symbol)}`),

  explain: (symbol) =>
    api.get(`/api/prediction/explain/${encodeURIComponent(symbol)}`),

}

export const academyAPI = {
  getModules: () =>
    api.get('/api/academy/modules'),

  getModuleLessons: (moduleId) =>
    api.get(`/api/academy/modules/${moduleId}/lessons`),

  completeLesson: (lessonId) =>
    api.post(`/api/academy/lessons/${lessonId}/complete`),

  getProgress: () =>
    api.get('/api/academy/progress'),
}
export const modelPerformanceAPI = {
  getPerformance: (symbol, period = '1y') =>
    api.get(
      `/api/model-performance/${encodeURIComponent(symbol)}?period=${period}`
    ),
}
export const tutorAPI = {
  chat: (data) =>
    api.post('/api/tutor/chat', data),
}
export default api
