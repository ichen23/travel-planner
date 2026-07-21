import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Card, Row, Col, Tag, Typography, Button, Space, message, Empty, Tabs,
  Statistic, Divider, Spin, Alert, Tooltip, Badge, Switch, Select, Segmented
} from 'antd'
import {
  ArrowLeftOutlined, CloudOutlined, StarFilled, EnvironmentOutlined,
  ThunderboltOutlined, CheckCircleFilled, InfoCircleOutlined, CalendarOutlined,
  DollarOutlined, CompassOutlined, ShareAltOutlined, HeartOutlined, HeartFilled,
  PlusOutlined, SwapOutlined, SafetyOutlined, MessageOutlined, 
  ArrowUpOutlined, ArrowDownOutlined, BulbFilled,
  AimOutlined
} from '@ant-design/icons'
import { getCityDetail, getWeather, getWeatherForecast } from '../services/destinationService'
import PoiCard from '../components/PoiCard'
import PoiDetailModal from '../components/PoiDetailModal'

const { Title, Text, Paragraph } = Typography

const WEATHER_ICONS = {
  sunny: '☀️',
  cloudy: '⛅',
  overcast: '☁️',
  rain: '🌧️',
  heavy_rain: '⛈️',
  snow: '🌨️',
  fog: '🌫️',
  thunder: '⛈️',
}

const getWeatherIcon = (text) => {
  if (!text) return '🌤️'
  const t = text.toLowerCase()
  if (t.includes('晴')) return '☀️'
  if (t.includes('云') || t.includes('阴')) return '⛅'
  if (t.includes('雨') && t.includes('雷')) return '⛈️'
  if (t.includes('雨')) return '🌧️'
  if (t.includes('雪')) return '🌨️'
  if (t.includes('雾') || t.includes('霾')) return '🌫️'
  if (t.includes('风')) return '💨'
  return '🌤️'
}

const getClothingAdvice = (temp) => {
  if (temp >= 30) return '🧥 建议穿着轻薄透气的短袖短裤，注意防晒'
  if (temp >= 25) return '👕 建议穿着短袖T恤、薄长裤或裙装'
  if (temp >= 20) return '🧶 建议穿着薄外套、长袖衬衫'
  if (temp >= 15) return '🧥 建议穿着夹克、风衣等春秋装'
  if (temp >= 10) return '🧥 建议穿着毛衣、厚外套'
  if (temp >= 0) return '🧣 建议穿着羽绒服、厚毛衣、围巾'
  return '🧤 建议穿着厚羽绒服、保暖内衣、手套'
}

const getUmbrellaTip = (weather) => {
  if (!weather) return null
  const t = weather.toLowerCase()
  if (t.includes('雨') && t.includes('雷')) return { icon: '⛈️', text: '有雷阵雨，建议携带雨具并注意安全', color: '#ff4d4f' }
  if (t.includes('雨')) return { icon: '🌧️', text: '有降雨，建议携带雨伞', color: '#1890ff' }
  return null
}

const getSunProtectionTip = (weather, temp) => {
  if (!weather) return null
  const t = weather.toLowerCase()
  if (t.includes('晴') || t.includes('云')) {
    if (temp >= 30) return { icon: '🔥', text: '高温炎热，务必做好防晒措施', color: '#ff7a45' }
    if (temp >= 25) return { icon: '☀️', text: '阳光充足，建议涂抹防晒霜', color: '#faad14' }
    return { icon: '🌤️', text: '紫外线较强，建议防晒', color: '#faad14' }
  }
  return null
}

const getActivitySuggestion = (weather, temp) => {
  if (!weather) return { outdoor: [], indoor: [] }
  const t = weather.toLowerCase()
  const rainy = t.includes('雨')
  const hot = temp >= 32
  const cold = temp <= 5

  let outdoor = []
  let indoor = []

  if (rainy) {
    outdoor = ['室内博物馆游览', '美术馆参观', '室内商场购物', '电影院观影']
    indoor = ['咖啡厅下午茶', 'SPA按摩放松', '图书馆阅读', '室内亲子乐园']
  } else if (hot) {
    outdoor = ['清晨公园散步', '水上乐园游玩', '室内游泳馆', '商场购物']
    indoor = ['空调房休息', '冰品甜品', '室内蹦床', 'VR体验馆']
  } else if (cold) {
    outdoor = ['滑雪场体验', '温泉泡汤', '冬季美食街', '室内活动为主']
    indoor = ['壁炉咖啡馆', '温泉酒店', '室内体育馆', '烘焙DIY']
  } else {
    outdoor = ['城市漫步拍照', '公园野餐', '骑行游览', '户外摄影', '徒步登山']
    indoor = ['特色餐厅美食', '文创市集', '书店咖啡馆', '手作工坊体验']
  }

  return { outdoor, indoor }
}

export default function DestinationDetailPage() {
  const { city } = useParams()
  const navigate = useNavigate()
  const [detail, setDetail] = useState(null)
  const [weather, setWeather] = useState(null)
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [realtimeLoading, setRealtimeLoading] = useState(false)
  const [forecastLoading, setForecastLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('attractions')
  const [selectedPoi, setSelectedPoi] = useState(null)
  const [poiModalVisible, setPoiModalVisible] = useState(false)

  const [mapLayer, setMapLayer] = useState('standard')
  const [showAttractions, setShowAttractions] = useState(true)
  const [showFoods, setShowFoods] = useState(true)
  const [showHotels, setShowHotels] = useState(true)

  const mapRef = useRef(null)
  const mapInstance = useRef(null)
  const layerInstance = useRef(null)
  const markerGroupsRef = useRef({ attractions: [], foods: [], hotels: [] })

  const loadRealtimeData = async () => {
    setRealtimeLoading(true)
    try {
      const result = await getCityDetail(city, true)
      if (result.success) {
        setDetail(result)
        setTimeout(() => initMap(result.geo), 300)
      }
    } catch (err) {
      console.error('实时数据加载失败:', err)
    } finally {
      setRealtimeLoading(false)
    }
  }

  const loadForecast = async () => {
    setForecastLoading(true)
    try {
      const result = await getWeatherForecast(city)
      if (result.success) {
        setForecast(result.forecast || result.data || result)
      }
    } catch (err) {
      console.error('天气预报加载失败:', err)
    } finally {
      setForecastLoading(false)
    }
  }

  useEffect(() => {
    let isMounted = true

    const loadData = async () => {
      setLoading(true)
      try {
        const results = await Promise.allSettled([
          getCityDetail(city, true),
          getWeather(city),
          getWeatherForecast(city),
        ])

        if (!isMounted) return

        const [d, w, f] = results

        if (d.status === 'fulfilled' && d.value.success) {
          setDetail(prev => {
            if (!prev || (d.value.attractions?.length > 0)) {
              setTimeout(() => initMap(d.value.geo), 500)
              return d.value
            }
            return prev
          })
        }
        if (w.status === 'fulfilled' && w.value.success) {
          setWeather(w.value.weather)
        }
        if (f.status === 'fulfilled' && f.value.success) {
          setForecast(f.value.forecast || f.value.data || f.value)
        }
      } catch (err) {
        console.error('Data loading error:', err)
        if (isMounted) message.error('数据加载失败')
      } finally {
        if (isMounted) setLoading(false)
      }
    }

    if (city) {
      loadData()
    }

    return () => { isMounted = false }
  }, [city])

  const clearMarkerGroups = () => {
    Object.keys(markerGroupsRef.current).forEach(key => {
      markerGroupsRef.current[key].forEach(m => m.setMap(null))
      markerGroupsRef.current[key] = []
    })
  }

  const addPoiMarkers = (pois, type) => {
    if (!mapInstance.current || !pois) return
    const colorMap = {
      attractions: '#ff6b6b',
      foods: '#ffa500',
      hotels: '#4ecdc4',
    }
    const group = markerGroupsRef.current[type]
    pois.forEach((poi, idx) => {
      if (poi.lng && poi.lat) {
        const color = colorMap[type] || '#1677ff'
        const marker = new window.AMap.Marker({
          position: [poi.lng, poi.lat],
          map: mapInstance.current,
          content: `<div style="background:${color};color:white;min-width:24px;height:24px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);padding:0 6px;cursor:pointer;">${idx + 1}</div>`,
          offset: new window.AMap.Pixel(-12, -12),
        })
        marker.on('click', () => handlePoiClick(poi))
        group.push(marker)
      }
    })
  }

  const initMap = (geo) => {
    if (!window.AMap || !mapRef.current || !geo) return

    if (mapInstance.current) {
      mapInstance.current.destroy()
    }
    clearMarkerGroups()

    mapInstance.current = new window.AMap.Map(mapRef.current, {
      zoom: 12,
      center: [geo.lng, geo.lat],
      viewMode: '2D',
    })

    if (mapLayer === 'satellite') {
      layerInstance.current = new window.AMap.TileLayer.Satellite()
      mapInstance.current.add(layerInstance.current)
    }

    new window.AMap.Marker({
      position: [geo.lng, geo.lat],
      map: mapInstance.current,
      content: `<div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:6px 14px;border-radius:20px;font-weight:bold;box-shadow:0 4px 12px rgba(102,126,234,0.5);border:2px solid white;font-size:13px;">📍 ${city}</div>`,
      offset: new window.AMap.Pixel(-40, -25),
    })

    if (showAttractions && detail?.attractions) {
      addPoiMarkers(detail.attractions, 'attractions')
    }
    if (showFoods && detail?.foods) {
      addPoiMarkers(detail.foods, 'foods')
    }
    if (showHotels && detail?.hotels) {
      addPoiMarkers(detail.hotels, 'hotels')
    }
  }

  useEffect(() => {
    if (detail?.geo) {
      setTimeout(() => initMap(detail.geo), 300)
    }
  }, [activeTab, mapLayer, showAttractions, showFoods, showHotels])

  useEffect(() => {
    return () => {
      if (mapInstance.current) {
        mapInstance.current.destroy()
      }
    }
  }, [])

  const handlePoiClick = (poi) => {
    setSelectedPoi(poi)
    setPoiModalVisible(true)
  }

  const closePoiModal = () => {
    setPoiModalVisible(false)
    setSelectedPoi(null)
  }

  const renderList = (items, type) => {
    if (!items || items.length === 0) {
      return <Empty description="暂无数据" />
    }

    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {items.map((item, index) => (
          <PoiCard
            key={item.id || index}
            poi={item}
            index={index}
            type={type}
            onClick={handlePoiClick}
          />
        ))}
      </div>
    )
  }

  const renderForecastChart = (forecastData) => {
    if (!forecastData || !Array.isArray(forecastData)) return null

    const temps = forecastData.map(d => ({
      date: d.date || d.day || '',
      high: d.day_temp || d.high || d.temp_max || d.temperature?.max || 0,
      low: d.night_temp || d.low || d.temp_min || d.temperature?.min || 0,
    }))

    const maxHigh = Math.max(...temps.map(t => t.high), 1)
    const minLow = Math.min(...temps.map(t => t.low), 0)
    const range = maxHigh - minLow || 1

    return (
      <div style={{ marginTop: 16, padding: '12px 0' }}>
        <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 6 }}>
          <ArrowUpOutlined style={{ color: '#667eea' }} />
          温度趋势图
        </div>
        <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: 120, gap: 4, padding: '0 4px', borderBottom: '2px solid #e8e8e8' }}>
          {temps.map((t, idx) => {
            const highHeight = ((t.high - minLow) / range) * 90 + 10
            const lowHeight = ((t.low - minLow) / range) * 90 + 10
            return (
              <div key={idx} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100%', justifyContent: 'flex-end' }}>
                <div style={{ fontSize: 10, color: '#667eea', fontWeight: 600, marginBottom: 2 }}>{t.high}°</div>
                <div style={{ width: '70%', height: highHeight - lowHeight, background: 'linear-gradient(to top, #764ba2, #667eea)', borderRadius: '4px 4px 0 0', position: 'relative' }} />
                <div style={{ width: '70%', height: lowHeight, background: 'linear-gradient(to bottom, #764ba2, #a78bfa)', borderRadius: '0 0 4px 4px', marginTop: 2 }} />
                <div style={{ fontSize: 10, color: '#ff6b6b', fontWeight: 600, marginTop: 2 }}>{t.low}°</div>
              </div>
            )
          })}
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, gap: 4 }}>
          {temps.map((t, idx) => (
            <div key={idx} style={{ flex: 1, textAlign: 'center', fontSize: 11, color: '#666' }}>
              {t.date.slice(-2)}日
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderForecastCard = () => {
    const forecastData = forecast?.forecast || forecast?.days || forecast?.list || (Array.isArray(forecast) ? forecast : null)

    if (!forecastData || forecastData.length === 0) {
      return (
        <Card
          title={<span>📅 7天天气预报</span>}
          style={{ marginBottom: 24, borderRadius: 16 }}
          extra={<Button size="small" onClick={loadForecast} loading={forecastLoading}>刷新</Button>}
        >
          <Empty description="暂无天气预报数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        </Card>
      )
    }

    const today = forecastData[0]
    const umbrellaTip = getUmbrellaTip(today?.day_weather || today?.weather || today?.text || '')
    const sunTip = getSunProtectionTip(today?.day_weather || today?.weather || today?.text || '', today?.day_temp || today?.high || today?.temp_max || today?.temperature?.max || 25)
    const avgTemp = forecastData.reduce((s, d) => s + (d.day_temp || d.high || d.temp_max || d.temperature?.max || 20), 0) / forecastData.length

    return (
      <Card
        title={
          <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <CloudOutlined style={{ color: '#667eea' }} />
            7天天气预报
          </span>
        }
        style={{ marginBottom: 24, borderRadius: 16 }}
        extra={<Button size="small" onClick={loadForecast} loading={forecastLoading}>刷新</Button>}
      >
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'flex', gap: 8, minWidth: 'fit-content', paddingBottom: 8 }}>
            {forecastData.slice(0, 7).map((day, idx) => {
              const isToday = idx === 0
              const dayOfWeek = isToday ? '今天' : (day.weekday || ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][new Date(day.date || day.day).getDay()])
              const weatherText = day.day_weather || day.weather || day.text || day.description || ''
              const high = day.day_temp || day.high || day.temp_max || day.temperature?.max || day.max || 25
              const low = day.night_temp || day.low || day.temp_min || day.temperature?.min || day.min || 15
              const wind = day.day_wind || day.wind_direction || day.wind || ''
              const windLevel = day.day_wind_level || day.wind_power || day.wind_level || ''

              return (
                <div
                  key={idx}
                  style={{
                    flex: '0 0 auto',
                    width: 110,
                    padding: '12px 8px',
                    background: isToday ? 'linear-gradient(135deg, #f0f0ff 0%, #e6e6ff 100%)' : '#fafafa',
                    borderRadius: 12,
                    border: isToday ? '2px solid #667eea' : '1px solid #f0f0f0',
                    textAlign: 'center',
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 600, color: isToday ? '#667eea' : '#333' }}>
                    {dayOfWeek}
                  </div>
                  <div style={{ fontSize: 11, color: '#999', marginTop: 2 }}>
                    {(day.date || day.day || '').slice(5)}
                  </div>
                  <div style={{ fontSize: 32, margin: '8px 0' }}>
                    {getWeatherIcon(weatherText)}
                  </div>
                  <div style={{ fontSize: 12, color: '#555', marginBottom: 4 }}>
                    {weatherText}
                  </div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: '#ff6b6b' }}>
                    {high}°
                  </div>
                  <div style={{ fontSize: 12, color: '#667eea' }}>
                    {low}°
                  </div>
                  {(wind || windLevel) && (
                    <div style={{ fontSize: 10, color: '#888', marginTop: 4 }}>
                      💨 {wind}{windLevel ? `${windLevel}级` : ''}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {renderForecastChart(forecastData)}

        <Divider style={{ margin: '16px 0' }} />

        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 12,
            padding: '10px 14px', background: '#f6ffed', borderRadius: 10, borderLeft: '4px solid #52c41a',
          }}>
            <span style={{ fontSize: 22 }}>👔</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#389e0d' }}>穿衣建议</div>
              <div style={{ fontSize: 13, color: '#555', marginTop: 2 }}>
                {getClothingAdvice(avgTemp)}
              </div>
            </div>
          </div>

          {sunTip && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 14px', background: '#fffbe6', borderRadius: 10, borderLeft: `4px solid ${sunTip.color}`,
            }}>
              <span style={{ fontSize: 22 }}>{sunTip.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: sunTip.color }}>防晒提示</div>
                <div style={{ fontSize: 13, color: '#555', marginTop: 2 }}>{sunTip.text}</div>
              </div>
            </div>
          )}

          {umbrellaTip && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 14px', background: '#e6f7ff', borderRadius: 10, borderLeft: `4px solid ${umbrellaTip.color}`,
            }}>
              <span style={{ fontSize: 22 }}>{umbrellaTip.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: umbrellaTip.color }}>雨伞提醒</div>
                <div style={{ fontSize: 13, color: '#555', marginTop: 2 }}>{umbrellaTip.text}</div>
              </div>
            </div>
          )}
        </div>
      </Card>
    )
  }

  const renderSmartSuggestions = () => {
    const currentWeather = weather
    const forecastData = forecast?.forecast || forecast?.days || (Array.isArray(forecast) ? forecast : null)
    const firstDay = forecastData?.[0] || {}
    const weatherText = currentWeather?.weather || firstDay.weather || firstDay.text || ''
    const temp = currentWeather?.temperature || firstDay.high || firstDay.temp_max || 25

    const suggestions = getActivitySuggestion(weatherText, temp)
    const isRainy = weatherText.toLowerCase().includes('雨')
    const isHot = temp >= 32
    const seasonTip = temp >= 25 ? '夏季出游旺季，建议提前预订酒店和景点门票' :
      temp >= 15 ? '春秋季节气候宜人，是最佳出游时段' :
      temp >= 5 ? '冬季较冷，注意保暖防寒，部分景点可能关闭' : '严寒天气，建议以室内活动为主'

    return (
      <Card
        title={
          <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <BulbFilled style={{ color: '#faad14' }} />
            智能建议
          </span>
        }
        style={{ marginBottom: 24, borderRadius: 16 }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
              <span>🌳</span> 户外活动推荐
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {suggestions.outdoor.map((item, idx) => (
                <Tag
                  key={idx}
                  color="geekblue"
                  style={{
                    padding: '4px 12px',
                    borderRadius: 12,
                    fontSize: 13,
                    margin: 0,
                  }}
                >
                  {item}
                </Tag>
              ))}
            </div>
          </div>

          <div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
              <span>🏠</span> 室内活动推荐
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {suggestions.indoor.map((item, idx) => (
                <Tag
                  key={idx}
                  color="purple"
                  style={{
                    padding: '4px 12px',
                    borderRadius: 12,
                    fontSize: 13,
                    margin: 0,
                  }}
                >
                  {item}
                </Tag>
              ))}
            </div>
          </div>

          <Divider style={{ margin: '8px 0' }} />

          <div style={{
            padding: '12px 14px',
            background: 'linear-gradient(135deg, #f9f0ff 0%, #e6f7ff 100%)',
            borderRadius: 12,
            border: '1px solid #d3adf7',
          }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#764ba2', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
              <CalendarOutlined />
              最佳旅行时间提示
            </div>
            <div style={{ fontSize: 13, color: '#555', lineHeight: 1.6 }}>{seasonTip}</div>
          </div>

          {detail?.best_time && (
            <div style={{
              padding: '10px 14px', background: '#e6f7ff', borderRadius: 10, borderLeft: '4px solid #1890ff',
            }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: '#1890ff', marginBottom: 4 }}>本地推荐时间</div>
              <div style={{ fontSize: 13, color: '#555' }}>{detail.best_time}</div>
            </div>
          )}

          <div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
              <SafetyOutlined style={{ color: '#ff4d4f' }} />
              注意事项
            </div>
            <div style={{ fontSize: 13, color: '#666', lineHeight: 1.8 }}>
              {isRainy && '• 雨天路滑，注意行车安全，景点开放可能受影响\n'}
              {isHot && '• 高温天气避免长时间户外活动，多补充水分\n'}
              {temp >= 30 && '• 建议随身携带防晒用品，注意防暑降温\n'}
              {temp <= 5 && '• 天气寒冷，注意保暖防滑\n'}
              {'• 建议提前查询景点开放时间\n'}
              {'• 周末及节假日人流较大，建议错峰出行'}
            </div>
          </div>
        </div>
      </Card>
    )
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16, color: '#999' }}>正在加载城市信息...</div>
      </div>
    )
  }

  if (!detail) {
    return <Empty description="未找到该城市信息" style={{ padding: 100 }} />
  }

  const hasRealtime = detail.realtime_data && (
    (detail.realtime_data.attractions?.length > 0) ||
    (detail.realtime_data.foods?.length > 0) ||
    (detail.realtime_data.hotels?.length > 0)
  )

  return (
    <div className="page-container" style={{ padding: '24px 16px', maxWidth: 1400, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate(-1)}
        >
          返回
        </Button>

        <Space>
          <Tooltip title="分享">
            <Button icon={<ShareAltOutlined />} />
          </Tooltip>
          <Tooltip title="收藏">
            <Button icon={<HeartOutlined />} />
          </Tooltip>
        </Space>
      </div>

      <div style={{
        background: detail.image
          ? `linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%), url(${detail.image})`
          : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        borderRadius: 16,
        padding: 32,
        color: 'white',
        marginBottom: 24,
        position: 'relative',
        overflow: 'hidden',
      }}>
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
            <div>
              <Title level={1} style={{ color: 'white', margin: 0, fontSize: 42, fontWeight: 700 }}>
                {detail.city}
              </Title>

              {detail.rating > 0 && (
                <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
                  <StarFilled style={{ color: '#ffd700', fontSize: 20 }} />
                  <span style={{ fontSize: 24, fontWeight: 600 }}>{detail.rating}</span>
                  <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 14 }}>城市推荐指数</Text>
                </div>
              )}

              {detail.tags && detail.tags.length > 0 && (
                <div style={{ marginTop: 16 }}>
                  {detail.tags.map((tag, i) => (
                    <Tag key={i} style={{
                      marginBottom: 4,
                      color: 'white',
                      background: 'rgba(255,255,255,0.2)',
                      border: '1px solid rgba(255,255,255,0.3)',
                      fontSize: 13,
                      padding: '4px 12px',
                      borderRadius: 12
                    }}>
                      {tag}
                    </Tag>
                  ))}
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: 16 }}>
              {weather && (
                <div style={{
                  background: 'rgba(255,255,255,0.2)',
                  padding: 16,
                  borderRadius: 12,
                  backdropFilter: 'blur(10px)',
                  minWidth: 180
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <CloudOutlined style={{ fontSize: 24 }} />
                    <span style={{ fontSize: 24, fontWeight: 600 }}>{weather.temperature}°C</span>
                  </div>
                  <div style={{ fontSize: 14 }}>{weather.weather}</div>
                  <div style={{ fontSize: 12, opacity: 0.85, marginTop: 4 }}>
                    💨 {weather.wind_direction}风 {weather.wind_power}级
                  </div>
                  <div style={{ fontSize: 12, opacity: 0.85 }}>
                    💧 湿度 {weather.humidity}%
                  </div>
                </div>
              )}

              <div style={{
                background: 'rgba(255,255,255,0.2)',
                padding: 16,
                borderRadius: 12,
                backdropFilter: 'blur(10px)',
                minWidth: 200
              }}>
                <div style={{ fontSize: 12, opacity: 0.85, marginBottom: 8 }}>数据统计</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
                    <span>🏛️ 景点</span>
                    <span style={{ fontWeight: 600 }}>{(detail.attractions?.length || 0) + (detail.static_data?.attractions?.length || 0)}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
                    <span>🍜 美食</span>
                    <span style={{ fontWeight: 600 }}>{(detail.foods?.length || 0) + (detail.static_data?.foods?.length || 0)}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 14 }}>
                    <span>🏨 住宿</span>
                    <span style={{ fontWeight: 600 }}>{(detail.hotels?.length || 0) + (detail.static_data?.hotels?.length || 0)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {detail.description && (
            <Paragraph style={{
              marginTop: 20,
              color: 'rgba(255,255,255,0.95)',
              fontSize: 15,
              lineHeight: 1.8,
              maxWidth: 800,
              marginBottom: 0,
              background: 'rgba(255,255,255,0.1)',
              padding: 16,
              borderRadius: 12
            }}>
              {detail.description}
            </Paragraph>
          )}
        </div>
      </div>

      <Row gutter={24}>
        <Col xs={24} lg={16}>
          {renderForecastCard()}

          <Card
            title={
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span>📋 发现探索</span>
                {hasRealtime && (
                  <Tag color="success" style={{ margin: 0 }}>
                    <ThunderboltOutlined /> 含实时数据
                  </Tag>
                )}
              </div>
            }
            style={{ marginBottom: 24, borderRadius: 16 }}
            bodyStyle={{ padding: 0 }}
          >
            <Tabs
              activeKey={activeTab}
              onChange={setActiveTab}
              style={{ padding: '16px 16px 0' }}
              items={[
                {
                  key: 'attractions',
                  label: (
                    <span style={{ padding: '8px 12px' }}>
                      🏛️ 景点
                      <Tag color="red" style={{ marginLeft: 4 }}>
                        {(detail.attractions?.length || 0) + (detail.static_data?.attractions?.length || 0)}
                      </Tag>
                    </span>
                  ),
                  children: (
                    <div style={{ padding: 16 }}>
                      {renderList(
                        detail.attractions?.length > 0 ? detail.attractions : detail.static_data?.attractions,
                        'attraction'
                      )}
                    </div>
                  ),
                },
                {
                  key: 'foods',
                  label: (
                    <span style={{ padding: '8px 12px' }}>
                      🍜 美食
                      <Tag color="orange" style={{ marginLeft: 4 }}>
                        {(detail.foods?.length || 0) + (detail.static_data?.foods?.length || 0)}
                      </Tag>
                    </span>
                  ),
                  children: (
                    <div style={{ padding: 16 }}>
                      {renderList(
                        detail.foods?.length > 0 ? detail.foods : detail.static_data?.foods,
                        'food'
                      )}
                    </div>
                  ),
                },
                {
                  key: 'hotels',
                  label: (
                    <span style={{ padding: '8px 12px' }}>
                      🏨 住宿
                      <Tag color="cyan" style={{ marginLeft: 4 }}>
                        {(detail.hotels?.length || 0) + (detail.static_data?.hotels?.length || 0)}
                      </Tag>
                    </span>
                  ),
                  children: (
                    <div style={{ padding: 16 }}>
                      {renderList(
                        detail.hotels?.length > 0 ? detail.hotels : detail.static_data?.hotels,
                        'hotel'
                      )}
                    </div>
                  ),
                },
              ]}
            />
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card
            title={
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span>🗺️ 地图导航</span>
              </div>
            }
            style={{ marginBottom: 24, borderRadius: 16 }}
            bodyStyle={{ padding: 8 }}
          >
            <div style={{ padding: '8px 12px', marginBottom: 8, display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 12, color: '#666' }}>地图图层</span>
                <Segmented
                  size="small"
                  value={mapLayer}
                  onChange={(v) => setMapLayer(v)}
                  options={[
                    { label: '标准', value: 'standard' },
                    { label: '卫星', value: 'satellite' },
                  ]}
                />
              </div>
              <Divider style={{ margin: '4px 0' }} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 12, color: '#666', display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#ff6b6b' }} />
                    景点标记
                  </span>
                  <Switch size="small" checked={showAttractions} onChange={setShowAttractions} />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 12, color: '#666', display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#ffa500' }} />
                    美食标记
                  </span>
                  <Switch size="small" checked={showFoods} onChange={setShowFoods} />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 12, color: '#666', display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#4ecdc4' }} />
                    酒店标记
                  </span>
                  <Switch size="small" checked={showHotels} onChange={setShowHotels} />
                </div>
              </div>
            </div>

            <div
              ref={mapRef}
              style={{
                width: '100%',
                height: 320,
                borderRadius: 12,
                overflow: 'hidden',
                background: '#f5f5f5',
              }}
            />
            <div style={{ padding: '8px 16px' }}>
              <Text type="secondary" style={{ fontSize: 12 }}>
                点击标记查看详情，或在列表中点击卡片
              </Text>
            </div>
          </Card>

          {renderSmartSuggestions()}

          <Card style={{ borderRadius: 16 }} bodyStyle={{ padding: 20 }}>
            <Button
              type="primary"
              size="large"
              block
              icon={<SwapOutlined />}
              onClick={() => navigate(`/compare?cities=${encodeURIComponent(city)}`)}
              style={{
                borderRadius: 12,
                height: 48,
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                border: 'none',
                marginBottom: 12,
                fontSize: 14,
                fontWeight: 500,
                boxShadow: '0 4px 12px rgba(240,147,251,0.3)',
              }}
            >
              🔍 前往对比
            </Button>

            <Button
              size="large"
              block
              icon={<ThunderboltOutlined />}
              onClick={() => navigate(`/planner?city=${encodeURIComponent(city)}`)}
              style={{
                borderRadius: 12,
                height: 48,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                marginBottom: 12,
                fontSize: 14,
                fontWeight: 500,
                color: 'white',
                boxShadow: '0 4px 12px rgba(102,126,234,0.3)',
              }}
            >
              ✨ 生成行程
            </Button>

            <Button
              size="large"
              block
              icon={<ThunderboltOutlined />}
              onClick={loadRealtimeData}
              loading={realtimeLoading}
              style={{
                borderRadius: 12,
                height: 48,
                fontSize: 14,
                borderColor: '#667eea',
                color: '#667eea',
              }}
            >
              🔄 刷新实时数据
            </Button>
          </Card>
        </Col>
      </Row>

      {selectedPoi && (
        <PoiDetailModal
          visible={poiModalVisible}
          poi={selectedPoi}
          onClose={closePoiModal}
        />
      )}
    </div>
  )
}