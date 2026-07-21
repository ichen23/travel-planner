import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card, Row, Col, Button, InputNumber, Select, Space, Typography,
  List, Tag, Divider, Steps, Alert, Empty, Spin, Progress, message,
  Modal, Timeline, Tooltip, Badge, Statistic
} from 'antd'
import {
  PlusOutlined, DeleteOutlined, ArrowUpOutlined, ArrowDownOutlined,
  ThunderboltOutlined, DollarOutlined, CalendarOutlined, EnvironmentOutlined,
  ClockCircleOutlined, CarOutlined, StarOutlined, HomeOutlined,
  CheckCircleOutlined, InfoCircleOutlined, ShoppingOutlined,
  CopyOutlined, PrinterOutlined, ShareAltOutlined,
  SwapOutlined, TeamOutlined
} from '@ant-design/icons'
import {
  getMultiCityCities, generateMultiCityItinerary, getTrainInfo
} from '../services/multiCityService'

const { Title, Text, Paragraph } = Typography

export default function MultiCityPlanner() {
  const navigate = useNavigate()
  
  const [availableCities, setAvailableCities] = useState([])
  const [selectedCities, setSelectedCities] = useState([{ name: '开封', days: 2 }])
  const [totalDays, setTotalDays] = useState(4)
  const [budget, setBudget] = useState(3000)
  const [loadingCities, setLoadingCities] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState(null)
  const [showTips, setShowTips] = useState(false)
  const [showPacking, setShowPacking] = useState(false)

  useEffect(() => {
    loadAvailableCities()
  }, [])

  const loadAvailableCities = async () => {
    try {
      const response = await getMultiCityCities()
      if (response.success) {
        setAvailableCities(response.cities.map(c => c.name))
      }
    } catch (error) {
      message.error('加载城市列表失败')
    } finally {
      setLoadingCities(false)
    }
  }

  const handleAddCity = () => {
    const usedCities = selectedCities.map(c => c.name)
    const availableToAdd = availableCities.filter(c => !usedCities.includes(c))
    
    if (availableToAdd.length === 0) {
      message.warning('所有城市都已选择')
      return
    }

    setSelectedCities(prev => {
      const newCities = [...prev, { name: availableToAdd[0], days: 1 }]
      updateTotalDays(newCities)
      return newCities
    })
  }

  const handleRemoveCity = (index) => {
    if (selectedCities.length <= 1) {
      message.warning('至少需要保留一个城市')
      return
    }
    setSelectedCities(prev => {
      const newCities = prev.filter((_, i) => i !== index)
      updateTotalDays(newCities)
      return newCities
    })
  }

  const handleCityChange = (index, newCity) => {
    setSelectedCities(prev => {
      const newCities = [...prev]
      newCities[index] = { ...newCities[index], name: newCity }
      return newCities
    })
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
    const sum = cities.reduce((acc, c) => acc + c.days, 0)
    setTotalDays(sum)
  }

  const handleGenerate = async () => {
    if (selectedCities.length < 2) {
      message.warning('至少需要选择2个城市')
      return
    }

    setGenerating(true)
    setResult(null)

    try {
      const cities = selectedCities.map(c => c.name)
      const dayAllocation = selectedCities.map(c => c.days)

      const response = await generateMultiCityItinerary(
        cities,
        dayAllocation,
        totalDays,
        budget
      )

      if (response.success) {
        setResult(response)
        message.success('行程生成成功！')
      } else {
        message.error(response.message || '生成失败')
      }
    } catch (error) {
      console.error('生成行程错误:', error)
      message.error('生成行程失败，请稍后重试')
    } finally {
      setGenerating(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setSelectedCities([{ name: '开封', days: 2 }])
    setTotalDays(4)
    setBudget(3000)
  }

  const handleCopyResult = () => {
    if (!result) return

    let text = `${result.cities.join(' → ')} ${result.total_days}日游\n\n`
    text += `预算: ¥${result.total_budget}\n\n`
    text += '='.repeat(50) + '\n'

    result.transfer_segments.forEach((seg, i) => {
      text += `\n🚄 第${i + 1}段交通\n`
      text += `${seg.from_city} → ${seg.to_city}\n`
      text += `${seg.train_number}次 ${seg.departure} - ${seg.arrival}\n`
      text += `车程: ${seg.duration_text} | 票价: ¥${seg.price}\n`
    })

    result.days.forEach(day => {
      text += `\n${'='.repeat(50)}\n`
      text += `【${day.date_label}】${day.city}\n`
      text += `${'='.repeat(50)}\n`

      day.schedule.forEach(item => {
        text += `\n${item.icon} ${item.start_time} - ${item.end_time} ${item.name}\n`
        if (item.tips) text += `   💡 ${item.tips}\n`
        if (item.ticket) text += `   🎫 ${item.ticket}\n`
        if (item.location) text += `   📍 ${item.location}\n`
      })
    })

    text += `\n${'='.repeat(50)}\n`
    text += '💰 预算明细\n'
    const budget = result.budget_breakdown
    Object.entries(budget).forEach(([key, value]) => {
      text += `${key}: ¥${value.toFixed(0)}\n`
    })

    navigator.clipboard.writeText(text)
    message.success('行程已复制到剪贴板')
  }

  const handlePrint = () => {
    window.print()
  }

  const renderCitySelector = () => {
    const usedCities = selectedCities.map(c => c.name)
    const cityOptions = availableCities.filter(c => !usedCities.includes(c) || true)

    return (
      <Card 
        title={
          <Space>
            <TeamOutlined />
            <span>选择城市 ({selectedCities.length}个)</span>
          </Space>
        }
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleAddCity}
            disabled={selectedCities.length >= availableCities.length}
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
            {selectedCities.map((city, index) => (
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
                  value={city.name}
                  onChange={(val) => handleCityChange(index, val)}
                  style={{ flex: 1 }}
                  showSearch
                  placeholder="选择城市"
                  filterOption={(input, option) =>
                    option.children.toLowerCase().includes(input.toLowerCase())
                  }
                >
                  {cityOptions.map(c => (
                    <Select.Option key={c} value={c}>
                      {c}
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

                <Space>
                  <Button
                    icon={<ArrowUpOutlined />}
                    onClick={() => handleMoveUp(index)}
                    disabled={index === 0}
                    size="small"
                  />
                  <Button
                    icon={<ArrowDownOutlined />}
                    onClick={() => handleMoveDown(index)}
                    disabled={index === selectedCities.length - 1}
                    size="small"
                  />
                  <Button
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => handleRemoveCity(index)}
                    size="small"
                  />
                </Space>
              </div>
            ))}
          </div>
        )}

        <Divider />

        <Row gutter={16}>
          <Col span={12}>
            <Statistic
              title="总天数"
              value={totalDays}
              prefix={<CalendarOutlined />}
              suffix="天"
            />
          </Col>
          <Col span={12}>
            <Statistic
              title="总预算"
              value={budget}
              prefix={<DollarOutlined />}
              suffix="元"
            />
          </Col>
        </Row>

        <Divider />

        <div style={{ textAlign: 'center' }}>
          <Space>
            <Button
              type="primary"
              size="large"
              icon={<ThunderboltOutlined />}
              onClick={handleGenerate}
              loading={generating}
              disabled={selectedCities.length < 2}
              style={{ 
                minWidth: 200,
                height: 48,
                fontSize: 18,
                background: 'linear-gradient(135deg, #667eea, #764ba2)',
                border: 'none',
              }}
            >
              🚄 生成详细行程
            </Button>
            <Button size="large" onClick={handleReset}>
              重置
            </Button>
          </Space>
        </div>
      </Card>
    )
  }

  const renderTransportSegment = (seg, index) => (
    <Card
      key={index}
      style={{
        marginBottom: 16,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        border: 'none',
        borderRadius: 16,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, color: 'white' }}>
        <div style={{ fontSize: 32 }}>🚄</div>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <Text strong style={{ color: 'white', fontSize: 18 }}>{seg.from_city}</Text>
            <div style={{ flex: 1, height: 2, background: 'rgba(255,255,255,0.3)', position: 'relative' }}>
              <CarOutlined style={{ position: 'absolute', left: '45%', top: -8, fontSize: 20 }} />
            </div>
            <Text strong style={{ color: 'white', fontSize: 18 }}>{seg.to_city}</Text>
          </div>
          <div style={{ marginTop: 8, fontSize: 14, opacity: 0.9 }}>
            <Space>
              <ClockCircleOutlined />
              <span>{seg.train_number}次 {seg.departure} - {seg.arrival}</span>
              <span>|</span>
              <span>{seg.duration_text}</span>
              <span>|</span>
              <span>¥{seg.price}</span>
            </Space>
          </div>
        </div>
      </div>
    </Card>
  )

  const renderDaySchedule = (day, index) => (
    <Card
      key={index}
      style={{ 
        marginBottom: 16,
        borderLeft: `4px solid ${day.is_transfer_day ? '#faad14' : '#1890ff'}`,
      }}
    >
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Badge 
            count={day.day} 
            style={{ backgroundColor: day.is_transfer_day ? '#faad14' : '#1890ff' }}
          />
          <Title level={4} style={{ margin: 0 }}>
            {day.date_label}: {day.city}
          </Title>
          {day.is_transfer_day && (
            <Tag color="warning">中转日</Tag>
          )}
        </Space>
        {!day.is_transfer_day && (
          <div style={{ marginTop: 8, color: '#666' }}>
            <Tooltip title="本地交通建议">
              <InfoCircleOutlined /> {day.transport_tips}
            </Tooltip>
          </div>
        )}
      </div>

      <Timeline
        items={day.schedule.map((item, itemIndex) => ({
          color: item.type === 'transport' ? '#faad14' : item.type === 'food' ? '#f5222d' : '#1890ff',
          children: (
            <div style={{ padding: 8, background: '#fafafa', borderRadius: 8 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 4 }}>
                <span style={{ fontSize: 20 }}>{item.icon}</span>
                <div style={{ flex: 1 }}>
                  <Text strong style={{ fontSize: 16 }}>{item.name}</Text>
                </div>
                <Tag color="blue">{item.start_time} - {item.end_time}</Tag>
              </div>
              {item.tips && (
                <div style={{ marginLeft: 32, color: '#666', fontSize: 14 }}>
                  💡 {item.tips}
                </div>
              )}
              {item.ticket && (
                <div style={{ marginLeft: 32, color: '#faad14', fontSize: 14 }}>
                  🎫 票价: {item.ticket}
                </div>
              )}
              {item.location && (
                <div style={{ marginLeft: 32, color: '#52c41a', fontSize: 14 }}>
                  📍 {item.location}
                </div>
              )}
              {item.recommend && (
                <div style={{ marginLeft: 32, color: '#f5222d', fontSize: 14 }}>
                  🍽️ 推荐: {item.recommend}
                </div>
              )}
            </div>
          )
        }))}
      />
    </Card>
  )

  const renderResult = () => {
    if (!result) return null

    return (
      <div>
        <Card 
          title={
            <Space>
              <StarOutlined style={{ color: '#faad14' }} />
              <span style={{ fontSize: 20 }}>行程生成成功！</span>
            </Space>
          }
          extra={
            <Space>
              <Button icon={<CopyOutlined />} onClick={handleCopyResult}>
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
          <Alert
            message="行程概览"
            description={
              <Space>
                <span>🗺️ 路线: <Text strong>{result.cities.join(' → ')}</Text></span>
                <span>|</span>
                <span>📅 总天数: <Text strong>{result.total_days}天</Text></span>
                <span>|</span>
                <span>💰 总预算: <Text strong>¥{result.total_budget}</Text></span>
              </Space>
            }
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />

          <Divider orientation="left" style={{ fontSize: 16 }}>🚄 交通安排</Divider>
          {result.transfer_segments.map((seg, i) => renderTransportSegment(seg, i))}

          <Divider orientation="left" style={{ fontSize: 16 }}>📅 每日行程</Divider>
          {result.days.map((day, i) => renderDaySchedule(day, i))}

          <Divider orientation="left" style={{ fontSize: 16 }}>💰 预算明细</Divider>
          <Row gutter={16}>
            {Object.entries(result.budget_breakdown).map(([key, value]) => (
              <Col span={8} key={key}>
                <Card size="small">
                  <Statistic
                    title={key === 'accommodation' ? '住宿' : 
                          key === 'food' ? '餐饮' : 
                          key === 'transport' ? '交通' :
                          key === 'tickets' ? '门票' : '其他'}
                    value={value}
                    prefix="¥"
                    precision={0}
                    valueStyle={{ color: '#3f8600' }}
                  />
                </Card>
              </Col>
            ))}
          </Row>

          <Divider orientation="left" style={{ fontSize: 16 }}>💡 实用贴士</Divider>
          <List
            dataSource={result.tips}
            renderItem={(item, i) => (
              <List.Item key={i}>
                <Alert message={item} type="success" showIcon />
              </List.Item>
            )}
          />
        </Card>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '24px 16px' }}>
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <Title level={2}>
          <SwapOutlined style={{ color: '#667eea' }} />
          <span style={{ marginLeft: 8 }}>多城市行程规划</span>
        </Title>
        <Text type="secondary" style={{ fontSize: 16 }}>
          选择多个城市，设置天数和预算，智能生成包含高铁交通的详细行程
        </Text>
      </div>

      {renderCitySelector()}

      {generating ? (
        <Card style={{ textAlign: 'center', padding: '60px 0' }}>
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
                选择城市并点击"生成详细行程"开始规划你的旅行！
              </span>
            }
          >
            <Button type="primary" icon={<ThunderboltOutlined />} onClick={handleGenerate}>
              立即生成
            </Button>
          </Empty>
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
        {result && result.packing_list && (
          <div>
            {result.packing_list['必带物品'] && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>✅ 必带物品</Title>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {result.packing_list['必带物品'].map((item, i) => (
                    <Tag key={i} color="red">{item}</Tag>
                  ))}
                </div>
              </div>
            )}
            {result.packing_list['季节推荐'] && result.packing_list['季节推荐'].length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <Title level={5}>🌞 季节推荐</Title>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {result.packing_list['季节推荐'].map((item, i) => (
                    <Tag key={i} color="orange">{item}</Tag>
                  ))}
                </div>
              </div>
            )}
            {result.packing_list['可选物品'] && result.packing_list['可选物品'].length > 0 && (
              <div>
                <Title level={5}>🎒 可选物品</Title>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {result.packing_list['可选物品'].map((item, i) => (
                    <Tag key={i} color="blue">{item}</Tag>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}
