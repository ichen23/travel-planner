import { Card, Tag, Typography, Row, Col, Tooltip, Button, Collapse } from 'antd'
import { ClockCircleOutlined, DollarOutlined, StarOutlined, EnvironmentOutlined, RightOutlined, CheckCircleOutlined, WarningOutlined, CameraOutlined, ShopOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Text, Title } = Typography

const getGradient = (cityName) => {
  const colors = [
    ['#667eea', '#764ba2'],
    ['#f093fb', '#f5576c'],
    ['#4facfe', '#00f2fe'],
    ['#43e97b', '#38f9d7'],
    ['#fa709a', '#fee140'],
    ['#a8edea', '#fed6e3'],
    ['#ff9a9e', '#fecfef'],
    ['#ffecd2', '#fcb69f'],
    ['#a1c4fd', '#c2e9fb'],
    ['#d4fc79', '#96e6a1'],
    ['#ff6b6b', '#feca57'],
    ['#48dbfb', '#ff9ff3'],
    ['#54a0ff', '#5f27cd'],
    ['#00d2d3', '#54a0ff'],
    ['#ff9ff3', '#feca57'],
  ]
  const index = cityName.charCodeAt(0) % colors.length
  return colors[index]
}

const RatingStars = ({ rating }) => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
      <StarOutlined style={{ color: '#faad14' }} />
      <Text strong style={{ color: '#faad14' }}>{rating}</Text>
    </div>
  )
}

const QuickInfo = ({ duration, price, rating }) => {
  return (
    <div style={{
      display: 'flex',
      gap: 12,
      alignItems: 'center',
      padding: '12px 16px',
      background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
      borderRadius: 12,
      marginBottom: 12,
    }}>
      <div style={{ flex: 1, textAlign: 'center' }}>
        <ClockCircleOutlined style={{ fontSize: 20, color: '#1677ff', marginBottom: 4 }} />
        <div style={{ fontSize: 14, fontWeight: 600 }}>{duration}</div>
        <div style={{ fontSize: 11, color: '#999' }}>高铁时间</div>
      </div>
      <div style={{ width: 1, height: 32, background: '#d9d9d9' }} />
      <div style={{ flex: 1, textAlign: 'center' }}>
        <DollarOutlined style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 4 }} />
        <div style={{ fontSize: 14, fontWeight: 600 }}>
          {price && price !== '以实际为准' ? `¥${price}` : '以实际为准'}
        </div>
        <div style={{ fontSize: 11, color: '#999' }}>参考票价</div>
      </div>
      <div style={{ width: 1, height: 32, background: '#d9d9d9' }} />
      <div style={{ flex: 1, textAlign: 'center' }}>
        <StarOutlined style={{ fontSize: 20, color: '#faad14', marginBottom: 4 }} />
        <div style={{ fontSize: 14, fontWeight: 600 }}>{rating || 4.5}</div>
        <div style={{ fontSize: 11, color: '#999' }}>推荐指数</div>
      </div>
    </div>
  )
}

const TipsSection = ({ tips }) => {
  if (!tips) return null

  const hasContent = tips.food?.length > 0 || tips.attractions?.length > 0 || 
                     tips.avoid_traps?.length > 0 || tips.best_photo_spots?.length > 0 ||
                     tips.clothing_advice || tips.souvenirs?.length > 0 || tips.budget

  if (!hasContent) return null

  return (
    <Collapse
      size="small"
      ghost
      style={{ marginTop: 8 }}
      items={[
        {
          key: 'tips',
          label: (
            <Text type="secondary" style={{ fontSize: 12 }}>
              查看详细攻略
            </Text>
          ),
          children: (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {tips.food && tips.food.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#ff6b6b', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <ShopOutlined /> 必吃美食
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {tips.food.slice(0, 6).map((item, i) => (
                      <Tag key={i} color="volcano" style={{ fontSize: 11 }}>
                        {item}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}

              {tips.food_spots && tips.food_spots.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#fa8c16', marginBottom: 6 }}>
                    美食好去处
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {tips.food_spots.slice(0, 4).map((item, i) => (
                      <Tag key={i} color="orange" style={{ fontSize: 11 }}>{item}</Tag>
                    ))}
                  </div>
                </div>
              )}

              {tips.attractions && tips.attractions.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#1677ff', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <EnvironmentOutlined /> 必去景点
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {tips.attractions.slice(0, 6).map((item, i) => (
                      <Tag key={i} color="blue" style={{ fontSize: 11 }}>
                        {item}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}

              {tips.avoid_traps && tips.avoid_traps.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#faad14', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <WarningOutlined /> 避坑指南
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {tips.avoid_traps.slice(0, 3).map((item, i) => (
                      <Text key={i} type="warning" style={{ fontSize: 11 }}>⚠ {item}</Text>
                    ))}
                  </div>
                </div>
              )}

              {tips.best_photo_spots && tips.best_photo_spots.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#52c41a', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <CameraOutlined /> 拍照好去处
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {tips.best_photo_spots.slice(0, 4).map((item, i) => (
                      <Tag key={i} color="success" style={{ fontSize: 11 }}>{item}</Tag>
                    ))}
                  </div>
                </div>
              )}

              {tips.clothing_advice && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#722ed1', marginBottom: 6 }}>
                    穿衣建议
                  </div>
                  <Text style={{ fontSize: 11, color: '#666' }}>{tips.clothing_advice}</Text>
                </div>
              )}

              {tips.souvenirs && tips.souvenirs.length > 0 && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#13c2c2', marginBottom: 6 }}>
                    推荐特产
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                    {tips.souvenirs.slice(0, 4).map((item, i) => (
                      <Tag key={i} color="cyan" style={{ fontSize: 11 }}>{item}</Tag>
                    ))}
                  </div>
                </div>
              )}

              {tips.budget && (
                <div>
                  <div style={{ fontSize: 12, fontWeight: 600, color: '#eb2f96', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                    <DollarOutlined /> 预算参考
                  </div>
                  <div style={{ display: 'flex', gap: 8 }}>
                    {tips.budget.economy && (
                      <div style={{ flex: 1, fontSize: 10, padding: '4px 6px', background: '#f6ffed', borderRadius: 4 }}>
                        💰经济: {tips.budget.economy.total_daily || '200-400'}
                      </div>
                    )}
                    {tips.budget.mid && (
                      <div style={{ flex: 1, fontSize: 10, padding: '4px 6px', background: '#fff7e6', borderRadius: 4 }}>
                        💴中等: {tips.budget.mid.total_daily || '400-800'}
                      </div>
                    )}
                    {tips.budget.luxury && (
                      <div style={{ flex: 1, fontSize: 10, padding: '4px 6px', background: '#fff0f6', borderRadius: 4 }}>
                        💎豪华: {tips.budget.luxury.total_daily || '1000+'}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )
        }
      ]}
    />
  )
}

const BudgetBar = ({ avgDailyBudget }) => {
  if (!avgDailyBudget) return null
  
  let level = '经济'
  let color = '#52c41a'
  if (avgDailyBudget >= 800) { level = '豪华'; color = '#eb2f96' }
  else if (avgDailyBudget >= 500) { level = '中等'; color = '#faad14' }
  
  return (
    <div style={{ 
      display: 'inline-flex', 
      alignItems: 'center', 
      gap: 4,
      padding: '2px 8px',
      background: `${color}20`,
      borderRadius: 4,
      fontSize: 11,
      color: color,
    }}>
      <DollarOutlined />
      <span>日均 {avgDailyBudget} ({level})</span>
    </div>
  )
}

export default function DestinationCard({ dest }) {
  const navigate = useNavigate()
  const [c1, c2] = getGradient(dest.city)

  const tips = dest.tips

  return (
    <Card
      className="destination-card"
      hoverable
      variant="borderless"
      style={{
        borderRadius: 16,
        overflow: 'hidden',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        boxShadow: '0 2px 12px rgba(0,0,0,0.08)',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
      styles={{ body: { padding: 0, display: 'flex', flexDirection: 'column', height: '100%' } }}
      onClick={() => navigate(`/destinations/${dest.city}`)}
    >
      <div style={{
        height: 90,
        background: `linear-gradient(135deg, ${c1}, ${c2})`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}>
        <div style={{
          fontSize: 32,
          fontWeight: 700,
          color: 'white',
          textShadow: '2px 2px 8px rgba(0,0,0,0.2)',
        }}>
          {dest.city}
        </div>
        
        {dest.best_time && (
          <div style={{
            position: 'absolute',
            bottom: 8,
            left: 12,
            fontSize: 11,
            color: 'rgba(255,255,255,0.9)',
            background: 'rgba(0,0,0,0.2)',
            padding: '2px 8px',
            borderRadius: 4,
          }}>
            最佳: {dest.best_time.split('、')[0]}
          </div>
        )}
        
        <BudgetBar avgDailyBudget={dest.avg_daily_budget} />
      </div>

      <div style={{ padding: 16, flex: 1, display: 'flex', flexDirection: 'column' }}>
        <QuickInfo 
          duration={dest.duration} 
          price={dest.price} 
          rating={dest.rating} 
        />

        {dest.description && (
          <div style={{
            fontSize: 13,
            color: '#666',
            marginBottom: 12,
            lineHeight: 1.5,
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}>
            {dest.description}
          </div>
        )}

        {dest.highlights && (
          <div style={{ marginBottom: 12 }}>
            <Text type="secondary" style={{ fontSize: 11, marginBottom: 4, display: 'block' }}>精选景点</Text>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {(Array.isArray(dest.highlights) ? dest.highlights : dest.highlights.split(/[、,，]/)).slice(0, 3).map((h, i) => (
                <Tag key={i} color="cyan" style={{ fontSize: 11 }}>{h}</Tag>
              ))}
            </div>
          </div>
        )}

        {dest.tags && dest.tags.length > 0 && (
          <div style={{ marginBottom: 8 }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {dest.tags.slice(0, 4).map((tag, i) => (
                <Tag key={i} color="geekblue" style={{ fontSize: 11 }}>
                  {tag}
                </Tag>
              ))}
            </div>
          </div>
        )}

        <TipsSection tips={tips} />

        <div style={{ marginTop: 'auto' }}>
          <div 
            onClick={(e) => {
              e.stopPropagation()
              navigate(`/destinations/${dest.city}`)
            }}
            style={{
              marginTop: 12,
              padding: '10px 16px',
              background: 'linear-gradient(90deg, #667eea, #764ba2)',
              borderRadius: 10,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 8,
              color: 'white',
              fontWeight: 500,
              fontSize: 14,
              transition: 'all 0.3s',
              cursor: 'pointer',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)'
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = 'none'
            }}
          >
            <span><EnvironmentOutlined /> 查看完整攻略</span>
            <RightOutlined style={{ fontSize: 12 }} />
          </div>
        </div>
      </div>
    </Card>
  )
}
