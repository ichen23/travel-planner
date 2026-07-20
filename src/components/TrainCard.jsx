import { Card, Tag, Button, Row, Col, Space, message } from 'antd'
import { HeartOutlined, HeartFilled, ArrowRightOutlined } from '@ant-design/icons'
import { useState } from 'react'
import { useFavoritesStore } from '../stores'
import { formatPrice, formatDuration, getAvailabilityColor } from '../utils/helpers'

export default function TrainCard({ train }) {
  const [liked, setLiked] = useState(false)
  const addToFavs = useFavoritesStore(s => s.addToFavorites)

  const handleFavorite = () => {
    addToFavs('trains', train)
    setLiked(true)
    message.success('已收藏')
  }

  const secAvail = train.availability?.second_seat
  const firstAvail = train.availability?.first_seat
  const secColor = getAvailabilityColor(secAvail)
  const firstColor = getAvailabilityColor(firstAvail)

  return (
    <Card
      className="card-hover"
      variant="borderless"
      style={{ borderRadius: 12, marginBottom: 12 }}
      bodyStyle={{ padding: 20 }}
    >
      <Row gutter={16} align="middle">
        <Col xs={6} sm={4}>
          <div style={{ fontSize: 24, fontWeight: 'bold', color: train.is_high ? '#ff6b6b' : '#1677ff' }}>
            {train.train_no}
          </div>
          <Tag color={train.is_high ? 'red' : 'blue'} style={{ marginTop: 4 }}>
            {train.is_high ? '高铁' : train.type || '普快'}
          </Tag>
        </Col>
        
        <Col xs={12} sm={10}>
          <Space align="center" size="large" style={{ width: '100%', justifyContent: 'center' }}>
            <div style={{ textAlign: 'center', minWidth: 60 }}>
              <div style={{ fontSize: 20, fontWeight: 'bold' }}>{train.departure_time}</div>
              <div style={{ color: '#999', fontSize: 12 }}>{train.from}</div>
            </div>
            <div style={{ textAlign: 'center', color: '#999' }}>
              <ArrowRightOutlined />
              <div style={{ fontSize: 11, marginTop: 4 }}>{train.duration}</div>
            </div>
            <div style={{ textAlign: 'center', minWidth: 60 }}>
              <div style={{ fontSize: 20, fontWeight: 'bold' }}>{train.arrival_time}</div>
              <div style={{ color: '#999', fontSize: 12 }}>{train.to}</div>
            </div>
          </Space>
        </Col>
        
        <Col xs={6} sm={6}>
          <Space size={[4, 4]} wrap>
            <Tag color={secColor} style={{ marginRight: 4 }}>二等座 {secAvail || '-'}</Tag>
            <Tag color={firstColor} style={{ marginRight: 4 }}>一等座 {firstAvail || '-'}</Tag>
            {train.availability?.business_seat && train.availability.business_seat !== '--' && (
              <Tag color="purple">商务座 {train.availability.business_seat}</Tag>
            )}
            {train.availability?.no_seat && train.availability.no_seat !== '--' && (
              <Tag color="orange">无座 {train.availability.no_seat}</Tag>
            )}
          </Space>
        </Col>
        
        <Col span={4} style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 22, color: '#ff6b6b', fontWeight: 'bold' }}>
            {formatPrice(train.prices?.second_seat)}
          </div>
          <Button
            type="text"
            size="small"
            icon={liked ? <HeartFilled style={{ color: '#ff4d4f' }} /> : <HeartOutlined />}
            onClick={handleFavorite}
          >
            {liked ? '已收藏' : '收藏'}
          </Button>
        </Col>
      </Row>
    </Card>
  )
}
