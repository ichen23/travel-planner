export const HOT_CITIES = [
  '北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉',
  '西安', '重庆', '长沙', '郑州', '苏州', '天津', '青岛', '厦门',
]

export const PREFERENCES = [
  { value: '', label: '综合推荐' },
  { value: '自然', label: '自然风光' },
  { value: '历史', label: '历史文化' },
  { value: '美食', label: '美食之旅' },
  { value: '购物', label: '都市购物' },
  { value: '亲子', label: '亲子度假' },
]

export const DURATION_OPTIONS = [
  { value: 1, label: '1小时内' },
  { value: 2, label: '2小时内' },
  { value: 3, label: '3小时内' },
  { value: 4, label: '4小时内' },
  { value: 5, label: '5小时内' },
  { value: 6, label: '6小时内' },
  { value: 7, label: '7小时以上' },
]

export const TRANSPORT_MODES = [
  { value: 'walk', label: '步行' },
  { value: 'drive', label: '打车' },
  { value: 'transit', label: '公交/地铁' },
]

export const CITY_TYPES = [
  { value: 'all', label: '全部类型', icon: '🌍' },
  { value: 'popular', label: '热门城市', icon: '⭐' },
  { value: 'provincial', label: '省会城市', icon: '🏛️' },
  { value: 'prefecture', label: '地级市', icon: '🏙️' },
  { value: 'scenic', label: '特色景点', icon: '🏔️' },
  { value: 'ancient', label: '古城古镇', icon: '🏯' },
]

export const CATEGORY_FILTERS = [
  { value: 'all', label: '全部分类' },
  { value: 'food', label: '🍜 美食' },
  { value: 'nature', label: '🏔️ 自然' },
  { value: 'history', label: '🏛️ 历史' },
  { value: 'sea', label: '🌊 海滨' },
  { value: 'ancient', label: '🏯 古城' },
  { value: 'modern', label: '🏙️ 都市' },
  { value: 'family', label: '👨‍👩‍👧 亲子' },
  { value: 'adventure', label: '🎒 冒险' },
]

export const SORT_OPTIONS = [
  { value: 'default', label: '默认排序' },
  { value: 'rating', label: '评分最高' },
  { value: 'duration', label: '时间最短' },
  { value: 'price', label: '价格最低' },
  { value: 'popular', label: '最热门' },
]

export const PROVINCIAL_CITIES = [
  '石家庄', '太原', '沈阳', '长春', '哈尔滨', '南京', '杭州', '合肥',
  '福州', '南昌', '济南', '郑州', '武汉', '长沙', '广州', '海口',
  '成都', '贵阳', '昆明', '西安', '兰州', '西宁', '台北',
  '呼和浩特', '南宁', '银川', '乌鲁木齐', '拉萨',
]

export const SPECIAL_SCENIC_CITIES = [
  '丽江', '大理', '九寨沟', '香格里拉', '张家界', '黄山', '三亚',
  '桂林', '黄山市', '敦煌', '吐鲁番', '拉萨', '呼伦贝尔',
  '承德', '秦皇岛', '五台山', '平遥',
]

export const ANCIENT_TOWNS = [
  '平遥', '丽江', '大理', '凤凰', '周庄', '乌镇', '西塘',
  '阆中', '歙县', '宏村', '西递', '芙蓉镇', '束河',
]

export const CATEGORY_KEYWORDS = {
  food: ['美食', '美食之都', '美食天堂', '地道小吃', '特产'],
  nature: ['自然', '山水', '风景', '自然景观', '世界遗产', '摄影'],
  history: ['历史', '文化', '古迹', '古都', '古城', '遗址', '博物馆'],
  sea: ['海滨', '海', '海岛', '海岸', '海滩', '水下', '海洋'],
  ancient: ['古城', '古镇', '古街', '古巷', '古村落'],
  modern: ['都市', '现代', '购物', '商圈', '主题乐园', '摩天'],
  family: ['亲子', '家庭', '主题乐园', '动物园', '游乐园'],
  adventure: ['冒险', '探险', '户外', '登山', '徒步', '漂流', '极限'],
}

export function getCityType(cityName, tags = []) {
  if (SPECIAL_SCENIC_CITIES.includes(cityName)) return 'scenic'
  if (ANCIENT_TOWNS.includes(cityName)) return 'ancient'
  if (HOT_CITIES.includes(cityName)) return 'popular'
  if (PROVINCIAL_CITIES.includes(cityName)) return 'provincial'
  return 'prefecture'
}

export function getCategories(tags = []) {
  const categories = ['all']
  const tagsStr = tags.join('')
  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (keywords.some(kw => tagsStr.includes(kw))) {
      categories.push(category)
    }
  }
  return categories
}

export function matchCategory(cityName, tags = [], category) {
  if (category === 'all') return true
  const tagsStr = tags.join('')
  const keywords = CATEGORY_KEYWORDS[category] || []
  return keywords.some(kw => tagsStr.includes(kw)) || 
         (category === 'scenic' && SPECIAL_SCENIC_CITIES.includes(cityName)) ||
         (category === 'ancient' && ANCIENT_TOWNS.includes(cityName)) ||
         (category === 'sea' && tagsStr.includes('海'))
}

export function getDurationMinutes(durationStr) {
  if (!durationStr) return 0
  const match = durationStr.match(/(\d+)/)
  if (match) {
    const num = parseInt(match[1])
    if (durationStr.includes('小时') || durationStr.includes('h')) {
      return num * 60
    }
    return num
  }
  return 0
}

export function getPriceNumber(price) {
  if (!price || price === '以实际为准' || price === '参考价') return Infinity
  if (typeof price === 'number') return price
  const num = parseInt(price.replace(/[^\d]/g, ''))
  return num || Infinity
}
