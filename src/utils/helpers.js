export const formatPrice = (p) => p ? `¥${Number(p).toFixed(0)}` : '-'

export const formatDuration = (d) => {
  if (!d) return '-'
  const parts = d.split(':')
  return `${parts[0]}小时${parts[1]}分`
}

export const formatDateTime = (d) => {
  if (!d) return '-'
  return d.replace('T', ' ').slice(0, 16)
}

export const getDurationColor = (hours) => {
  if (hours <= 2) return 'green'
  if (hours <= 4) return 'blue'
  if (hours <= 6) return 'orange'
  return 'red'
}

export const getAvailabilityColor = (availability) => {
  if (availability === '有' || (availability && parseInt(availability) > 0)) return 'green'
  if (availability === '无') return 'red'
  return 'default'
}
