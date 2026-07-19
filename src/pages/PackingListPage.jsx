import { useState, useMemo } from 'react'
import { Card, Row, Col, Select, Slider, Checkbox, Button, Tag, Typography, Divider, message } from 'antd'
import { ShoppingOutlined, CopyOutlined, CloudOutlined, UserOutlined } from '@ant-design/icons'

const { Title, Text } = Typography

const SEASONS = [
  { value: 'spring', label: '🌸 春季 (3-5月)', items: ['薄外套', '长袖衬衫', '轻便长裤', '运动鞋', '雨伞', '防晒霜'] },
  { value: 'summer', label: '☀️ 夏季 (6-8月)', items: ['短袖T恤', '短裤/裙子', '凉鞋/拖鞋', '太阳镜', '遮阳帽', '防晒霜', '驱蚊液', '轻薄外套(空调房)'] },
  { value: 'autumn', label: '🍂 秋季 (9-11月)', items: ['长袖T恤', '薄外套', '长裤', '运动鞋', '围巾(早晚凉)', '保湿护肤品'] },
  { value: 'winter', label: '❄️ 冬季 (12-2月)', items: ['羽绒服/厚外套', '保暖内衣', '毛衣', '厚裤子', '保暖鞋', '手套', '围巾', '帽子', '暖宝宝'] },
]

const TRAVELERS = [
  { value: 'adult', label: '👤 成人', extra: ['身份证', '手机充电器', '充电宝(≤20000mAh)', '耳机', '洗漱用品', '护肤品', '化妆品(可选)', '现金/银行卡'] },
  { value: 'child', label: '👶 儿童', extra: ['户口本/身份证', '儿童票', '零食', '玩具/绘本', '备用衣物', '体温计', '常用药'] },
  { value: 'elder', label: '👴 老人', extra: ['身份证', '老年证', '常用药', '血压计', '老花镜', '轻便拐杖(如有)', '保暖衣物', '保温杯'] },
  { value: 'pregnant', label: '🤰 孕妇', extra: ['产检资料', '孕妇装', '防辐射服(可选)', '孕期维生素', '防滑鞋', 'U型枕', '宽松衣物'] },
]

const PURPOSE = [
  { value: 'general', label: '🎯 通用', extra: [] },
  { value: 'business', label: '💼 商务', extra: ['正装/西装', '领带', '商务笔记本', '充电器(多口)', '公文包', '名片'] },
  { value: 'leisure', label: '🏖️ 休闲度假', extra: ['泳衣', '沙滩鞋', '遮阳伞', '防水袋', '浮潜装备(可选)'] },
  { value: 'mountain', label: '🏔️ 登山户外', extra: ['登山鞋', '冲锋衣', '背包(40L+)', '头灯', '登山杖', '速干衣裤', '保温水壶'] },
]

const HIGH_SPEED_RAIL_ITEMS = {
  mustHave: ['身份证(必带)', '手机+充电器', '充电宝(≤20000mAh)', '口罩(可选)'],
  tips: ['提前到站：建议提前45分钟到达车站', '行李限制：成人20kg，儿童10kg', '禁带物品：打火机、刀具、酒精等', '液体限制：单瓶≤100ml，总量≤1L', '可带物品：食品、饮料、水果、鲜花']
}

export default function PackingListPage() {
  const [days, setDays] = useState(3)
  const [season, setSeason] = useState('spring')
  const [travelers, setTravelers] = useState(['adult'])
  const [purpose, setPurpose] = useState('general')
  const [checkedItems, setCheckedItems] = useState({})

  const allItems = useMemo(() => {
    const seasonData = SEASONS.find(s => s.value === season)
    const purposeData = PURPOSE.find(p => p.value === purpose)
    
    const travelerItems = travelers.flatMap(t => {
      const travelerData = TRAVELERS.find(tr => tr.value === t)
      return travelerData ? travelerData.extra : []
    })

    const baseItems = [
      `身份证 (每人必带)`,
      `手机 + 充电器`,
      `充电宝 ≤20000mAh`,
      `行李箱/背包`,
      `洗漱用品 (${days}天用量)`,
      `换洗衣物 (${days}套)`,
    ]

    const items = [
      { category: '🎫 证件电子', items: ['身份证', '车票截图', '健康码', '核酸证明(如有需要)'] },
      { category: '👕 衣物穿搭', items: [...(seasonData?.items || []), ...(purposeData?.extra || [])].filter((v, i, a) => a.indexOf(v) === i) },
      { category: '🔌 电子设备', items: ['手机', '充电器', '充电宝(≤20000mAh)', '耳机', '数据线', '相机(可选)', '手表充电线'] },
      { category: '🧴 洗护美妆', items: [`洗漱用品(${days}天)`, `护肤品(${days}天)`, `化妆品(可选)`, '防晒霜', '梳子/镜子'] },
      { category: '💊 药品健康', items: ['常用药', '创可贴', '晕车药', '感冒灵', '肠胃药', '体温计'] },
      { category: '🎒 出行配件', items: ['背包/行李箱', '手提袋', '雨伞', '水杯/保温杯', '纸巾/湿巾', '眼罩/耳塞'] },
      { category: '🍱 零食补给', items: ['水/饮料', '零食', '水果', '泡面(可选)', '糖/巧克力'] },
      { category: '👤 特殊人群', items: [...travelerItems].filter((v, i, a) => a.indexOf(v) === i) },
    ]

    return items
  }, [days, season, travelers, purpose])

  const toggleItem = (category, item) => {
    const key = `${category}_${item}`
    setCheckedItems(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const getProgress = () => {
    const total = allItems.reduce((sum, cat) => sum + cat.items.length, 0)
    const checked = Object.values(checkedItems).filter(Boolean).length
    return { total, checked, percent: total > 0 ? Math.round((checked / total) * 100) : 0 }
  }

  const handleCopy = () => {
    const progress = getProgress()
    let text = `📋 高铁出行清单 (${days}天)\n\n`
    allItems.forEach(cat => {
      text += `${cat.category}\n`
      cat.items.forEach(item => {
        const key = `${cat.category}_${item}`
        text += `${checkedItems[key] ? '✅' : '⬜'} ${item}\n`
      })
      text += '\n'
    })
    text += `\n完成进度: ${progress.checked}/${progress.total} (${progress.percent}%)`
    navigator.clipboard.writeText(text)
    message.success('已复制清单到剪贴板')
  }

  const progress = getProgress()

  return (
    <div className="page-container">
      <Title level={2} style={{ marginBottom: 24 }}>
        <ShoppingOutlined /> 高铁出行清单助手
      </Title>
      <Text type="secondary" style={{ display: 'block', marginBottom: 24 }}>
        根据出行天数、季节、人群智能生成专属打包清单
      </Text>

      <Card style={{ marginBottom: 24, borderRadius: 12 }}>
        <Row gutter={[24, 24]}>
          <Col xs={24} md={8}>
            <Text strong>
              <CloudOutlined /> 出行天数
            </Text>
            <Slider
              min={1}
              max={15}
              value={days}
              onChange={setDays}
              marks={{ 1: '1天', 3: '3天', 7: '7天', 15: '15天' }}
            />
          </Col>
          <Col xs={24} md={8}>
            <Text strong>季节</Text>
            <Select
              value={season}
              onChange={setSeason}
              style={{ width: '100%', marginTop: 8 }}
              options={SEASONS.map(s => ({ value: s.value, label: s.label }))}
            />
          </Col>
          <Col xs={24} md={8}>
            <Text strong>出行人群</Text>
            <Select
              mode="multiple"
              value={travelers}
              onChange={setTravelers}
              style={{ width: '100%', marginTop: 8 }}
              options={TRAVELERS.map(t => ({ value: t.value, label: t.label }))}
              placeholder="可多选"
            />
          </Col>
        </Row>
        <Row gutter={[24, 24]} style={{ marginTop: 16 }}>
          <Col xs={24} md={8}>
            <Text strong>出行目的</Text>
            <Select
              value={purpose}
              onChange={setPurpose}
              style={{ width: '100%', marginTop: 8 }}
              options={PURPOSE.map(p => ({ value: p.value, label: p.label }))}
            />
          </Col>
          <Col xs={24} md={16} style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 12 }}>
            <div style={{ flex: 1, maxWidth: 300 }}>
              <Text type="secondary">完成进度</Text>
              <div style={{ background: '#f0f0f0', borderRadius: 10, height: 20, position: 'relative', overflow: 'hidden' }}>
                <div style={{ 
                  background: progress.percent >= 80 ? '#52c41a' : progress.percent >= 50 ? '#faad14' : '#1677ff',
                  height: '100%', 
                  width: `${progress.percent}%`,
                  transition: 'width 0.3s'
                }} />
                <span style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontSize: 12, fontWeight: 'bold' }}>
                  {progress.checked}/{progress.total} ({progress.percent}%)
                </span>
              </div>
            </div>
            <Button icon={<CopyOutlined />} onClick={handleCopy}>复制清单</Button>
          </Col>
        </Row>
      </Card>

      <Card style={{ marginBottom: 24, borderRadius: 12, background: '#fffbe6', borderColor: '#ffe58f' }}>
        <Title level={5} style={{ marginBottom: 12, color: '#faad14' }}>⚠️ 高铁出行注意事项</Title>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12}>
            <Text strong>✅ 必带物品：</Text>
            <div style={{ marginTop: 4 }}>
              {HIGH_SPEED_RAIL_ITEMS.mustHave.map(item => (
                <Tag color="green" key={item}>{item}</Tag>
              ))}
            </div>
          </Col>
          <Col xs={24} sm={12}>
            <Text strong>💡 温馨提示：</Text>
            <ul style={{ marginTop: 4, paddingLeft: 20, fontSize: 13 }}>
              {HIGH_SPEED_RAIL_ITEMS.tips.map(tip => (
                <li key={tip} style={{ color: '#666', marginBottom: 2 }}>{tip}</li>
              ))}
            </ul>
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        {allItems.map((category, idx) => (
          <Col xs={24} sm={12} md={8} key={idx}>
            <Card 
              title={<Text strong>{category.category}</Text>}
              style={{ borderRadius: 12, height: '100%' }}
              bodyStyle={{ padding: 16 }}
            >
              {category.items.map((item, i) => {
                const key = `${category.category}_${item}`
                return (
                  <Checkbox
                    key={i}
                    checked={!!checkedItems[key]}
                    onChange={() => toggleItem(category.category, item)}
                    style={{ display: 'block', marginBottom: 8 }}
                  >
                    {item}
                  </Checkbox>
                )
              })}
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  )
}
