import api from './api'

export const searchTrains = (from, to, date, isHigh = true) =>
  api.get('/train/search', { params: { from_station: from, to_station: to, date, is_high_speed: isHigh } })

export const getRecommendations = (fromCity, travelDate, maxDuration = 4) =>
  api.get('/destination/recommend', { params: { from_city: fromCity, travel_date: travelDate, max_duration: maxDuration } })
