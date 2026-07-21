import { useState } from 'react'
import { Layout, Menu, Modal, Input } from 'antd'
import { HomeOutlined, CarOutlined, EnvironmentOutlined, ScheduleOutlined, HeartOutlined, BarChartOutlined, ToolOutlined, WalletOutlined, GiftOutlined, ShoppingOutlined, SearchOutlined, CloseOutlined } from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import CitySearch from '../components/CitySearch'

const { Header } = Layout

export default function AppHeader() {
  const navigate = useNavigate()
  const location = useLocation()
  const [searchOpen, setSearchOpen] = useState(false)

  const menuItems = [
    { key: '/', icon: <HomeOutlined />, label: '首页' },
    { key: '/trains', icon: <CarOutlined />, label: '查车票' },
    { key: '/destinations', icon: <EnvironmentOutlined />, label: '推荐目的地' },
    { key: '/blindbox', icon: <GiftOutlined />, label: '旅行盲盒' },
    { key: '/planner', icon: <ScheduleOutlined />, label: '行程规划' },
    { key: '/packing', icon: <ShoppingOutlined />, label: '行李清单' },
    { key: '/budget', icon: <WalletOutlined />, label: '费用统计' },
    { key: '/compare', icon: <BarChartOutlined />, label: '城市对比' },
    { key: '/toolbox', icon: <ToolOutlined />, label: 'AI工具箱' },
    { key: '/favorites', icon: <HeartOutlined />, label: '我的收藏' },
  ]

  return (
    <>
      <Header style={{ display: 'flex', alignItems: 'center', background: '#001529', padding: '0 24px' }}>
        <div style={{ color: 'white', fontSize: 20, fontWeight: 'bold', marginRight: 24, cursor: 'pointer', whiteSpace: 'nowrap' }} onClick={() => navigate('/')}>
          🚄 高铁旅行
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1, background: '#001529', minWidth: 0 }}
        />
        <div
          onClick={() => setSearchOpen(true)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '6px 16px',
            background: 'rgba(255,255,255,0.15)',
            borderRadius: 20,
            cursor: 'pointer',
            color: 'white',
            transition: 'all 0.3s',
            marginLeft: 16,
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(255,255,255,0.25)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(255,255,255,0.15)'
          }}
        >
          <SearchOutlined />
          <span style={{ fontSize: 14 }}>搜索城市</span>
        </div>
      </Header>

      <Modal
        title={null}
        open={searchOpen}
        onCancel={() => setSearchOpen(false)}
        footer={null}
        width={600}
        closable={false}
        centered
        styles={{
          body: { padding: '24px 32px' },
          mask: { background: 'rgba(0,0,0,0.5)' },
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 20 }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>🔍</div>
          <h2 style={{ margin: '0 0 8px', fontSize: 24, color: '#333' }}>搜索城市</h2>
          <p style={{ margin: 0, color: '#666', fontSize: 14 }}>
            支持搜索全国 2000+ 行政区划
          </p>
          <button
            onClick={() => setSearchOpen(false)}
            style={{
              position: 'absolute',
              top: 16,
              right: 16,
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              fontSize: 20,
              color: '#999',
            }}
          >
            <CloseOutlined />
          </button>
        </div>
        <CitySearch
          placeholder="输入城市名称，如：北京、丽江、九寨沟..."
          onSelectCity={(city) => {
            setSearchOpen(false)
            navigate(`/destination/${encodeURIComponent(city.name)}`)
          }}
        />
      </Modal>
    </>
  )
}