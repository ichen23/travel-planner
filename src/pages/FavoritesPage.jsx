import { useState, useEffect } from 'react'
import { Tabs, Card, Row, Col, Tag, Typography, Empty, Button, Space, Input, List, Tooltip, Popconfirm, Dropdown } from 'antd'
import { 
  DeleteOutlined, ArrowRightOutlined, CalendarOutlined, ThunderboltOutlined,
  FolderOutlined, FolderAddOutlined, PlusOutlined, DragOutlined,
  InboxOutlined
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useFavoritesStore } from '../stores'

const { Title, Text } = Typography

export default function FavoritesPage() {
  const navigate = useNavigate()
  const [newFolderName, setNewFolderName] = useState('')
  const [showInput, setShowInput] = useState(false)
  const [dragOverFolder, setDragOverFolder] = useState(null)
  const [selectedTab, setSelectedTab] = useState('trains')

  const favorites = useFavoritesStore(s => s.favorites)
  const folders = useFavoritesStore(s => s.folders)
  const activeFolder = useFavoritesStore(s => s.activeFolder)
  const loadFavorites = useFavoritesStore(s => s.loadFavorites)
  const removeFromFavorites = useFavoritesStore(s => s.removeFromFavorites)
  const createFolder = useFavoritesStore(s => s.createFolder)
  const deleteFolder = useFavoritesStore(s => s.deleteFolder)
  const setActiveFolder = useFavoritesStore(s => s.setActiveFolder)
  const moveToFolder = useFavoritesStore(s => s.moveToFolder)

  useEffect(() => {
    loadFavorites()
  }, [])

  const folderList = Object.values(folders)
  const currentFolder = folders[activeFolder] || { items: [] }

  const getFilteredItems = (type) => {
    return currentFolder.items.filter(item => item.type === type)
  }

  const handleCreateFolder = () => {
    if (newFolderName.trim()) {
      createFolder(newFolderName.trim())
      setNewFolderName('')
      setShowInput(false)
    }
  }

  const handleDeleteFolder = (folderName) => {
    deleteFolder(folderName)
  }

  const handleDragStart = (e, type, index) => {
    e.dataTransfer.setData('application/json', JSON.stringify({ type, index, fromFolder: activeFolder }))
    e.dataTransfer.effectAllowed = 'move'
  }

  const handleDragOver = (e, folderName) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
    if (folderName !== activeFolder) {
      setDragOverFolder(folderName)
    }
  }

  const handleDragLeave = () => {
    setDragOverFolder(null)
  }

  const handleDrop = (e, toFolder) => {
    e.preventDefault()
    setDragOverFolder(null)
    try {
      const data = JSON.parse(e.dataTransfer.getData('application/json'))
      if (data.fromFolder !== toFolder) {
        moveToFolder(data.type, data.index, data.fromFolder, toFolder)
      }
    } catch (err) {
      console.error('拖拽数据解析失败:', err)
    }
  }

  const handleMoveToFolder = (type, index, toFolder) => {
    if (toFolder !== activeFolder) {
      moveToFolder(type, index, activeFolder, toFolder)
    }
  }

  const renderFolderList = () => (
    <div style={{ 
      background: '#fff', 
      borderRadius: 12, 
      padding: 16, 
      height: '100%',
      border: '1px solid #f0f0f0'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
        <FolderOutlined style={{ fontSize: 18, marginRight: 8, color: '#1677ff' }} />
        <Title level={5} style={{ margin: 0, flex: 1 }}>收藏夹</Title>
        <Tooltip title="新建收藏夹">
          <Button 
            type="text" 
            icon={<PlusOutlined />} 
            onClick={() => setShowInput(!showInput)}
          />
        </Tooltip>
      </div>

      {showInput && (
        <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
          <Input
            size="small"
            placeholder="输入收藏夹名称"
            value={newFolderName}
            onChange={(e) => setNewFolderName(e.target.value)}
            onPressEnter={handleCreateFolder}
            autoFocus
          />
          <Button size="small" type="primary" onClick={handleCreateFolder}>
            创建
          </Button>
        </div>
      )}

      <List
        dataSource={folderList}
        renderItem={(folder) => {
          const isActive = folder.name === activeFolder
          const isDragOver = dragOverFolder === folder.name
          const itemCount = folder.items?.length || 0
          const isDefault = folder.name === '默认收藏夹'

          return (
            <div
              draggable={false}
              onDragOver={(e) => handleDragOver(e, folder.name)}
              onDragLeave={handleDragLeave}
              onDrop={(e) => handleDrop(e, folder.name)}
              onClick={() => setActiveFolder(folder.name)}
              style={{
                padding: '10px 12px',
                marginBottom: 8,
                borderRadius: 8,
                cursor: 'pointer',
                background: isActive ? '#e6f4ff' : isDragOver ? '#f6ffed' : '#fafafa',
                border: `2px solid ${isActive ? '#1677ff' : isDragOver ? '#52c41a' : 'transparent'}`,
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', flex: 1, minWidth: 0 }}>
                <FolderOutlined style={{ 
                  marginRight: 8, 
                  color: isActive ? '#1677ff' : '#faad14',
                  fontSize: 16
                }} />
                <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  <div style={{ fontWeight: isActive ? 600 : 400, fontSize: 14 }}>
                    {folder.name}
                  </div>
                  <div style={{ fontSize: 11, color: '#999' }}>
                    {itemCount} 项
                  </div>
                </div>
              </div>
              {!isDefault && (
                <Popconfirm
                  title="确定删除此收藏夹？"
                  description="收藏夹中的项目将被移至默认收藏夹"
                  onConfirm={(e) => {
                    e.stopPropagation()
                    handleDeleteFolder(folder.name)
                  }}
                  onCancel={(e) => e.stopPropagation()}
                  okText="删除"
                  cancelText="取消"
                >
                  <Button
                    type="text"
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={(e) => e.stopPropagation()}
                  />
                </Popconfirm>
              )}
            </div>
          )
        }}
      />

      <div style={{ 
        marginTop: 16, 
        padding: 12, 
        background: '#f6f8fa', 
        borderRadius: 8,
        fontSize: 12,
        color: '#666',
        textAlign: 'center'
      }}>
        <DragOutlined style={{ marginRight: 4 }} />
        拖拽项目到此处移动收藏夹
      </div>
    </div>
  )

  const renderTrains = () => {
    const trainItems = getFilteredItems('trains')
    const trainList = trainItems.map(item => item.item)

    if (trainList.length === 0) {
      return <Empty description="当前收藏夹中没有车票" image={Empty.PRESENTED_IMAGE_SIMPLE} />
    }

    return (
      <div>
        <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
          共 {trainList.length} 趟列车
        </Text>
        {trainList.map((t, idx) => {
          const originalIndex = favorites.trains?.indexOf(t) ?? idx
          return (
            <Card 
              key={idx} 
              size="small" 
              style={{ marginBottom: 12, borderRadius: 12, cursor: 'grab' }}
              draggable
              onDragStart={(e) => handleDragStart(e, 'trains', originalIndex)}
            >
              <Row align="middle" gutter={16}>
                <Col xs={24} sm={2}>
                  <DragOutlined style={{ color: '#ccc', fontSize: 16 }} />
                </Col>
                <Col xs={24} sm={4}>
                  <div style={{ fontSize: 20, fontWeight: 'bold', color: t.is_high ? '#ff6b6b' : '#1677ff' }}>
                    {t.train_no}
                  </div>
                  <Tag color={t.is_high ? 'red' : 'blue'} style={{ marginTop: 4 }}>
                    {t.is_high ? '高铁' : t.type || '普快'}
                  </Tag>
                </Col>
                <Col xs={24} sm={10}>
                  <Space size="large">
                    <div>
                      <div style={{ fontWeight: 'bold', fontSize: 18 }}>{t.departure_time}</div>
                      <div style={{ color: '#999', fontSize: 12 }}>{t.from}</div>
                    </div>
                    <div style={{ color: '#ccc' }}>→</div>
                    <div>
                      <div style={{ fontWeight: 'bold', fontSize: 18 }}>{t.arrival_time}</div>
                      <div style={{ color: '#999', fontSize: 12 }}>{t.to}</div>
                    </div>
                  </Space>
                </Col>
                <Col xs={24} sm={4}>
                  <div style={{ fontSize: 20, color: '#ff6b6b', fontWeight: 'bold' }}>
                    ¥{t.prices?.second_seat || '-'}
                  </div>
                  <div style={{ fontSize: 11, color: '#999' }}>{t.duration}</div>
                </Col>
                <Col xs={24} sm={4} style={{ textAlign: 'right' }}>
                  <Dropdown
                    menu={{
                      items: folderList
                        .filter(f => f.name !== activeFolder)
                        .map(f => ({
                          key: f.name,
                          label: f.name,
                          icon: <FolderOutlined />
                        })),
                      onClick: ({ key }) => handleMoveToFolder('trains', originalIndex, key)
                    }}
                    disabled={folderList.length <= 1}
                  >
                    <Button size="small" icon={<FolderAddOutlined />} style={{ marginRight: 8 }}>
                      移动
                    </Button>
                  </Dropdown>
                  <Button
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => removeFromFavorites('trains', originalIndex)}
                  >
                    删除
                  </Button>
                </Col>
              </Row>
            </Card>
          )
        })}
      </div>
    )
  }

  const renderPlanners = () => {
    const plannerItems = getFilteredItems('planners')
    const plannerList = plannerItems.map(item => item.item)

    if (plannerList.length === 0) {
      return <Empty description="当前收藏夹中没有行程" image={Empty.PRESENTED_IMAGE_SIMPLE} />
    }

    return (
      <div>
        <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
          共 {plannerList.length} 个行程
        </Text>
        {plannerList.map((p, idx) => {
          const totalItems = (p.schedule || []).reduce((sum, d) => sum + (d.items?.length || 0), 0)
          const daysCount = p.schedule?.length || 0
          const originalIndex = favorites.planners?.indexOf(p) ?? idx

          return (
            <Card 
              key={idx} 
              size="small" 
              style={{ marginBottom: 12, borderRadius: 12, cursor: 'grab' }}
              draggable
              onDragStart={(e) => handleDragStart(e, 'planners', originalIndex)}
            >
              <Row align="middle" gutter={16}>
                <Col xs={24} sm={2}>
                  <DragOutlined style={{ color: '#ccc', fontSize: 16 }} />
                </Col>
                <Col xs={24} sm={6}>
                  <div style={{ fontSize: 18, fontWeight: 'bold' }}>
                    📍 {p.city}
                  </div>
                  {p.fromCity && (
                    <div style={{ fontSize: 12, color: '#999', marginTop: 4 }}>
                      从 {p.fromCity} 出发
                    </div>
                  )}
                </Col>
                <Col xs={24} sm={6}>
                  <Space>
                    <Tag icon={<CalendarOutlined />} color="blue">{daysCount}天</Tag>
                    <Tag color="green">{totalItems}个安排</Tag>
                  </Space>
                </Col>
                <Col xs={24} sm={4}>
                  <Text type="secondary" style={{ fontSize: 11 }}>
                    收藏于 {new Date(p.savedAt).toLocaleString('zh-CN')}
                  </Text>
                </Col>
                <Col xs={24} sm={6} style={{ textAlign: 'right' }}>
                  <Dropdown
                    menu={{
                      items: folderList
                        .filter(f => f.name !== activeFolder)
                        .map(f => ({
                          key: f.name,
                          label: f.name,
                          icon: <FolderOutlined />
                        })),
                      onClick: ({ key }) => handleMoveToFolder('planners', originalIndex, key)
                    }}
                    disabled={folderList.length <= 1}
                  >
                    <Button size="small" icon={<FolderAddOutlined />} style={{ marginRight: 8 }}>
                      移动
                    </Button>
                  </Dropdown>
                  <Button
                    type="primary"
                    size="small"
                    icon={<ArrowRightOutlined />}
                    onClick={() => navigate(`/planner?city=${p.city}&from=${p.fromCity || ''}`)}
                    style={{ marginRight: 8 }}
                  >
                    查看
                  </Button>
                  <Button
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => removeFromFavorites('planners', originalIndex)}
                  >
                    删除
                  </Button>
                </Col>
              </Row>
            </Card>
          )
        })}
      </div>
    )
  }

  const totalItems = currentFolder.items?.length || 0

  return (
    <div className="page-container" style={{ padding: '16px 0' }}>
      <Title level={2} style={{ marginBottom: 24 }}>
        ❤️ 我的收藏
      </Title>

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={24} md={6} lg={5}>
          {renderFolderList()}
        </Col>

        <Col xs={24} sm={24} md={18} lg={19}>
          <Card 
            style={{ borderRadius: 12, minHeight: 400 }}
            title={
              <Space>
                <InboxOutlined style={{ color: '#1677ff' }} />
                <span>{activeFolder}</span>
                <Tag color="blue">{totalItems} 项</Tag>
              </Space>
            }
          >
            <Tabs
              activeKey={selectedTab}
              onChange={setSelectedTab}
              items={[
                {
                  key: 'trains',
                  label: (
                    <span>
                      <ThunderboltOutlined /> 火车票
                      <Tag color="blue" style={{ marginLeft: 4 }}>
                        {getFilteredItems('trains').length}
                      </Tag>
                    </span>
                  ),
                  children: renderTrains(),
                },
                {
                  key: 'planners',
                  label: (
                    <span>
                      <CalendarOutlined /> 行程方案
                      <Tag color="green" style={{ marginLeft: 4 }}>
                        {getFilteredItems('planners').length}
                      </Tag>
                    </span>
                  ),
                  children: renderPlanners(),
                },
              ]}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}