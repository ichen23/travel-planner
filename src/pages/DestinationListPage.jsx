import { useState, useEffect } from 'react'
import { Row, Col, Card, Typography, Spin, Empty, Select, Slider, message } from 'antd'
import { useSearchParams } from 'react-router-dom'
import { getRecommendations } from '../services/destinationService'
import DestinationCard from '../components/DestinationCard'
import { PREFERENCES, DURATION_OPTIONS } from '../utils/constants'

const { Title, Text } = Typography

export default function DestinationListPage() {
  const [params] = useSearchParams()
  const [fromCity, setFromCity] = useState(params.get('from') || '')
  const [date, setDate] = useState(params.get('date') || '')
  const [duration, setDuration] = useState(Number(params.get('duration')) || 3)
  const [preference, setPreference] = useState(params.get('preference') || '')
  const [destinations, setDestinations] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const fetchData = async () => {
    if (!fromCity || !date) {
      message.warning('请先在首页选择出发城市和日期')
      return
    }
    setLoading(true)
    setSearched(true)
    try {
      const result = await getRecommendations(fromCity, date, duration, preference)
      if (result.success) {
        setDestinations(result.destinations)
      } else {
        message.error('获取推荐失败')
      }
    } catch (err) {
      message.error('网络错误，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (fromCity && date) {
      fetchData()
    }
  }, [])

  return (
    <div className="page-container">
      <Title level={2} style={{ marginBottom: 8 }}>
        推荐目的地 - 从 <Text type="secondary">{fromCity}</Text> 出发
      </Title>
      {date && (
        <Text type="secondary" style={{ display: 'block', marginBottom: 24 }}>
          出行日期: {date} | 最大高铁行程: {duration}小时 | 偏好: {preference || '综合推荐'}
        </Text>
      )}

      <Card size="small" style={{ marginBottom: 24, borderRadius: 12 }}>
        <Row gutter={16} align="middle">
          <Col xs={24} sm={8} md={6}>
            <Text>最大高铁行程: </Text>
            <Select
              value={duration}
              onChange={(v) => { setDuration(v); fetchData() }}
              options={DURATION_OPTIONS}
              style={{ width: 120 }}
            />
          </Col>
          <Col xs={24} sm={8} md={6}>
            <Text>偏好类型: </Text>
            <Select
              value={preference}
              onChange={(v) => { setPreference(v); fetchData() }}
              options={PREFERENCES}
              style={{ width: 120 }}
            />
          </Col>
          <Col xs={24} sm={8} md={12} style={{ textAlign: 'right' }}>
            <Text type="secondary">
              已找到 <Text strong>{destinations.length}</Text> 个推荐目的地
            </Text>
          </Col>
        </Row>
      </Card>

      {loading && <Spin style={{ display: 'block', margin: '80px auto' }} size="large" />}

      {!loading && searched && destinations.length === 0 && (
        <Empty
          description="没有符合条件的目的地，试试放宽时间限制或更换出发城市"
          style={{ margin: '80px 0' }}
        />
      )}

      {!loading && destinations.length > 0 && (
        <Row gutter={[16, 16]}>
          {destinations.map((d, i) => (
            <Col xs={24} sm={12} md={8} lg={6} key={i}>
              <DestinationCard dest={d} />
            </Col>
          ))}
        </Row>
      )}

      {!searched && (
        <Card style={{ textAlign: 'center', padding: 48, borderRadius: 12 }}>
          <Empty
            description="请先在首页选择出发城市和日期，然后点击搜索"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      )}
    </div>
  )
}
