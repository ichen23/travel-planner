import { Row, Col, Card, Typography } from 'antd'
import { RocketOutlined, StarOutlined, ThunderboltOutlined, EnvironmentOutlined, CheckCircleOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import SearchBar from '../components/SearchBar'

const { Title, Paragraph } = Typography

const FEATURES = [
  { icon: <ThunderboltOutlined style={{ fontSize: 32, color: '#ff6b6b' }} />, title: '实时余票查询', desc: '12306数据源，秒级刷新余票状态' },
  { icon: <RocketOutlined style={{ fontSize: 32, color: '#4ecdc4' }} />, title: '智能推荐', desc: '根据高铁时长和偏好推荐合适目的地' },
  { icon: <StarOutlined style={{ fontSize: 32, color: '#ffa502' }} />, title: '精选攻略', desc: '景点、美食、住宿、交通一站式信息' },
  { icon: <EnvironmentOutlined style={{ fontSize: 32, color: '#a55eea' }} />, title: '地图规划', desc: '可视化地图，清晰展示景点位置' },
]

const POPULAR_ROUTES = [
  { from: '北京', to: '上海', time: '4.5h', price: 553 },
  { from: '上海', to: '杭州', time: '1h', price: 73 },
  { from: '广州', to: '深圳', time: '30min', price: 74 },
  { from: '成都', to: '重庆', time: '2h', price: 96 },
  { from: '武汉', to: '长沙', time: '1.5h', price: 164 },
  { from: '西安', to: '郑州', time: '2.5h', price: 230 },
]

const TIPS = [
  '📌 提前7-14天订票价格最优',
  '🎁 学生票可享受75折优惠',
  '🚄 高铁二等座舒适度最高',
  '🍜 车上有免费开水供应',
  '📱 下载12306 APP方便改签',
  '🗺️ 到站后地铁可达市区',
]

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, #f0f5ff 0%, #ffffff 100%)' }}>
      <div className="page-container">
        <div style={{ textAlign: 'center', padding: '60px 24px 32px' }}>
          <Title level={1} style={{ fontSize: 48, marginBottom: 16 }}>
            🚄 高铁时代的<span style={{ color: '#ff6b6b' }}>旅行新方式</span>
          </Title>
          <Paragraph style={{ fontSize: 18, color: '#666', maxWidth: 600, margin: '0 auto' }}>
            输入一个出发城市，帮你找到最合适的旅行目的地
          </Paragraph>
        </div>

        <SearchBar />

        <Row gutter={[24, 24]} style={{ marginTop: 48 }}>
          {FEATURES.map((f, i) => (
            <Col xs={24} sm={12} md={6} key={i}>
              <Card className="card-hover" variant="borderless" style={{ textAlign: 'center', padding: '24px 16px' }}>
                {f.icon}
                <Title level={4} style={{ marginTop: 16, marginBottom: 8 }}>{f.title}</Title>
                <Paragraph type="secondary" style={{ margin: 0 }}>{f.desc}</Paragraph>
              </Card>
            </Col>
          ))}
        </Row>

        <div style={{ marginTop: 48 }}>
          <Title level={3}>🔥 热门高铁线路</Title>
          <Row gutter={[16, 16]}>
            {POPULAR_ROUTES.map((route, i) => (
              <Col xs={12} md={8} lg={4} key={i}>
                <Card
                  className="card-hover"
                  variant="borderless"
                  hoverable
                  onClick={() => navigate(`/trains?from=${route.from}&to=${route.to}&date=${new Date(Date.now() + 7*24*60*60*1000).toISOString().slice(0, 10)}`)}
                  style={{ borderRadius: 12, textAlign: 'center', padding: 16 }}
                >
                  <div style={{ fontSize: 24, fontWeight: 'bold', color: '#1677ff' }}>
                    {route.from} → {route.to}
                  </div>
                  <div style={{ marginTop: 8, color: '#666' }}>
                    🕐 {route.time}
                  </div>
                  <div style={{ marginTop: 4, color: '#ff6b6b', fontWeight: 'bold', fontSize: 18 }}>
                    ¥{route.price}起
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
        </div>

        <div style={{ marginTop: 48, marginBottom: 48 }}>
          <Title level={3}>💡 出行小贴士</Title>
          <Card variant="borderless" style={{ borderRadius: 12 }}>
            <Row gutter={[16, 16]}>
              {TIPS.map((tip, i) => (
                <Col xs={24} sm={12} md={8} key={i}>
                  <div style={{ padding: '8px 0', fontSize: 14 }}>
                    <CheckCircleOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                    {tip}
                  </div>
                </Col>
              ))}
            </Row>
          </Card>
        </div>
      </div>
    </div>
  )
}
