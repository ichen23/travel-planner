import { useState, useEffect } from 'react'
import { 
  Card, Tabs, Input, Select, Button, Row, Col, Typography, 
  Space, Divider, List, Tag, message, Modal, Empty, Statistic,
  InputNumber, Table, Tooltip, Segmented, Checkbox, Form
} from 'antd'
import {
  CalculatorOutlined, CarryOutOutlined, WarningOutlined, CameraOutlined,
  FileTextOutlined, EditOutlined, PlusOutlined, DeleteOutlined,
  CopyOutlined, DownloadOutlined, SaveOutlined
} from '@ant-design/icons'
import AiGenerateButton from '../components/AiGenerateButton'
import { 
  getNotes, saveNote, deleteNote,
  getDrafts, saveDraft, deleteDraft,
  getPreferences, updatePreferences,
  exportAllData, importAllData,
} from '../services/storageService'

const { Title, Text, Paragraph } = Typography
const { TabPane } = Tabs

const SEASONS = [
  { value: '春', label: '🌸 春季' },
  { value: '夏', label: '☀️ 夏季' },
  { value: '秋', label: '🍂 秋季' },
  { value: '冬', label: '❄️ 冬季' },
]

const PEOPLE_TYPES = [
  { value: '单人', label: '👤 单人' },
  { value: '情侣', label: '💕 情侣' },
  { value: '亲子', label: '👨‍👩‍👧 亲子' },
  { value: '朋友', label: '👥 朋友' },
]

export default function ToolboxPage() {
  const [activeTab, setActiveTab] = useState('budget')
  
  return (
    <div style={{ padding: '24px 0' }}>
      <Title level={2}>🧰 旅行工具箱</Title>
      <Text type="secondary">所有工具数据本地存储，无需登录，即开即用</Text>
      
      <Card style={{ marginTop: 24, borderRadius: 16 }}>
        <Tabs activeKey={activeTab} onChange={setActiveTab} size="large">
          <TabPane tab={<span><CalculatorOutlined /> 预算计算器</span>} key="budget">
            <BudgetCalculator />
          </TabPane>
          <TabPane tab={<span><CarryOutOutlined /> 行李清单</span>} key="luggage">
            <LuggageGenerator />
          </TabPane>
          <TabPane tab={<span><WarningOutlined /> 避坑助手</span>} key="pitfall">
            <PitfallAssistant />
          </TabPane>
          <TabPane tab={<span><CameraOutlined /> 拍照机位</span>} key="photo">
            <PhotoSpots />
          </TabPane>
          <TabPane tab={<span><FileTextOutlined /> 文档合并</span>} key="merge">
            <DocumentMerger />
          </TabPane>
          <TabPane tab={<span><EditOutlined /> 备忘录</span>} key="notes">
            <NotesManager />
          </TabPane>
        </Tabs>
      </Card>
    </div>
  )
}

function BudgetCalculator() {
  const [items, setItems] = useState([
    { id: 1, category: '交通', name: '高铁票', amount: 500, note: '' },
    { id: 2, category: '住宿', name: '酒店3晚', amount: 900, note: '300/晚' },
    { id: 3, category: '餐饮', name: '每日三餐', amount: 600, note: '200/天' },
    { id: 4, category: '门票', name: '景区门票', amount: 200, note: '' },
    { id: 5, category: '其他', name: '市内交通', amount: 150, note: '' },
  ])
  const [newItem, setNewItem] = useState({ category: '交通', name: '', amount: 0, note: '' })
  
  const categories = ['交通', '住宿', '餐饮', '门票', '购物', '其他']
  
  const addItem = () => {
    if (newItem.name && newItem.amount > 0) {
      setItems([...items, { ...newItem, id: Date.now() }])
      setNewItem({ category: '交通', name: '', amount: 0, note: '' })
    }
  }
  
  const removeItem = (id) => setItems(items.filter(i => i.id !== id))
  
  const updateItem = (id, field, value) => {
    setItems(items.map(i => i.id === id ? { ...i, [field]: value } : i))
  }
  
  const total = items.reduce((sum, i) => sum + i.amount, 0)
  
  const categoryTotals = categories.map(cat => ({
    category: cat,
    total: items.filter(i => i.category === cat).reduce((sum, i) => sum + i.amount, 0),
  })).filter(c => c.total > 0)

  const columns = [
    { title: '类别', dataIndex: 'category', key: 'category', width: 80 },
    { title: '项目', dataIndex: 'name', key: 'name' },
    { 
      title: '金额', 
      dataIndex: 'amount', 
      key: 'amount', 
      width: 100,
      render: (val) => <Text strong style={{ color: '#ff4d4f' }}>¥{val}</Text>,
    },
    { title: '备注', dataIndex: 'note', key: 'note' },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_, record) => (
        <Button type="text" danger icon={<DeleteOutlined />} onClick={() => removeItem(record.id)} />
      ),
    },
  ]

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={16}>
          <Card title="费用明细" size="small" style={{ marginBottom: 16 }}>
            <Form layout="inline" style={{ marginBottom: 16 }}>
              <Form.Item>
                <Select 
                  value={newItem.category} 
                  onChange={(v) => setNewItem({...newItem, category: v})}
                  style={{ width: 100 }}
                >
                  {categories.map(c => <Select.Option key={c} value={c}>{c}</Select.Option>)}
                </Select>
              </Form.Item>
              <Form.Item>
                <Input 
                  placeholder="项目名称" 
                  value={newItem.name}
                  onChange={(e) => setNewItem({...newItem, name: e.target.value})}
                  style={{ width: 150 }}
                />
              </Form.Item>
              <Form.Item>
                <InputNumber 
                  placeholder="金额" 
                  min={0}
                  value={newItem.amount}
                  onChange={(v) => setNewItem({...newItem, amount: v || 0})}
                  style={{ width: 120 }}
                  prefix="¥"
                />
              </Form.Item>
              <Form.Item>
                <Button type="primary" icon={<PlusOutlined />} onClick={addItem}>添加</Button>
              </Form.Item>
            </Form>
            
            <Table 
              columns={columns} 
              dataSource={items} 
              rowKey="id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
        
        <Col xs={24} md={8}>
          <Card title="预算汇总" size="small" style={{ marginBottom: 16 }}>
            <Statistic 
              title="总预算" 
              value={total} 
              prefix="¥" 
              valueStyle={{ color: '#ff4d4f', fontSize: 32 }}
            />
            <Divider />
            {categoryTotals.map(ct => (
              <div key={ct.category} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <Text>{ct.category}</Text>
                <Text strong>¥{ct.total}</Text>
              </div>
            ))}
          </Card>
        </Col>
      </Row>
    </div>
  )
}

function LuggageGenerator() {
  const [form, setForm] = useState({
    city: '北京',
    days: 3,
    season: '春',
    people: '单人',
    weather: '晴',
  })
  
  const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '西安', '重庆', '南京', '武汉', '厦门', '青岛', '大理', '丽江']

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={10}>
          <Card title="出行信息" size="small">
            <Form layout="vertical">
              <Form.Item label="目的地">
                <Select 
                  value={form.city} 
                  onChange={(v) => setForm({...form, city: v})}
                  showSearch
                  placeholder="选择城市"
                >
                  {cities.map(c => <Select.Option key={c} value={c}>{c}</Select.Option>)}
                </Select>
              </Form.Item>
              <Form.Item label="出行天数">
                <InputNumber 
                  min={1} 
                  max={30} 
                  value={form.days}
                  onChange={(v) => setForm({...form, days: v || 1})}
                  style={{ width: '100%' }}
                />
              </Form.Item>
              <Form.Item label="出行季节">
                <Segmented 
                  value={form.season}
                  onChange={(v) => setForm({...form, season: v})}
                  options={SEASONS.map(s => ({ label: s.label, value: s.value }))}
                  style={{ width: '100%' }}
                />
              </Form.Item>
              <Form.Item label="同行人员">
                <Segmented 
                  value={form.people}
                  onChange={(v) => setForm({...form, people: v})}
                  options={PEOPLE_TYPES.map(p => ({ label: p.label, value: p.value }))}
                  style={{ width: '100%' }}
                />
              </Form.Item>
              <Form.Item label="天气情况">
                <Select 
                  value={form.weather} 
                  onChange={(v) => setForm({...form, weather: v})}
                >
                  <Select.Option value="晴">☀️ 晴天</Select.Option>
                  <Select.Option value="雨">🌧️ 雨天</Select.Option>
                  <Select.Option value="多云">⛅ 多云</Select.Option>
                  <Select.Option value="雪">❄️ 下雪</Select.Option>
                </Select>
              </Form.Item>
            </Form>
            
            <AiGenerateButton
              templateType="packing_list"
              context={form}
              buttonText="一键生成行李清单"
              buttonType="primary"
            />
          </Card>
        </Col>
        
        <Col xs={24} md={14}>
          <Card title="快速生成入口" size="small">
            <Space direction="vertical" style={{ width: '100%' }}>
              <AiGenerateButton
                templateType="packing_list"
                context={{ days: form.days, season: form.season, people: form.people, weather: form.weather }}
                buttonText="📋 标准行李清单"
              />
              <AiGenerateButton
                templateType="packing_list"
                context={{ days: form.days + 2, season: form.season, people: form.people, weather: form.weather === '雨' ? '多雨' : '干燥' }}
                buttonText="🎒 周末短途 (2+天)"
              />
              <AiGenerateButton
                templateType="packing_list"
                context={{ days: 5, season: form.season, people: '亲子', weather: form.weather }}
                buttonText="👨‍👩‍👧 亲子出行"
              />
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

function PitfallAssistant() {
  const [city, setCity] = useState('北京')
  
  const cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '西安', '重庆', '南京', '武汉', '厦门', '青岛', '大理', '丽江', '三亚', '长沙', '张家界', '桂林']

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={10}>
          <Card title="选择城市" size="small">
            <Form layout="vertical">
              <Form.Item label="目的地">
                <Select 
                  value={city} 
                  onChange={(v) => setCity(v)}
                  showSearch
                  placeholder="选择要去的城市"
                >
                  {cities.map(c => <Select.Option key={c} value={c}>{c}</Select.Option>)}
                </Select>
              </Form.Item>
            </Form>
            
            <Space direction="vertical" style={{ width: '100%' }}>
              <AiGenerateButton
                templateType="pitfall_guide"
                context={{ city }}
                buttonText="⚠️ 生成避坑指南"
                buttonType="primary"
              />
              <AiGenerateButton
                templateType="station_guide"
                context={{ station: `${city}站` }}
                buttonText="🚄 生成车站攻略"
              />
            </Space>
          </Card>
        </Col>
        
        <Col xs={24} md={14}>
          <Card title="城市速览" size="small">
            <AiGenerateButton
              templateType="city_brief"
              context={{ city, days: 3 }}
              buttonText={`📍 ${city}3天速览`}
              buttonType="primary"
              block
            />
            <Divider />
            <Space direction="vertical" style={{ width: '100%' }}>
              <Text strong>其他工具：</Text>
              <Row gutter={8}>
                <Col span={12}>
                  <AiGenerateButton
                    templateType="pitfall_guide"
                    context={{ city }}
                    buttonText="避坑指南"
                    size="small"
                  />
                </Col>
                <Col span={12}>
                  <AiGenerateButton
                    templateType="city_brief"
                    context={{ city, days: 5 }}
                    buttonText="5天速览"
                    size="small"
                  />
                </Col>
              </Row>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

function PhotoSpots() {
  const [form, setForm] = useState({
    city: '北京',
    location: '故宫',
    time: '',
  })
  
  const citySpots = {
    '北京': ['故宫', '长城', '颐和园', '天坛', '天安门', '南锣鼓巷'],
    '上海': ['外滩', '东方明珠', '豫园', '田子坊', '陆家嘴', '南京路'],
    '成都': ['宽窄巷子', '锦里', '大熊猫基地', '春熙路', '都江堰'],
    '西安': ['兵马俑', '古城墙', '大雁塔', '回民街', '华山'],
    '杭州': ['西湖', '灵隐寺', '千岛湖', '宋城', '西溪湿地'],
  }

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={12}>
          <Card title="拍照设置" size="small">
            <Form layout="vertical">
              <Form.Item label="城市">
                <Select 
                  value={form.city} 
                  onChange={(v) => setForm({...form, city: v, location: (citySpots[v] || [''])[0]})}
                >
                  {Object.keys(citySpots).map(c => <Select.Option key={c} value={c}>{c}</Select.Option>)}
                </Select>
              </Form.Item>
              <Form.Item label="景点">
                <Select 
                  value={form.location} 
                  onChange={(v) => setForm({...form, location: v})}
                >
                  {(citySpots[form.city] || ['']).map(s => <Select.Option key={s} value={s}>{s}</Select.Option>)}
                </Select>
              </Form.Item>
              <Form.Item label="拍摄时段">
                <Select 
                  value={form.time} 
                  onChange={(v) => setForm({...form, time: v})}
                  placeholder="可选"
                >
                  <Select.Option value="日出">🌅 日出</Select.Option>
                  <Select.Option value="上午">☀️ 上午</Select.Option>
                  <Select.Option value="下午">🌤️ 下午</Select.Option>
                  <Select.Option value="日落">🌇 日落</Select.Option>
                  <Select.Option value="夜晚">🌃 夜晚</Select.Option>
                </Select>
              </Form.Item>
            </Form>
            
            <AiGenerateButton
              templateType="photo_spots"
              context={form}
              buttonText="📸 生成拍照攻略"
              buttonType="primary"
            />
          </Card>
        </Col>
        
        <Col xs={24} md={12}>
          <Card title="推荐景点" size="small">
            <List
              dataSource={citySpots[form.city] || []}
              renderItem={(spot) => (
                <List.Item
                  actions={[
                    <AiGenerateButton
                      templateType="photo_spots"
                      context={{ city: form.city, location: spot, time: form.time }}
                      buttonText="拍照"
                      size="small"
                    />
                  ]}
                >
                  <List.Item.Meta
                    avatar={<CameraOutlined style={{ fontSize: 24, color: '#667eea' }} />}
                    title={spot}
                    description={`${form.city}热门拍照点`}
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

function DocumentMerger() {
  const [contents, setContents] = useState({
    itinerary: '',
    ticket: '',
    city: '',
    packing: '',
  })
  const [mergedContent, setMergedContent] = useState('')
  
  const mergeDocuments = () => {
    const parts = []
    if (contents.itinerary) parts.push('【行程安排】\n' + contents.itinerary)
    if (contents.ticket) parts.push('\n【车票信息】\n' + contents.ticket)
    if (contents.city) parts.push('\n【城市攻略】\n' + contents.city)
    if (contents.packing) parts.push('\n【行李清单】\n' + contents.packing)
    
    if (parts.length === 0) {
      message.warning('请至少填写一个文档内容')
      return
    }
    
    const header = '═══════════════════════════════════\n' +
                   '        🚄 旅行出行合集\n' +
                   '═══════════════════════════════════\n\n' +
                   `生成时间：${new Date().toLocaleString()}\n\n`
    
    setMergedContent(header + parts.join('\n\n' + '─'.repeat(40) + '\n\n'))
    message.success('文档合并成功！')
  }
  
  const copyMerged = async () => {
    if (mergedContent) {
      await navigator.clipboard.writeText(mergedContent)
      message.success('已复制到剪贴板')
    }
  }
  
  const downloadMerged = () => {
    if (mergedContent) {
      const blob = new Blob([mergedContent], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `旅行出行合集_${new Date().toISOString().slice(0,10)}.txt`
      a.click()
      URL.revokeObjectURL(url)
      message.success('下载成功')
    }
  }

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={12}>
          <Card title="文档内容" size="small">
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text strong>📋 行程安排：</Text>
                <Input.TextArea
                  rows={4}
                  value={contents.itinerary}
                  onChange={(e) => setContents({...contents, itinerary: e.target.value})}
                  placeholder="粘贴你的行程安排..."
                />
              </div>
              <div>
                <Text strong>🎫 车票信息：</Text>
                <Input.TextArea
                  rows={3}
                  value={contents.ticket}
                  onChange={(e) => setContents({...contents, ticket: e.target.value})}
                  placeholder="粘贴车票信息..."
                />
              </div>
              <div>
                <Text strong>🗺️ 城市攻略：</Text>
                <Input.TextArea
                  rows={3}
                  value={contents.city}
                  onChange={(e) => setContents({...contents, city: e.target.value})}
                  placeholder="粘贴城市攻略..."
                />
              </div>
              <div>
                <Text strong>🎒 行李清单：</Text>
                <Input.TextArea
                  rows={3}
                  value={contents.packing}
                  onChange={(e) => setContents({...contents, packing: e.target.value})}
                  placeholder="粘贴行李清单..."
                />
              </div>
            </Space>
            
            <Divider />
            
            <Button type="primary" size="large" block onClick={mergeDocuments}>
              <FileTextOutlined /> 合并文档
            </Button>
          </Card>
        </Col>
        
        <Col xs={24} md={12}>
          <Card 
            title="合并结果" 
            size="small"
            extra={
              <Space>
                <Button 
                  size="small" 
                  icon={<CopyOutlined />} 
                  onClick={copyMerged}
                  disabled={!mergedContent}
                >
                  复制
                </Button>
                <Button 
                  size="small" 
                  icon={<DownloadOutlined />} 
                  onClick={downloadMerged}
                  disabled={!mergedContent}
                >
                  下载
                </Button>
              </Space>
            }
          >
            {mergedContent ? (
              <div style={{
                background: '#f5f5f5',
                padding: 16,
                borderRadius: 8,
                maxHeight: '500px',
                overflow: 'auto',
                whiteSpace: 'pre-wrap',
                fontFamily: 'monospace',
                fontSize: 12,
              }}>
                {mergedContent}
              </div>
            ) : (
              <Empty description="点击左侧按钮合并文档" />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  )
}

function NotesManager() {
  const [notes, setNotes] = useState([])
  const [editingNote, setEditingNote] = useState(null)
  const [form, setForm] = useState({ title: '', content: '', category: '出行' })
  
  const categories = ['出行', '住宿', '美食', '购物', '其他']
  
  useEffect(() => {
    setNotes(getNotes())
  }, [])
  
  const saveNoteHandler = () => {
    if (!form.title.trim()) {
      message.warning('请输入标题')
      return
    }
    
    const saved = saveNote({
      id: editingNote?.id,
      ...form,
    })
    
    setNotes(getNotes())
    setEditingNote(null)
    setForm({ title: '', content: '', category: '出行' })
    message.success('保存成功')
  }
  
  const editNote = (note) => {
    setEditingNote(note)
    setForm({ title: note.title, content: note.content, category: note.category || '出行' })
  }
  
  const deleteNoteHandler = (id) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这条笔记吗？',
      onOk: () => {
        deleteNote(id)
        setNotes(getNotes())
        message.success('删除成功')
      },
    })
  }
  
  const cancelEdit = () => {
    setEditingNote(null)
    setForm({ title: '', content: '', category: '出行' })
  }

  return (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={10}>
          <Card 
            title={editingNote ? '编辑笔记' : '新建笔记'} 
            size="small"
            extra={editingNote ? <Button size="small" onClick={cancelEdit}>取消</Button> : null}
          >
            <Form layout="vertical">
              <Form.Item label="标题">
                <Input 
                  value={form.title}
                  onChange={(e) => setForm({...form, title: e.target.value})}
                  placeholder="笔记标题"
                />
              </Form.Item>
              <Form.Item label="分类">
                <Select 
                  value={form.category}
                  onChange={(v) => setForm({...form, category: v})}
                >
                  {categories.map(c => <Select.Option key={c} value={c}>{c}</Select.Option>)}
                </Select>
              </Form.Item>
              <Form.Item label="内容">
                <Input.TextArea
                  rows={8}
                  value={form.content}
                  onChange={(e) => setForm({...form, content: e.target.value})}
                  placeholder="记录你的想法..."
                />
              </Form.Item>
              <Button type="primary" block onClick={saveNoteHandler}>
                <SaveOutlined /> {editingNote ? '更新' : '保存'}笔记
              </Button>
            </Form>
          </Card>
        </Col>
        
        <Col xs={24} md={14}>
          <Card title={`我的笔记 (${notes.length})`} size="small">
            {notes.length === 0 ? (
              <Empty description="还没有笔记，新建一条吧" />
            ) : (
              <List
                dataSource={notes}
                itemLayout="vertical"
                renderItem={(note) => (
                  <List.Item
                    actions={[
                      <Button size="small" type="link" onClick={() => editNote(note)}>编辑</Button>,
                      <Button size="small" type="link" danger onClick={() => deleteNoteHandler(note.id)}>删除</Button>,
                    ]}
                  >
                    <List.Item.Meta
                      title={
                        <Space>
                          <span>{note.title}</span>
                          <Tag color="blue">{note.category || '其他'}</Tag>
                        </Space>
                      }
                      description={
                        <div>
                          <div style={{ 
                            whiteSpace: 'pre-wrap',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            display: '-webkit-box',
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: 'vertical',
                            color: '#666',
                          }}>
                            {note.content}
                          </div>
                          <Text type="secondary" style={{ fontSize: 12 }}>
                            更新于 {new Date(note.updatedAt).toLocaleString()}
                          </Text>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  )
}
