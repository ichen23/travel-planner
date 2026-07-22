import { useState, useEffect } from 'react'
import {
  Card, Row, Col, Button, InputNumber, Select, Space, Typography,
  List, Tag, Divider, Steps, Alert, Empty, Spin, Progress, message,
  Modal, Timeline, Tooltip, Badge, Statistic, Checkbox, Input
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, ArrowUpOutlined, ArrowDownOutlined,
  ThunderboltOutlined, DollarOutlined, CalendarOutlined, EnvironmentOutlined,
  ClockCircleOutlined, CarOutlined, StarOutlined, HomeOutlined,
  CheckCircleOutlined, InfoCircleOutlined, ShoppingOutlined,
  CopyOutlined, PrinterOutlined, ShareAltOutlined,
  SwapOutlined, TeamOutlined, FilterOutlined, HeartOutlined
} from '@ant-design/icons'
import {
  getMultiCityCities, generateMultiCityItinerary, getTrainInfo, getCityAttractions
} from '../services/multiCityService'
import { getRealPoi } from '../services/mapService'

const { Text, Title } = Typography

export default function MultiCityPlanner() {
  const [loadingCities, setLoadingCities] = useState(true)
  const [availableCities, setAvailableCities] = useState([])
  const [availableCitiesFull, setAvailableCitiesFull] = useState([])
  const [selectedCities, setSelectedCities] = useState([
    { name: '', days: 2 },
    { name: '', days: 1 },
    { name: '', days: 1 }
  ])
  const [totalDays, setTotalDays] = useState(4)
  const [budget, setBudget] = useState(2000)
  const [preference, setPreference] = useState('all')
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState(null)
  const [showPacking, setShowPacking] = useState(false)
  
  const [userSelectedAttractions, setUserSelectedAttractions] = useState({})
  const [showAttractionModal, setShowAttractionModal] = useState(false)
  const [modalCity, setModalCity] = useState('')
  const [modalAttractions, setModalAttractions] = useState([])
  const [loadingAttractions, setLoadingAttractions] = useState(false)
  const [tempSelectedAttractions, setTempSelectedAttractions] = useState([])

  useEffect(() => {
    loadAvailableCities()
  }, [])

  const loadAvailableCities = async () => {
    try {
      const response = await getMultiCityCities()
      if (response.success) {
        const cities = response.cities || []
        setAvailableCities(cities.map(c => c.name))
        setAvailableCitiesFull(cities)
      }
    } catch (error) {
      message.error('加载城市列表失败')
    } finally {
      setLoadingCities(false)
    }
  }

  const handleShowAttractionSelector = async (cityName) => {
    if (!cityName) {
      message.warning('请先选择城市')
      return
    }
    
    setModalCity(cityName)
    setLoadingAttractions(true)
    setShowAttractionModal(true)
    setTempSelectedAttractions(userSelectedAttractions[cityName] || [])
    
    try {
      let attractions = []
      
      // 优先获取高德真实POI数据
      try {
        const realResponse = await getRealPoi(cityName)
        if (realResponse.success && realResponse.attractions && realResponse.attractions.length > 0) {
          attractions = realResponse.attractions.map(a => ({
            name: a.name,
            address: a.address,
            rating: a.rating,
            tags: a.type ? a.type.split(';').slice(0, 2) : []
          }))
          message.success(`已加载 ${attractions.length} 个真实景点数据`)
        }
      } catch (e) {
        console.log('真实POI获取失败，使用备用数据')
      }
      
      // 如果没有真实数据，使用备用数据
      if (attractions.length === 0) {
        const response = await getCityAttractions(cityName)
        if (response.success) {
          attractions = response.attractions || []
        }
      }
      
      setModalAttractions(attractions)
    } catch (error) {
      message.error('加载景点列表失败')
      setModalAttractions([])
    } finally {
      setLoadingAttractions(false)
    }
  }

  const handleSaveAttractions = () => {
    setUserSelectedAttractions(prev => ({
      ...prev,
      [modalCity]: tempSelectedAttractions
    }))
    setShowAttractionModal(false)
    message.success(`已为${modalCity}选择${tempSelectedAttractions.length}个景点`)
  }

  const handleAttractionToggle = (attractionName) => {
    setTempSelectedAttractions(prev => {
      if (prev.includes(attractionName)) {
        return prev.filter(name => name !== attractionName)
      } else {
        return [...prev, attractionName]
      }
    })
  }

  const getCityOptions = (excludeCities = []) => {
    return availableCitiesFull
      .filter(c => !excludeCities.includes(c.name))
      .map(c => ({
        value: c.name,
        label: (
          <span>
            {c.name}
            {c.province && <span style={{ color: '#999', marginLeft: 8, fontSize: 12 }}>({c.province})</span>}
          </span>
        ),
        searchValue: `${c.name} ${c.province || ''}`,
        rating: c.rating || 0
      }))
  }

  const handleAddCity = () => {
    setSelectedCities(prev => [...prev, { name: '', days: 1 }])
  }

  const handleRemoveCity = (index) => {
    if (selectedCities.length <= 1) {
      message.warning('至少需要保留一个城市')
      return
    }
    const cityName = selectedCities[index]?.name
    if (cityName && userSelectedAttractions[cityName]) {
      setUserSelectedAttractions(prev => {
        const newSelected = { ...prev }
        delete newSelected[cityName]
        return newSelected
      })
    }
    setSelectedCities(prev => prev.filter((_, i) => i !== index))
  }

  const handleCityChange = (index, newCity) => {
    const oldCity = selectedCities[index]?.name
    setSelectedCities(prev => {
      const newCities = [...prev]
      newCities[index] = { ...newCities[index], name: newCity }
      return newCities
    })
    
    if (oldCity && userSelectedAttractions[oldCity]) {
      setUserSelectedAttractions(prev => {
        const newSelected = { ...prev }
        if (newCity !== oldCity) {
          delete newSelected[oldCity]
        }
        return newSelected
      })
    }
  }

  const handleDaysChange = (index, newDays) => {
    setSelectedCities(prev => {
      const newCities = [...prev]
      newCities[index] = { ...newCities[index], days: Math.max(1, newDays) }
      updateTotalDays(newCities)
      return newCities
    })
  }

  const handleMoveUp = (index) => {
    if (index === 0) return
    setSelectedCities(prev => {
      const newCities = [...prev]
      ;[newCities[index - 1], newCities[index]] = [newCities[index], newCities[index - 1]]
      return newCities
    })
  }

  const handleMoveDown = (index) => {
    if (index === selectedCities.length - 1) return
    setSelectedCities(prev => {
      const newCities = [...prev]
      ;[newCities[index], newCities[index + 1]] = [newCities[index + 1], newCities[index]]
      return newCities
    })
  }

  const updateTotalDays = (cities) => {
    const total = cities.reduce((sum, c) => sum + c.days, 0)
    setTotalDays(total)
  }

  const handleGenerate = async () => {
    const cityNames = selectedCities.map(c => c.name).filter(n => n)
    const dayAllocation = selectedCities.map(c => c.days)

    if (cityNames.length < 2) {
      message.warning('请至少选择2个城市')
      return
    }

    if (cityNames.some(name => !name)) {
      message.warning('请填写所有城市')
      return
    }

    if (new Set(cityNames).size !== cityNames.length) {
      message.warning('不能选择重复的城市')
      return
    }

    setGenerating(true)
    try {
      const validUserAttractions = {}
      Object.entries(userSelectedAttractions).forEach(([city, attractions]) => {
        if (cityNames.includes(city) && attractions.length > 0) {
          validUserAttractions[city] = attractions
        }
      })

      const response = await generateMultiCityItinerary(
        cityNames,
        dayAllocation,
        totalDays,
        budget,
        preference,
        Object.keys(validUserAttractions).length > 0 ? validUserAttractions : null
      )

      if (response.success) {
        setResult(response)
        message.success('行程生成成功！')
      } else {
        message.error(response.message || '生成失败')
      }
    } catch (error) {
      message.error('生成行程失败: ' + (error.response?.data?.detail || error.message))
    } finally {
      setGenerating(false)
    }
  }

  const handlePrint = () => {
    window.print()
  }

  const handleCopy = () => {
    if (!result) return
    
    let text = `【${result.cities.join(' → ')}】${result.total_days}天行程\n\n`
    
    if (result.transfer_segments?.length) {
      text += "📦 交通安排\n"
      result.transfer_segments.forEach(seg => {
        text += `${seg.from_city} → ${seg.to_city}: ${seg.train_number} ${seg.departure}-${seg.arrival} ${seg.duration_text}\n`
      })
      text += "\n"
    }
    
    text += "📅 详细行程\n"
    result.days.forEach(day => {
      text += `\n【${day.date_label} - ${day.city}】\n`
      day.schedule.forEach(item => {
        const icon = item.type === 'attraction' ? '🏛️' : item.type === 'food' ? '🍜' : '🚇'
        text += `${icon} ${item.start_time}-${item.end_time} ${item.name}`
        if (item.ticket) text += ` (${item.ticket})`
        text += `\n`
        if (item.tips) text += `   💡 ${item.tips}\n`
      })
    })
    
    if (result.budget_breakdown) {
      text += `\n💰 预算总计: ¥${result.total_budget}\n`
    }
    
    navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  }

  const getTransportIcon = (type) => {
    const icons = {
      '高铁': '🚄',
      '动车': '🚅',
      '普通列车': '🚆',
      '航空': '✈️',
      '大巴': '🚌'
    }
    return icons[type] || '🚇'
  }

  const renderCitySelector = () => {
    const usedCities = selectedCities.map(c => c.name).filter(n => n)
    const cityOptions = getCityOptions(usedCities)

    return (
      <Card 
        title={
          <Space>
            <TeamOutlined />
            <span>选择城市 ({selectedCities.length}个) - 共 {availableCities.length} 个城市支持</span>
          </Space>
        }
        extra={
          <Button
            icon={<PlusOutlined />}
            onClick={handleAddCity}
          >
            添加城市
          </Button>
        }
        style={{ marginBottom: 16 }}
      >
        {loadingCities ? (
          <Spin />
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div style={{ 
              padding: '12px 16px', 
              background: '#e6f7ff', 
              border: '1px solid #91d5ff', 
              borderRadius: 8,
              fontSize: 14
            }}>
              💡 提示：可以通过输入城市名称或省份来快速搜索，如"杭州"或"浙江"
            </div>
            
            {selectedCities.map((city, index) => {
              const selectedCount = userSelectedAttractions[city.name]?.length || 0
              return (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    padding: '12px 16px',
                    background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
                    borderRadius: 12,
                    border: '2px solid transparent',
                    borderColor: index === 0 ? '#1890ff' : index === selectedCities.length - 1 ? '#52c41a' : '#faad14',
                  }}
                >
                  <div style={{ fontSize: 24, fontWeight: 'bold', color: '#666', minWidth: 30 }}>
                    {index + 1}
                  </div>
                  
                  <Select
                    value={city.name || undefined}
                    onChange={(val) => handleCityChange(index, val)}
                    style={{ flex: 1, minWidth: 200 }}
                    showSearch
                    placeholder="搜索城市名称或省份..."
                    filterOption={(input, option) => {
                      const searchVal = option.searchValue || ''
                      return searchVal.toLowerCase().includes(input.toLowerCase())
                    }}
                    optionFilterProp="searchValue"
                    listHeight={300}
                  >
                    {cityOptions.map(c => (
                      <Select.Option 
                        key={c.value} 
                        value={c.value}
                        searchValue={c.searchValue}
                      >
                        {c.label}
                      </Select.Option>
                    ))}
                  </Select>

                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <CalendarOutlined style={{ color: '#1890ff' }} />
                    <InputNumber
                      min={1}
                      max={10}
                      value={city.days}
                      onChange={(val) => handleDaysChange(index, val)}
                      addonAfter="天"
                      style={{ width: 100 }}
                    />
                  </div>

                  <Tooltip title={city.name ? "选择必去景点" : "请先选择城市"}>
                    <Button 
                      icon={<HeartOutlined />}
                      onClick={() => handleShowAttractionSelector(city.name)}
                      disabled={!city.name}
                      type={selectedCount > 0 ? "primary" : "default"}
                    >
                      {selectedCount > 0 ? `已选${selectedCount}个` : "选景点"}
                    </Button>
                  </Tooltip>

                  <Space>
                    <Tooltip title="上移">
                      <Button 
                        icon={<ArrowUpOutlined />} 
                        onClick={() => handleMoveUp(index)}
                        disabled={index === 0}
                      />
                    </Tooltip>
                    <Tooltip title="下移">
                      <Button 
                        icon={<ArrowDownOutlined />} 
                        onClick={() => handleMoveDown(index)}
                        disabled={index === selectedCities.length - 1}
                      />
                    </Tooltip>
                    <Tooltip title="删除">
                      <Button 
                        danger 
                        icon={<DeleteOutlined />} 
                        onClick={() => handleRemoveCity(index)}
                        disabled={selectedCities.length <= 1}
                      />
                    </Tooltip>
                  </Space>
                </div>
              )
            })}

            {selectedCities.length === 0 && (
              <Empty 
                description="还没有选择城市，点击上方添加按钮开始选择" 
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
            )}
          </div>
        )}
      </Card>
    )
  }

  const renderAttractionModal = () => (
    <Modal
      title={
        <Space>
          <HeartOutlined />
          <span>为 {modalCity} 选择必去景点</span>
        </Space>
      }
      open={showAttractionModal}
      onCancel={() => setShowAttractionModal(false)}
      onOk={handleSaveAttractions}
      okText="保存选择"
      cancelText="取消"
      width={600}
    >
      {loadingAttractions ? (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Spin />
          <div style={{ marginTop: 16 }}>加载景点列表中...</div>
        </div>
      ) : modalAttractions.length === 0 ? (
        <Alert
          message="暂无景点数据"
          description="该城市暂无详细景点数据，系统将为您智能推荐"
          type="info"
          showIcon
        />
      ) : (
        <div>
          <div style={{ marginBottom: 16 }}>
            <Alert
              message="提示：选择您感兴趣的景点，系统会将这些景点安排到行程中，其他时间会自动安排美食和交通"
              type="info"
              showIcon
            />
          </div>
          
          <div style={{ marginBottom: 12 }}>
            <Text strong>已选择 {tempSelectedAttractions.length} 个景点</Text>
          </div>
          
          <List
            size="small"
            dataSource={modalAttractions}
            renderItem={(attraction) => {
              const isSelected = tempSelectedAttractions.includes(attraction.name)
              return (
                <List.Item>
                  <Checkbox
                    checked={isSelected}
                    onChange={() => handleAttractionToggle(attraction.name)}
                  >
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                      <Text strong>
                        {attraction.name}
                        {attraction.rating && (
                          <StarOutlined style={{ color: '#faad14', marginLeft: 8 }} />
                        )}
                      </Text>
                      <div style={{ fontSize: 12, color: '#666' }}>
                        {attraction.ticket && attraction.ticket !== '免费' && (
                          <Tag color="orange">¥{attraction.ticket}</Tag>
                        )}
                        {attraction.ticket === '免费' && (
                          <Tag color="green">免费</Tag>
                        )}
                        {attraction.best_period && (
                          <Tag color="blue">
                            {attraction.best_period === 'morning' ? '上午' : 
                             attraction.best_period === 'afternoon' ? '下午' : '晚上'}
                          </Tag>
                        )}
                        {attraction.duration_hours && (
                          <Tag>{attraction.duration_hours}小时</Tag>
                        )}
                      </div>
                      {attraction.tags && attraction.tags.length > 0 && (
                        <div style={{ marginTop: 4 }}>
                          {attraction.tags.map(tag => (
                            <Tag key={tag} style={{ marginBottom: 2 }}>{tag}</Tag>
                          ))}
                        </div>
                      )}
                      {attraction.tips && (
                        <div style={{ fontSize: 12, color: '#999', marginTop: 2 }}>
                          💡 {attraction.tips}
                        </div>
                      )}
                    </div>
                  </Checkbox>
                </List.Item>
              )
            }}
          />
        </div>
      )}
    </Modal>
  )

  const renderSettingsPanel = () => (
    <Card 
      title={<Space><DollarOutlined />预算设置</Space>}
      style={{ marginBottom: 16 }}
    >
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <div style={{ marginBottom: 12 }}>
            <Text>总天数: <Text strong style={{ color: '#1890ff' }}>{totalDays}</Text> 天</Text>
          </div>
          <div>
            <Text>总预算: </Text>
            <InputNumber
              min={500}
              max={50000}
              step={500}
              value={budget}
              onChange={setBudget}
              formatter={value => `¥ ${value}`}
              parser={value => value.replace(/¥\s?|(,*)/g, '')}
              style={{ width: 150 }}
            />
          </div>
        </Col>
        <Col span={12}>
          <div style={{ marginBottom: 12 }}>
            <Text>日均预算: <Text strong style={{ color: '#52c41a' }}>¥{Math.floor(budget / totalDays)}</Text>/天</Text>
          </div>
          <div>
            <Text>偏好: </Text>
            <Select
              value={preference}
              onChange={setPreference}
              style={{ width: 150 }}
            >
              <Select.Option value="all">综合推荐</Select.Option>
              <Select.Option value="history">历史文化</Select.Option>
              <Select.Option value="nature">自然风光</Select.Option>
              <Select.Option value="food">美食之旅</Select.Option>
              <Select.Option value="shopping">购物休闲</Select.Option>
            </Select>
          </div>
        </Col>
      </Row>
      
      {Object.keys(userSelectedAttractions).length > 0 && (
        <>
          <Divider />
          <Alert
            message={
              <Space>
                <HeartOutlined style={{ color: '#ff4d4f' }} />
                <span>已为以下城市选择必去景点:</span>
              </Space>
            }
            description={
              <div>
                {Object.entries(userSelectedAttractions).map(([city, attractions]) => (
                  <div key={city} style={{ marginBottom: 4 }}>
                    <Tag color="blue">{city}</Tag>
                    <span style={{ marginLeft: 8 }}>
                      {attractions.join('、')}
                    </span>
                  </div>
                ))}
              </div>
            }
            type="info"
            showIcon={false}
            style={{ marginBottom: 16 }}
          />
        </>
      )}
      
      <Divider />
      
      <Button
        type="primary"
        size="large"
        icon={<ThunderboltOutlined />}
        onClick={handleGenerate}
        loading={generating}
        block
        style={{ height: 50, fontSize: 16 }}
      >
        {generating ? '正在生成详细行程...' : '✨ 生成详细行程'}
      </Button>
    </Card>
  )

  const renderTransportCard = (seg) => (
    <Card
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        marginBottom: 16
      }}
      bodyStyle={{ padding: 24 }}
    >
      <div style={{ textAlign: 'center', marginBottom: 16 }}>
        <Text style={{ color: 'rgba(255,255,255,0.9)' }}>🚄 交通安排</Text>
      </div>
      
      <div style={{ position: 'relative' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div style={{ fontSize: 28, fontWeight: 'bold' }}>{seg.from_city}</div>
            <div style={{ fontSize: 14, opacity: 0.8 }}>{seg.departure}</div>
          </div>
          
          <div style={{ flex: 1 }}>
            <div style={{ 
              height: 2, 
              background: 'rgba(255,255,255,0.3)', 
              position: 'relative',
              margin: '0 20px'
            }}>
              <CarOutlined style={{ position: 'absolute', left: '45%', top: -12, fontSize: 24 }} />
            </div>
            <div style={{ textAlign: 'center', marginTop: 16, fontSize: 14, opacity: 0.9 }}>
              {seg.train_number}次 · {seg.duration_text}
            </div>
          </div>
          
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div style={{ fontSize: 28, fontWeight: 'bold' }}>{seg.to_city}</div>
            <div style={{ fontSize: 14, opacity: 0.8 }}>{seg.arrival}</div>
          </div>
        </div>
        
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: 32, 
          marginTop: 24,
          fontSize: 14 
        }}>
          <div>
            <DollarOutlined /> ¥{seg.price}
          </div>
          <div>
            <InfoCircleOutlined /> {seg.type || '高铁'}
          </div>
        </div>
      </div>
    </Card>
  )

  const getTypeIcon = (type) => {
    const icons = {
      'attraction': '🏛️',
      'food': '🍜',
      'transport': '🚇',
      'routine': '🌅',
      'rest': '☕',
      'entertainment': '🌆'
    }
    return icons[type] || '📍'
  }

  const getTypeColor = (type) => {
    const colors = {
      'attraction': 'blue',
      'food': 'green',
      'transport': 'orange',
      'routine': 'cyan',
      'rest': 'purple',
      'entertainment': 'magenta'
    }
    return colors[type] || 'default'
  }

  const renderDaySchedule = (day, dayIndex) => (
    <Card
      key={dayIndex}
      style={{ marginBottom: 16 }}
      title={
        <Space>
          <Badge 
            count={dayIndex + 1} 
            style={{ backgroundColor: dayIndex === 0 ? '#1890ff' : '#52c41a' }}
          />
          <Title level={4} style={{ margin: 0 }}>{day.city}</Title>
          <Tag color="blue">{day.date_label}</Tag>
          {day.is_transfer_day && <Tag color="orange">中转日</Tag>}
        </Space>
      }
    >
      {day.hotel_recommendation && (
        <Alert
          message={<Space><HomeOutlined />🏨 酒店推荐：{day.hotel_recommendation}</Space>}
          type="success"
          showIcon={false}
          style={{ marginBottom: 16 }}
        />
      )}
      
      {day.transport_tips && (
        <Alert
          message={<Space><CarOutlined />🚗 交通提示：{day.transport_tips}</Space>}
          type="info"
          showIcon={false}
          style={{ marginBottom: 16 }}
        />
      )}
      
      {day.morning_foods && day.morning_foods.length > 0 && (
        <Alert
          message={<Space><StarOutlined />🍽️ 当地美食：{day.morning_foods.join('、')}</Space>}
          type="warning"
          showIcon={false}
          style={{ marginBottom: 16 }}
        />
      )}
      
      <Timeline
        style={{ padding: '8px 0' }}
        items={day.schedule.map((item, idx) => ({
          color: getTypeColor(item.type),
          dot: <span style={{ fontSize: 16 }}>{item.icon || getTypeIcon(item.type)}</span>,
          children: (
            <div style={{ padding: '8px 0' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                <ClockCircleOutlined style={{ color: '#666' }} />
                <Text strong>{item.start_time}{item.end_time ? ` - ${item.end_time}` : ''}</Text>
                {item.duration_minutes && (
                  <Tag color="default">{item.duration_minutes}分钟</Tag>
                )}
                {item.ticket && item.ticket !== '免费' && (
                  <Tag color="orange">💰 {item.ticket}</Tag>
                )}
                {item.ticket === '免费' && (
                  <Tag color="green">🎉 免费</Tag>
                )}
                {item.rating && item.rating >= 4 && (
                  <Tag color="gold">⭐ {item.rating}</Tag>
                )}
              </div>
              
              <div style={{ fontSize: 16, fontWeight: 500, marginBottom: 4 }}>
                {item.name}
              </div>
              
              {item.description && (
                <div style={{ 
                  color: '#333', 
                  fontSize: 14, 
                  marginTop: 4,
                  padding: '8px 12px',
                  background: '#f0f5ff',
                  borderRadius: 4
                }}>
                  📖 {item.description}
                </div>
              )}
              
              {item.best_visit_time && (
                <div style={{ color: '#1890ff', fontSize: 14, marginTop: 4 }}>
                  ⏰ 最佳游玩时间：{item.best_visit_time}
                </div>
              )}
              
              {item.visit_duration && (
                <div style={{ color: '#52c41a', fontSize: 14, marginTop: 2 }}>
                  🕐 建议游玩时长：{item.visit_duration}
                </div>
              )}
              
              {item.open_hours && (
                <div style={{ color: '#722ed1', fontSize: 14, marginTop: 2 }}>
                  📅 开放时间：{item.open_hours}
                </div>
              )}
              
              {item.location && (
                <div style={{ color: '#666', fontSize: 14, marginTop: 4 }}>
                  📍 {item.location}
                </div>
              )}
              
              {item.recommend && (
                <div style={{ color: '#1890ff', fontSize: 14, marginTop: 4 }}>
                  推荐: {item.recommend}
                </div>
              )}
              
              {item.tags && item.tags.length > 0 && (
                <div style={{ marginTop: 4 }}>
                  {item.tags.map(tag => (
                    <Tag key={tag} style={{ marginBottom: 2 }}>{tag}</Tag>
                  ))}
                </div>
              )}
              
              {item.tips && (
                <div style={{ 
                  marginTop: 8, 
                  padding: '8px 12px', 
                  background: '#fffbe6', 
                  borderRadius: 4,
                  fontSize: 13,
                  color: '#d48806',
                  borderLeft: '3px solid #faad14'
                }}>
                  💡 {item.tips}
                </div>
              )}
            </div>
          )
        }))}
      />
      
      {day.city_tips && (
        <div style={{ 
          marginTop: 16, 
          padding: '12px 16px', 
          background: '#e6f7ff', 
          borderRadius: 8,
          border: '1px solid #91d5ff'
        }}>
          <InfoCircleOutlined style={{ color: '#1890ff', marginRight: 8 }} />
          <strong>{day.city}旅游小贴士：</strong> {day.city_tips}
        </div>
      )}
    </Card>
  )

  const renderBudgetSection = () => (
    <Card
      title={<Space><DollarOutlined />预算明细</Space>}
      style={{ marginBottom: 16 }}
    >
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Statistic
            title="总预算"
            value={result.total_budget}
            precision={0}
            prefix="¥"
            valueStyle={{ color: '#1890ff' }}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="交通费用"
            value={result.budget_breakdown?.transport || 0}
            precision={0}
            prefix="¥"
            valueStyle={{ color: '#722ed1' }}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="住宿费用"
            value={result.budget_breakdown?.accommodation || 0}
            precision={0}
            prefix="¥"
            valueStyle={{ color: '#52c41a' }}
          />
        </Col>
        <Col span={6}>
          <Statistic
            title="餐饮费用"
            value={result.budget_breakdown?.food || 0}
            precision={0}
            prefix="¥"
            valueStyle={{ color: '#fa8c16' }}
          />
        </Col>
      </Row>
      
      <Divider />
      
      <Title level={5}>各城市预算分配</Title>
      <Row gutter={[16, 16]}>
        {Object.entries(result.city_budgets || {}).map(([city, cityBudget]) => (
          <Col key={city} span={8}>
            <Card size="small" title={city}>
              <div>🎫 门票: ¥{cityBudget.ticket}</div>
              <div>🍜 餐饮: ¥{cityBudget.food}</div>
              <div>🚕 交通: ¥{cityBudget.local_transport}</div>
              {cityBudget.ticket_attractions?.length > 0 && (
                <div style={{ marginTop: 8 }}>
                  <div style={{ fontSize: 12, color: '#666' }}>主要门票:</div>
                  {cityBudget.ticket_attractions.slice(0, 3).map(t => (
                    <div key={t.name} style={{ fontSize: 12 }}>
                      - {t.name}: ¥{t.ticket}
                    </div>
                  ))}
                </div>
              )}
              <div style={{ marginTop: 8, fontWeight: 'bold' }}>
                合计: ¥{cityBudget.total}
              </div>
            </Card>
          </Col>
        ))}
      </Row>
    </Card>
  )

  const renderTipsSection = () => (
    <Card
      title={<Space><InfoCircleOutlined />实用贴士</Space>}
      style={{ marginBottom: 16 }}
    >
      <List
        dataSource={result.tips || []}
        renderItem={(tip, idx) => (
          <List.Item>
            <Text>
              <Tag color="blue">{idx + 1}</Tag>
              {tip}
            </Text>
          </List.Item>
        )}
      />
    </Card>
  )

  const renderResult = () => (
    <div>
      <Card
        title={
          <Space>
            <SwapOutlined />
            <span>行程总览: {result.cities.join(' → ')}</span>
            <Tag color="blue">{result.total_days}天</Tag>
            <Tag color="green">¥{result.total_budget}</Tag>
          </Space>
        }
        extra={
          <Space>
            <Button icon={<CopyOutlined />} onClick={handleCopy}>
              复制行程
            </Button>
            <Button icon={<PrinterOutlined />} onClick={handlePrint}>
              打印
            </Button>
            <Button icon={<ShoppingOutlined />} onClick={() => setShowPacking(true)}>
              打包建议
            </Button>
          </Space>
        }
        style={{ marginBottom: 16 }}
      >
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 16 }}>
          <Steps
            current={result.cities.length - 1}
            items={result.cities.map(city => ({
              title: city,
              icon: <HomeOutlined />
            }))}
          />
        </div>
      </Card>

      {result.transfer_segments?.length > 0 && (
        <Title level={4} style={{ marginTop: 24 }}>🚄 城市间交通</Title>
      )}
      {result.transfer_segments?.map((seg, idx) => renderTransportCard(seg))}

      <Title level={4} style={{ marginTop: 24 }}>📅 每日详细安排</Title>
      {result.days?.map((day, idx) => renderDaySchedule(day, idx))}

      {renderBudgetSection()}
      {renderTipsSection()}
    </div>
  )

  return (
    <div style={{ padding: '24px 32px', maxWidth: 1200, margin: '0 auto' }}>
      <Title level={2}>
        <SwapOutlined /> 多城市行程规划
      </Title>
      <Text type="secondary">
        选择多个城市，指定必去景点，系统会自动生成包含城市间交通、每日景点安排、美食推荐、预算明细的完整行程
      </Text>
      
      <Divider />
      
      {renderCitySelector()}
      {renderSettingsPanel()}

      {generating ? (
        <Card style={{ textAlign: 'center', padding: 60 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16, fontSize: 18 }}>正在生成详细行程...</div>
          <Progress percent={60} status="active" style={{ maxWidth: 400, margin: '16px auto' }} />
        </Card>
      ) : result ? (
        renderResult()
      ) : (
        <Card style={{ textAlign: 'center', padding: 40 }}>
          <Empty
            description={
              <span style={{ fontSize: 16 }}>
                选择城市并点击"生成详细行程"开始规划您的旅行！
              </span>
            }
          />
        </Card>
      )}

      <Modal
        title={
          <Space>
            <ShoppingOutlined />
            <span>打包建议</span>
          </Space>
        }
        open={showPacking}
        onCancel={() => setShowPacking(false)}
        footer={null}
        width={600}
      >
        {result?.packing_list && (
          <div>
            <Title level={5}>✅ 必带物品</Title>
            <List
              size="small"
              dataSource={result.packing_list['必带物品'] || []}
              renderItem={item => <List.Item>{item}</List.Item>}
            />
            
            {result.packing_list && result.packing_list["季节推荐"]?.length > 0 && (
              <Title level={5} style={{ marginTop: 16 }}>
                ☀️ 季节推荐
              </Title>
            )}
            {result.packing_list && result.packing_list["季节推荐"]?.length > 0 && (
              <List
                size="small"
                dataSource={result.packing_list["季节推荐"]}
                renderItem={(item) => <List.Item>{item}</List.Item>}
              />
            )}
            
            {result.packing_list && result.packing_list["可选物品"]?.length > 0 && (
              <Title level={5} style={{ marginTop: 16 }}>
                🎒 可选物品
              </Title>
            )}
            {result.packing_list && result.packing_list["可选物品"]?.length > 0 && (
              <List
                size="small"
                dataSource={result.packing_list["可选物品"]}
                renderItem={(item) => <List.Item>{item}</List.Item>}
              />
            )}
          </div>
        )}
      </Modal>

      {renderAttractionModal()}
    </div>
  )
}
