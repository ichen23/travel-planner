import { RouterProvider } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { router } from './routes'
import './styles/global.css'

export default function App() {
  return (
    <ConfigProvider
      locale={zhCN}
      theme={{
        token: {
          colorPrimary: '#667eea',
          colorLink: '#667eea',
          borderRadius: 8,
          colorGradientStart: '#667eea',
          colorGradientEnd: '#764ba2',
        },
        components: {
          Button: {
            controlHeight: 40,
            primaryShadow: '0 2px 8px rgba(102, 126, 234, 0.4)',
          },
          Card: {
            borderRadiusLG: 16,
          },
        },
      }}
    >
      <RouterProvider router={router} />
    </ConfigProvider>
  )
}
