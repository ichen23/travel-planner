import { useState, useEffect } from 'react'
import { Card, Checkbox, Row, Col, Typography, Button, InputNumber, Select, Space, Tag, message, Spin, Divider, Progress, Empty, Collapse, Badge, Tooltip } from 'antd'
import { CarryOutOutlined, ReloadOutlined, CheckCircleOutlined, ClockCircleOutlined, ThunderboltOutlined, ShoppingOutlined, CloudOutlined, UserOutlined, ExclamationCircleOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Title, Text, Paragraph } = Typography
const { Panel } = Collapse

const SCENARIO_OPTIONS = [
  { value: '', label: '通用' },
  { value: 'beach', label: '🏖️ 海滩度假' },
  { value: 'mountain', label: '🏔️ 登山徒步' },
  { value: 'business', label: '💼 商务出行' },
  { value: 'family', label: '👨‍👩‍👧 亲子家庭' },
  { value: 'elderly', label: '👴 老人随行' },
  { value: 'hiking', label: '🥾 户外徒步' },
  { value: 'photography', label: '📷 摄影采风' },
  { value: 'night_out', label: '🌃 夜生活' },
]

const SEASON_OPTIONS = [
  { value: '', label: '自动识别' },
  { value: 'spring', label: '🌸 春季' },
  { value: 'summer', label: '☀️ 夏季' },
  { value: 'autumn', label: '🍂 秋季' },
  { value: 'winter', label: '❄️ 冬季' },
]

export default function LuggageChecklist({ days = 3, city = '', scenario = '', onUpdate }) {
  const [loading, setLoading] = useState(false)
  const [checklist, setChecklist] = useState(null)
  const [formData, setFormData] = useState({
    days,
    season: '',
    scenario,
    weather_temp: 25,
    has_rain: false,
    people_count: 2,
    special_needs: [],
  })

  const fetchChecklist = async () => {
    setLoading(true)
    try {
      const result = await api.post('/destination/luggage-checklist', formData)
      if (result.success) {
        if (result.checklist.categories) {
          result.checklist.categories = result.checklist.categories.map(cat => ({
            ...cat,
            items: cat.items.map(item => ({ ...item, checked: false }))
          }))
        }
        setChecklist(result.checklist)
        message.success('行李清单生成成功')
        if (onUpdate) {
          onUpdate(result.checklist)
        }
      } else {
        message.error(result.message || '生成失败')
      }
    } catch (err) {
      console.error('生成行李清单失败:', err)
      message.error('生成行李清单失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchChecklist()
  }, [])

  const toggleItem = (categoryIndex, itemIndex) => {
    const newChecklist = { ...checklist }
    newChecklist.categories = newChecklist.categories.map((cat, ci) => {
      if (ci === categoryIndex) {
        return {
          ...cat,
          items: cat.items.map((item, ii) => {
            if (ii === itemIndex) {
              return { ...item, checked: !item.checked }
            }
            return item
          })
        }
      }
      return cat
    })
    setChecklist(newChecklist)
  }

  const toggleCategory = (categoryIndex, checked) => {
    const newChecklist = { ...checklist }
    newChecklist.categories = newChecklist.categories.map((cat, ci) => {
      if (ci === categoryIndex) {
        return {
          ...cat,
          items: cat.items.map(item => ({ ...item, checked }))
        }
      }
      return cat
    })
    setChecklist(newChecklist)
  }

  const getStats = () => {
    if (!checklist) return { total: 0, checked: 0, progress: 0 }
    
    let total = 0
    let checked = 0
    
    checklist.categories.forEach(cat => {
      cat.items.forEach(item => {
        total++
        if (item.checked) checked++
      })
    })
    
    return {
      total,
      checked,
      progress: total > 0 ? Math.round((checked / total) * 100) : 0
    }
  }

  const stats = getStats()

  const renderSettings = () => (
    <Card 
      title={
        <Space>
          <CarryOutOutlined />
          <span>行李清单设置</span>
        </Space>
      }
      style={{ borderRadius: 12, marginBottom: 16 }}
      extra={
        <Button 
          type="primary" 
          icon={<ReloadOutlined />} 
          onClick={fetchChecklist}
          loading={loading}
          style={{ borderRadius: 8 }}
        >
          生成清单
        </Button>
      }
    >
      <Row gutter={[16, 16]}>
        <Col xs={12} sm={6}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">天数</Text>
          </div>
          <InputNumber
            min={1}
            max={30}
            value={formData.days}
            onChange={v => setFormData({ ...formData, days: v })}
            style={{ width: '100%' }}
          />
        </Col>
        <Col xs={12} sm={6}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">季节</Text>
          </div>
          <Select
            value={formData.season}
            onChange={v => setFormData({ ...formData, season: v })}
            options={SEASON_OPTIONS}
            style={{ width: '100%' }}
          />
        </Col>
        <Col xs={12} sm={6}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">场景</Text>
          </div>
          <Select
            value={formData.scenario}
            onChange={v => setFormData({ ...formData, scenario: v })}
            options={SCENARIO_OPTIONS}
            style={{ width: '100%' }}
          />
        </Col>
        <Col xs={12} sm={6}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">人数</Text>
          </div>
          <InputNumber
            min={1}
            max={10}
            value={formData.people_count}
            onChange={v => setFormData({ ...formData, people_count: v })}
            style={{ width: '100%' }}
          />
        </Col>
      </Row>
      <Row gutter={[16, 16]} style={{ marginTop: 8 }}>
        <Col xs={12} sm={8}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">预计温度 (°C)</Text>
          </div>
          <InputNumber
            min={-20}
            max={45}
            value={formData.weather_temp}
            onChange={v => setFormData({ ...formData, weather_temp: v })}
            style={{ width: '100%' }}
          />
        </Col>
        <Col xs={12} sm={8}>
          <div style={{ marginBottom: 8 }}>
            <Text type="secondary">天气</Text>
          </div>
          <Select
            value={formData.has_rain ? 'rain' : 'sunny'}
            onChange={v => setFormData({ ...formData, has_rain: v === 'rain' })}
            options={[
              { value: 'sunny', label: '☀️ 晴朗' },
              { value: 'rain', label: '🌧️ 有雨' },
            ]}
            style={{ width: '100%' }}
          />
        </Col>
      </Row>
    </Card>
  )

  const renderChecklist = () => {
    if (loading) {
      return (
        <div style={{ textAlign: 'center', padding: 80 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16, color: '#666' }}>正在生成行李清单...</div>
        </div>
      )
    }

    if (!checklist) {
      return (
        <Card style={{ borderRadius: 12 }}>
          <Empty description="暂无行李清单，请点击生成" />
        </Card>
      )
    }

    return (
      <>
        <Card 
          style={{ 
            borderRadius: 12, 
            marginBottom: 16,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            color: '#fff'
          }}
          bodyStyle={{ padding: 20 }}
        >
          <Row gutter={16} align="middle">
            <Col xs={24} sm={8}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 32, fontWeight: 'bold' }}>
                  {stats.checked}/{stats.total}
                </div>
                <div style={{ opacity: 0.85 }}>已打包物品</div>
              </div>
            </Col>
            <Col xs={24} sm={16}>
              <Progress 
                percent={stats.progress} 
                strokeColor={{ from: '#52c41a', to: '#73d13d' }}
                style={{ marginBottom: 8 }}
              />
              <Space style={{ color: 'rgba(255,255,255,0.85)' }}>
                <Tag style={{ background: 'rgba(255,255,255,0.2)', border: 'none', color: '#fff' }}>
                  <ClockCircleOutlined /> {checklist.days}天行程
                </Tag>
                {checklist.estimated_weight && (
                  <Tag style={{ background: 'rgba(255,255,255,0.2)', border: 'none', color: '#fff' }}>
                    <CarryOutOutlined /> 约{checklist.estimated_weight}kg
                  </Tag>
                )}
                <Tag style={{ background: 'rgba(255,255,255,0.2)', border: 'none', color: '#fff' }}>
                  <CloudOutlined /> {checklist.season === 'spring' ? '春季' : checklist.season === 'summer' ? '夏季' : checklist.season === 'autumn' ? '秋季' : '冬季'}
                </Tag>
              </Space>
            </Col>
          </Row>
          {checklist.summary && (
            <div style={{ marginTop: 12, fontSize: 13, opacity: 0.9 }}>
              💡 {checklist.summary}
            </div>
          )}
        </Card>

        <Collapse 
          defaultActiveKey={checklist.categories?.map((_, i) => i) || []}
          ghost
        >
          {checklist.categories?.map((category, categoryIndex) => {
            const categoryChecked = category.items.filter(item => item.checked).length
            const categoryTotal = category.items.length
            
            return (
              <Panel
                key={categoryIndex}
                header={
                  <Space>
                    <span style={{ fontSize: 20 }}>{category.icon}</span>
                    <span style={{ fontWeight: 600 }}>{category.name}</span>
                    <Badge 
                      count={`${categoryChecked}/${categoryTotal}`} 
                      showZero
                      style={{ 
                        backgroundColor: categoryChecked === categoryTotal ? '#52c41a' : '#1677ff',
                        marginLeft: 8
                      }}
                    />
                  </Space>
                }
                extra={
                  <Checkbox
                    checked={categoryChecked === categoryTotal && categoryTotal > 0}
                    indeterminate={categoryChecked > 0 && categoryChecked < categoryTotal}
                    onChange={e => toggleCategory(categoryIndex, e.target.checked)}
                    onClick={e => e.stopPropagation()}
                  >
                    全选
                  </Checkbox>
                }
                style={{ 
                  background: '#fff', 
                  marginBottom: 8, 
                  borderRadius: 8,
                  border: '1px solid #f0f0f0'
                }}
              >
                <Row gutter={[8, 8]}>
                  {category.items.map((item, itemIndex) => (
                    <Col xs={24} sm={12} md={8} lg={6} key={itemIndex}>
                      <Card
                        size="small"
                        style={{
                          borderRadius: 8,
                          cursor: 'pointer',
                          background: item.checked ? '#f6ffed' : '#fff',
                          borderColor: item.checked ? '#b7eb8f' : '#e8e8e8',
                          transition: 'all 0.3s'
                        }}
                        bodyStyle={{ padding: '8px 12px' }}
                        onClick={() => toggleItem(categoryIndex, itemIndex)}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          <Checkbox checked={item.checked} />
                          <div style={{ flex: 1, overflow: 'hidden' }}>
                            <div style={{ 
                              fontSize: 14, 
                              fontWeight: 500,
                              textDecoration: item.checked ? 'line-through' : 'none',
                              color: item.checked ? '#999' : '#333'
                            }}>
                              {item.name}
                            </div>
                            {item.quantity > 1 && (
                              <div style={{ fontSize: 12, color: '#999' }}>
                                x{item.quantity}
                              </div>
                            )}
                          </div>
                          {item.checked && <CheckCircleOutlined style={{ color: '#52c41a', fontSize: 16 }} />}
                        </div>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Panel>
            )
          })}
        </Collapse>

        {checklist.tips && checklist.tips.length > 0 && (
          <Card 
            title={
              <Space>
                <ThunderboltOutlined style={{ color: '#faad14' }} />
                <span>打包小贴士</span>
              </Space>
            }
            style={{ borderRadius: 12, marginTop: 16 }}
          >
            {checklist.tips.map((tip, index) => (
              <div key={index} style={{ 
                padding: '8px 12px', 
                background: '#fffbe6', 
                borderRadius: 8,
                marginBottom: index < checklist.tips.length - 1 ? 8 : 0,
                borderLeft: '3px solid #faad14'
              }}>
                <ExclamationCircleOutlined style={{ marginRight: 8, color: '#faad14' }} />
                <Text>{tip}</Text>
              </div>
            ))}
          </Card>
        )}
      </>
    )
  }

  return (
    <div>
      {renderSettings()}
      {renderChecklist()}
    </div>
  )
}
