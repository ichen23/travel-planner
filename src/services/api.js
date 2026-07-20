import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
})

api.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response) {
      return { success: false, message: err.response.data?.detail || err.message }
    }
    return { success: false, message: err.message }
  }
)

export default api
