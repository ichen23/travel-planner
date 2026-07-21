import { useState, useEffect, useRef } from 'react'
import { Input, List, Card, Tag, Empty, Spin, Typography } from 'antd'
import { SearchOutlined, EnvironmentOutlined, CompassOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { searchCities } from '../services/destinationService'

const { Text } = Typography

const CITY_TYPES = {
  '直辖市': { color: 'red', icon: '🏙️' },
  '省会': { color: 'blue', icon: '🏛️' },
  '地级市': { color: 'geekblue', icon: '🏘️' },
  '县级市': { color: 'purple', icon: '🏡' },
  '市辖区': { color: 'cyan', icon: '📍' },
  '县': { color: 'green', icon: '🌾' },
  '自治县': { color: 'orange', icon: '🏔️' },
  '特别行政区': { color: 'gold', icon: '⭐' },
  '推荐城市': { color: 'magenta', icon: '💝' },
  '行政区划': { color: 'default', icon: '🗺️' },
}

export default function CitySearch({ onSelectCity, placeholder = '搜索城市名称...' }) {
  const [keyword, setKeyword] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const inputRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (!keyword.trim()) {
      setResults([])
      setHasSearched(false)
      return
    }

    const timer = setTimeout(async () => {
      setLoading(true)
      setHasSearched(true)
      try {
        const response = await searchCities(keyword.trim(), 20, 'all')
        if (response.data.success) {
          setResults(response.data.results || [])
        } else {
          setResults([])
        }
      } catch (error) {
        console.error('搜索城市失败:', error)
        setResults([])
      } finally {
        setLoading(false)
      }
    }, 300)

    return () => clearTimeout(timer)
  }, [keyword])

  const handleSelectCity = (city) => {
    setShowResults(false)
    setKeyword('')
    
    if (onSelectCity) {
      onSelectCity(city)
    } else {
      navigate(`/destination/${encodeURIComponent(city.name)}`)
    }
  }

  const getTypeInfo = (type) => {
    return CITY_TYPES[type] || { color: 'default', icon: '📍' }
  }

  const groupedResults = results.reduce((acc, city) => {
    const type = city.type || '其他'
    if (!acc[type]) acc[type] = []
    acc[type].push(city)
    return acc
  }, {})

  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: 600, margin: '0 auto' }}>
      <Input
        ref={inputRef}
        size="large"
        placeholder={placeholder}
        prefix={<SearchOutlined style={{ color: '#ff6b6b' }} />}
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        onFocus={() => setShowResults(true)}
        onBlur={() => setTimeout(() => setShowResults(false), 200)}
        onPressEnter={() => setShowResults(true)}
        style={{
          borderRadius: 24,
          border: '2px solid #e8e8e8',
          boxShadow: showResults ? '0 4px 12px rgba(0,0,0,0.1)' : 'none',
          transition: 'all 0.3s',
          background: '#fff',
        }}
      />

      {showResults && keyword.trim() && (
        <Card
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            marginTop: 8,
            borderRadius: 16,
            boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
            zIndex: 1000,
            maxHeight: 480,
            overflow: 'auto',
          }}
          bodyStyle={{ padding: 0 }}
        >
          {loading ? (
            <div style={{ padding: 40, textAlign: 'center' }}>
              <Spin tip="搜索中..." />
            </div>
          ) : results.length > 0 ? (
            <div>
              {Object.entries(groupedResults).map(([type, cities]) => (
                <div key={type} style={{ marginBottom: 8 }}>
                  <div style={{ padding: '8px 16px', background: '#fafafa', borderBottom: '1px solid #f0f0f0' }}>
                    <Tag color={getTypeInfo(type).color} style={{ margin: 0 }}>
                      {getTypeInfo(type).icon} {type} ({cities.length})
                    </Tag>
                  </div>
                  <List
                    size="small"
                    dataSource={cities}
                    renderItem={(city) => {
                      const typeInfo = getTypeInfo(city.type)
                      return (
                        <List.Item
                          style={{
                            cursor: 'pointer',
                            padding: '10px 16px',
                            transition: 'background 0.2s',
                          }}
                          onMouseEnter={(e) => {
                            e.currentTarget.style.background = '#f5f5f5'
                          }}
                          onMouseLeave={(e) => {
                            e.currentTarget.style.background = 'transparent'
                          }}
                          onClick={() => handleSelectCity(city)}
                        >
                          <List.Item.Meta
                            avatar={<EnvironmentOutlined style={{ fontSize: 20, color: '#ff6b6b' }} />}
                            title={
                              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <Text strong>{city.name}</Text>
                                {city.province && (
                                  <Tag color="blue" style={{ margin: 0 }}>{city.province}</Tag>
                                )}
                                {city.parent && city.parent !== city.name && (
                                  <Tag color="default" style={{ margin: 0 }}>{city.parent}</Tag>
                                )}
                              </div>
                            }
                            description={
                              city.coords ? (
                                <Text type="secondary" style={{ fontSize: 12 }}>
                                  📍 {city.coords[0].toFixed(4)}, {city.coords[1].toFixed(4)}
                                </Text>
                              ) : null
                            }
                          />
                        </List.Item>
                      )
                    }}
                  />
                </div>
              ))}
            </div>
          ) : hasSearched ? (
            <Empty
              image={Empty.PRESENTED_IMAGE_SIMPLE}
              description="未找到匹配的城市"
              style={{ padding: 40 }}
            />
          ) : null}
        </Card>
      )}

      {showResults && !keyword.trim() && (
        <Card
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            marginTop: 8,
            borderRadius: 16,
            boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
            zIndex: 1000,
          }}
          bodyStyle={{ padding: 16 }}
        >
          <div style={{ textAlign: 'center', padding: 20 }}>
            <CompassOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
            <div>
              <Text type="secondary">请输入城市名称开始搜索</Text>
            </div>
            <div style={{ marginTop: 12 }}>
              <Text type="secondary" style={{ fontSize: 12 }}>
                支持搜索全国 2000+ 行政区划
              </Text>
            </div>
          </div>
        </Card>
      )}
    </div>
  )
}
