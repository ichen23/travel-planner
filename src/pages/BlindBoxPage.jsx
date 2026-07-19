import { useState, useEffect } from 'react'
import { Card, Row, Col, Select, InputNumber, Button, Tag, Typography, Spin, Empty, Slider, message, Divider } from 'antd'
import { GiftOutlined, ThunderboltOutlined, DollarOutlined, CalendarOutlined, BulbOutlined, ReloadOutlined, ArrowRightOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { getRecommendations } from '../services/trainService'
import dayjs from 'dayjs'

const { Title, Text } = Typography

const THEMES = [
  { value: 'food', label: '🍜 美食探店', keywords: ['成都', '广州', '长沙', '重庆', '武汉', '西安', '南京', '厦门'] },
  { value: 'nature', label: '🏔️ 山水风光', keywords: ['桂林', '黄山', '张家界', '九寨沟', '丽江', '大理', '杭州', '青岛'] },
  { value: 'ancient', label: '🏛️ 古城古镇', keywords: ['西安', '南京', '北京', '苏州', '乌镇', '周庄', '凤凰', '平遥'] },
  { value: 'sea', label: '🏖️ 海滨度假', keywords: ['厦门', '青岛', '大连', '三亚', '烟台', '威海', '北海', '泉州'] },
  { value: 'modern', label: '🏙️ 都市购物', keywords: ['上海', '北京', '广州', '深圳', '成都', '杭州', '南京', '武汉'] },
  { value: 'random', label: '🎲 完全随机', keywords: [] },
]

const SURPRISE_TIPS = [
  '说走就走，才是旅行的真谛！',
  '人生就像一盒巧克力，你永远不知道下一颗是什么味道。',
  '不期而遇的惊喜，才是最好的旅行！',
  '每一次出发，都是新的故事开始。',
  '冒险让你见识到更多风景！',
  '未知的旅途，充满无限可能！',
  '有时候，最好的计划就是没有计划。',
]

export default function BlindBoxPage() {
  const navigate = useNavigate()
  const [fromCity, setFromCity] = useState('北京')
  const [budget, setBudget] = useState(500)
  const [days, setDays] = useState(2)
  const [theme, setTheme] = useState('random')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [isSpinning, setIsSpinning] = useState(false)
  const [currentTip, setCurrentTip] = useState('')

  const generateBlindBox = async () => {
    setIsSpinning(true)
    setResult(null)
    setCurrentTip(SURPRISE_TIPS[Math.floor(Math.random() * SURPRISE_TIPS.length)])

    await new Promise(resolve => setTimeout(resolve, 2000))

    setLoading(true)
    try {
      const date = dayjs().format('YYYY-MM-DD')
      const response = await getRecommendations(fromCity, date, Math.min(days * 3, 8))
      
      if (response.success && response.destinations) {
        let filteredDests = response.destinations
        
        if (theme !== 'random') {
          const themeData = THEMES.find(t => t.value === theme)
          if (themeData && themeData.keywords.length > 0) {
            filteredDests = filteredDests.filter(dest => 
              themeData.keywords.some(kw => dest.city_name?.includes(kw) || dest.name?.includes(kw))
            )
          }
        }

        filteredDests = filteredDests.filter(dest => {
          const price = dest.min_price || dest.price || 0
          return price <= budget * days * 2
        })

        if (filteredDests.length > 0) {
          const randomIndex = Math.floor(Math.random() * Math.min(5, filteredDests.length))
          const selectedDest = filteredDests[randomIndex]
          
          const nearbyAttractions = [
            '当地特色小吃街',
            '历史博物馆',
            '城市地标建筑',
            '夜景打卡点',
            '公园休闲区',
          ]

          const suggestions = {
            food: `去品尝当地特色美食，推荐必吃的${['火锅', '面食', '海鲜', '小吃', '烧烤'][Math.floor(Math.random() * 5)]}！`,
            culture: `参观博物馆了解历史文化，或者去老城区漫步感受当地生活。`,
            nature: `附近有不少自然风光，可以安排半天去郊外踏青。`,
            shopping: `市中心有大型商场和特色小店，适合购物逛街。`,
          }

          setResult({
            destination: selectedDest,
            tripDays: days,
            estimatedBudget: Math.round((selectedDest.min_price || selectedDest.price || 200) * days * 2),
            topAttractions: nearbyAttractions.slice(0, 3),
            suggestion: suggestions[Math.floor(Math.random() * suggestions.length)],
            trainDeparture: fromCity,
            trainArrival: selectedDest.city_name || selectedDest.name,
          })
        } else {
          message.info('暂无符合条件的目的地，已为您推荐热门景点')
          const fallbackDest = response.destinations[0]
          setResult({
            destination: fallbackDest,
            tripDays: days,
            estimatedBudget: budget * days,
            topAttractions: ['当地热门景点', '特色美食街', '城市地标'],
            suggestion: '虽然预算有限，但旅行的意义不在于花费多少！',
            trainDeparture: fromCity,
            trainArrival: fallbackDest.city_name || fallbackDest.name,
          })
        }
      } else {
        message.error('获取目的地失败，请稍后重试')
      }
    } catch (err) {
      message.error('网络错误，请检查网络连接')
    } finally {
      setLoading(false)
      setIsSpinning(false)
    }
  }

  const resetBox = () => {
    setResult(null)
    setCurrentTip('')
  }

  return (
    <div className="page-container">
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <Title level={2}>
          <GiftOutlined /> 高铁旅行盲盒 🎁
        </Title>
        <Text type="secondary">
          输入出发地、预算和天数，随机开启一段说走就走的旅程！
        </Text>
      </div>

      <Row justify="center" style={{ marginBottom: 32 }}>
        <Col xs={24} md={16}>
          <Card 
            style={{ 
              borderRadius: 16, 
              background: isSpinning 
                ? 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)' 
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              boxShadow: isSpinning ? '0 0 40px rgba(252, 182, 159, 0.6)' : '0 4px 20px rgba(102, 126, 234, 0.3)',
              transition: 'all 0.3s',
              transform: isSpinning ? 'scale(1.02)' : 'scale(1)',
            }}
            bodyStyle={{ padding: 40 }}
          >
            {!result && !loading && (
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 80, marginBottom: 24 }}>🎁</div>
                <Title level={3} style={{ color: 'white', marginBottom: 16 }}>准备好了吗？</Title>
                <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 16 }}>
                  点击下方按钮，开启你的旅行盲盒
                </Text>
              </div>
            )}

            {loading && (
              <div style={{ textAlign: 'center' }}>
                <Spin size="large" tip="正在抽取神秘目的地..." />
                <div style={{ marginTop: 24 }}>
                  <Text style={{ color: 'white', fontSize: 18 }}>{currentTip}</Text>
                </div>
                <div style={{ fontSize: 60, marginTop: 24, animation: 'bounce 0.6s infinite' }}>🎲</div>
              </div>
            )}

            {result && !loading && (
              <div>
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                  <div style={{ fontSize: 48, marginBottom: 8 }}>🎉</div>
                  <Title level={3} style={{ color: 'white' }}>恭喜！你的盲盒目的地是</Title>
                </div>

                <Card 
                  style={{ borderRadius: 12, marginBottom: 16, border: 'none' }}
                  bodyStyle={{ padding: 24 }}
                >
                  <div style={{ textAlign: 'center', marginBottom: 20 }}>
                    <Title level={2} style={{ color: '#667eea', margin: 0 }}>
                      {result.destination.city_name || result.destination.name || '神秘目的地'}
                    </Title>
                    <div style={{ marginTop: 8 }}>
                      <Tag color="blue">🚄 {result.trainDeparture} → {result.trainArrival}</Tag>
                      <Tag color="green">📅 {result.tripDays} 天</Tag>
                      <Tag color="orange">💰 约 ¥{result.estimatedBudget}</Tag>
                    </div>
                  </div>

                  <Divider />

                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ display: 'block', marginBottom: 8 }}>🏆 推荐景点</Text>
                    <div>
                      {result.topAttractions.map((attr, i) => (
                        <Tag key={i} style={{ margin: 4 }}>{attr}</Tag>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ display: 'block', marginBottom: 8 }}>💡 旅行小贴士</Text>
                    <Card size="small" style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
                      <Text>{result.suggestion}</Text>
                    </Card>
                  </div>

                  {currentTip && (
                    <div style={{ marginTop: 16, textAlign: 'center' }}>
                      <Text type="italic" style={{ color: '#999' }}>
                        "{currentTip}"
                      </Text>
                    </div>
                  )}
                </Card>

                <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
                  <Button 
                    type="primary" 
                    size="large"
                    icon={<ArrowRightOutlined />}
                    onClick={() => navigate(`/destinations/${result.trainArrival}`)}
                  >
                    查看详情
                  </Button>
                  <Button 
                    size="large"
                    icon={<ReloadOutlined />}
                    onClick={resetBox}
                  >
                    再抽一次
                  </Button>
                </div>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      {!result && !loading && (
        <Row justify="center">
          <Col xs={24} md={16}>
            <Card 
              title={<Text strong><BulbOutlined /> 盲盒设置</Text>}
              style={{ borderRadius: 12 }}
            >
              <Row gutter={[16, 24]}>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>出发城市</Text>
                  <Select
                    value={fromCity}
                    onChange={setFromCity}
                    style={{ width: '100%', marginTop: 8 }}
                    showSearch
                    options={['北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉', '西安', '重庆', '长沙', '郑州'].map(c => ({ value: c, label: c }))}
                  />
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>旅行天数</Text>
                  <div style={{ marginTop: 8 }}>
                    <Slider
                      min={1}
                      max={7}
                      value={days}
                      onChange={setDays}
                      marks={{ 1: '1天', 3: '3天', 5: '5天', 7: '7天' }}
                    />
                  </div>
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>预算范围（每人每天）</Text>
                  <div style={{ marginTop: 8 }}>
                    <InputNumber
                      min={100}
                      max={2000}
                      step={50}
                      value={budget}
                      onChange={setBudget}
                      style={{ width: '100%' }}
                      prefix={<DollarOutlined />}
                      formatter={value => `¥ ${value}`}
                    />
                  </div>
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>旅行主题</Text>
                  <Select
                    value={theme}
                    onChange={setTheme}
                    style={{ width: '100%', marginTop: 8 }}
                    options={THEMES.map(t => ({ value: t.value, label: t.label }))}
                  />
                </Col>
              </Row>

              <div style={{ textAlign: 'center', marginTop: 24 }}>
                <Button
                  type="primary"
                  size="large"
                  icon={<GiftOutlined />}
                  onClick={generateBlindBox}
                  loading={loading}
                  style={{ minWidth: 200, height: 48, fontSize: 16 }}
                >
                  🎁 开启盲盒
                </Button>
              </div>
            </Card>

            <Card style={{ marginTop: 16, borderRadius: 12 }}>
              <Title level={5} style={{ marginBottom: 12 }}>🎲 盲盒玩法说明</Title>
              <ul style={{ paddingLeft: 20 }}>
                <li style={{ marginBottom: 8 }}>设置你的出发城市、预算、天数和感兴趣的主题</li>
                <li style={{ marginBottom: 8 }}>系统会从所有可达目的地中随机为你推荐</li>
                <li style={{ marginBottom: 8 }}>你可以选择查看详情，或者再抽一次</li>
                <li style={{ marginBottom: 8 }}>完全随机主题可能会给你惊喜！</li>
                <li>预算仅作为参考，实际花费以购票为准</li>
              </ul>
            </Card>
          </Col>
        </Row>
      )}

      <style>{`
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </div>
  )
}
