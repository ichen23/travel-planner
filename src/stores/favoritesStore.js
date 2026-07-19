import { create } from 'zustand'
import { getFavorites, addFavorite, removeFavorite } from '../services/storageService'

export const useFavoritesStore = create((set, get) => ({
  favorites: getFavorites(),
  folders: getFavorites().folders || {
    '默认收藏夹': { id: 'default', name: '默认收藏夹', items: [] },
  },
  activeFolder: '默认收藏夹',
  
  loadFavorites: () => set({ 
    favorites: getFavorites(),
    folders: getFavorites().folders || { '默认收藏夹': { id: 'default', name: '默认收藏夹', items: [] } }
  }),
  
  addToFavorites: (type, item, folderName = null) => {
    const state = get()
    const folder = folderName || state.activeFolder
    if (state.folders[folder]) {
      state.folders[folder].items.push({ type, item, addedAt: new Date().toISOString() })
    }
    addFavorite(type, item)
    localStorage.setItem('travel_folders', JSON.stringify(state.folders))
    set({ favorites: getFavorites(), folders: state.folders })
  },
  
  removeFromFavorites: (type, index) => {
    removeFavorite(type, index)
    set({ favorites: getFavorites() })
  },
  
  createFolder: (folderName) => {
    const state = get()
    if (!state.folders[folderName]) {
      state.folders[folderName] = { id: Date.now().toString(), name: folderName, items: [] }
      localStorage.setItem('travel_folders', JSON.stringify(state.folders))
      set({ folders: { ...state.folders } })
    }
  },
  
  deleteFolder: (folderName) => {
    const state = get()
    if (folderName !== '默认收藏夹' && state.folders[folderName]) {
      delete state.folders[folderName]
      const newActive = Object.keys(state.folders)[0] || '默认收藏夹'
      localStorage.setItem('travel_folders', JSON.stringify(state.folders))
      set({ folders: state.folders, activeFolder: newActive })
    }
  },
  
  setActiveFolder: (folderName) => set({ activeFolder: folderName }),
  
  moveToFolder: (type, itemIndex, fromFolder, toFolder) => {
    const state = get()
    if (state.folders[fromFolder] && state.folders[toFolder]) {
      const item = state.folders[fromFolder].items.splice(itemIndex, 1)[0]
      state.folders[toFolder].items.push(item)
      localStorage.setItem('travel_folders', JSON.stringify(state.folders))
      set({ folders: { ...state.folders } })
    }
  },
}))