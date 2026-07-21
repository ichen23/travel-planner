import api from './api'

export const getDrivingDirection = (origin, destination, strategy = 32) =>
  api.get('/map/direction/driving', { params: { origin, destination, strategy } })

export const getTransitDirection = (origin, destination, city, strategy = 0) =>
  api.get('/map/direction/transit', { params: { origin, destination, city, strategy } })

export const getWalkingDirection = (origin, destination) =>
  api.get('/map/direction/walking', { params: { origin, destination } })

export const getRidingDirection = (origin, destination) =>
  api.get('/map/direction/riding', { params: { origin, destination } })

export const getAllDirections = (origin, destination, city = '') =>
  api.get('/map/direction/all', { params: { origin, destination, city } })

export const getReverseGeocode = (lng, lat) =>
  api.get('/map/reverse-geocode', { params: { lng, lat } })

export const getIpLocation = (ip = '') =>
  api.get('/map/ip-location', { params: { ip } })

export const getMapWeather = (city = '', adcode = '') =>
  api.get('/map/weather', { params: { city, adcode } })

export const getStaticMapUrl = (lng, lat, zoom = 11, width = 750, height = 400, markers = '', paths = '') =>
  api.get('/map/static-map', { params: { lng, lat, zoom, width, height, markers, paths } })

export const compareRoutes = (fromCity, toCity, transportTypes = 'driving,transit,walking') =>
  api.get('/map/route-compare', { params: { from_city: fromCity, to_city: toCity, transport_types: transportTypes } })

export const getRealPoi = (city) =>
  api.get(`/multi-city/real-poi/${encodeURIComponent(city)}`)
