import { useState, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  Row, Col, Card, Typography, Button, Input, Select,
  Space, Tag, Empty, message, Steps, Slider,
  Spin, Result, Divider, List, Tooltip, Progress,
  Modal, Collapse, Badge
} from 'antd'
import {
  ArrowLeftOutlined, CheckCircleOutlined, CalendarOutlined,
  DollarOutlined, HeartOutlined, ThunderboltOutlined,
  ReloadOutlined, SaveOutlined, EditOutlined, PlusOutlined,
  EnvironmentOutlined, StarFilled, CarOutlined, BankOutlined,
  CoffeeOutlined, ShoppingOutlined, PictureOutlined, TeamOutlined,
  RobotOutlined, ExportOutlined, SyncOutlined, AppstoreOutlined,
  SwapOutlined, EyeOutlined, ArrowRightOutlined,
  CarryOutOutlined, CopyOutlined, DownloadOutlined, FileTextOutlined
} from '@ant-design/icons'
import { generateItinerary, generateAIContent } from '../services/destinationService'
import { getAICache, setAICache } from '../services/storageService'
import { usePlannerStore, useFavoritesStore } from '../stores'
import AiChatInput from '../components/AiChatInput'
import ExportModal from '../components/ExportModal'
import LuggageChecklist from '../components/LuggageChecklist'

const { Title, Text, Paragraph } = Typography
const { Panel } = Collapse

const PREFERENCES = [
  { value: 'all', label: '综合推荐', icon: <StarFilled /> },
  { value: 'scenery', label: '自然风光', icon: <PictureOutlined /> },
  { value: 'culture', label: '历史文化', icon: <BankOutlined /> },
  { value: 'food', label: '美食探索', icon: <CoffeeOutlined /> },
  { value: 'shopping', label: '购物休闲', icon: <ShoppingOutlined /> },
  { value: 'family', label: '亲子游玩', icon: <TeamOutlined /> },
]

const BUDGET_RANGES = [
  { value: 1000, label: '经济型', desc: '舒适出行', color: '#52c41a' },
  { value: 3000, label: '中档', desc: '品质出游', color: '#1890ff' },
  { value: 5000, label: '高档', desc: '豪华体验', color: '#722ed1' },
  { value: 10000, label: '奢华', desc: '尊享之旅', color: '#eb2f96' },
]

const CROWD_TYPES = [
  { value: 'elderly', label: '老人友好', icon: '👴' },
  { value: 'family', label: '亲子', icon: '👨‍👩‍👧' },
  { value: 'couple', label: '情侣', icon: '💑' },
  { value: 'hiking', label: '徒步', icon: '🥾' },
  { value: 'photo', label: '摄影', icon: '📷' },
]

const FOOD_PREFS = [
  { value: 'no_spicy', label: '不辣', icon: '🌶️' },
  { value: 'foodie', label: '美食优先', icon: '🍜' },
  { value: 'night_snack', label: '夜宵', icon: '🌙' },
]

const HOTEL_PREFS = [
  { value: 'homestay', label: '民宿', icon: '🏠' },
  { value: 'near_attraction', label: '近景区', icon: '🎯' },
  { value: 'near_station', label: '近车站', icon: '🚉' },
  { value: 'luxury', label: '高星酒店', icon: '⭐' },
  { value: 'pool', label: '有泳池', icon: '🏊' },
]

const TRANSPORT_PREFS = [
  { value: 'subway', label: '地铁优先', icon: '🚇' },
  { value: 'taxi', label: '打车优先', icon: '🚕' },
  { value: 'min_walk', label: '少步行', icon: '🚶' },
]

const VERSION_STYLES = [
  { value: 'classic', label: '经典稳妥', desc: '大众化景点，安排合理', color: '#1890ff' },
  { value: 'adventure', label: '冒险探索', desc: '小众路线，体验独特', color: '#fa541c' },
  { value: 'relax', label: '悠闲放松', desc: '慢节奏，享受生活', color: '#52c41a' },
]

export default function PlannerPage() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const exportModalRef = useRef(null)

  const [currentStep, setCurrentStep] = useState(0)
  const [generating, setGenerating] = useState(false)
  const [generatedResult, setGeneratedResult] = useState(null)
  const [editingMode, setEditingMode] = useState(false)
  const [aiModalOpen, setAiModalOpen] = useState(false)
  const [luggageModalOpen, setLuggageModalOpen] = useState(false)
  const [versions, setVersions] = useState([])
  const [selectedVersion, setSelectedVersion] = useState(null)
  const [showVersions, setShowVersions] = useState(false)
  const [multiGenerating, setMultiGenerating] = useState(false)
  const [aiGenerateModalOpen, setAiGenerateModalOpen] = useState(false)
  const [aiGenerateLoading, setAiGenerateLoading] = useState(false)
  const [aiGenerateResult, setAiGenerateResult] = useState(null)
  const [aiGenerateType, setAiGenerateType] = useState(null)

  const [formData, setFormData] = useState({
    city: params.get('city') || '',
    fromCity: params.get('from') || '',
    days: 3,
    budget: 3000,
    preference: 'all',
    travelers: 2,
    crowdTypes: [],
    foodPrefs: [],
    hotelPrefs: [],
    transportPrefs: [],
  })

  const schedule = usePlannerStore(s => s.schedule)
  const addToFavorites = useFavoritesStore(s => s.addToFavorites)

  const updateFormData = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  const toggleArrayItem = (key, value) => {
    setFormData(prev => {
      const arr = prev[key] || []
      const newArr = arr.includes(value)
        ? arr.filter(v => v !== value)
        : [...arr, value]
      return { ...prev, [key]: newArr }
    })
  }

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleGenerate = async () => {
    if (!formData.city) {
      message.warning('请输入目的地城市')
      return
    }

    setGenerating(true)
    try {
      const result = await generateItinerary(
        formData.city,
        formData.days,
        formData.budget,
        formData.preference === 'all' ? '' : formData.preference
      )

      if (result.success) {
        setGeneratedResult(result)
        setCurrentStep(3)
        setShowVersions(false)
        message.success('行程生成成功！')
      } else {
        message.error(result.message || '生成失败，请重试')
      }
    } catch (error) {
      console.error('生成行程失败:', error)
      message.error('生成失败，请检查网络连接')
    } finally {
      setGenerating(false)
    }
  }

  const handleMultiGenerate = async () => {
    if (!formData.city) {
      message.warning('请输入目的地城市')
      return
    }

    setMultiGenerating(true)
    setVersions([])
    setShowVersions(true)

    try {
      const stylePromises = VERSION_STYLES.map(async (style) => {
        try {
          const result = await generateItinerary(
            formData.city,
            formData.days,
            formData.budget,
            formData.preference === 'all' ? '' : formData.preference
          )
          return {
            ...result,
            style,
            styleLabel: style.label,
            styleDesc: style.desc,
            styleColor: style.color,
          }
        } catch (err) {
          return null
        }
      })

      const results = await Promise.all(stylePromises)
      const validVersions = results.filter(r => r !== null && r.success)

      if (validVersions.length > 0) {
        setVersions(validVersions)
        setSelectedVersion(validVersions[0])
        message.success(`已生成 ${validVersions.length} 个风格版本！`)
      } else {
        message.error('生成多个版本失败，请重试')
      }
    } catch (error) {
      console.error('多版本生成失败:', error)
      message.error('生成失败，请检查网络连接')
    } finally {
      setMultiGenerating(false)
    }
  }

  const handleSelectVersion = (version) => {
    setSelectedVersion(version)
    setGeneratedResult(version)
    setCurrentStep(3)
    message.success(`已选择「${version.styleLabel}」版本`)
  }

  const handleSave = () => {
    if (!generatedResult) return

    const itineraryData = generatedResult?.itinerary || generatedResult
    const plannerData = {
      type: 'generated_planner',
      city: formData.city,
      fromCity: formData.fromCity,
      days: formData.days,
      budget: formData.budget,
      preference: formData.preference,
      itinerary: itineraryData,
      style: selectedVersion?.style || null,
      advancedPrefs: {
        crowdTypes: formData.crowdTypes,
        foodPrefs: formData.foodPrefs,
        hotelPrefs: formData.hotelPrefs,
        transportPrefs: formData.transportPrefs,
      },
      generatedAt: new Date().toISOString(),
    }

    addToFavorites('planners', plannerData)
    message.success('行程已保存到收藏')
  }

  const handleExport = () => {
    if (!generatedResult) {
      message.warning('请先生成行程')
      return
    }
    const itineraryData = generatedResult?.itinerary || generatedResult
    const exportData = {
      title: `${formData.city} ${formData.days}天行程`,
      days: itineraryData?.days || itineraryData?.itinerary_days || [],
      summary: itineraryData?.summary || [],
      tips: itineraryData?.tips || [],
      total_cost_estimate: itineraryData?.total_cost_estimate || {},
    }
    exportModalRef.current?.open()
    return exportData
  }

  const handleReset = () => {
    setCurrentStep(0)
    setGeneratedResult(null)
    setEditingMode(false)
    setVersions([])
    setSelectedVersion(null)
    setShowVersions(false)
  }

  const handleAiConfirm = (parsedParams) => {
    if (parsedParams) {
      const newData = { ...formData }
      if (parsedParams.city) newData.city = parsedParams.city
      if (parsedParams.days) newData.days = parsedParams.days
      if (parsedParams.budget) newData.budget = parsedParams.budget
      if (parsedParams.people) newData.travelers = parsedParams.people
      if (parsedParams.preference) newData.preference = parsedParams.preference
      if (parsedParams.elderly_friendly) newData.crowdTypes = [...newData.crowdTypes, 'elderly']
      if (parsedParams.is_couple) newData.crowdTypes = [...newData.crowdTypes, 'couple']
      if (parsedParams.is_hiking) newData.crowdTypes = [...newData.crowdTypes, 'hiking']
      if (parsedParams.no_spicy) newData.foodPrefs = [...newData.foodPrefs, 'no_spicy']
      if (parsedParams.homestay) newData.hotelPrefs = [...newData.hotelPrefs, 'homestay']
      if (parsedParams.near_station) newData.hotelPrefs = [...newData.hotelPrefs, 'near_station']
      if (parsedParams.near_attraction) newData.hotelPrefs = [...newData.hotelPrefs, 'near_attraction']
      setFormData(newData)
      setAiModalOpen(false)
      setCurrentStep(2)
      message.success('已根据AI解析结果更新表单')
    }
  }

  const handleAiGenerate = (itinerary) => {
    if (itinerary) {
      setGeneratedResult({ itinerary, success: true })
      setCurrentStep(3)
      setAiModalOpen(false)
      message.success('AI已生成行程')
    }
  }

  const handleAIGenerate = async (type) => {
    setAiGenerateType(type)
    setAiGenerateModalOpen(true)
    setAiGenerateLoading(true)
    setAiGenerateResult(null)

    const cacheKey = `planner_${type}_${formData.city}_${formData.days}`
    const cached = getAICache(cacheKey)
    if (cached) {
      setAiGenerateResult(cached)
      setAiGenerateLoading(false)
      return
    }

    try {
      const itinerary = generatedResult?.itinerary || {}
      const response = await generateAIContent(type, {
        city: formData.city,
        days: formData.days,
        budget: formData.budget,
        travelers: formData.travelers,
        itinerary: itinerary,
      })

      if (response.success) {
        setAiGenerateResult(response.data)
        setAICache(cacheKey, response.data)
      } else {
        message.error(response.error || '生成失败')
      }
    } catch (error) {
      console.error('AI生成失败:', error)
      message.error('生成失败')
    } finally {
      setAiGenerateLoading(false)
    }
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  }

  const handleDownload = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
    message.success('下载成功')
  }

  const renderStep0 = () => (
    <div>
      <Title level={4}>📍 选择目的地</Title>
      <Paragraph type="secondary">请输入您想要游览的城市</Paragraph>

      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        <div style={{ marginBottom: 16 }}>
          <Text strong>出发城市</Text>
          <Input
            placeholder="如：北京（可选）"
            value={formData.fromCity}
            onChange={e => updateFormData('fromCity', e.target.value)}
            style={{ marginTop: 8 }}
          />
        </div>

        <div>
          <Text strong>目的地城市 *</Text>
          <Input
            size="large"
            placeholder="如：上海、杭州、成都"
            value={formData.city}
            onChange={e => updateFormData('city', e.target.value)}
            style={{ marginTop: 8 }}
          />
        </div>
      </Card>

      <div style={{ marginBottom: 16 }}>
        <Text type="secondary">热门目的地：</Text>
        <Space style={{ marginTop: 8 }} wrap>
          {['北京', '上海', '杭州', '成都', '西安', '重庆', '广州', '厦门'].map(city => (
            <Button
              key={city}
              onClick={() => updateFormData('city', city)}
              type={formData.city === city ? 'primary' : 'default'}
            >
              {city}
            </Button>
          ))}
        </Space>
      </div>

      <Divider>或使用AI智能对话</Divider>

      <Button
        size="large"
        icon={<RobotOutlined />}
        block
        onClick={() => setAiModalOpen(true)}
        style={{
          height: 56,
          borderRadius: 12,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: 'none',
          color: '#fff',
          fontSize: 16,
          fontWeight: 500,
        }}
      >
        <ThunderboltOutlined style={{ marginRight: 8 }} />
        AI智能对话规划
      </Button>
    </div>
  )

  const renderStep1 = () => (
    <div>
      <Title level={4}>📅 设置天数与人数</Title>
      <Paragraph type="secondary">告诉我们您的行程安排</Paragraph>

      <Row gutter={24}>
        <Col xs={24} md={12}>
          <Card title="行程天数" style={{ borderRadius: 12, height: '100%' }}>
            <div style={{ marginBottom: 16 }}>
              <Text type="secondary">已选择 {formData.days} 天</Text>
            </div>
            <Slider
              min={1}
              max={7}
              value={formData.days}
              onChange={v => updateFormData('days', v)}
              marks={{ 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7' }}
            />
            <div style={{ marginTop: 16 }}>
              <Space wrap>
                {[2, 3, 5, 7].map(d => (
                  <Button
                    key={d}
                    size="small"
                    type={formData.days === d ? 'primary' : 'default'}
                    onClick={() => updateFormData('days', d)}
                  >
                    {d}天
                  </Button>
                ))}
              </Space>
            </div>
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card title="出行人数" style={{ borderRadius: 12, height: '100%' }}>
            <div style={{ marginBottom: 16 }}>
              <Text type="secondary">已选择 {formData.travelers} 人</Text>
            </div>
            <Slider
              min={1}
              max={10}
              value={formData.travelers}
              onChange={v => updateFormData('travelers', v)}
              marks={{ 1: '1', 2: '2', 4: '4', 6: '6', 10: '10' }}
            />
            <div style={{ marginTop: 16 }}>
              <Space wrap>
                {[1, 2, 4].map(n => (
                  <Button
                    key={n}
                    size="small"
                    type={formData.travelers === n ? 'primary' : 'default'}
                    onClick={() => updateFormData('travelers', n)}
                  >
                    {n}人
                  </Button>
                ))}
              </Space>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )

  const renderAdvancedPrefs = () => (
    <Card
      title={
        <Space>
          <AppstoreOutlined />
          <span>高级偏好设置（可选）</span>
        </Space>
      }
      style={{ borderRadius: 12, marginBottom: 24 }}
    >
      <Collapse ghost defaultActiveKey={['crowd', 'food', 'hotel', 'transport']}>
        <Panel header={<Space><span>👥</span><Text strong>人群类型</Text></Space>} key="crowd">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {CROWD_TYPES.map(item => (
              <Tag.CheckableTag
                key={item.value}
                checked={formData.crowdTypes.includes(item.value)}
                onChange={() => toggleArrayItem('crowdTypes', item.value)}
                style={{
                  padding: '6px 14px',
                  fontSize: 14,
                  borderRadius: 16,
                  border: formData.crowdTypes.includes(item.value)
                    ? '1px solid #722ed1'
                    : '1px solid #d9d9d9',
                  background: formData.crowdTypes.includes(item.value) ? '#f9f0ff' : '#fff',
                }}
              >
                {item.icon} {item.label}
              </Tag.CheckableTag>
            ))}
          </div>
        </Panel>

        <Panel header={<Space><span>🍜</span><Text strong>饮食偏好</Text></Space>} key="food">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {FOOD_PREFS.map(item => (
              <Tag.CheckableTag
                key={item.value}
                checked={formData.foodPrefs.includes(item.value)}
                onChange={() => toggleArrayItem('foodPrefs', item.value)}
                style={{
                  padding: '6px 14px',
                  fontSize: 14,
                  borderRadius: 16,
                  border: formData.foodPrefs.includes(item.value)
                    ? '1px solid #722ed1'
                    : '1px solid #d9d9d9',
                  background: formData.foodPrefs.includes(item.value) ? '#f9f0ff' : '#fff',
                }}
              >
                {item.icon} {item.label}
              </Tag.CheckableTag>
            ))}
          </div>
        </Panel>

        <Panel header={<Space><span>🏨</span><Text strong>住宿偏好</Text></Space>} key="hotel">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {HOTEL_PREFS.map(item => (
              <Tag.CheckableTag
                key={item.value}
                checked={formData.hotelPrefs.includes(item.value)}
                onChange={() => toggleArrayItem('hotelPrefs', item.value)}
                style={{
                  padding: '6px 14px',
                  fontSize: 14,
                  borderRadius: 16,
                  border: formData.hotelPrefs.includes(item.value)
                    ? '1px solid #722ed1'
                    : '1px solid #d9d9d9',
                  background: formData.hotelPrefs.includes(item.value) ? '#f9f0ff' : '#fff',
                }}
              >
                {item.icon} {item.label}
              </Tag.CheckableTag>
            ))}
          </div>
        </Panel>

        <Panel header={<Space><span>🚕</span><Text strong>交通偏好</Text></Space>} key="transport">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {TRANSPORT_PREFS.map(item => (
              <Tag.CheckableTag
                key={item.value}
                checked={formData.transportPrefs.includes(item.value)}
                onChange={() => toggleArrayItem('transportPrefs', item.value)}
                style={{
                  padding: '6px 14px',
                  fontSize: 14,
                  borderRadius: 16,
                  border: formData.transportPrefs.includes(item.value)
                    ? '1px solid #722ed1'
                    : '1px solid #d9d9d9',
                  background: formData.transportPrefs.includes(item.value) ? '#f9f0ff' : '#fff',
                }}
              >
                {item.icon} {item.label}
              </Tag.CheckableTag>
            ))}
          </div>
        </Panel>
      </Collapse>
    </Card>
  )

  const renderStep2 = () => (
    <div>
      <Title level={4}>💰 预算与偏好</Title>
      <Paragraph type="secondary">帮助我们为您定制最合适的行程</Paragraph>

      <Card title="预算范围" style={{ borderRadius: 12, marginBottom: 24 }}>
        <div style={{ marginBottom: 16 }}>
          <Text strong>总预算：¥{formData.budget.toLocaleString()}</Text>
        </div>
        <Slider
          min={500}
          max={15000}
          step={500}
          value={formData.budget}
          onChange={v => updateFormData('budget', v)}
        />
        <Row gutter={16} style={{ marginTop: 16 }}>
          {BUDGET_RANGES.map(range => (
            <Col key={range.value} xs={12} md={6}>
              <Card
                size="small"
                hoverable
                onClick={() => updateFormData('budget', range.value)}
                style={{
                  textAlign: 'center',
                  cursor: 'pointer',
                  border: formData.budget === range.value ? `2px solid ${range.color}` : undefined,
                  background: formData.budget === range.value ? `${range.color}15` : undefined
                }}
              >
                <div style={{ fontSize: 18, fontWeight: 'bold', color: range.color }}>
                  ¥{range.value.toLocaleString()}
                </div>
                <div style={{ fontSize: 14, fontWeight: 500 }}>{range.label}</div>
                <div style={{ fontSize: 12, color: '#999' }}>{range.desc}</div>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      <Card title="兴趣偏好" style={{ borderRadius: 12, marginBottom: 24 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: 12 }}>
          {PREFERENCES.map(pref => (
            <div
              key={pref.value}
              onClick={() => updateFormData('preference', pref.value)}
              style={{
                padding: 16,
                border: formData.preference === pref.value ? '2px solid #722ed1' : '1px solid #e8e8e8',
                borderRadius: 12,
                cursor: 'pointer',
                textAlign: 'center',
                background: formData.preference === pref.value ? '#f9f0ff' : 'white',
                transition: 'all 0.3s'
              }}
            >
              <div style={{ fontSize: 24, color: formData.preference === pref.value ? '#722ed1' : '#666', marginBottom: 8 }}>
                {pref.icon}
              </div>
              <div style={{ fontWeight: formData.preference === pref.value ? 600 : 400 }}>
                {pref.label}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {renderAdvancedPrefs()}

      <Card
        style={{
          borderRadius: 12,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: 'none',
          color: '#fff',
        }}
        bodyStyle={{ padding: 20 }}
      >
        <Row align="middle" gutter={16}>
          <Col xs={24} sm={12}>
            <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>
              <SwapOutlined style={{ marginRight: 8 }} />
              多版本对比生成
            </div>
            <div style={{ fontSize: 13, opacity: 0.85 }}>
              一键生成3种不同风格的行程，选择最适合您的版本
            </div>
          </Col>
          <Col xs={24} sm={12} style={{ textAlign: 'right' }}>
            <Button
              size="large"
              icon={<AppstoreOutlined />}
              onClick={handleMultiGenerate}
              loading={multiGenerating}
              style={{
                background: '#fff',
                color: '#722ed1',
                border: 'none',
                borderRadius: 8,
                height: 44,
                fontWeight: 500,
              }}
            >
              生成3个版本
            </Button>
          </Col>
        </Row>
      </Card>
    </div>
  )

  const renderVersionCompare = () => {
    if (!showVersions) return null

    return (
      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        <Title level={5} style={{ marginBottom: 16 }}>
          <SwapOutlined style={{ marginRight: 8 }} />
          多版本对比（{versions.length}/3 已生成）
        </Title>

        {multiGenerating && versions.length < 3 && (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Spin size="large" />
            <div style={{ marginTop: 12, color: '#666' }}>
              正在生成剩余 {3 - versions.length} 个版本...
            </div>
            <Progress
              percent={Math.round((versions.length / 3) * 100)}
              style={{ marginTop: 16, maxWidth: 300 }}
            />
          </div>
        )}

        {!multiGenerating && versions.length > 0 && (
          <Row gutter={16}>
            {VERSION_STYLES.map(style => {
              const version = versions.find(v => v.style.value === style.value)
              const isSelected = selectedVersion?.style?.value === style.value

              return (
                <Col key={style.value} xs={24} md={8}>
                  <Card
                    hoverable={!!version}
                    style={{
                      borderRadius: 12,
                      border: isSelected ? `2px solid ${style.color}` : '1px solid #e8e8e8',
                      background: isSelected ? `${style.color}15` : '#fff',
                      cursor: version ? 'pointer' : 'not-allowed',
                      opacity: version ? 1 : 0.5,
                    }}
                    onClick={() => version && handleSelectVersion(version)}
                  >
                    <div style={{ textAlign: 'center' }}>
                      <div
                        style={{
                          width: 48,
                          height: 48,
                          borderRadius: 24,
                          background: style.color,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: '#fff',
                          fontWeight: 'bold',
                          margin: '0 auto 12px',
                          fontSize: 18,
                        }}
                      >
                        {style.label.charAt(0)}
                      </div>
                      <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 4 }}>
                        {style.label}
                      </div>
                      <div style={{ fontSize: 12, color: '#999', marginBottom: 12 }}>
                        {style.desc}
                      </div>
                      {version ? (
                        <>
                          <Tag color={isSelected ? 'purple' : 'default'}>
                            {version?.itinerary?.days?.length || 0}天 · {version?.itinerary?.total_cost_estimate?.total ? `¥${version.itinerary.total_cost_estimate.total}` : '已生成'}
                          </Tag>
                          {isSelected && (
                            <Badge
                              count={<CheckCircleOutlined style={{ color: '#fff' }} />}
                              style={{ backgroundColor: style.color, marginTop: 8 }}
                            />
                          )}
                          {!isSelected && (
                            <div style={{ marginTop: 8 }}>
                              <Button size="small" type="primary" ghost>
                                <EyeOutlined /> 选择此版本
                              </Button>
                            </div>
                          )}
                        </>
                      ) : (
                        <div style={{ fontSize: 12, color: '#ff4d4f' }}>生成失败</div>
                      )}
                    </div>
                  </Card>
                </Col>
              )
            })}
          </Row>
        )}
      </Card>
    )
  }

  const renderStep3 = () => {
    if (generating) {
      return (
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <Spin size="large" />
          <Title level={4} style={{ marginTop: 24 }}>AI智能生成中...</Title>
          <Paragraph type="secondary">
            正在为您搜索{formData.city}的最佳行程安排
          </Paragraph>
          <div style={{ maxWidth: 400, margin: '20px auto' }}>
            <Progress percent={100} status="active" strokeColor={{ '0%': '#108ee9', '100%': '#87d068' }} />
          </div>
        </div>
      )
    }

    if (!generatedResult) {
      return (
        <Result
          status="info"
          title="准备好生成您的专属行程了吗？"
          subTitle={`${formData.city} · ${formData.days}天 · 预算¥${formData.budget.toLocaleString()}`}
          extra={[
            <Button key="back" onClick={() => setCurrentStep(2)}>返回修改</Button>,
            <Button key="versions" icon={<AppstoreOutlined />} onClick={handleMultiGenerate} loading={multiGenerating}>
              多版本对比
            </Button>,
            <Button key="generate" type="primary" icon={<ThunderboltOutlined />} onClick={handleGenerate}>
              立即生成
            </Button>,
          ]}
        />
      )
    }

    const itineraryData = generatedResult?.itinerary || {}
    const itineraryDays = itineraryData?.days || []
    const total_cost_estimate = itineraryData?.total_cost_estimate || {}
    const summary = itineraryData?.summary || []
    const tips = itineraryData?.tips || []
    const hotel_recommendations = itineraryData?.hotel_recommendations || []

    return (
      <div>
        {renderVersionCompare()}

        <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
          <div>
            <Title level={3} style={{ marginBottom: 4 }}>
              {formData.city} · {formData.days}天行程
              {selectedVersion && (
                <Tag color="purple" style={{ marginLeft: 8 }}>
                  {selectedVersion.styleLabel}风格
                </Tag>
              )}
            </Title>
            <Space wrap>
              <Tag color="blue"><CalendarOutlined /> {formData.days}天</Tag>
              <Tag color="green"><DollarOutlined /> 预算¥{formData.budget.toLocaleString()}</Tag>
              <Tag color="purple"><ThunderboltOutlined /> AI智能生成</Tag>
              {formData.crowdTypes.map(t => {
                const item = CROWD_TYPES.find(c => c.value === t)
                return item ? <Tag key={t} color="cyan">{item.icon} {item.label}</Tag> : null
              })}
              {formData.foodPrefs.map(t => {
                const item = FOOD_PREFS.find(c => c.value === t)
                return item ? <Tag key={t} color="orange">{item.icon} {item.label}</Tag> : null
              })}
              {formData.hotelPrefs.map(t => {
                const item = HOTEL_PREFS.find(c => c.value === t)
                return item ? <Tag key={t} color="geekblue">{item.icon} {item.label}</Tag> : null
              })}
            </Space>
          </div>
          <Space wrap>
            <Button icon={<RobotOutlined />} onClick={() => setAiModalOpen(true)}>
              AI对话
            </Button>
            <Button icon={<CarryOutOutlined />} onClick={() => setLuggageModalOpen(true)}>
              行李清单
            </Button>
            <Button icon={<EditOutlined />} onClick={() => setEditingMode(!editingMode)}>
              {editingMode ? '预览模式' : '编辑模式'}
            </Button>
            <Button icon={<ReloadOutlined />} onClick={handleGenerate}>重新生成</Button>
            <Button
              type="primary"
              icon={<ExportOutlined />}
              onClick={handleExport}
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
              }}
            >
              导出行程
            </Button>
          </Space>
        </div>

        {summary && summary.length > 0 && (
          <Card style={{ marginBottom: 24, borderRadius: 12 }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
              <div style={{
                width: 48,
                height: 48,
                borderRadius: 24,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: 24
              }}>
                <ThunderboltOutlined />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, marginBottom: 8 }}>行程概览</div>
                {summary.map((s, i) => (
                  <div key={i} style={{ fontSize: 14, color: '#666', marginBottom: 4 }}>• {s}</div>
                ))}
              </div>
            </div>
          </Card>
        )}

        <Row gutter={24}>
          <Col xs={24} lg={16}>
            {itineraryDays?.map((day, dayIdx) => (
              <Card
                key={dayIdx}
                title={
                  <Space>
                    <div style={{
                      width: 40,
                      height: 40,
                      borderRadius: 20,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontWeight: 'bold',
                      fontSize: 14
                    }}>
                      D{day.day}
                    </div>
                    <span>{day.title}</span>
                  </Space>
                }
                style={{ marginBottom: 16, borderRadius: 12 }}
              >
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  {day.schedule?.map((item, itemIdx) => (
                    <div key={itemIdx} style={{
                      display: 'flex',
                      gap: 12,
                      padding: 12,
                      background: '#fafafa',
                      borderRadius: 8,
                      borderLeft: `4px solid ${item.type === 'attraction' ? '#ff6b6b' : item.type === 'food' ? '#ffa500' : '#4ecdc4'}`
                    }}>
                      <div style={{ flex: '0 0 auto' }}>
                        <Tag color={item.type === 'attraction' ? 'red' : item.type === 'food' ? 'orange' : 'cyan'}>
                          {item.time}
                        </Tag>
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 600, marginBottom: 4 }}>
                          {item.item?.name || item.description}
                        </div>
                        <div style={{ fontSize: 12, color: '#666' }}>
                          {item.description}
                          {item.item?.rating > 0 && (
                            <span style={{ marginLeft: 8 }}>
                              <StarFilled style={{ color: '#faad14' }} /> {item.item.rating}
                            </span>
                          )}
                        </div>
                        {item.item?.address && (
                          <div style={{ fontSize: 11, color: '#999', marginTop: 4 }}>
                            <EnvironmentOutlined /> {item.item.address}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}

                  {day.hotel && (
                    <div style={{
                      padding: 12,
                      background: '#f9f0ff',
                      borderRadius: 8,
                      borderLeft: '4px solid #722ed1'
                    }}>
                      <div style={{ fontWeight: 600, marginBottom: 4, color: '#722ed1' }}>
                        🏨 推荐住宿
                      </div>
                      <div style={{ fontSize: 14 }}>{day.hotel.name}</div>
                      {day.hotel.address && (
                        <div style={{ fontSize: 12, color: '#666' }}>
                          {day.hotel.address}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </Col>

          <Col xs={24} lg={8}>
            <Card title="💰 预算估算" style={{ marginBottom: 16, borderRadius: 12 }}>
              <div style={{ textAlign: 'center', marginBottom: 16 }}>
                <div style={{ fontSize: 36, fontWeight: 'bold', color: '#ff6b6b' }}>
                  ¥{total_cost_estimate?.total?.toLocaleString() || '--'}
                </div>
                <div style={{ fontSize: 13, color: '#999' }}>预计总花费</div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>🏨 住宿费用</span>
                  <span>¥{total_cost_estimate?.hotel?.toLocaleString() || '--'}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>🍜 餐饮费用</span>
                  <span>¥{total_cost_estimate?.food?.toLocaleString() || '--'}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>🎫 景点门票</span>
                  <span>¥{total_cost_estimate?.attraction?.toLocaleString() || '--'}</span>
                </div>
              </div>

              <Divider />

              <div style={{
                padding: 12,
                background: total_cost_estimate?.budget_level === 'low' ? '#f6ffed' :
                           total_cost_estimate?.budget_level === 'high' ? '#fff1f0' : '#e6f7ff',
                borderRadius: 8
              }}>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>预算匹配度</div>
                <Progress
                  percent={Math.min(100, Math.abs(total_cost_estimate?.budget_match || 0))}
                  status={
                    total_cost_estimate?.budget_level === 'low' ? 'success' :
                    total_cost_estimate?.budget_level === 'high' ? 'exception' : 'active'
                  }
                />
                <div style={{ fontSize: 12, color: '#666', marginTop: 8 }}>
                  {total_cost_estimate?.budget_level === 'low' && '预算充足，可考虑升级体验'}
                  {total_cost_estimate?.budget_level === 'medium' && '预算适中，行程合理'}
                  {total_cost_estimate?.budget_level === 'high' && '预算偏紧，建议适当减少'}
                </div>
              </div>
            </Card>

            <Card title="💡 温馨提示" style={{ marginBottom: 16, borderRadius: 12 }}>
              <List
                size="small"
                dataSource={tips || []}
                renderItem={(tip, i) => (
                  <List.Item style={{ padding: '8px 0' }}>
                    <Space align="start">
                      <span style={{
                        width: 20,
                        height: 20,
                        borderRadius: 10,
                        background: '#722ed1',
                        color: 'white',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: 12,
                        flex: '0 0 auto'
                      }}>
                        {i + 1}
                      </span>
                      <span style={{ fontSize: 13 }}>{tip}</span>
                    </Space>
                  </List.Item>
                )}
              />
            </Card>

            <Card
              title={
                <Space>
                  <CarryOutOutlined />
                  <span>实用工具</span>
                </Space>
              }
              style={{ marginBottom: 16, borderRadius: 12 }}
            >
              <Space direction="vertical" style={{ width: '100%' }}>
                <Button
                  block
                  size="large"
                  icon={<CarryOutOutlined />}
                  onClick={() => setLuggageModalOpen(true)}
                  style={{
                    borderRadius: 8,
                    height: 44,
                    borderColor: '#722ed1',
                    color: '#722ed1',
                  }}
                >
                  🧳 生成行李清单
                </Button>
                <Button
                  block
                  size="large"
                  icon={<ExportOutlined />}
                  onClick={handleExport}
                  style={{
                    borderRadius: 8,
                    height: 44,
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    border: 'none',
                    color: '#fff',
                  }}
                >
                  📤 导出行程
                </Button>
              </Space>
            </Card>

            <Card
              title={
                <Space>
                  <RobotOutlined style={{ color: '#722ed1' }} />
                  <span>AI 一键生成</span>
                </Space>
              }
              style={{ marginBottom: 16, borderRadius: 12 }}
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <Button
                  block
                  size="large"
                  icon={<FileTextOutlined />}
                  onClick={() => handleAIGenerate('itinerary_memo')}
                  style={{ borderRadius: 8, height: 44 }}
                >
                  📝 生成出行备忘录
                </Button>
                <Button
                  block
                  size="large"
                  icon={<FileTextOutlined />}
                  onClick={() => handleAIGenerate('pocket_itinerary')}
                  style={{ borderRadius: 8, height: 44 }}
                >
                  📱 生成极简口袋版
                </Button>
                <Button
                  block
                  size="large"
                  icon={<FileTextOutlined />}
                  onClick={() => handleAIGenerate('travel_copy')}
                  style={{ borderRadius: 8, height: 44 }}
                >
                  ✨ 生成旅行文案
                </Button>
                <Button
                  block
                  size="large"
                  icon={<CarryOutOutlined />}
                  onClick={() => handleAIGenerate('packing_list')}
                  style={{ borderRadius: 8, height: 44 }}
                >
                  🎒 生成行李清单
                </Button>
              </div>
            </Card>

            {hotel_recommendations?.length > 0 && (
              <Card title="🏨 酒店推荐" style={{ borderRadius: 12 }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  {hotel_recommendations.map((hotel, i) => (
                    <div key={i} style={{
                      padding: 12,
                      border: '1px solid #e8e8e8',
                      borderRadius: 8
                    }}>
                      <div style={{ fontWeight: 600 }}>{hotel.name}</div>
                      {hotel.rating > 0 && (
                        <div style={{ fontSize: 12, color: '#faad14', marginBottom: 4 }}>
                          <StarFilled /> {hotel.rating}
                        </div>
                      )}
                      {hotel.cost > 0 && (
                        <div style={{ fontSize: 12, color: '#ff6b6b' }}>
                          <DollarOutlined /> 参考价 ¥{hotel.cost}/晚
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </Card>
            )}
          </Col>
        </Row>
      </div>
    )
  }

  return (
    <div className="page-container" style={{ padding: '24px 16px', maxWidth: 1200, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate(-1)}
        >
          返回
        </Button>
      </div>

      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: 16,
        padding: 32,
        color: 'white',
        marginBottom: 24
      }}>
        <Title level={2} style={{ color: 'white', margin: 0 }}>
          ✨ 智能行程规划
        </Title>
        <Paragraph style={{ color: 'rgba(255,255,255,0.9)', marginTop: 8, fontSize: 15 }}>
          只需几步，AI为您定制专属旅行路线
        </Paragraph>
      </div>

      {currentStep < 3 && (
        <Card style={{ marginBottom: 24, borderRadius: 12 }}>
          <Steps
            current={currentStep}
            items={[
              { title: '目的地', icon: <EnvironmentOutlined /> },
              { title: '天数人数', icon: <CalendarOutlined /> },
              { title: '预算偏好', icon: <DollarOutlined /> },
              { title: '生成结果', icon: <CheckCircleOutlined /> },
            ]}
          />
        </Card>
      )}

      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        {currentStep === 0 && renderStep0()}
        {currentStep === 1 && renderStep1()}
        {currentStep === 2 && renderStep2()}
        {currentStep === 3 && renderStep3()}
      </Card>

      {currentStep < 3 && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
          <Button
            onClick={handlePrev}
            disabled={currentStep === 0}
            size="large"
            icon={<ArrowLeftOutlined />}
          >
            上一步
          </Button>
          {currentStep < 2 ? (
            <Button
              type="primary"
              onClick={handleNext}
              size="large"
              icon={<ArrowRightOutlined />}
            >
              下一步
            </Button>
          ) : (
            <Space wrap>
              <Button
                size="large"
                icon={<AppstoreOutlined />}
                onClick={handleMultiGenerate}
                loading={multiGenerating}
              >
                多版本对比
              </Button>
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                onClick={handleGenerate}
                size="large"
                loading={generating}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none'
                }}
              >
                生成行程
              </Button>
            </Space>
          )}
        </div>
      )}

      {currentStep === 3 && !generating && (
        <div style={{ display: 'flex', justifyContent: 'center', gap: 16, flexWrap: 'wrap' }}>
          <Button onClick={handleReset} size="large" icon={<ReloadOutlined />}>
            重新规划
          </Button>
          <Button
            size="large"
            icon={<CarryOutOutlined />}
            onClick={() => setLuggageModalOpen(true)}
          >
            行李清单
          </Button>
          <Button
            size="large"
            icon={<ExportOutlined />}
            onClick={handleExport}
          >
            导出行程
          </Button>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            onClick={handleSave}
            size="large"
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
            }}
          >
            保存行程
          </Button>
        </div>
      )}

      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#722ed1' }} />
            <span>AI智能对话规划</span>
          </Space>
        }
        open={aiModalOpen}
        onCancel={() => setAiModalOpen(false)}
        footer={null}
        width={680}
        centered
        destroyOnClose
      >
        <AiChatInput
          onConfirm={handleAiConfirm}
          onGenerate={handleAiGenerate}
        />
      </Modal>

      <Modal
        title={
          <Space>
            <CarryOutOutlined style={{ color: '#722ed1' }} />
            <span>行李清单</span>
          </Space>
        }
        open={luggageModalOpen}
        onCancel={() => setLuggageModalOpen(false)}
        footer={null}
        width={720}
        centered
        destroyOnClose
      >
        <LuggageChecklist
          days={formData.days}
          city={formData.city}
          people={formData.travelers}
        />
      </Modal>

      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#722ed1' }} />
            <span>AI 生成结果</span>
          </Space>
        }
        open={aiGenerateModalOpen}
        onCancel={() => setAiGenerateModalOpen(false)}
        footer={null}
        width={650}
      >
        {aiGenerateLoading ? (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>AI 正在生成内容，请稍候...</div>
          </div>
        ) : aiGenerateResult ? (
          <div>
            {Object.entries(aiGenerateResult).map(([key, value]) => (
              <div key={key} style={{ marginBottom: 16 }}>
                {typeof value === 'string' ? (
                  <Card size="small" style={{ background: '#fafafa' }}>
                    <Typography.Text style={{ whiteSpace: 'pre-wrap' }}>
                      {value}
                    </Typography.Text>
                  </Card>
                ) : Array.isArray(value) ? (
                  <ul style={{ paddingLeft: 20, margin: '8px 0' }}>
                    {value.map((item, idx) => (
                      <li key={idx} style={{ marginBottom: 4 }}>{item}</li>
                    ))}
                  </ul>
                ) : typeof value === 'object' ? (
                  Object.entries(value).map(([k, v]) => (
                    <div key={k} style={{ marginBottom: 8 }}>
                      <Text strong style={{ color: '#722ed1' }}>{k}: </Text>
                      <span>{v}</span>
                    </div>
                  ))
                ) : null}
              </div>
            ))}
            <div style={{ textAlign: 'center', marginTop: 24, display: 'flex', gap: 12, justifyContent: 'center' }}>
              <Button icon={<CopyOutlined />} onClick={() => handleCopy(JSON.stringify(aiGenerateResult, null, 2))}>
                复制内容
              </Button>
              <Button
                type="primary"
                icon={<DownloadOutlined />}
                onClick={() => handleDownload(
                  JSON.stringify(aiGenerateResult, null, 2),
                  `${formData.city}_${aiGenerateType || '行程'}_AI生成.txt`
                )}
              >
                下载文件
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>

      <ExportModal
        ref={exportModalRef}
        itineraryData={{
          days: generatedResult?.itinerary?.days || [],
          summary: generatedResult?.itinerary?.summary || [],
          tips: generatedResult?.itinerary?.tips || [],
          total_cost_estimate: generatedResult?.itinerary?.total_cost_estimate || {},
        }}
        title={`${formData.city} ${formData.days}天行程`}
      />
    </div>
  )
}
