import { useState } from 'react'
import { Button, message, Modal, Typography, Space } from 'antd'
import { RobotOutlined, CopyOutlined, DownloadOutlined, ReloadOutlined } from '@ant-design/icons'
import { generateAIContent } from '../services/destinationService'
import { getAICacheItem, setAICache } from '../services/storageService'

const { Text, Paragraph } = Typography

const TEMPLATE_NAMES = {
  city_brief: '城市速览',
  station_guide: '车站攻略',
  travel_copy: '游玩文案',
  punch_card: '打卡攻略',
  photo_spots: '拍照建议',
  pitfall_guide: '避坑指南',
  itinerary_memo: '行程备忘录',
  pocket_itinerary: '口袋版行程',
  packing_list: '行李清单',
}

export default function AiGenerateButton({ 
  templateType, 
  context = {}, 
  buttonText = null,
  buttonType = 'default',
  iconSize = 16,
  onGenerate = null,
  size = 'middle',
}) {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [showModal, setShowModal] = useState(false)

  const generateContent = async (forceRegenerate = false) => {
    setLoading(true)
    
    const cacheKey = `${templateType}:${JSON.stringify(context)}`
    
    if (!forceRegenerate) {
      const cached = getAICacheItem(cacheKey)
      if (cached) {
        setResult(cached)
        setShowModal(true)
        setLoading(false)
        if (onGenerate) onGenerate(cached)
        return
      }
    }

    try {
      const response = await generateAIContent(templateType, context)
      const data = response.data || response
      
      if (data.success !== false) {
        const resultData = data.data || data
        setResult(resultData)
        setAICache(cacheKey, resultData)
        setShowModal(true)
        if (onGenerate) onGenerate(resultData)
      } else {
        message.error(data.error || '生成失败')
      }
    } catch (error) {
      message.error('生成失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const copyContent = async () => {
    if (result?.content) {
      try {
        await navigator.clipboard.writeText(result.content)
        message.success('已复制到剪贴板')
      } catch {
        message.error('复制失败')
      }
    }
  }

  const downloadContent = () => {
    if (result?.content) {
      const blob = new Blob([result.content], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${result.title || TEMPLATE_NAMES[templateType] || 'AI生成内容'}.txt`
      a.click()
      URL.revokeObjectURL(url)
      message.success('下载成功')
    }
  }

  const templateName = TEMPLATE_NAMES[templateType] || 'AI生成'

  return (
    <>
      <Button
        type={buttonType}
        icon={<RobotOutlined style={{ fontSize: iconSize }} />}
        loading={loading}
        onClick={() => generateContent(false)}
        size={size}
        style={{ 
          borderRadius: 8,
          background: buttonType === 'primary' 
            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
            : undefined,
          border: buttonType === 'primary' ? 'none' : undefined,
        }}
      >
        {buttonText || `生成${templateName}`}
      </Button>

      <Modal
        title={
          <Space>
            <RobotOutlined style={{ color: '#667eea' }} />
            <span>{result?.title || templateName}</span>
          </Space>
        }
        open={showModal}
        onCancel={() => setShowModal(false)}
        footer={[
          <Button key="regenerate" onClick={() => generateContent(true)} loading={loading}>
            <ReloadOutlined /> 重新生成
          </Button>,
          <Button key="copy" onClick={copyContent} disabled={!result?.content}>
            <CopyOutlined /> 复制
          </Button>,
          <Button key="download" type="primary" onClick={downloadContent} disabled={!result?.content}>
            <DownloadOutlined /> 下载
          </Button>,
        ]}
        width={600}
      >
        {result?.content && (
          <div style={{ 
            whiteSpace: 'pre-wrap', 
            fontFamily: 'monospace',
            background: '#f5f5f5',
            padding: 16,
            borderRadius: 8,
            maxHeight: '60vh',
            overflow: 'auto',
          }}>
            {result.content}
          </div>
        )}
      </Modal>
    </>
  )
}
