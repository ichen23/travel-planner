import axios from 'axios'

const isLocal = typeof window !== 'undefined' && window.location.hostname === 'localhost'
const baseURL = isLocal ? 'http://localhost:8000/api' : '/api'

const api = axios.create({
  baseURL,
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
