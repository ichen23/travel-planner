import { useState, useRef, useEffect } from 'react'
import { Row, Col, Card, Typography, Button, Select, Tag, Space, message, Spin, Divider, Rate, Progress, Empty, Table, Tooltip, Badge, Statistic, List } from 'antd'
import { ArrowLeftOutlined, PlusOutlined, DeleteOutlined, ThunderboltOutlined, StarFilled, EnvironmentOutlined, CrownOutlined, TrophyOutlined, ArrowUpOutlined, FallOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import * as echarts from 'echarts'
import api from '../services/api'
import { HOT_CITIES } from '../utils/constants'

const { Title, Text } = Typography

const COMPARE_COLORS = ['#1677ff', '#52c41a', '#faad14', '#eb2f96']

const WIND_DIRECTIONS = {
  N: '北风',
  S: '南风',
  E: '东风',
  W: '西风',
  NE: '东北风',
  NW: '西北风',
  SE: '东南风',
  SW: '西南风',
}

export default function ComparePage() {
  const navigate = useNavigate()
  const [selectedCities, setSelectedCities] = useState(['北京', '上海'])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [chartData, setChartData] = useState(null)
  
  const radarChartRef = useRef(null)
  const barChartRef = useRef(null)
  const radarChartInstance = useRef(null)
  const barChartInstance = useRef(null)

  const addCity = () => {
    if (selectedCities.length >= 4) {
      message.warning('最多只能选择4个城市')
      return
    }
    setSelectedCities([...selectedCities, ''])
  }

  const removeCity = (index) => {
    if (selectedCities.length <= 2) {
      message.warning('至少需要2个城市进行对比')
      return
    }
    setSelectedCities(selectedCities.filter((_, i) => i !== index))
  }

  const updateCity = (index, value) => {
    const newCities = [...selectedCities]
    newCities[index] = value
    setSelectedCities(newCities)
  }

  const handleCompare = async () => {
    const validCities = selectedCities.filter(city => city && city.trim())
    
    if (validCities.length < 2) {
      message.warning('请至少选择2个城市')
      return
    }
    
    setLoading(true)
    setResult(null)
    
    try {
      const response = await api.post('/destination/compare-cities', { cities: validCities })
      
      if (response.success) {
        setResult(response)
        setChartData(response.cities)
        message.success('对比完成')
      } else {
        message.error(response.message || '对比失败')
      }
    } catch (err) {
      console.error('对比城市失败:', err)
      message.error('对比城市失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (chartData && chartData.length > 0) {
      initRadarChart()
      initBarChart()
    }
    
    return () => {
      if (radarChartInstance.current) {
        radarChartInstance.current.dispose()
      }
      if (barChartInstance.current) {
        barChartInstance.current.dispose()
      }
    }
  }, [chartData])

  useEffect(() => {
    const handleResize = () => {
      radarChartInstance.current?.resize()
      barChartInstance.current?.resize()
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const initRadarChart = () => {
    if (!radarChartRef.current || !chartData) return
    
    if (radarChartInstance.current) {
      radarChartInstance.current.dispose()
    }
    
    radarChartInstance.current = echarts.init(radarChartRef.current)
    
    const indicators = [
      { name: '景点评分', max: 5 },
      { name: '美食评分', max: 5 },
      { name: '酒店评分', max: 5 },
      { name: '性价比', max: 100 },
      { name: '气候', max: 100 },
      { name: '特色', max: 100 },
    ]
    
    const seriesData = chartData.map((city, index) => {
      const priceScore = city.stats.avg_hotel_price > 0 
        ? Math.max(0, 100 - (city.stats.avg_hotel_price / 10))
        : 50
      
      const weatherScore = city.weather.best_temp 
        ? (city.weather.best_temp >= 18 && city.weather.best_temp <= 28 ? 100 : 
           city.weather.best_temp >= 10 && city.weather.best_temp <= 32 ? 70 : 40)
        : 50
      
      const tagScore = Math.min(100, (city.tags?.length || 0) * 20)
      
      return {
        value: [
          city.stats.avg_attraction_rating * 20 || 0,
          city.stats.avg_food_rating * 20 || 0,
          city.stats.avg_hotel_rating * 20 || 0,
          priceScore,
          weatherScore,
          tagScore,
        ],
        name: city.name,
        itemStyle: { color: COMPARE_COLORS[index] }
      }
    })
    
    radarChartInstance.current.setOption({
      tooltip: { trigger: 'item' },
      legend: {
        data: chartData.map(c => c.name),
        bottom: 0
      },
      radar: {
        indicator: indicators,
        center: ['50%', '50%'],
        radius: '60%',
        axisName: { color: '#666' }
      },
      series: [{
        type: 'radar',
        data: seriesData,
        areaStyle: { opacity: 0.2 }
      }]
    })
  }

  const initBarChart = () => {
    if (!barChartRef.current || !chartData) return
    
    if (barChartInstance.current) {
      barChartInstance.current.dispose()
    }
    
    barChartInstance.current = echarts.init(barChartRef.current)
    
    const metrics = [
      { key: 'stats.attraction_count', label: '景点数量' },
      { key: 'stats.food_count', label: '美食数量' },
      { key: 'stats.hotel_count', label: '酒店数量' },
    ]
    
    const seriesData = metrics.map((metric, metricIndex) => ({
      name: metric.label,
      type: 'bar',
      data: chartData.map(city => {
        const keys = metric.key.split('.')
        let val = city
        for (const k of keys) val = val?.[k]
        return val || 0
      }),
      itemStyle: { 
        color: ['#1677ff', '#52c41a', '#faad14'][metricIndex],
        borderRadius: [4, 4, 0, 0]
      }
    }))
    
    barChartInstance.current.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      legend: { bottom: 0 },
      grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
      xAxis: {
        type: 'category',
        data: chartData.map(c => c.name),
        axisLabel: { color: '#666' }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#666' }
      },
      series: seriesData
    })
  }

  const renderCitySelector = () => (
    <Card 
      style={{ borderRadius: 12, marginBottom: 24 }}
      title={
        <Space>
          <ThunderboltOutlined style={{ color: '#1677ff' }} />
          <span>选择对比城市</span>
        </Space>
      }
      extra={
        <Button 
          type="primary" 
          icon={<ThunderboltOutlined />} 
          onClick={handleCompare}
          loading={loading}
          disabled={selectedCities.filter(c => c).length < 2}
          style={{ 
            borderRadius: 8,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none'
          }}
        >
          开始对比
        </Button>
      }
    >
      <Row gutter={[16, 16]}>
        {selectedCities.map((city, index) => (
          <Col xs={24} sm={12} md={8} lg={6} key={index}>
            <div style={{ 
              display: 'flex', 
              gap: 8,
              alignItems: 'center',
              padding: '8px 12px',
              background: COMPARE_COLORS[index] + '15',
              borderRadius: 8,
              border: `2px solid ${COMPARE_COLORS[index]}`
            }}>
              <div style={{
                width: 24,
                height: 24,
                borderRadius: 12,
                background: COMPARE_COLORS[index],
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 12,
                fontWeight: 'bold',
                flexShrink: 0
              }}>
                {index + 1}
              </div>
              <Select
                value={city || undefined}
                onChange={value => updateCity(index, value)}
                placeholder="选择城市"
                style={{ flex: 1 }}
                showSearch
                optionFilterProp="label"
                options={HOT_CITIES.filter(c => !selectedCities.includes(c) || c === city).map(c => ({
                  value: c,
                  label: c
                }))}
              />
              {selectedCities.length > 2 && (
                <Button
                  type="text"
                  danger
                  icon={<DeleteOutlined />}
                  onClick={() => removeCity(index)}
                />
              )}
            </div>
          </Col>
        ))}
      </Row>
      
      {selectedCities.length < 4 && (
        <Button 
          icon={<PlusOutlined />} 
          onClick={addCity}
          style={{ marginTop: 16, borderRadius: 8 }}
        >
          添加城市 (最多4个)
        </Button>
      )}
    </Card>
  )

  const renderComparisonTable = () => {
    if (!result?.comparison) return null
    
    const { dimensions } = result.comparison
    
    return (
      <Card 
        title={
          <Space>
            <ArrowUpOutlined style={{ color: '#52c41a' }} />
            <span>对比详情</span>
          </Space>
        }
        style={{ borderRadius: 12, marginBottom: 24 }}
      >
        <Table
          dataSource={dimensions.map((dim, index) => ({
            key: index,
            label: dim.label,
            ...Object.fromEntries(dim.values.map(v => [v.city, v]))
          }))}
          pagination={false}
          size="middle"
          bordered
          columns={[
            {
              title: '对比维度',
              dataIndex: 'label',
              width: 120,
              fixed: 'left',
              render: text => <Text strong>{text}</Text>
            },
            ...selectedCities.filter(c => c).map((city, index) => ({
              title: (
                <Space>
                  <div style={{
                    width: 12,
                    height: 12,
                    borderRadius: 6,
                    background: COMPARE_COLORS[index]
                  }} />
                  {city}
                </Space>
              ),
              dataIndex: city,
              render: (value) => {
                if (!value) return '-'
                const { val, is_winner } = value
                const displayVal = typeof val === 'number' 
                  ? (dimensions[0]?.values?.[0]?.city === city && dimensions[0]?.label === '人均消费' 
                      ? `¥${val}` 
                      : dimensions[0]?.label === '酒店均价' 
                        ? `¥${val}`
                        : dimensions[0]?.label === '平均气温'
                          ? `${val}°C`
                          : val.toFixed(1))
                  : val
                
                return (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 8,
                    fontWeight: is_winner ? 600 : 400,
                    color: is_winner ? '#52c41a' : '#333'
                  }}>
                    {displayVal}
                    {is_winner && <CrownOutlined style={{ color: '#faad14' }} />}
                  </div>
                )
              }
            }))
          ]}
        />
      </Card>
    )
  }

  const renderCityCards = () => {
    if (!result?.cities) return null
    
    return (
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        {result.cities.map((city, index) => (
          <Col xs={24} sm={12} md={result.cities.length <= 3 ? 8 : 6} key={city.name}>
            <Card 
              style={{ 
                borderRadius: 12,
                border: `2px solid ${COMPARE_COLORS[index]}`,
                position: 'relative',
                overflow: 'hidden'
              }}
              bodyStyle={{ padding: 16 }}
            >
              {result.recommendation && result.recommendation.find(r => r.city === city.name)?.rank === 1 && (
                <div style={{
                  position: 'absolute',
                  top: 12,
                  right: 12,
                  width: 32,
                  height: 32,
                  borderRadius: 16,
                  background: '#faad14',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 16
                }}>
                  <TrophyOutlined />
                </div>
              )}
              
              <div style={{ marginBottom: 16 }}>
                <Title level={4} style={{ margin: 0, color: COMPARE_COLORS[index] }}>
                  {city.name}
                </Title>
                <div style={{ marginTop: 8 }}>
                  {city.tags?.slice(0, 4).map(tag => (
                    <Tag key={tag} color="blue">{tag}</Tag>
                  ))}
                </div>
              </div>
              
              <div style={{ 
                textAlign: 'center', 
                padding: '16px 0', 
                background: COMPARE_COLORS[index] + '15',
                borderRadius: 8,
                marginBottom: 16
              }}>
                <Statistic
                  value={city.total_score || 0}
                  precision={1}
                  suffix={<span style={{ fontSize: 14 }}>分</span>}
                  valueStyle={{ color: COMPARE_COLORS[index], fontSize: 28 }}
                />
                <div style={{ fontSize: 12, color: '#666', marginTop: 4 }}>综合评分</div>
              </div>
              
              <Row gutter={[8, 8]} size="small">
                <Col span={12}>
                  <div style={{ textAlign: 'center', padding: 8, background: '#f6ffed', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#52c41a' }}>
                      {city.stats.attraction_count}
                    </div>
                    <div style={{ fontSize: 12, color: '#666' }}>景点</div>
                  </div>
                </Col>
                <Col span={12}>
                  <div style={{ textAlign: 'center', padding: 8, background: '#fff7e6', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#faad14' }}>
                      {city.stats.food_count}
                    </div>
                    <div style={{ fontSize: 12, color: '#666' }}>美食</div>
                  </div>
                </Col>
                <Col span={12}>
                  <div style={{ textAlign: 'center', padding: 8, background: '#e6f7ff', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#1677ff' }}>
                      {city.stats.hotel_count}
                    </div>
                    <div style={{ fontSize: 12, color: '#666' }}>酒店</div>
                  </div>
                </Col>
                <Col span={12}>
                  <div style={{ textAlign: 'center', padding: 8, background: '#f9f0ff', borderRadius: 8 }}>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#722ed1' }}>
                      ¥{city.stats.avg_hotel_price || 0}
                    </div>
                    <div style={{ fontSize: 12, color: '#666' }}>均价</div>
                  </div>
                </Col>
              </Row>
              
              <Divider style={{ margin: '16px 0' }} />
              
              <div style={{ marginBottom: 8 }}>
                <Text type="secondary" style={{ fontSize: 12 }}>评分</Text>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Text style={{ fontSize: 12, width: 60 }}>景点</Text>
                  <Rate disabled value={city.stats.avg_attraction_rating / 2} allowHalf style={{ fontSize: 12 }} />
                  <Text style={{ fontSize: 12 }}>{city.stats.avg_attraction_rating.toFixed(1)}</Text>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Text style={{ fontSize: 12, width: 60 }}>美食</Text>
                  <Rate disabled value={city.stats.avg_food_rating / 2} allowHalf style={{ fontSize: 12 }} />
                  <Text style={{ fontSize: 12 }}>{city.stats.avg_food_rating.toFixed(1)}</Text>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Text style={{ fontSize: 12, width: 60 }}>酒店</Text>
                  <Rate disabled value={city.stats.avg_hotel_rating / 2} allowHalf style={{ fontSize: 12 }} />
                  <Text style={{ fontSize: 12 }}>{city.stats.avg_hotel_rating.toFixed(1)}</Text>
                </div>
              </div>
              
              {city.weather && (
                <>
                  <Divider style={{ margin: '16px 0' }} />
                  <div>
                    <Text type="secondary" style={{ fontSize: 12 }}>天气</Text>
                    {city.weather.current && (
                      <div style={{ marginTop: 4 }}>
                        <div style={{ fontSize: 16, fontWeight: 'bold' }}>
                          {city.weather.current.temp}°C
                        </div>
                        <div style={{ fontSize: 12, color: '#666' }}>
                          {city.weather.current.text} · {WIND_DIRECTIONS[city.weather.current.wind_dir] || ''} {city.weather.current.wind_class}
                        </div>
                      </div>
                    )}
                    {city.weather.best_temp && (
                      <div style={{ fontSize: 12, color: '#52c41a', marginTop: 4 }}>
                        🌡️ 最佳气温: {city.weather.best_temp}°C
                      </div>
                    )}
                    {city.weather.rain_days_7d > 0 && (
                      <div style={{ fontSize: 12, color: '#faad14' }}>
                        🌧️ 7天内{city.weather.rain_days_7d}天有雨
                      </div>
                    )}
                  </div>
                </>
              )}
              
              {city.best_season?.length > 0 && (
                <>
                  <Divider style={{ margin: '16px 0' }} />
                  <div>
                    <Text type="secondary" style={{ fontSize: 12 }}>最佳季节</Text>
                    <div style={{ marginTop: 4 }}>
                      {city.best_season.map(s => (
                        <Tag key={s} color="green" style={{ fontSize: 11 }}>{s}</Tag>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </Card>
          </Col>
        ))}
      </Row>
    )
  }

  const renderCharts = () => {
    if (!result) return null
    
    return (
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} md={12}>
          <Card 
            title={
              <Space>
                <StarFilled style={{ color: '#faad14' }} />
                <span>综合能力雷达图</span>
              </Space>
            }
            style={{ borderRadius: 12, height: '100%' }}
          >
            <div ref={radarChartRef} style={{ width: '100%', height: 350 }} />
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card 
            title={
              <Space>
                <EnvironmentOutlined style={{ color: '#1677ff' }} />
                <span>资源数量对比</span>
              </Space>
            }
            style={{ borderRadius: 12, height: '100%' }}
          >
            <div ref={barChartRef} style={{ width: '100%', height: 350 }} />
          </Card>
        </Col>
      </Row>
    )
  }

  const renderRecommendation = () => {
    if (!result?.recommendation) return null
    
    return (
      <Card 
        title={
          <Space>
            <TrophyOutlined style={{ color: '#faad14' }} />
            <span>推荐排名</span>
          </Space>
        }
        style={{ borderRadius: 12, marginBottom: 24 }}
      >
        <List
          dataSource={result.recommendation}
          renderItem={(item, index) => (
            <List.Item>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                width: '100%',
                padding: '12px 16px',
                background: index === 0 ? '#fffbe6' : '#fafafa',
                borderRadius: 8,
                border: index === 0 ? '1px solid #ffe58f' : '1px solid #f0f0f0'
              }}>
                <div style={{
                  width: 40,
                  height: 40,
                  borderRadius: 20,
                  background: index === 0 ? '#faad14' : index === 1 ? '#d9d9d9' : index === 2 ? '#ff7a45' : '#f0f0f0',
                  color: index < 3 ? '#fff' : '#666',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  fontSize: 18,
                  marginRight: 16,
                  flexShrink: 0
                }}>
                  {index + 1}
                </div>
                
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                    <Title level={5} style={{ margin: 0 }}>{item.city}</Title>
                    <Badge count={`${item.score}分`} style={{ backgroundColor: '#1677ff' }} />
                  </div>
                  
                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 8 }}>
                    {item.tags?.map(tag => (
                      <Tag key={tag} style={{ fontSize: 11 }}>{tag}</Tag>
                    ))}
                  </div>
                  
                  <div style={{ display: 'flex', gap: 16, fontSize: 12 }}>
                    <span style={{ color: '#52c41a' }}>
                      <ArrowUpOutlined /> {item.strengths?.join(' · ')}
                    </span>
                  </div>
                </div>
                
                <div style={{ textAlign: 'right', marginLeft: 16 }}>
                  <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677ff' }}>
                    {item.score}
                  </div>
                  <div style={{ fontSize: 12, color: '#999' }}>最佳: {item.best_season}</div>
                </div>
              </div>
            </List.Item>
          )}
        />
      </Card>
    )
  }

  return (
    <div className="page-container" style={{ padding: '24px 16px', maxWidth: 1400, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} style={{ borderRadius: 8 }}>
          返回
        </Button>
      </div>
      
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: 16,
        padding: 32,
        color: 'white',
        marginBottom: 24
      }}>
        <Title level={2} style={{ color: 'white', margin: 0 }}>
          🏙️ 城市对比
        </Title>
        <div style={{ marginTop: 8, opacity: 0.9 }}>
          选择2-4个城市进行全方位对比，帮您找到最理想的旅行目的地
        </div>
      </div>
      
      {renderCitySelector()}
      
      {loading && (
        <div style={{ textAlign: 'center', padding: 80 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16, color: '#666' }}>正在对比城市数据...</div>
        </div>
      )}
      
      {!loading && result && (
        <>
          {renderRecommendation()}
          {renderCityCards()}
          {renderCharts()}
          {renderComparisonTable()}
        </>
      )}
      
      {!loading && !result && (
        <Card style={{ borderRadius: 12 }}>
          <Empty 
            description="选择您想对比的城市，点击开始对比" 
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      )}
    </div>
  )
}
