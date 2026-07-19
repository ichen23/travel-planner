import { useState, useEffect, useMemo } from 'react'
import { Card, Row, Col, InputNumber, Button, Table, Statistic, Progress, Tag, Typography, Divider, message, Empty, Modal, Form, Select } from 'antd'
import { WalletOutlined, PlusOutlined, DeleteOutlined, EditOutlined, PieChartOutlined, DollarOutlined, CarOutlined, HomeOutlined, ShoppingOutlined, CoffeeOutlined, CameraOutlined } from '@ant-design/icons'
import { usePlannerStore } from '../stores'

const { Title, Text } = Typography

const EXPENSE_CATEGORIES = [
  { value: 'ticket', label: '🎫 交通', icon: CarOutlined, color: '#1677ff' },
  { value: 'hotel', label: '🏨 住宿', icon: HomeOutlined, color: '#52c41a' },
  { value: 'food', label: '🍜 餐饮', icon: CoffeeOutlined, color: '#faad14' },
  { value: 'ticket_entrance', label: '🎫 门票', icon: CameraOutlined, color: '#eb2f96' },
  { value: 'shopping', label: '🛍️ 购物', icon: ShoppingOutlined, color: '#722ed1' },
  { value: 'other', label: '📦 其他', icon: DollarOutlined, color: '#999' },
]

const STORAGE_KEY = 'travel_expenses'

export default function BudgetPage() {
  const schedule = usePlannerStore(s => s.schedule)
  const [expenses, setExpenses] = useState([])
  const [modalOpen, setModalOpen] = useState(false)
  const [editingExpense, setEditingExpense] = useState(null)
  const [form] = Form.useForm()

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      setExpenses(JSON.parse(saved))
    }
  }, [])

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses))
  }, [expenses])

  const addExpense = (values) => {
    const newExpense = {
      id: Date.now(),
      ...values,
      date: values.date || new Date().toISOString().split('T')[0],
    }
    setExpenses(prev => [...prev, newExpense])
    setModalOpen(false)
    form.resetFields()
    message.success('已添加支出')
  }

  const editExpense = (record) => {
    setEditingExpense(record)
    form.setFieldsValue(record)
    setModalOpen(true)
  }

  const updateExpense = (values) => {
    setExpenses(prev => prev.map(e => e.id === editingExpense.id ? { ...e, ...values } : e))
    setModalOpen(false)
    setEditingExpense(null)
    form.resetFields()
    message.success('已更新支出')
  }

  const deleteExpense = (id) => {
    setExpenses(prev => prev.filter(e => e.id !== id))
    message.success('已删除支出')
  }

  const totalBudget = useMemo(() => {
    return expenses.reduce((sum, e) => sum + (e.amount || 0), 0)
  }, [expenses])

  const categoryStats = useMemo(() => {
    const stats = {}
    EXPENSE_CATEGORIES.forEach(cat => {
      stats[cat.value] = { category: cat, amount: 0, count: 0 }
    })
    expenses.forEach(e => {
      if (stats[e.category]) {
        stats[e.category].amount += e.amount || 0
        stats[e.category].count++
      }
    })
    return Object.values(stats).filter(s => s.amount > 0).sort((a, b) => b.amount - a.amount)
  }, [expenses])

  const columns = [
    { title: '日期', dataIndex: 'date', width: 120 },
    { 
      title: '类别', 
      dataIndex: 'category', 
      width: 120,
      render: (cat) => {
        const category = EXPENSE_CATEGORIES.find(c => c.value === cat)
        return category ? <Tag color={category.color}>{category.label}</Tag> : cat
      }
    },
    { title: '说明', dataIndex: 'description', ellipsis: true },
    { 
      title: '金额', 
      dataIndex: 'amount', 
      width: 120,
      align: 'right',
      render: (amount) => <Text strong style={{ color: '#ff4d4f' }}>¥{amount?.toFixed(2)}</Text>
    },
    {
      title: '操作',
      width: 140,
      render: (_, record) => (
        <div>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => editExpense(record)}>
            编辑
          </Button>
          <Button type="link" size="small" danger icon={<DeleteOutlined />} onClick={() => deleteExpense(record.id)}>
            删除
          </Button>
        </div>
      ),
    },
  ]

  const getTotalDays = () => {
    return schedule?.days?.length || 1
  }

  return (
    <div className="page-container">
      <Title level={2} style={{ marginBottom: 24 }}>
        <WalletOutlined /> 旅行成本统计
      </Title>
      <Text type="secondary" style={{ display: 'block', marginBottom: 24 }}>
        记录每笔支出，智能统计旅行花费，帮你更好地规划预算
      </Text>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card style={{ borderRadius: 12, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', border: 'none' }}>
            <Statistic
              title={<Text style={{ color: 'rgba(255,255,255,0.85)' }}>总支出</Text>}
              value={totalBudget}
              precision={2}
              prefix={<DollarOutlined style={{ color: 'white' }} />}
              suffix="元"
              valueStyle={{ color: 'white', fontSize: 32 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card style={{ borderRadius: 12, background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', border: 'none' }}>
            <Statistic
              title={<Text style={{ color: 'rgba(255,255,255,0.85)' }}>日均支出</Text>}
              value={totalBudget / getTotalDays()}
              precision={2}
              prefix={<DollarOutlined style={{ color: 'white' }} />}
              suffix="元"
              valueStyle={{ color: 'white', fontSize: 32 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card style={{ borderRadius: 12, background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', border: 'none' }}>
            <Statistic
              title={<Text style={{ color: 'rgba(255,255,255,0.85)' }}>支出笔数</Text>}
              value={expenses.length}
              prefix={<ShoppingOutlined style={{ color: 'white' }} />}
              valueStyle={{ color: 'white', fontSize: 32 }}
            />
          </Card>
        </Col>
      </Row>

      {categoryStats.length > 0 && (
        <Card title={<Text strong><PieChartOutlined /> 分类统计</Text>} style={{ marginBottom: 24, borderRadius: 12 }}>
          <Row gutter={[16, 16]}>
            {categoryStats.map(stat => (
              <Col xs={24} sm={12} md={8} key={stat.category.value}>
                <Card 
                  size="small" 
                  style={{ borderRadius: 8, borderLeft: `4px solid ${stat.category.color}` }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <Text strong>{stat.category.label}</Text>
                      <div>
                        <Text type="secondary">¥{stat.amount.toFixed(2)}</Text>
                        <Tag color={stat.category.color} style={{ marginLeft: 8 }}>
                          {((stat.amount / totalBudget) * 100).toFixed(1)}%
                        </Tag>
                      </div>
                    </div>
                  </div>
                  <Progress 
                    percent={Number(((stat.amount / totalBudget) * 100).toFixed(1))} 
                    strokeColor={stat.category.color}
                    size="small"
                    showInfo={false}
                  />
                </Card>
              </Col>
            ))}
          </Row>
        </Card>
      )}

      <Card 
        title={<Text strong>📝 支出明细</Text>}
        style={{ borderRadius: 12 }}
        extra={
          <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setEditingExpense(null); setModalOpen(true); }}>
            添加支出
          </Button>
        }
      >
        {expenses.length === 0 ? (
          <Empty 
            description="暂无支出记录" 
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>
              添加第一笔支出
            </Button>
          </Empty>
        ) : (
          <Table 
            columns={columns} 
            dataSource={expenses} 
            rowKey="id"
            pagination={{ pageSize: 10, showSizeChanger: true }}
          />
        )}
      </Card>

      <Modal
        title={editingExpense ? '编辑支出' : '添加支出'}
        open={modalOpen}
        onCancel={() => { setModalOpen(false); setEditingExpense(null); form.resetFields(); }}
        onOk={() => {
          form.validateFields().then(values => {
            if (editingExpense) {
              updateExpense(values)
            } else {
              addExpense(values)
            }
          })
        }}
        okText="确定"
        cancelText="取消"
      >
        <Form form={form} layout="vertical" initialValues={{ category: 'food', amount: 0, date: new Date().toISOString().split('T')[0] }}>
          <Form.Item name="date" label="日期" rules={[{ required: true, message: '请选择日期' }]}>
            <input type="date" style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #d9d9d9' }} />
          </Form.Item>
          <Form.Item name="category" label="类别" rules={[{ required: true, message: '请选择类别' }]}>
            <Select options={EXPENSE_CATEGORIES.map(c => ({ value: c.value, label: c.label }))} />
          </Form.Item>
          <Form.Item name="description" label="说明" rules={[{ required: true, message: '请输入说明' }]}>
            <input placeholder="例如：北京-上海高铁票" style={{ width: '100%', padding: '8px 12px', borderRadius: 6, border: '1px solid #d9d9d9' }} />
          </Form.Item>
          <Form.Item name="amount" label="金额（元）" rules={[{ required: true, message: '请输入金额' }, { type: 'number', min: 0.01, message: '金额必须大于0' }]}>
            <InputNumber min={0.01} step={0.5} style={{ width: '100%' }} prefix="¥" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}
