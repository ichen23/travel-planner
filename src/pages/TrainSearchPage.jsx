import { useState, useEffect, useMemo } from 'react'
import { Input, DatePicker, Button, Row, Col, Card, Typography, Empty, Spin, Tag, message, Switch, Select, Space } from 'antd'
import { SearchOutlined, SwapOutlined, ThunderboltOutlined, FilterOutlined, SortAscendingOutlined } from '@ant-design/icons'
import { useSearchParams } from 'react-router-dom'
import dayjs from 'dayjs'
import { searchTrains } from '../services/trainService'
import TrainCard from '../components/TrainCard'
import { HOT_CITIES } from '../utils/constants'

const { Title, Text } = Typography

export default function TrainSearchPage() {
  const [params, setParams] = useSearchParams()
  const [from, setFrom] = useState(params.get('from') || '')
  const [to, setTo] = useState(params.get('to') || '')
  const [date, setDate] = useState(params.get('date') ? dayjs(params.get('date')) : dayjs().add(7, 'day'))
  const [isHigh, setIsHigh] = useState(true)
  const [trains, setTrains] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const [onlyHasSeat, setOnlyHasSeat] = useState(false)
  const [sortBy, setSortBy] = useState('time')

  const filteredAndSortedTrains = useMemo(() => {
    let result = [...trains]

    if (onlyHasSeat) {
      result = result.filter(train => {
        const avail = train.availability || {}
        const hasSeat = (avail.second_seat && avail.second_seat !== '无' && avail.second_seat !== '--' && parseInt(avail.second_seat) > 0) ||
                        (avail.first_seat && avail.first_seat !== '无' && avail.first_seat !== '--' && parseInt(avail.first_seat) > 0) ||
                        (avail.business_seat && avail.business_seat !== '无' && avail.business_seat !== '--' && parseInt(avail.business_seat) > 0)
        return hasSeat
      })
    }

    if (sortBy === 'time') {
      result.sort((a, b) => a.departure_time.localeCompare(b.departure_time))
    } else if (sortBy === 'price') {
      result.sort((a, b) => {
        const priceA = a.prices?.second_seat || a.prices?.first_seat || 99999
        const priceB = b.prices?.second_seat || b.prices?.first_seat || 99999
        return priceA - priceB
      })
    } else if (sortBy === 'duration') {
      result.sort((a, b) => {
        const parseDuration = (d) => {
          if (!d) return 9999
          const parts = d.split(':')
          return parseInt(parts[0]) * 60 + parseInt(parts[1] || 0)
        }
        return parseDuration(a.duration) - parseDuration(b.duration)
      })
    }

    return result
  }, [trains, onlyHasSeat, sortBy])

  const handleSearch = async () => {
    if (!from || !to) {
      message.warning('请输入出发和到达城市')
      return
    }
    setLoading(true)
    setSearched(true)
    try {
      const result = await searchTrains(from, to, date.format('YYYY-MM-DD'), isHigh)
      if (result.success) {
        setTrains(result.trains)
      } else {
        message.error(result.message || '查询失败')
        setTrains([])
      }
    } catch (err) {
      message.error('网络错误，请稍后重试')
      setTrains([])
    } finally {
      setLoading(false)
    }
  }

  const swap = () => {
    setFrom(to)
    setTo(from)
  }

  const quickSearch = (city) => {
    if (!from) setFrom(city)
    else if (!to) setTo(city)
    else {
      setFrom(city)
      setTo('')
    }
  }

  useEffect(() => {
    if (from && to && params.get('from')) {
      handleSearch()
    }
  }, [])

  return (
    <div className="page-container">
      <Title level={2} style={{ marginBottom: 24 }}>
        <ThunderboltOutlined /> 实时火车票查询
      </Title>

      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        <Row gutter={[16, 16]} align="middle">
          <Col xs={24} sm={7}>
            <Input
              size="large"
              placeholder="出发城市"
              value={from}
              onChange={e => setFrom(e.target.value)}
              onPressEnter={handleSearch}
              style={{ borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={2} style={{ textAlign: 'center' }}>
            <Button icon={<SwapOutlined />} onClick={swap} shape="circle" />
          </Col>
          <Col xs={24} sm={7}>
            <Input
              size="large"
              placeholder="到达城市"
              value={to}
              onChange={e => setTo(e.target.value)}
              onPressEnter={handleSearch}
              style={{ borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={4}>
            <DatePicker
              value={date}
              onChange={setDate}
              disabledDate={d => d && d.isBefore(dayjs())}
              style={{ width: '100%', borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={4}>
            <Button
              type="primary"
              size="large"
              icon={<SearchOutlined />}
              onClick={handleSearch}
              style={{ width: '100%', borderRadius: 8 }}
            >
              查询
            </Button>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: 16 }} align="middle">
          <Col>
            <Text>只看高铁: </Text>
            <Switch checked={isHigh} onChange={setIsHigh} />
          </Col>
          <Col>
            <Text>只看有座: </Text>
            <Switch checked={onlyHasSeat} onChange={setOnlyHasSeat} />
          </Col>
          <Col>
            <Space>
              <Text><SortAscendingOutlined /> 排序:</Text>
              <Select
                value={sortBy}
                onChange={setSortBy}
                style={{ width: 120 }}
                options={[
                  { value: 'time', label: '出发时间' },
                  { value: 'price', label: '价格最低' },
                  { value: 'duration', label: '历时最短' },
                ]}
              />
            </Space>
          </Col>
        </Row>

        <Row style={{ marginTop: 16 }}>
          <Col span={24}>
            <Text type="secondary">快捷选择: </Text>
            {HOT_CITIES.slice(0, 12).map(city => (
              <Tag
                key={city}
                color={from === city || to === city ? 'blue' : 'default'}
                style={{ cursor: 'pointer', margin: '4px' }}
                onClick={() => quickSearch(city)}
              >
                {city}
              </Tag>
            ))}
          </Col>
        </Row>
      </Card>

      {loading && <Spin style={{ display: 'block', margin: '80px auto' }} size="large" />}

      {!loading && searched && trains.length === 0 && (
        <Empty description="未找到相关车次，请尝试其他日期或线路" style={{ margin: '80px 0' }} />
      )}

      {!loading && trains.length > 0 && (
        <>
          <div style={{ marginBottom: 16 }}>
            <Text type="secondary">
              <FilterOutlined /> 
              共 <Text strong>{trains.length}</Text> 趟
              {onlyHasSeat && <Tag color="green" style={{ marginLeft: 8 }}>有座 {filteredAndSortedTrains.length}</Tag>}
              {from && to && <Text type="secondary"> | {from} → {to} | {date.format('YYYY-MM-DD')}</Text>}
            </Text>
          </div>
          {filteredAndSortedTrains.length === 0 ? (
            <Empty description="没有符合条件的车次" />
          ) : (
            filteredAndSortedTrains.map((train, i) => (
              <TrainCard key={i} train={train} />
            ))
          )}
        </>
      )}

      {!loading && !searched && (
        <Card style={{ textAlign: 'center', padding: 48, borderRadius: 12 }}>
          <Empty
            description="输入出发地、到达地和日期，查询实时车票信息"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      )}
    </div>
  )
}
