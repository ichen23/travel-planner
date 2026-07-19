const KEY_FAVORITES = 'travel_favorites'
const KEY_PLANNERS = 'travel_planners'
const KEY_NOTES = 'travel_notes'
const KEY_HISTORY = 'travel_history'
const KEY_PREFERENCES = 'travel_preferences'
const KEY_AI_CACHE = 'travel_ai_cache'
const KEY_DRAFTS = 'travel_drafts'
const KEY_STATION_NOTES = 'travel_station_notes'

export const getFavorites = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_FAVORITES) || '{"trains":[],"destinations":[],"planners":[]}')
  } catch {
    return { trains: [], destinations: [], planners: [] }
  }
}

export const addFavorite = (type, item) => {
  const favs = getFavorites()
  const list = favs[type] || []
  list.push({ ...item, savedAt: new Date().toISOString() })
  favs[type] = list
  localStorage.setItem(KEY_FAVORITES, JSON.stringify(favs))
}

export const removeFavorite = (type, index) => {
  const favs = getFavorites()
  favs[type] = (favs[type] || []).filter((_, i) => i !== index)
  localStorage.setItem(KEY_FAVORITES, JSON.stringify(favs))
}

export const savePlanner = (planner) => {
  const planners = JSON.parse(localStorage.getItem(KEY_PLANNERS) || '[]')
  planners.push({ ...planner, savedAt: new Date().toISOString() })
  localStorage.setItem(KEY_PLANNERS, JSON.stringify(planners))
}

export const getPlanners = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_PLANNERS) || '[]')
  } catch {
    return []
  }
}

export const getNotes = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_NOTES) || '[]')
  } catch {
    return []
  }
}

export const saveNote = (note) => {
  const notes = getNotes()
  const newNote = {
    id: note.id || Date.now().toString(),
    title: note.title || '未命名笔记',
    content: note.content || '',
    category: note.category || '其他',
    updatedAt: new Date().toISOString(),
    createdAt: note.createdAt || new Date().toISOString(),
  }
  
  const existingIndex = notes.findIndex(n => n.id === newNote.id)
  if (existingIndex >= 0) {
    notes[existingIndex] = newNote
  } else {
    notes.unshift(newNote)
  }
  
  localStorage.setItem(KEY_NOTES, JSON.stringify(notes))
  return newNote
}

export const deleteNote = (noteId) => {
  const notes = getNotes().filter(n => n.id !== noteId)
  localStorage.setItem(KEY_NOTES, JSON.stringify(notes))
}

export const getHistory = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_HISTORY) || '{"searches":[],"cities":[],"trains":[]}')
  } catch {
    return { searches: [], cities: [], trains: [] }
  }
}

export const addToHistory = (type, item) => {
  const history = getHistory()
  const list = history[type] || []
  
  const newItem = { ...item, timestamp: new Date().toISOString() }
  const filtered = list.filter(i => {
    if (type === 'searches') return i.query !== newItem.query
    if (type === 'cities') return i !== newItem.city
    if (type === 'trains') return i.trainNo !== newItem.trainNo
    return true
  })
  
  history[type] = [newItem, ...filtered].slice(0, 50)
  localStorage.setItem(KEY_HISTORY, JSON.stringify(history))
}

export const clearHistory = (type = null) => {
  if (type) {
    const history = getHistory()
    history[type] = []
    localStorage.setItem(KEY_HISTORY, JSON.stringify(history))
  } else {
    localStorage.setItem(KEY_HISTORY, JSON.stringify({ searches: [], cities: [], trains: [] }))
  }
}

export const getPreferences = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_PREFERENCES) || JSON.stringify({
      foodRestrictions: [],
      departureCity: '',
      walkingLimit: 5000,
      budgetRange: { min: 1000, max: 5000 },
      theme: 'dark',
      fontSize: 'normal',
      travelStyle: 'comfort',
    }))
  } catch {
    return {
      foodRestrictions: [],
      departureCity: '',
      walkingLimit: 5000,
      budgetRange: { min: 1000, max: 5000 },
      theme: 'dark',
      fontSize: 'normal',
      travelStyle: 'comfort',
    }
  }
}

export const updatePreferences = (updates) => {
  const prefs = getPreferences()
  const newPrefs = { ...prefs, ...updates }
  localStorage.setItem(KEY_PREFERENCES, JSON.stringify(newPrefs))
  return newPrefs
}

export const getAICache = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_AI_CACHE) || '{}')
  } catch {
    return {}
  }
}

export const setAICache = (key, value, ttl = 86400000) => {
  const cache = getAICache()
  cache[key] = {
    value,
    timestamp: Date.now(),
    expiresAt: Date.now() + ttl,
  }
  localStorage.setItem(KEY_AI_CACHE, JSON.stringify(cache))
}

export const getAICacheItem = (key) => {
  const cache = getAICache()
  const item = cache[key]
  
  if (!item) return null
  if (item.expiresAt < Date.now()) {
    delete cache[key]
    localStorage.setItem(KEY_AI_CACHE, JSON.stringify(cache))
    return null
  }
  
  return item.value
}

export const clearAICache = () => {
  localStorage.setItem(KEY_AI_CACHE, JSON.stringify({}))
}

export const getDrafts = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_DRAFTS) || '[]')
  } catch {
    return []
  }
}

export const saveDraft = (draft) => {
  const drafts = getDrafts()
  const newDraft = {
    id: draft.id || Date.now().toString(),
    title: draft.title || '未命名行程',
    data: draft.data,
    updatedAt: new Date().toISOString(),
    createdAt: draft.createdAt || new Date().toISOString(),
  }
  
  const existingIndex = drafts.findIndex(d => d.id === newDraft.id)
  if (existingIndex >= 0) {
    drafts[existingIndex] = newDraft
  } else {
    drafts.unshift(newDraft)
  }
  
  localStorage.setItem(KEY_DRAFTS, JSON.stringify(drafts))
  return newDraft
}

export const deleteDraft = (draftId) => {
  const drafts = getDrafts().filter(d => d.id !== draftId)
  localStorage.setItem(KEY_DRAFTS, JSON.stringify(drafts))
}

export const getStationNotes = () => {
  try {
    return JSON.parse(localStorage.getItem(KEY_STATION_NOTES) || '{}')
  } catch {
    return {}
  }
}

export const saveStationNote = (stationId, note) => {
  const notes = getStationNotes()
  notes[stationId] = {
    note,
    updatedAt: new Date().toISOString(),
  }
  localStorage.setItem(KEY_STATION_NOTES, JSON.stringify(notes))
}

export const getStationNote = (stationId) => {
  const notes = getStationNotes()
  return notes[stationId]?.note || ''
}

export const exportAllData = () => {
  return {
    favorites: getFavorites(),
    planners: getPlanners(),
    notes: getNotes(),
    history: getHistory(),
    preferences: getPreferences(),
    drafts: getDrafts(),
    stationNotes: getStationNotes(),
    exportedAt: new Date().toISOString(),
  }
}

export const importAllData = (data) => {
  if (data.favorites) localStorage.setItem(KEY_FAVORITES, JSON.stringify(data.favorites))
  if (data.planners) localStorage.setItem(KEY_PLANNERS, JSON.stringify(data.planners))
  if (data.notes) localStorage.setItem(KEY_NOTES, JSON.stringify(data.notes))
  if (data.history) localStorage.setItem(KEY_HISTORY, JSON.stringify(data.history))
  if (data.preferences) localStorage.setItem(KEY_PREFERENCES, JSON.stringify(data.preferences))
  if (data.drafts) localStorage.setItem(KEY_DRAFTS, JSON.stringify(data.drafts))
  if (data.stationNotes) localStorage.setItem(KEY_STATION_NOTES, JSON.stringify(data.stationNotes))
}

export const clearAllData = () => {
  localStorage.removeItem(KEY_FAVORITES)
  localStorage.removeItem(KEY_PLANNERS)
  localStorage.removeItem(KEY_NOTES)
  localStorage.removeItem(KEY_HISTORY)
  localStorage.removeItem(KEY_PREFERENCES)
  localStorage.removeItem(KEY_AI_CACHE)
  localStorage.removeItem(KEY_DRAFTS)
  localStorage.removeItem(KEY_STATION_NOTES)
}
