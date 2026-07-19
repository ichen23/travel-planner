import { create } from 'zustand'

export const usePlannerStore = create((set) => ({
  fromCity: '',
  travelDate: '',
  maxDuration: 4,
  preference: '',
  selectedDestination: null,
  schedule: {
    days: [{ day: 1, date: '', items: [] }]
  },
  setFromCity: (v) => set({ fromCity: v }),
  setTravelDate: (v) => set({ travelDate: v }),
  setMaxDuration: (v) => set({ maxDuration: v }),
  setPreference: (v) => set({ preference: v }),
  setSelectedDestination: (d) => set({ selectedDestination: d }),
  addScheduleItem: (dayIndex, item) => set((state) => {
    const days = [...state.schedule.days]
    days[dayIndex].items.push(item)
    return { schedule: { days } }
  }),
  removeScheduleItem: (dayIndex, itemIndex) => set((state) => {
    const days = [...state.schedule.days]
    days[dayIndex].items = days[dayIndex].items.filter((_, i) => i !== itemIndex)
    return { schedule: { days } }
  }),
  moveItem: (dayIndex, fromIdx, toIdx) => set((state) => {
    const days = [...state.schedule.days]
    const items = [...days[dayIndex].items]
    const [moved] = items.splice(fromIdx, 1)
    items.splice(toIdx, 0, moved)
    days[dayIndex].items = items
    return { schedule: { days } }
  }),
  setDays: (count) => set((state) => {
    const days = []
    for (let i = 0; i < count; i++) {
      days.push(state.schedule.days[i] || { day: i + 1, date: '', items: [] })
    }
    return { schedule: { days } }
  }),
  resetSchedule: () => set({ schedule: { days: [{ day: 1, date: '', items: [] }] } }),
}))
