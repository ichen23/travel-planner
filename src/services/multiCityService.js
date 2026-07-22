import api from './api'

export const getMultiCityCities = () =>
  api.get('/multi-city/cities')

export const getTrainInfo = (fromCity, toCity) =>
  api.get(`/multi-city/train-info/${encodeURIComponent(fromCity)}/${encodeURIComponent(toCity)}`)

export const getCityAttractions = (city) =>
  api.get(`/multi-city/city-attractions/${encodeURIComponent(city)}`)

export const generateMultiCityItinerary = (cities, dayAllocation, totalDays, budget, preference = '', userAttractions = null) =>
  api.post('/multi-city/generate', {
    cities,
    day_allocation: dayAllocation,
    total_days: totalDays,
    budget,
    preference,
    user_attractions: userAttractions
  })

export const quickPlanMultiCity = (cities, dayAllocation, totalDays, budget, preference = '', userAttractions = null) =>
  api.post('/multi-city/quick-plan', {
    cities,
    day_allocation: dayAllocation,
    total_days: totalDays,
    budget,
    preference,
    user_attractions: userAttractions
  })

export const getMultiCityDetail = (city) =>
  api.get(`/multi-city/city-detail/${encodeURIComponent(city)}`)

export const modifyDayItinerary = (itinerary, dayIndex, action, params) =>
  api.post('/multi-city/modify-day', {
    itinerary,
    day_index: dayIndex,
    action,
    params
  })

export const getAvailableAttractions = (city) =>
  api.get(`/multi-city/available-attractions/${encodeURIComponent(city)}`)
