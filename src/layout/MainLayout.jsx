import { Layout } from 'antd'
import { Outlet } from 'react-router-dom'
import AppHeader from './Header'

const { Content } = Layout

export default function MainLayout() {
  return (
    <Layout style={{ minHeight: '100vh', background: '#f5f7fa' }}>
      <AppHeader />
      <Content style={{ padding: 0, minHeight: 'calc(100vh - 64px)' }}>
        <Outlet />
      </Content>
    </Layout>
  )
}
