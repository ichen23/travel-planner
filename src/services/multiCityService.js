import api from './api'

export const getMultiCityCities = () =>
  api.get('/multi-city/cities')

export const getTrainInfo = (fromCity, toCity) =>
  api.get(`/multi-city/train-info/${encodeURIComponent(fromCity)}/${encodeURIComponent(toCity)}`)

export const generateMultiCityItinerary = (cities, dayAllocation, totalDays, budget, preference = '') =>
  api.post('/multi-city/generate', {
    cities,
    day_allocation: dayAllocation,
    total_days: totalDays,
    budget,
    preference
  })

export const quickPlanMultiCity = (cities, dayAllocation, totalDays, budget, preference = '') =>
  api.post('/multi-city/quick-plan', {
    cities,
    day_allocation: dayAllocation,
    total_days: totalDays,
    budget,
    preference
  })

export const getMultiCityDetail = (city) =>
  api.get(`/multi-city/city-detail/${encodeURIComponent(city)}`)
