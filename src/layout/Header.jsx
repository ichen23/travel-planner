import { Layout, Menu } from 'antd'
import { HomeOutlined, CarOutlined, EnvironmentOutlined, ScheduleOutlined, HeartOutlined, BarChartOutlined, ToolOutlined, WalletOutlined, GiftOutlined, ShoppingOutlined } from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header } = Layout

export default function AppHeader() {
  const navigate = useNavigate()
  const location = useLocation()

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
    <Header style={{ display: 'flex', alignItems: 'center', background: '#001529', padding: '0 24px' }}>
      <div style={{ color: 'white', fontSize: 20, fontWeight: 'bold', marginRight: 40, cursor: 'pointer', whiteSpace: 'nowrap' }} onClick={() => navigate('/')}>
        🚄 高铁旅行规划
      </div>
      <Menu
        theme="dark"
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={({ key }) => navigate(key)}
        style={{ flex: 1, background: '#001529', minWidth: 0 }}
      />
    </Header>
  )
}
