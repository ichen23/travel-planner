import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 15000,
})

api.interceptors.response.use(
  res => res.data,
  err => ({ success: false, message: err.message })
)

export default api
