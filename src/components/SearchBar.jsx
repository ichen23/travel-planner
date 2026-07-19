import { useState } from 'react'
import { Input, DatePicker, Select, Button, Row, Col, Card, message } from 'antd'
import { SearchOutlined, EnvironmentOutlined, SwapOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import dayjs from 'dayjs'
import { HOT_CITIES, PREFERENCES, DURATION_OPTIONS } from '../utils/constants'

export default function SearchBar({ showPreference = true }) {
  const [fromCity, setFromCity] = useState('')
  const [toCity, setToCity] = useState('')
  const [date, setDate] = useState(dayjs().add(7, 'day'))
  const [duration, setDuration] = useState(3)
  const [preference, setPreference] = useState('')
  const [mode, setMode] = useState('search')
  const navigate = useNavigate()

  const handleSearch = () => {
    if (mode === 'search') {
      if (!fromCity || !toCity) {
        message.error('请选择出发和到达城市')
        return
      }
      const params = new URLSearchParams({
        from: fromCity,
        to: toCity,
        date: date.format('YYYY-MM-DD'),
      })
      navigate(`/trains?${params.toString()}`)
    } else {
      if (!fromCity) {
        message.error('请选择出发城市')
        return
      }
      const params = new URLSearchParams({
        from: fromCity,
        date: date.format('YYYY-MM-DD'),
        duration: duration,
        preference: preference,
      })
      navigate(`/destinations?${params.toString()}`)
    }
  }

  const swap = () => {
    setFromCity(toCity)
    setToCity(fromCity)
  }

  return (
    <Card style={{ marginBottom: 24, borderRadius: 16, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }} variant="borderless">
      <Row gutter={[16, 16]} align="middle" style={{ padding: '16px 16px 0' }}>
        <Col>
          <Button
            type={mode === 'search' ? 'primary' : 'default'}
            onClick={() => setMode('search')}
            ghost={mode !== 'search'}
          >
            查车票
          </Button>
        </Col>
        <Col>
          <Button
            type={mode === 'discover' ? 'primary' : 'default'}
            onClick={() => setMode('discover')}
            ghost={mode !== 'discover'}
          >
            发现目的地
          </Button>
        </Col>
      </Row>

      {mode === 'search' ? (
        <Row gutter={[16, 16]} align="middle" style={{ padding: '16px' }}>
          <Col xs={24} sm={10}>
            <Input
              size="large"
              placeholder="出发城市"
              prefix={<EnvironmentOutlined />}
              value={fromCity}
              onChange={e => setFromCity(e.target.value)}
              onPressEnter={handleSearch}
              style={{ borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={2} style={{ textAlign: 'center' }}>
            <Button icon={<SwapOutlined />} onClick={swap} shape="circle" />
          </Col>
          <Col xs={24} sm={10}>
            <Input
              size="large"
              placeholder="到达城市"
              value={toCity}
              onChange={e => setToCity(e.target.value)}
              onPressEnter={handleSearch}
              style={{ borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={2}>
            <DatePicker
              value={date}
              onChange={setDate}
              disabledDate={d => d && d.isBefore(dayjs())}
              style={{ width: '100%', borderRadius: 8 }}
            />
          </Col>
        </Row>
      ) : (
        <Row gutter={[16, 16]} align="middle" style={{ padding: '16px' }}>
          <Col xs={24} sm={8} md={6}>
            <Input
              size="large"
              placeholder="出发城市"
              prefix={<EnvironmentOutlined />}
              value={fromCity}
              onChange={e => setFromCity(e.target.value)}
              style={{ borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={8} md={5}>
            <DatePicker
              size="large"
              value={date}
              onChange={setDate}
              disabledDate={d => d && d.isBefore(dayjs())}
              style={{ width: '100%', borderRadius: 8 }}
            />
          </Col>
          <Col xs={24} sm={8} md={4}>
            <Select
              size="large"
              value={duration}
              onChange={setDuration}
              options={DURATION_OPTIONS}
              style={{ width: '100%', borderRadius: 8 }}
            />
          </Col>
          {showPreference && (
            <Col xs={24} sm={8} md={4}>
              <Select
                size="large"
                value={preference}
                onChange={setPreference}
                options={PREFERENCES}
                style={{ width: '100%', borderRadius: 8 }}
              />
            </Col>
          )}
          <Col xs={24} sm={showPreference ? 24 : 8} md={showPreference ? 5 : 5}>
            <Button
              type="primary"
              size="large"
              icon={<SearchOutlined />}
              onClick={handleSearch}
              style={{ width: '100%', height: 40, borderRadius: 8, background: '#ff6b6b', border: 'none' }}
            >
              发现目的地
            </Button>
          </Col>
        </Row>
      )}

      <Row gutter={[8, 8]} style={{ padding: '0 16px 16px' }}>
        <Col span={24}>
          <span style={{ color: '#fff', marginRight: 8, fontSize: 13 }}>热门城市:</span>
          {HOT_CITIES.slice(0, 10).map(city => (
            <Button
              key={city}
              size="small"
              ghost
              style={{ marginRight: 6, marginBottom: 4 }}
              onClick={() => {
                if (mode === 'search') {
                  if (!fromCity) setFromCity(city)
                  else if (!toCity) setToCity(city)
                  else setFromCity(city)
                } else {
                  setFromCity(city)
                }
              }}
            >
              {city}
            </Button>
          ))}
        </Col>
      </Row>
    </Card>
  )
}
