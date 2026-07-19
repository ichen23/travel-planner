import { useState } from 'react'
import { Input, Button, Card, Typography, Space, Tag, message, Spin, Divider, Row, Col, Empty } from 'antd'
import { ThunderboltOutlined, SendOutlined, ReloadOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons'
import api from '../services/api'

const { Text, Title } = Typography

const PRESET_EXAMPLES = [
  '北京3天2晚，预算人均1500，带老人，少走路',
  '成都5天，喜欢美食和熊猫，预算3000',
  '三亚4天3晚，蜜月旅行，预算8000',
  '西安周末2天，历史文化，预算1000',
  '杭州3天2晚，亲子游，预算2000',
]

const PARAM_LABELS = {
  city: '目的地',
  days: '天数',
  nights: '晚数',
  budget: '预算',
  people: '人数',
  preference: '偏好',
  elderly_friendly: '老人友好',
  easy_walk: '少走路',
  no_spicy: '不吃辣',
  photo_focus: '拍照重点',
  homestay: '民宿',
  near_station: '近车站',
  near_attraction: '近景点',
  max_walk_per_day: '每日最大步行',
  max_travel_time: '最大交通时间',
  wake_up_time: '起床时间',
  sleep_time: '睡觉时间',
  include_night: '含夜生活',
  is_couple: '情侣',
  is_hiking: '徒步',
}

const PARAM_ICONS = {
  city: '📍',
  days: '📅',
  nights: '🌙',
  budget: '💰',
  people: '👥',
  preference: '❤️',
  elderly_friendly: '👴',
  easy_walk: '🚶',
  no_spicy: '🌶️',
  photo_focus: '📷',
  homestay: '🏠',
  near_station: '🚉',
  near_attraction: '🎯',
  max_walk_per_day: '👟',
  max_travel_time: '⏱️',
  wake_up_time: '⏰',
  sleep_time: '🌙',
  include_night: '🌃',
  is_couple: '💑',
  is_hiking: '🥾',
}

export default function AiChatInput({ onConfirm, onGenerate }) {
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [parsedResult, setParsedResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSend = async () => {
    if (!inputValue.trim()) {
      message.warning('请输入您的旅行需求')
      return
    }

    setLoading(true)
    setError(null)
    setParsedResult(null)

    try {
      const result = await api.post('/destination/parse-text', { text: inputValue.trim() })
      
      if (result.success) {
        setParsedResult(result.parsed_params)
        message.success('解析成功！')
      } else {
        setError(result.message || '解析失败')
        message.error(result.message || '解析失败')
      }
    } catch (err) {
      setError(err.message || '网络错误')
      message.error('网络错误，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    if (!inputValue.trim()) {
      message.warning('请输入您的旅行需求')
      return
    }

    setLoading(true)
    setError(null)
    setParsedResult(null)

    try {
      const result = await api.post('/destination/generate-from-text', { text: inputValue.trim() })
      
      if (result.success) {
        setParsedResult(result.parsed_params || result)
        message.success('行程生成成功！')
        if (onGenerate && result.itinerary) {
          onGenerate(result.itinerary)
        }
      } else {
        setError(result.message || '生成失败')
        message.error(result.message || '生成失败')
      }
    } catch (err) {
      setError(err.message || '网络错误')
      message.error('网络错误，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleConfirm = () => {
    if (parsedResult && onConfirm) {
      onConfirm(parsedResult)
      message.success('已确认参数，开始规划行程')
    }
  }

  const handlePreset = (text) => {
    setInputValue(text)
  }

  const renderParsedParams = () => {
    if (!parsedResult) return null

    const entries = Object.entries(parsedResult).filter(
      ([key, value]) => value !== null && value !== undefined && value !== '' && value !== false
    )

    if (entries.length === 0) {
      return <Empty description="未能识别有效参数" style={{ margin: '24px 0' }} />
    }

    return (
      <div style={{ marginTop: 16 }}>
        <Divider style={{ margin: '12px 0' }}>
          <Text type="secondary" style={{ fontSize: 13 }}>解析结果</Text>
        </Divider>
        <Row gutter={[12, 12]}>
          {entries.map(([key, value]) => (
            <Col xs={12} sm={8} md={6} key={key}>
              <Card 
                size="small" 
                style={{ 
                  borderRadius: 8,
                  border: '1px solid #e6f7ff',
                  background: '#f0f8ff'
                }}
                bodyStyle={{ padding: '8px 12px' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ fontSize: 16 }}>{PARAM_ICONS[key] || '📌'}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 11, color: '#999' }}>
                      {PARAM_LABELS[key] || key}
                    </div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: '#1677ff' }}>
                      {typeof value === 'boolean' ? (
                        value ? <CheckCircleOutlined style={{ color: '#52c41a' }} /> : <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                      ) : (
                        String(value)
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      </div>
    )
  }

  return (
    <Card
      style={{ 
        borderRadius: 16, 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        border: 'none',
        marginBottom: 24
      }}
      bodyStyle={{ padding: 24 }}
    >
      <div style={{ marginBottom: 16 }}>
        <Title level={4} style={{ color: '#fff', margin: 0 }}>
          <ThunderboltOutlined style={{ marginRight: 8 }} />
          AI 智能行程规划
        </Title>
        <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 13 }}>
          用自然语言描述您的需求，AI 会自动解析参数并生成行程
        </Text>
      </div>

      <Card 
        style={{ borderRadius: 12, background: '#fff' }}
        bodyStyle={{ padding: 16 }}
      >
        <Input.TextArea
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          placeholder="例如：北京3天2晚，预算人均1500，带老人，少走路"
          autoSize={{ minRows: 3, maxRows: 6 }}
          style={{ 
            borderRadius: 8, 
            marginBottom: 12,
            resize: 'none',
            fontSize: 14
          }}
          onPressEnter={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              handleSend()
            }
          }}
        />

        <div style={{ display: 'flex', gap: 8 }}>
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSend}
            loading={loading}
            style={{ 
              borderRadius: 8,
              height: 40,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              flex: 1
            }}
          >
            解析参数
          </Button>
          <Button
            icon={<ThunderboltOutlined />}
            onClick={handleGenerate}
            loading={loading}
            style={{ 
              borderRadius: 8,
              height: 40,
              flex: 1
            }}
          >
            直接生成行程
          </Button>
          <Button
            icon={<ReloadOutlined />}
            onClick={() => {
              setInputValue('')
              setParsedResult(null)
              setError(null)
            }}
            style={{ borderRadius: 8, height: 40 }}
          />
        </div>

        <div style={{ marginTop: 16 }}>
          <Text type="secondary" style={{ fontSize: 12 }}>试试这些示例：</Text>
          <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {PRESET_EXAMPLES.map((example, i) => (
              <Tag
                key={i}
                color="blue"
                style={{ cursor: 'pointer', margin: 0 }}
                onClick={() => handlePreset(example)}
              >
                {example}
              </Tag>
            ))}
          </div>
        </div>
      </Card>

      {loading && (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Spin size="large" />
          <div style={{ marginTop: 12, color: '#fff' }}>AI 正在分析您的需求...</div>
        </div>
      )}

      {error && !loading && (
        <Card style={{ marginTop: 16, borderRadius: 12, background: '#fff2f0', border: '1px solid #ffccc7' }}>
          <Text type="danger">{error}</Text>
        </Card>
      )}

      {parsedResult && !loading && (
        <Card style={{ marginTop: 16, borderRadius: 12 }}>
          {renderParsedParams()}
          
          {onConfirm && (
            <div style={{ marginTop: 16, textAlign: 'right' }}>
              <Space>
                <Button onClick={() => setParsedResult(null)}>重新解析</Button>
                <Button type="primary" onClick={handleConfirm} style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', border: 'none' }}>
                  确认参数并生成行程
                </Button>
              </Space>
            </div>
          )}
        </Card>
      )}
    </Card>
  )
}
