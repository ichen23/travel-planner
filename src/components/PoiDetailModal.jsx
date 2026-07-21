import { Modal, Image, Tag, Rate, Typography, Descriptions, List, Button, Divider, Space, Tooltip, Empty, Spin, message, Row, Col, Select, Form } from 'antd'
import { EnvironmentOutlined, ClockCircleOutlined, DollarOutlined, PhoneOutlined, StarFilled, CalendarOutlined, CarOutlined, CameraOutlined, FileTextOutlined, ThunderboltOutlined, ExclamationCircleOutlined, RobotOutlined, ArrowLeftOutlined, PlusOutlined, CheckCircleOutlined, FormatPainterOutlined } from '@ant-design/icons'
import { useState, useEffect } from 'react'
import { getPoiDetail, generateAIContent, searchNearby } from '../services/destinationService'
import { getAICacheItem, setAICache } from '../services/storageService'
import { useFavoritesStore } from '../stores/favoritesStore'
import { usePlannerStore } from '../stores/plannerStore'

const { Title, Text, Paragraph } = Typography

const PoiDetailModal = ({ visible, poi, onClose, nestedMode = false, onOpenNested }) => {
  const [detail, setDetail] = useState(null)
  const [loading, setLoading] = useState(false)
  const [aiModalOpen, setAiModalOpen] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiResult, setAiResult] = useState(null)
  const [styleModalOpen, setStyleModalOpen] = useState(false)
  const [pendingTemplateType, setPendingTemplateType] = useState(null)
  const [nearbyData, setNearbyData] = useState({ attractions: [], foods: [], hotels: [] })
  const [nearbyLoading, setNearbyLoading] = useState(false)
  const [nestedPoi, setNestedPoi] = useState(null)
  const [nestedVisible, setNestedVisible] = useState(false)
  const [addToItineraryModalOpen, setAddToItineraryModalOpen] = useState(false)
  const [selectedDay, setSelectedDay] = useState(1)
  const [form] = Form.useForm()
  const addToFavoritesStore = useFavoritesStore((state) => state.addToFavorites)
  const { schedule, addScheduleItem, setDays } = usePlannerStore()

  const STYLE_OPTIONS = {
    travel_copy: [
      { key: 'travel_copy', name: '📝 普通游玩', desc: '简洁的游玩记录' },
      { key: 'poetic', name: '🌸 诗意散文', desc: '文艺诗意的随笔' },
      { key: 'humorous', name: '😂 幽默吐槽', desc: '搞笑幽默的体验' },
      { key: 'literary', name: '📚 文艺风格', desc: '文艺青年的散文' },
      { key: 'ancient', name: '🏮 古风游记', desc: '仿古风格记录' },
      { key: 'epic', name: '⚔️ 史诗叙事', desc: '宏大叙事故事' },
    ],
    punch_card: [
      { key: 'punch_card', name: '✅ 实用攻略', desc: '简洁实用指南' },
      { key: 'poetic', name: '🎨 文艺打卡', desc: '文艺风格描述' },
      { key: 'humorous', name: '😄 搞笑打卡', desc: '轻松幽默风格' },
      { key: 'literary', name: '📖 深度游记', desc: '详细深度记录' },
    ],
    photo_spots: [
      { key: 'photo_spots', name: '📷 标准推荐', desc: '经典拍照位置' },
      { key: 'poetic', name: '🌅 光影意境', desc: '光影氛围建议' },
      { key: 'literary', name: '🎭 人像构图', desc: '人像拍照技巧' },
      { key: 'humorous', name: '🤳 趣味打卡', desc: '创意拍照点子' },
    ],
  }

  const getStyleOptions = (templateType) => {
    return STYLE_OPTIONS[templateType] || STYLE_OPTIONS.travel_copy
  }

  const handleStyleSelect = (templateType, styleKey) => {
    setStyleModalOpen(false)
    handleAIGenerate(styleKey)
  }

  useEffect(() => {
    if (visible && poi) {
      setDetail(poi)
      if (poi?.id) {
        loadDetail(poi)
      } else {
        loadNearbyData(poi)
      }
    }
  }, [visible, poi])

  const loadNearbyData = async (poiData) => {
    const data = poiData || detail || poi
    const lng = data?.lng || data?.location?.lng
    const lat = data?.lat || data?.location?.lat
    
    if (!lng || !lat) {
      console.warn('无法获取坐标，跳过附近搜索')
      return
    }
    
    setNearbyLoading(true)
    try {
      const [attractionsRes, foodsRes, hotelsRes] = await Promise.all([
        searchNearby(lng, lat, '', 5000, '风景名胜', 10),
        searchNearby(lng, lat, '', 5000, '餐厅', 10),
        searchNearby(lng, lat, '', 5000, '住宿服务', 10),
      ])
      
      setNearbyData({
        attractions: attractionsRes?.pois || [],
        foods: foodsRes?.pois || [],
        hotels: hotelsRes?.pois || [],
      })
    } catch (e) {
      console.error('加载附近数据失败:', e)
      message.error('加载附近信息失败')
    } finally {
      setNearbyLoading(false)
    }
  }

  const loadDetail = async (poiData) => {
    const targetPoi = poiData || poi
    if (!targetPoi?.id) {
      loadNearbyData(targetPoi)
      return
    }
    
    setLoading(true)
    try {
      const result = await getPoiDetail(targetPoi.id)
      if (result.success && result.poi) {
        setDetail(result.poi)
        loadNearbyData(result.poi)
      } else {
        loadNearbyData(targetPoi)
      }
    } catch (error) {
      console.error('加载POI详情失败:', error)
      loadNearbyData(targetPoi)
    } finally {
      setLoading(false)
    }
  }

  const handleAIGenerate = async (templateType, forceRefresh = false) => {
    const currentData = detail || poi
    if (!currentData) return
    
    const cacheKey = `${templateType}_${currentData.id || currentData.name}`
    
    if (!forceRefresh) {
      const cached = getAICacheItem(cacheKey)
      if (cached && typeof cached === 'object' && cached.content && cached.content.length > 50) {
        setAiResult(cached)
        setAiModalOpen(true)
        return
      }
    }
    
    setAiLoading(true)
    setAiModalOpen(true)
    
    const tipsText = currentData.tips ? currentData.tips.join('；') : ''
    const typeName = (currentData.type || '').split(';')[0] || '景点'
    const address = currentData.address || ''
    const openTime = typeof currentData.open_time === 'string' ? currentData.open_time : ''
    const cost = currentData.cost > 0 ? `人均¥${currentData.cost}` : ''
    const rating = currentData.rating > 0 ? `评分${currentData.rating}` : ''
    
    const contextData = {
      title: currentData.name || '景点',
      name: currentData.name || '景点',
      type: typeName,
      location: currentData.name + (address ? ' - ' + address : ''),
      city: currentData.cityname || currentData.city || '',
      description: `${currentData.name}是一个著名的${typeName}景点${address ? '，位于' + address : ''}`,
      content: '',
      highlight: tipsText || `来到${currentData.name}，体验${typeName}的独特魅力`,
      days: 1,
      season: '四季',
      budget: cost || '免费',
      people: '多人',
      tips: tipsText || '',
      address: address,
      open_time: openTime,
      rating: rating,
    }
    
    try {
      const response = await generateAIContent(templateType, contextData)
      console.log('AI生成响应:', response)
      
      if (response && response.success && response.content) {
        setAiResult(response)
        setAICache(cacheKey, response)
      } else {
        const errorMsg = response?.error || '生成内容为空，请重试'
        console.error('AI生成失败:', errorMsg, response)
        message.error(errorMsg)
      }
    } catch (error) {
      console.error('AI生成请求异常:', error)
      message.error('网络异常，请检查后端服务是否正常运行')
    } finally {
      setAiLoading(false)
    }
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  }

  const handlePoiClick = (nearbyPoi) => {
    setNestedPoi(nearbyPoi)
    setNestedVisible(true)
  }

  const handleAddToFavorites = () => {
    const data = detail || poi
    if (!data) return
    try {
      addToFavoritesStore('poi', data)
      message.success('已添加到收藏')
    } catch (error) {
      message.error('添加失败')
    }
  }

  const handleOpenAddToItinerary = () => {
    const dayCount = schedule?.days?.length || 1
    if (dayCount === 0) {
      setDays(1)
    }
    setSelectedDay(1)
    setAddToItineraryModalOpen(true)
  }

  const handleConfirmAddToItinerary = () => {
    const data = detail || poi
    if (!data) return
    
    const dayIndex = selectedDay - 1
    const item = {
      type: 'poi',
      name: data.name,
      address: data.address,
      time: '09:00-11:00',
      cost: data.cost > 0 ? data.cost : 0,
      rating: data.rating,
      image: data.photos?.[0],
      id: data.id || Date.now()
    }
    
    addScheduleItem(dayIndex, item)
    message.success(`已添加到第${selectedDay}天行程`)
    setAddToItineraryModalOpen(false)
  }

  const dayOptions = schedule?.days?.map((day, index) => ({
    label: `第${index + 1}天`,
    value: index + 1
  })) || [{ label: '第1天', value: 1 }]

  if (!visible) return null

  const currentData = detail || poi
  const photos = currentData?.photos || []
  const tips = currentData?.tips || []
  const tickets = currentData?.tickets || []
  const openTime = currentData?.open_time
  const hasTips = tips.length > 0 || tickets.length > 0 || currentData?.best_time

  const handleCloseNested = () => {
    setNestedVisible(false)
    setNestedPoi(null)
  }

  return (
    <>
    <Modal
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {nestedMode && <ArrowLeftOutlined onClick={onClose} style={{ cursor: 'pointer' }} />}
          <span style={{ flex: 1 }}>{currentData?.name || '景点详情'}</span>
        </div>
      }
      open={visible}
      onCancel={onClose}
      footer={
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
          {!nestedMode && (
            <>
              <Button type="primary" icon={<PlusOutlined />} onClick={handleOpenAddToItinerary}>
                加入行程
              </Button>
              <Button onClick={handleAddToFavorites}>
                ❤️ 收藏
              </Button>
            </>
          )}
          <Button onClick={onClose}>关闭</Button>
        </div>
      }
      width={720}
      centered
      styles={{ body: { padding: 0 } }}
      destroyOnClose
    >
      <Spin spinning={loading} tip="加载详情中...">
        <div>
          {photos.length > 0 && (
            <div style={{ position: 'relative', height: 300, overflow: 'hidden' }}>
              <Image.PreviewGroup items={photos}>
                <Image
                  src={photos[0]}
                  alt={currentData?.name}
                  style={{ width: '100%', height: '100%', objectFit: 'cover', cursor: 'pointer' }}
                  fallback="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect fill='%23f0f0f0' width='400' height='300'/%3E%3Ctext x='50%25' y='50%25' font-size='20' fill='%23999' text-anchor='middle' dominant-baseline='middle'%3E暂无图片%3C/text%3E%3C/svg%3E"
                />
              </Image.PreviewGroup>
              {photos.length > 1 && (
                <div 
                  style={{ 
                    position: 'absolute', 
                    bottom: 16, 
                    right: 16, 
                    background: 'rgba(0,0,0,0.6)', 
                    color: 'white', 
                    padding: '4px 12px', 
                    borderRadius: 16,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6
                  }}
                >
                  <CameraOutlined />
                  {photos.length} 张图片 · 点击预览全部
                </div>
              )}
            </div>
          )}

          <div style={{ padding: 24 }}>
            <div style={{ marginBottom: 24 }}>
              <Title level={3} style={{ margin: 0, marginBottom: 8 }}>
                {currentData?.name}
              </Title>
              
              <Space size={[8, 8]} wrap>
                {currentData?.rating > 0 && (
                  <Space>
                    <Rate disabled value={currentData.rating / 2} allowHalf style={{ fontSize: 14 }} />
                    <Text strong>{currentData.rating.toFixed(1)}</Text>
                  </Space>
                )}
                
                {currentData?.type && (
                  <Tag color="blue">{currentData.type.split(';')[0]}</Tag>
                )}
                
                {currentData?.id && (
                  <Tag color="green" icon={<ThunderboltOutlined />}>高德实时数据</Tag>
                )}
              </Space>
            </div>

            <Descriptions column={2} bordered size="small" style={{ marginBottom: 24 }}>
              {currentData?.address && (
                <Descriptions.Item label="地址" span={2}>
                  <Space>
                    <EnvironmentOutlined style={{ color: '#1677ff' }} />
                    {currentData.address}
                  </Space>
                </Descriptions.Item>
              )}
              
              {openTime && (
                <Descriptions.Item label="营业时间">
                  <Space>
                    <ClockCircleOutlined style={{ color: '#1677ff' }} />
                    {typeof openTime === 'string' ? openTime : (openTime[0] || '全天开放')}
                  </Space>
                </Descriptions.Item>
              )}
              
              {currentData?.cost > 0 && (
                <Descriptions.Item label="人均消费">
                  <Space>
                    <DollarOutlined style={{ color: '#faad14' }} />
                    ¥{currentData.cost}
                  </Space>
                </Descriptions.Item>
              )}
              
              {currentData?.tel && (
                <Descriptions.Item label="联系电话" span={2}>
                  <Space>
                    <PhoneOutlined style={{ color: '#722ed1' }} />
                    {Array.isArray(currentData.tel) ? currentData.tel.join(', ') : currentData.tel}
                  </Space>
                </Descriptions.Item>
              )}
            </Descriptions>

            {hasTips && (
              <>
                <Divider orientation="left">
                  <FileTextOutlined /> 实用信息
                </Divider>

                {tickets.length > 0 && (
                  <div style={{ marginBottom: 16 }}>
                    <Title level={5} style={{ marginBottom: 12, color: '#faad14' }}>
                      门票信息
                    </Title>
                    <List
                      size="small"
                      dataSource={tickets}
                      renderItem={(ticket) => (
                        <List.Item>
                          <Space direction="vertical" size={0} style={{ width: '100%' }}>
                            <Space>
                              <Text strong>{ticket.item}</Text>
                              <Tag color="orange">{ticket.price}</Tag>
                            </Space>
                            {ticket.booking && (
                              <Text type="secondary" style={{ fontSize: 12 }}>
                                <ExclamationCircleOutlined /> {ticket.booking}
                              </Text>
                            )}
                            {ticket.url && (
                              <a href={ticket.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: 12 }}>
                                预订链接
                              </a>
                            )}
                          </Space>
                        </List.Item>
                      )}
                    />
                  </div>
                )}

                {currentData?.best_time && (
                  <div style={{ marginBottom: 16 }}>
                    <Space>
                      <CalendarOutlined style={{ color: '#52c41a' }} />
                      <Text strong>最佳游览时间：</Text>
                      <Text>{currentData.best_time}</Text>
                    </Space>
                  </div>
                )}

                {currentData?.transport && (
                  <div style={{ marginBottom: 16 }}>
                    <Space>
                      <CarOutlined style={{ color: '#1677ff' }} />
                      <Text strong>交通指南：</Text>
                      <Text>{currentData.transport}</Text>
                    </Space>
                  </div>
                )}

                {tips.length > 0 && (
                  <div style={{ marginBottom: 16 }}>
                    <Title level={5} style={{ marginBottom: 12, color: '#1677ff' }}>
                      游览贴士
                    </Title>
                    <ul style={{ paddingLeft: 20, margin: 0 }}>
                      {tips.map((tip, index) => (
                        <li key={index} style={{ marginBottom: 6, fontSize: 13, color: '#555' }}>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {currentData?.photos_hint && (
                  <div>
                    <Space>
                      <CameraOutlined style={{ color: '#eb2f96' }} />
                      <Text strong>拍照建议：</Text>
                      <Text>{currentData.photos_hint}</Text>
                    </Space>
                  </div>
                )}
              </>
            )}

            <Divider orientation="left">
              <RobotOutlined style={{ color: '#722ed1' }} /> AI 一键生成
            </Divider>

            <Row gutter={[12, 12]} style={{ marginBottom: 16 }}>
              <Col span={8}>
                <Button
                  block
                  icon={<FileTextOutlined />}
                  onClick={() => { setPendingTemplateType('travel_copy'); setStyleModalOpen(true); }}
                  style={{ height: 40, borderRadius: 8 }}
                >
                  游玩文案
                </Button>
              </Col>
              <Col span={8}>
                <Button
                  block
                  icon={<FileTextOutlined />}
                  onClick={() => { setPendingTemplateType('punch_card'); setStyleModalOpen(true); }}
                  style={{ height: 40, borderRadius: 8 }}
                >
                  打卡攻略
                </Button>
              </Col>
              <Col span={8}>
                <Button
                  block
                  icon={<FileTextOutlined />}
                  onClick={() => { setPendingTemplateType('photo_spots'); setStyleModalOpen(true); }}
                  style={{ height: 40, borderRadius: 8 }}
                >
                  拍照建议
                </Button>
              </Col>
            </Row>

            <Divider orientation="left">
              <EnvironmentOutlined style={{ color: '#52c41a' }} /> 附近推荐
            </Divider>

            <NearbySection 
              data={nearbyData} 
              loading={nearbyLoading}
              onRefresh={loadNearbyData}
              onPoiClick={handlePoiClick}
            />

            {!hasTips && nearbyData.attractions.length === 0 && nearbyData.foods.length === 0 && nearbyData.hotels.length === 0 && (
              <Empty 
                description="暂无详细贴士" 
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                style={{ margin: '40px 0' }}
              />
            )}
          </div>
        </div>
      </Spin>

      <Modal
        title={
          <Space>
            <FormatPainterOutlined style={{ color: '#722ed1' }} />
            选择生成风格
          </Space>
        }
        open={styleModalOpen}
        onCancel={() => setStyleModalOpen(false)}
        footer={null}
        width={520}
      >
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12 }}>
          {getStyleOptions(pendingTemplateType).map(option => (
            <div
              key={option.key}
              onClick={() => handleStyleSelect(pendingTemplateType, option.key)}
              style={{
                padding: 16,
                borderRadius: 12,
                border: '2px solid #f0f0f0',
                cursor: 'pointer',
                transition: 'all 0.2s',
                background: '#fafafa',
              }}
              onMouseEnter={e => {
                e.target.style.borderColor = '#722ed1'
                e.target.style.background = '#f9f0ff'
              }}
              onMouseLeave={e => {
                e.target.style.borderColor = '#f0f0f0'
                e.target.style.background = '#fafafa'
              }}
            >
              <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 6 }}>
                {option.name}
              </div>
              <div style={{ fontSize: 12, color: '#888' }}>
                {option.desc}
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 16, textAlign: 'center', color: '#999', fontSize: 12 }}>
          💡 选择一种风格后，AI将为您生成对应的内容
        </div>
      </Modal>

      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#722ed1' }} />
            <span>AI 生成结果</span>
          </Space>
        }
        open={aiModalOpen}
        onCancel={() => setAiModalOpen(false)}
        footer={null}
        width={650}
      >
        {aiLoading ? (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>AI 正在生成内容...</div>
          </div>
        ) : aiResult ? (
          <div>
            {aiResult.title && (
              <div style={{
                fontSize: 18,
                fontWeight: 600,
                color: '#722ed1',
                marginBottom: 16,
                paddingBottom: 12,
                borderBottom: '2px solid #f0f0f0'
              }}>
                📌 {aiResult.title}
              </div>
            )}
            {aiResult.content && (
              <div style={{
                background: 'linear-gradient(135deg, #f9f0ff 0%, #f0f5ff 100%)',
                padding: 20,
                borderRadius: 12,
                marginBottom: 16,
                maxHeight: 400,
                overflowY: 'auto'
              }}>
                <Typography.Paragraph style={{ 
                  whiteSpace: 'pre-wrap',
                  margin: 0,
                  fontSize: 14,
                  lineHeight: 1.8,
                  color: '#333'
                }}>
                  {aiResult.content}
                </Typography.Paragraph>
              </div>
            )}
            {!aiResult.content && Object.entries(aiResult).map(([key, value]) => (
              key !== 'title' && key !== 'type' && (
                <div key={key} style={{ marginBottom: 16 }}>
                  <div style={{ fontWeight: 600, marginBottom: 8, color: '#722ed1' }}>
                    {typeof key === 'string' ? key.replace(/_/g, ' ') : ''}
                  </div>
                  {Array.isArray(value) ? (
                    <ul style={{ paddingLeft: 20, margin: 0 }}>
                      {value.map((item, idx) => (
                        <li key={idx} style={{ marginBottom: 4 }}>{item}</li>
                      ))}
                    </ul>
                  ) : typeof value === 'object' ? (
                    Object.entries(value).map(([k, v]) => (
                      <div key={k} style={{ marginBottom: 8 }}>
                        <Text strong>{k}: </Text>
                        <span>{v}</span>
                      </div>
                    ))
                  ) : (
                    <Typography.Paragraph style={{ whiteSpace: 'pre-wrap' }}>
                      {value}
                    </Typography.Paragraph>
                  )}
                </div>
              )
            ))}
            <div style={{ textAlign: 'center', marginTop: 16, display: 'flex', gap: 12, justifyContent: 'center' }}>
              {aiResult.content && (
                <Button type="primary" onClick={() => handleCopy(aiResult.content)}>
                  📋 复制内容
                </Button>
              )}
              <Button onClick={() => handleAIGenerate(aiResult.type || 'travel_copy', true)}>
                🔄 重新生成
              </Button>
            </div>
          </div>
        ) : null}
      </Modal>
    </Modal>

      <PoiDetailModal
        visible={nestedVisible}
        poi={nestedPoi}
        onClose={handleCloseNested}
        nestedMode={true}
      />

      <Modal
        title={
          <Space>
            <CheckCircleOutlined style={{ color: '#52c41a' }} />
            <span>加入行程</span>
          </Space>
        }
        open={addToItineraryModalOpen}
        onCancel={() => setAddToItineraryModalOpen(false)}
        onOk={handleConfirmAddToItinerary}
        okText="确认添加"
        cancelText="取消"
      >
        <div style={{ padding: '16px 0' }}>
          <div style={{ marginBottom: 16 }}>
            <Text strong>景点名称：</Text>
            <Text>{currentData?.name}</Text>
          </div>
          {currentData?.address && (
            <div style={{ marginBottom: 16 }}>
              <Text strong>地址：</Text>
              <Text>{currentData.address}</Text>
            </div>
          )}
          <div style={{ marginBottom: 16 }}>
            <Text strong>选择日期：</Text>
            <Select
              style={{ width: 150, marginLeft: 8 }}
              value={selectedDay}
              onChange={setSelectedDay}
              options={dayOptions}
            />
          </div>
          <div style={{ background: '#f6ffed', padding: 12, borderRadius: 8 }}>
            <Text type="success">
              💡 提示：添加后可在"行程规划"页面调整顺序和时间
            </Text>
          </div>
        </div>
      </Modal>
      </>
  )
}

const NearbySection = ({ data, loading, onRefresh, onPoiClick }) => {
  const [activeTab, setActiveTab] = useState('attractions')
  
  const tabs = [
    { key: 'attractions', label: '🎯 附近景点', data: data.attractions },
    { key: 'foods', label: '🍜 附近美食', data: data.foods },
    { key: 'hotels', label: '🏨 附近住宿', data: data.hotels },
  ]
  
  const activeData = tabs.find(t => t.key === activeTab)?.data || []
  
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 20 }}>
        <Spin size="small" />
        <div style={{ marginTop: 8, color: '#999', fontSize: 12 }}>加载附近信息中...</div>
      </div>
    )
  }
  
  if (activeData.length === 0) {
    return (
      <Empty 
        description="暂无附近推荐" 
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        style={{ margin: '20px 0' }}
      />
    )
  }
  
  return (
    <div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
        {tabs.map(tab => (
          <Button
            key={tab.key}
            type={activeTab === tab.key ? 'primary' : 'default'}
            onClick={() => setActiveTab(tab.key)}
            size="small"
          >
            {tab.label} ({tab.data.length})
          </Button>
        ))}
        <Button size="small" onClick={onRefresh}>
          🔄 刷新
        </Button>
      </div>
      
      <List
        size="small"
        dataSource={activeData.slice(0, 6)}
        renderItem={(item) => (
          <List.Item 
            style={{ 
              padding: '10px 0', 
              cursor: onPoiClick ? 'pointer' : 'default',
              transition: 'all 0.2s',
              borderRadius: 8
            }}
            onClick={() => onPoiClick && onPoiClick(item)}
            onMouseEnter={(e) => {
              if (onPoiClick) {
                e.currentTarget.style.background = '#f5f5f5'
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'flex-start', width: '100%', gap: 12 }}>
              {item.photos?.[0] ? (
                <img 
                  src={item.photos[0]} 
                  alt={item.name}
                  style={{ width: 60, height: 60, objectFit: 'cover', borderRadius: 8, flexShrink: 0 }}
                />
              ) : (
                <div style={{ width: 60, height: 60, backgroundColor: '#f5f5f5', borderRadius: 8, flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <EnvironmentOutlined style={{ fontSize: 24, color: '#bfbfbf' }} />
                </div>
              )}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 500, marginBottom: 4, fontSize: 14 }}>
                  {item.name}
                  {onPoiClick && <span style={{ fontSize: 12, color: '#1677ff', marginLeft: 8 }}>点击查看详情</span>}
                </div>
                {item.address && (
                  <div style={{ fontSize: 12, color: '#999', marginBottom: 4 }}>
                    📍 {item.address}
                  </div>
                )}
                <div style={{ display: 'flex', gap: 12, fontSize: 12 }}>
                  {item.distance && (
                    <span style={{ color: '#52c41a' }}>🚶 {Math.round(item.distance)}米</span>
                  )}
                  {item.rating > 0 && (
                    <span style={{ color: '#faad14' }}>⭐ {item.rating.toFixed(1)}</span>
                  )}
                  {item.cost && (
                    <span style={{ color: '#1890ff' }}>💰 ¥{item.cost}</span>
                  )}
                </div>
              </div>
            </div>
          </List.Item>
        )}
      />
    </div>
  )
}

export default PoiDetailModal
