import api from './api'

export const getRecommendations = (fromCity, travelDate, maxDuration = 3, preference = '') =>
  api.get('/destination/recommend', { params: { from_city: fromCity, travel_date: travelDate, max_duration: maxDuration, preference } })

export const getCityDetail = (city, realtime = true) =>
  api.get(`/destination/detail/${encodeURIComponent(city)}`, { params: { realtime } })

export const getCityRealtime = (city) =>
  api.get(`/destination/realtime/${encodeURIComponent(city)}`)

export const getFullContent = (city) =>
  api.get(`/destination/full-content/${encodeURIComponent(city)}`)

export const getStartCities = () =>
  api.get('/destination/start-cities')

export const getStats = () =>
  api.get('/destination/stats')

export const searchCities = (keyword, limit = 20, type = 'all') =>
  api.get('/destination/search-city', { params: { keyword, limit, type } })

export const searchCityDetail = (keyword, limit = 10) =>
  api.get('/destination/search-city-detail', { params: { keyword, limit } })

export const getRealCities = (province = '', limit = 100) =>
  api.get('/destination/real-cities', { params: { province, limit } })

export const searchPois = (city, keywords, types = '', offset = 20) =>
  api.get('/destination/poi', { params: { city, keywords, types, offset } })

export const searchNearby = (lng, lat, keywords = '', radius = 3000, types = '', offset = 20) =>
  api.get('/destination/nearby', { params: { lng, lat, keywords, radius, types, offset } })

export const searchAttractions = (city, keyword = '', limit = 20) =>
  api.get('/destination/attractions', { params: { city, keyword, limit } })

export const searchFoods = (city, keyword = '', limit = 20) =>
  api.get('/destination/foods', { params: { city, keyword, limit } })

export const searchHotels = (city, keyword = '', limit = 20) =>
  api.get('/destination/hotels', { params: { city, keyword, limit } })

export const getPoiDetail = (poiId) =>
  api.get('/destination/poi-detail', { params: { poi_id: poiId } })

export const searchTips = (keywords, city = '') =>
  api.get('/destination/tips', { params: { keywords, city } })

export const getGeocode = (city) =>
  api.get('/destination/geocode', { params: { city } })

export const getRoute = (originLng, originLat, destLng, destLat, mode = 'walking') =>
  api.get('/destination/route', { params: { origin_lng: originLng, origin_lat: originLat, dest_lng: destLng, dest_lat: destLat, mode } })

export const getWeather = (city) =>
  api.get('/weather/current', { params: { city } })

export const generateItinerary = (city, days = 3, budget = 3000, preference = '') =>
  api.post('/destination/generate-itinerary', { city, days, budget, preference })

export const generateItineraryAdvanced = (params) =>
  api.post('/destination/generate-itinerary', params)

export const generateMultipleItineraries = (params) =>
  api.post('/destination/generate-multiple', params)

export const generateFromNaturalLanguage = (text) =>
  api.post('/destination/generate-from-text', { text })

export const parseNaturalLanguage = (text) =>
  api.post('/destination/parse-text', { text })

export const compareCities = (cities) =>
  api.post('/destination/compare-cities', { cities })

export const getWeatherForecast = (city) =>
  api.get(`/destination/weather-forecast/${encodeURIComponent(city)}`)

export const generateLuggageChecklist = (params) =>
  api.post('/destination/luggage-checklist', params)

export const generateAIContent = (templateType, context = {}) =>
  api.post('/ai/generate', { template_type: templateType, context })

export const getAITemplates = () =>
  api.get('/ai/templates')
