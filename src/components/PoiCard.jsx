import { useState } from 'react'
import { Card, Tag, Typography, Rate, Space, Button, Image, Tooltip } from 'antd'
import { StarOutlined, EnvironmentOutlined, ClockCircleOutlined, DollarOutlined, PhoneOutlined, ThunderboltOutlined } from '@ant-design/icons'

const { Text, Paragraph } = Typography

const PoiCard = ({ poi, index, type, onClick, compact = false }) => {
  const [imageError, setImageError] = useState(false)
  
  const colors = {
    attraction: '#ff6b6b',
    food: '#ffa500',
    hotel: '#4ecdc4'
  }
  
  const labels = {
    attraction: '景点',
    food: '美食',
    hotel: '住宿'
  }
  
  const color = colors[type] || '#666'
  const label = labels[type] || 'POI'
  const firstPhoto = poi?.photos?.[0]
  const isRealtime = poi?.id && poi?.lng
  
  return (
    <Card
      hoverable
      className="poi-card"
      style={{
        marginBottom: 12,
        borderRadius: 12,
        overflow: 'hidden',
        border: `1px solid ${isRealtime ? '#52c41a' : '#e8e8e8'}`,
        boxShadow: isRealtime ? '0 2px 12px rgba(82, 196, 26, 0.15)' : '0 2px 8px rgba(0,0,0,0.08)',
        transition: 'all 0.3s ease'
      }}
      onClick={() => onClick && onClick(poi)}
      styles={{ body: { padding: 0 } }}
    >
      {!compact && firstPhoto && !imageError && (
        <div style={{ position: 'relative', height: 120, overflow: 'hidden' }}>
          <img
            src={firstPhoto}
            alt={poi.name}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            onError={() => setImageError(true)}
          />
          <div
            style={{
              position: 'absolute',
              top: 8,
              left: 8,
              background: color,
              color: 'white',
              padding: '2px 10px',
              borderRadius: 12,
              fontSize: 12,
              fontWeight: 500
            }}
          >
            {label} {index + 1}
          </div>
          {isRealtime && (
            <div
              style={{
                position: 'absolute',
                top: 8,
                right: 8,
                background: '#52c41a',
                color: 'white',
                padding: '2px 8px',
                borderRadius: 8,
                fontSize: 11,
                display: 'flex',
                alignItems: 'center',
                gap: 2
              }}
            >
              <ThunderboltOutlined />
              实时
            </div>
          )}
        </div>
      )}
      
      {!compact && !firstPhoto && (
        <div
          style={{
            height: 80,
            background: `linear-gradient(135deg, ${color} 0%, ${color}dd 100%)`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: 24
          }}
        >
          {label} {index + 1}
        </div>
      )}
      
      <div style={{ padding: compact ? 12 : 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <Text strong style={{ fontSize: 15 }}>{poi.name}</Text>
          {poi.rating > 0 && (
            <Space size={4}>
              <Rate disabled value={poi.rating / 2} allowHalf style={{ fontSize: 12 }} />
              <Text type="secondary" style={{ fontSize: 12 }}>{poi.rating.toFixed(1)}</Text>
            </Space>
          )}
        </div>
        
        {poi.address && !compact && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#999', fontSize: 12, marginBottom: 8 }}>
            <EnvironmentOutlined />
            <span style={{ 
              overflow: 'hidden', 
              textOverflow: 'ellipsis', 
              whiteSpace: 'nowrap',
              maxWidth: '100%'
            }}>
              {poi.address}
            </span>
          </div>
        )}
        
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
          {poi.cost > 0 && (
            <Tooltip title="人均消费">
              <Tag icon={<DollarOutlined />} color="gold" style={{ margin: 0 }}>
                ¥{poi.cost}
              </Tag>
            </Tooltip>
          )}
          {poi.open_time && (
            <Tooltip title={`营业时间: ${typeof poi.open_time === 'string' ? poi.open_time : poi.open_time[0] || '全天'}`}>
              <Tag icon={<ClockCircleOutlined />} color="blue" style={{ margin: 0 }}>
                {typeof poi.open_time === 'string' ? poi.open_time.slice(0, 15) + (poi.open_time.length > 15 ? '...' : '') : '营业时间'}
              </Tag>
            </Tooltip>
          )}
          {poi.tel && !compact && (
            <Tooltip title={poi.tel}>
              <Tag icon={<PhoneOutlined />} color="purple" style={{ margin: 0 }}>
                电话
              </Tag>
            </Tooltip>
          )}
        </div>
        
        {poi.type && !compact && (
          <div style={{ marginTop: 8, fontSize: 11, color: '#bbb' }}>
            {poi.type.split(';')[0]}
          </div>
        )}
      </div>
    </Card>
  )
}

export default PoiCard
