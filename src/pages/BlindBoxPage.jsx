import { useState, useEffect, useCallback } from 'react'
import { Card, Row, Col, Select, InputNumber, Button, Tag, Typography, Spin, Empty, Slider, message, Divider, Avatar, Progress } from 'antd'
import { GiftOutlined, ThunderboltOutlined, DollarOutlined, CalendarOutlined, BulbOutlined, ReloadOutlined, ArrowRightOutlined, StarOutlined, FireOutlined, CrownOutlined, RocketOutlined } from '@ant-design/icons'
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
  '旅行是消除仇恨和偏见的最好方式。',
  '世界那么大，我想去看看！',
  '生活不止眼前的苟且，还有诗和远方！',
  '最好的风景，永远在路上。',
  '读万卷书，行万里路！',
]

const OPENING_ANIMATIONS = [
  { emoji: '🎰', text: '转动命运之轮...' },
  { emoji: '🎲', text: '骰子正在决定...' },
  { emoji: '🎁', text: '打开神秘礼盒...' },
  { emoji: '🔮', text: '水晶球正在预测...' },
  { emoji: '✨', text: '星光闪烁中...' },
  { emoji: '🌙', text: '月光指引方向...' },
  { emoji: '🗺️', text: '地图正在展开...' },
  { emoji: '🎯', text: '瞄准目标...' },
]

const LUCKY_DESTINY = [
  { level: 'SSR', icon: '👑', name: '传说级', color: '#ff6b6b', rate: 0.05, desc: '超级幸运！这是今天最完美的目的地！', multiplier: 2 },
  { level: 'SR', icon: '⭐', name: '稀有级', color: '#ffd93d', rate: 0.15, desc: '非常棒的选择！这个目的地会给你惊喜！', multiplier: 1.5 },
  { level: 'R', icon: '✨', name: '精良级', color: '#6bcb77', rate: 0.3, desc: '不错的选择！这里一定有你喜欢的！', multiplier: 1.2 },
  { level: 'N', icon: '🎲', name: '普通级', color: '#4d96ff', rate: 0.5, desc: '稳妥之选，不会让你失望的！', multiplier: 1 },
]

const ZODIAC_SIGNS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']

const FUNNY_FACTS = [
  '据说99%的人去了这个地方都想再去一次！',
  '这里的美食能让你胖三斤，但值得！',
  '你的钱包准备好了吗？这里会让你忍不住买买买！',
  '记得带充电宝，拍照会拍到停不下来！',
  '这里的日出日落超级治愈！',
  '本地人可能会用奇怪的眼神看你的穿着...',
  '推荐带个空箱子，因为你一定会买很多！',
  '据说这里是网红打卡地，你的朋友圈会爆！',
  '可以考虑带上你的TA，浪漫指数爆表！',
  '单身狗慎入，这里处处是情侣！',
]

const DESTINATION_NAMES = [
  '神秘之城', '美食天堂', '世外桃源', '人间仙境', '宝藏之地',
  '梦想之城', '童话世界', '冒险乐园', '心灵驿站', '摄影圣地',
]

const getRandomItem = (arr) => arr[Math.floor(Math.random() * arr.length)]

const getLuckyRank = () => {
  const rand = Math.random()
  let cumulative = 0
  for (const rank of LUCKY_DESTINY) {
    cumulative += rank.rate
    if (rand <= cumulative) return rank
  }
  return LUCKY_DESTINY[LUCKY_DESTINY.length - 1]
}

const generateLuckyNumbers = () => {
  const count = Math.floor(Math.random() * 3) + 1
  return Array.from({ length: count }, () => Math.floor(Math.random() * 9) + 1)
}

const generateCombinations = (arr, count) => {
  if (!arr || arr.length === 0) return []
  const shuffled = [...arr].sort(() => Math.random() - 0.5)
  return shuffled.slice(0, Math.min(count, arr.length))
}

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
  const [animationData, setAnimationData] = useState(null)

  const generateBlindBox = useCallback(async () => {
    const animation = getRandomItem(OPENING_ANIMATIONS)
    setAnimationData(animation)
    setIsSpinning(true)
    setResult(null)
    setCurrentTip(getRandomItem(SURPRISE_TIPS))

    await new Promise(resolve => setTimeout(resolve, 2500))

    setLoading(true)
    try {
      const date = dayjs().format('YYYY-MM-DD')
      const response = await getRecommendations(fromCity, date, Math.min(days * 3, 8))
      
      if (response.success && response.destinations) {
        let filteredDests = response.destinations.filter(dest => 
          dest.city && dest.tips && dest.tips.attractions && dest.tips.attractions.length > 0
        )

        if (theme !== 'random') {
          const themeData = THEMES.find(t => t.value === theme)
          if (themeData && themeData.keywords.length > 0) {
            filteredDests = filteredDests.filter(dest => 
              themeData.keywords.some(kw => dest.city.includes(kw))
            )
          }
        }

        filteredDests = filteredDests.filter(dest => {
          const avgBudget = dest.avg_daily_budget || 300
          return avgBudget <= budget * 2
        })

        let selectedDest
        if (filteredDests.length > 0) {
          selectedDest = getRandomItem(filteredDests)
        } else {
          const allDests = response.destinations.filter(d => d.city)
          selectedDest = getRandomItem(allDests)
          message.info('预算范围内目的地较少，已为你推荐惊喜选项！')
        }

        const luckyRank = getLuckyRank()
        const luckyNumbers = generateLuckyNumbers()
        const zodiacSign = getRandomItem(ZODIAC_SIGNS)
        const funFact = getRandomItem(FUNNY_FACTS)

        const attractions = selectedDest.tips?.attractions || selectedDest.highlights?.split('、') || ['当地热门景点']
        const foods = selectedDest.tips?.food || ['当地特色美食']
        const itinerary = selectedDest.itinerary_suggestion || ['第一天：探索城市', '第二天：深度游']

        const luckySuggestions = [
          `🎉 恭喜获得「${luckyRank.level}」评价！这里绝对值得一去！`,
          `🏆 推荐指数：${'⭐'.repeat(Math.floor(selectedDest.rating || 4))}`,
          `🎯 幸运数字：${luckyNumbers.join(' ')}`,
          `${zodiacSign} ${funFact}`,
        ]

        const destinationName = selectedDest.city
        const randomDescNames = getRandomItem(DESTINATION_NAMES)
        
        setResult({
          destination: selectedDest,
          cityName: destinationName,
          tripDays: days,
          estimatedBudget: Math.round((selectedDest.avg_daily_budget || 300) * days),
          topAttractions: generateCombinations(attractions, 4),
          topFoods: generateCombinations(foods, 3),
          itinerary: generateCombinations(itinerary, 2),
          luckyRank: luckyRank,
          luckyNumbers: luckyNumbers,
          zodiacSign: zodiacSign,
          funFact: funFact,
          rating: selectedDest.rating || 4.0,
          tags: selectedDest.tags || [],
          description: selectedDest.description || `${destinationName}是一个很棒的旅游目的地`,
          bestTime: selectedDest.best_time || '四季皆宜',
          transportTip: selectedDest.tips?.transport_tips?.[0] || '交通便利，推荐高铁出行',
          trainDeparture: fromCity,
          trainArrival: destinationName,
          luckySuggestions: luckySuggestions,
        })
      } else {
        message.error('获取目的地失败，请稍后重试')
      }
    } catch (err) {
      console.error('BlindBox error:', err)
      message.error('网络错误，请检查网络连接')
    } finally {
      setLoading(false)
      setIsSpinning(false)
    }
  }, [fromCity, days, theme, budget])

  const resetBox = () => {
    setResult(null)
    setCurrentTip('')
    setAnimationData(null)
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
              borderRadius: 20, 
              background: isSpinning 
                ? 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)' 
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              boxShadow: isSpinning ? '0 0 60px rgba(255, 205, 0, 0.6)' : '0 4px 20px rgba(102, 126, 234, 0.3)',
              transition: 'all 0.3s',
              transform: isSpinning ? 'scale(1.02)' : 'scale(1)',
              overflow: 'hidden',
            }}
            bodyStyle={{ padding: 40 }}
          >
            {!result && !loading && (
              <div style={{ textAlign: 'center' }}>
                <div style={{ 
                  fontSize: 100, 
                  marginBottom: 24,
                  animation: 'float 3s ease-in-out infinite'
                }}>🎁</div>
                <Title level={3} style={{ color: 'white', marginBottom: 16 }}>准备好了吗？</Title>
                <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 16 }}>
                  设置你的条件，点击按钮，命运之轮将为你转动！
                </Text>
                <div style={{ marginTop: 20 }}>
                  <Text style={{ color: 'rgba(255,255,255,0.7)', fontSize: 14 }}>
                    🌟 每次抽取都是独一无二的体验
                  </Text>
                </div>
              </div>
            )}

            {loading && (
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 80, animation: 'spin 1s linear infinite' }}>
                  {animationData?.emoji || '🎲'}
                </div>
                <Title level={4} style={{ color: 'white', marginTop: 20 }}>
                  {animationData?.text || '正在抽取...'}
                </Title>
                <Progress 
                  percent={100} 
                  showInfo={false} 
                  strokeColor={{ '0%': '#ffecd2', '100%': '#fcb69f' }}
                  style={{ marginTop: 20 }}
                />
                <div style={{ marginTop: 24, minHeight: 24 }}>
                  <Text style={{ color: 'white', fontSize: 16, fontStyle: 'italic' }}>{currentTip}</Text>
                </div>
              </div>
            )}

            {result && !loading && (
              <div>
                <div style={{ textAlign: 'center', marginBottom: 20 }}>
                  <div style={{ 
                    fontSize: 60, 
                    marginBottom: 8,
                    animation: 'bounce 0.6s ease-out'
                  }}>
                    {result.luckyRank.icon}
                  </div>
                  <Title level={3} style={{ color: 'white', marginBottom: 8 }}>
                    恭喜！你的「{result.luckyRank.name}」目的地是
                  </Title>
                  <div style={{
                    background: 'rgba(255,255,255,0.2)',
                    borderRadius: 20,
                    padding: '8px 20px',
                    display: 'inline-block',
                    backdropFilter: 'blur(10px)',
                  }}>
                    <Text strong style={{ color: 'white', fontSize: 28 }}>
                      {result.cityName}
                    </Text>
                  </div>
                </div>

                <Card 
                  style={{ borderRadius: 16, marginBottom: 16, border: 'none', background: '#fff9f0' }}
                  bodyStyle={{ padding: 24 }}
                >
                  <div style={{ textAlign: 'center', marginBottom: 20 }}>
                    <Tag color="blue" style={{ fontSize: 16, padding: '4px 12px', margin: 4 }}>
                      🚄 {result.trainDeparture} → {result.trainArrival}
                    </Tag>
                    <Tag color="green" style={{ fontSize: 16, padding: '4px 12px', margin: 4 }}>
                      📅 {result.tripDays} 天
                    </Tag>
                    <Tag color="orange" style={{ fontSize: 16, padding: '4px 12px', margin: 4 }}>
                      💰 约 ¥{result.estimatedBudget}
                    </Tag>
                    <Tag color="red" style={{ fontSize: 16, padding: '4px 12px', margin: 4 }}>
                      ⭐ {result.rating} 分
                    </Tag>
                  </div>

                  {result.tags && result.tags.length > 0 && (
                    <div style={{ marginBottom: 16, textAlign: 'center' }}>
                      {result.tags.map((tag, i) => (
                        <Tag key={i} color="purple" style={{ margin: 4 }}>#{tag}</Tag>
                      ))}
                    </div>
                  )}

                  <Divider style={{ margin: '16px 0' }} />

                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ display: 'block', marginBottom: 8, fontSize: 15 }}>
                      <FireOutlined style={{ color: '#ff4d4f' }} /> 必去景点
                    </Text>
                    <div>
                      {result.topAttractions.map((attr, i) => (
                        <Tag key={i} color="geekblue" style={{ margin: 4, fontSize: 13 }}>
                          🎯 {attr}
                        </Tag>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ display: 'block', marginBottom: 8, fontSize: 15 }}>
                      🍽️ 必吃美食
                    </Text>
                    <div>
                      {result.topFoods.map((food, i) => (
                        <Tag key={i} color="volcano" style={{ margin: 4, fontSize: 13 }}>
                          😋 {food}
                        </Tag>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: 16 }}>
                    <Text strong style={{ display: 'block', marginBottom: 8, fontSize: 15 }}>
                      📋 行程建议
                    </Text>
                    {result.itinerary.map((item, i) => (
                      <div key={i} style={{ 
                        padding: '8px 12px', 
                        background: '#f6ffed', 
                        borderRadius: 8, 
                        marginBottom: 6,
                        borderLeft: '3px solid #52c41a'
                      }}>
                        <Text>📍 {item}</Text>
                      </div>
                    ))}
                  </div>

                  <Divider style={{ margin: '16px 0' }} />

                  <div style={{ 
                    background: `linear-gradient(135deg, ${result.luckyRank.color}10, ${result.luckyRank.color}30)`,
                    borderRadius: 12,
                    padding: 16,
                    marginBottom: 16
                  }}>
                    <div style={{ textAlign: 'center', marginBottom: 12 }}>
                      <Text strong style={{ fontSize: 16, color: result.luckyRank.color }}>
                        {result.luckyRank.icon} 今日幸运元素 {result.luckyRank.icon}
                      </Text>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap', gap: 12 }}>
                      <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: 28 }}>{result.zodiacSign}</div>
                        <Text type="secondary" style={{ fontSize: 12 }}>幸运星座</Text>
                      </div>
                      <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: 20, fontWeight: 'bold', color: result.luckyRank.color }}>
                          {result.luckyNumbers.join(' · ')}
                        </div>
                        <Text type="secondary" style={{ fontSize: 12 }}>幸运数字</Text>
                      </div>
                      <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: 20, fontWeight: 'bold', color: result.luckyRank.color }}>
                          x{result.luckyRank.multiplier}
                        </div>
                        <Text type="secondary" style={{ fontSize: 12 }}>运气加成</Text>
                      </div>
                    </div>
                  </div>

                  {result.luckySuggestions && (
                    <div style={{ marginBottom: 16 }}>
                      {result.luckySuggestions.map((tip, i) => (
                        <div key={i} style={{ 
                          padding: '8px 12px', 
                          background: '#fffbe6', 
                          borderRadius: 8, 
                          marginBottom: 6 
                        }}>
                          <Text>{tip}</Text>
                        </div>
                      ))}
                    </div>
                  )}

                  <div style={{ 
                    padding: '12px 16px', 
                    background: '#e6f7ff', 
                    borderRadius: 8,
                    borderLeft: '3px solid #1890ff'
                  }}>
                    <Text><strong>💡 小贴士：</strong>{result.funFact}</Text>
                  </div>
                </Card>

                <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
                  <Button 
                    type="primary" 
                    size="large"
                    icon={<ArrowRightOutlined />}
                    onClick={() => navigate(`/destinations/${encodeURIComponent(result.trainArrival)}`)}
                    style={{ 
                      minWidth: 140, 
                      height: 48, 
                      fontSize: 16,
                      background: 'linear-gradient(135deg, #ff6b6b, #ffd93d)',
                      border: 'none'
                    }}
                  >
                    去看看
                  </Button>
                  <Button 
                    size="large"
                    icon={<RocketOutlined />}
                    onClick={() => navigate(`/itinerary?city=${encodeURIComponent(result.trainArrival)}&days=${days}`)}
                    style={{ minWidth: 140, height: 48, fontSize: 16 }}
                  >
                    生成行程
                  </Button>
                  <Button 
                    size="large"
                    icon={<ReloadOutlined />}
                    onClick={resetBox}
                    style={{ minWidth: 120, height: 48, fontSize: 16 }}
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
              style={{ borderRadius: 16 }}
            >
              <Row gutter={[16, 24]}>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>🏠 出发城市</Text>
                  <Select
                    value={fromCity}
                    onChange={setFromCity}
                    style={{ width: '100%', marginTop: 8 }}
                    showSearch
                    options={['北京', '上海', '广州', '深圳', '杭州', '成都', '南京', '武汉', '西安', '重庆', '长沙', '郑州', '天津', '苏州', '厦门', '青岛'].map(c => ({ value: c, label: c }))}
                  />
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <Text strong>📅 旅行天数</Text>
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
                  <Text strong>💰 预算范围（每天）</Text>
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
                  <Text strong>🎨 旅行主题</Text>
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
                  style={{ 
                    minWidth: 220, 
                    height: 56, 
                    fontSize: 18,
                    background: 'linear-gradient(135deg, #ff6b6b, #ffd93d, #6bcb77)',
                    border: 'none',
                    fontWeight: 'bold',
                    boxShadow: '0 4px 15px rgba(255, 107, 107, 0.4)',
                  }}
                >
                  🎁 开启盲盒 🎁
                </Button>
                <div style={{ marginTop: 12 }}>
                  <Text type="secondary" style={{ fontSize: 13 }}>
                    点击按钮，让命运之轮为你选择目的地！
                  </Text>
                </div>
              </div>
            </Card>

            <Card style={{ marginTop: 16, borderRadius: 16 }}>
              <Title level={5} style={{ marginBottom: 12 }}>🎲 盲盒玩法说明</Title>
              <ul style={{ paddingLeft: 20 }}>
                <li style={{ marginBottom: 8 }}>设置你的出发城市、预算、天数和感兴趣的主题</li>
                <li style={{ marginBottom: 8 }}>系统会从所有可达目的地中<span style={{ color: '#ff4d4f', fontWeight: 'bold' }}>随机</span>为你推荐</li>
                <li style={{ marginBottom: 8 }}>每个目的地都有<span style={{ color: '#722ed1', fontWeight: 'bold' }}>稀有度</span>评级（SSR/SR/R/N）</li>
                <li style={{ marginBottom: 8 }}>还会给你<span style={{ color: '#faad14', fontWeight: 'bold' }}>幸运数字</span>和<span style={{ color: '#1890ff', fontWeight: 'bold' }}>幸运星座</span>！</li>
                <li style={{ marginBottom: 8 }}>你可以选择查看详情、生成行程，或者再抽一次！</li>
                <li>预算仅作为参考，实际花费以购票为准</li>
              </ul>
              <Divider />
              <div style={{ textAlign: 'center' }}>
                <Text type="secondary">
                  💡 试试不同的主题和预算，发现惊喜！完全随机模式最刺激哦～
                </Text>
              </div>
            </Card>
          </Col>
        </Row>
      )}

      <style>{`
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-15px); }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
