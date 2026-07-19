import { useState, useRef, forwardRef, useImperativeHandle } from 'react'
import { Modal, Button, Typography, Space, message, Spin, Progress, Card, Tooltip } from 'antd'
import { ExportOutlined, PrinterOutlined, FileImageOutlined, FileTextOutlined, CopyOutlined, DownloadOutlined } from '@ant-design/icons'
import html2canvas from 'html2canvas'

const { Text, Title, Paragraph } = Typography

const ExportModal = forwardRef(function ExportModal({ itineraryData, title = '我的旅行行程' }, ref) {
  const [visible, setVisible] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [exportProgress, setExportProgress] = useState(0)
  const contentRef = useRef(null)

  useImperativeHandle(ref, () => ({
    open: () => setVisible(true),
    close: () => setVisible(false),
  }))

  const generateTextContent = () => {
    if (!itineraryData) return ''

    let text = `${title}\n`
    text += `${'='.repeat(40)}\n\n`

    if (itineraryData.summary && itineraryData.summary.length > 0) {
      text += '【行程概览】\n'
      itineraryData.summary.forEach((item, i) => {
        text += `${i + 1}. ${item}\n`
      })
      text += '\n'
    }

    if (itineraryData.days && itineraryData.days.length > 0) {
      text += '【详细行程】\n\n'
      itineraryData.days.forEach((day, dayIdx) => {
        text += `第 ${day.day || dayIdx + 1} 天 - ${day.title || ''}\n`
        text += '-'.repeat(30) + '\n'
        
        if (day.schedule && day.schedule.length > 0) {
          day.schedule.forEach((item, itemIdx) => {
            text += `${item.time || ''} ${item.item?.name || item.description || ''}\n`
            if (item.description) {
              text += `  ${item.description}\n`
            }
            if (item.item?.rating) {
              text += `  评分: ${item.item.rating}\n`
            }
          })
        }

        if (day.hotel) {
          text += `\n🏨 住宿: ${day.hotel.name}\n`
          if (day.hotel.address) {
            text += `  地址: ${day.hotel.address}\n`
          }
        }
        text += '\n'
      })
    }

    if (itineraryData.total_cost_estimate) {
      text += '【费用估算】\n'
      text += `总费用: ¥${itineraryData.total_cost_estimate.total || 0}\n`
      text += `  住宿: ¥${itineraryData.total_cost_estimate.hotel || 0}\n`
      text += `  餐饮: ¥${itineraryData.total_cost_estimate.food || 0}\n`
      text += `  门票: ¥${itineraryData.total_cost_estimate.attraction || 0}\n\n`
    }

    if (itineraryData.tips && itineraryData.tips.length > 0) {
      text += '【温馨提示】\n'
      itineraryData.tips.forEach((tip, i) => {
        text += `${i + 1}. ${tip}\n`
      })
    }

    return text
  }

  const handleExportText = () => {
    const text = generateTextContent()
    
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${title}_${new Date().toISOString().slice(0, 10)}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    message.success('文本文件已下载')
  }

  const handleCopyText = async () => {
    const text = generateTextContent()
    
    try {
      await navigator.clipboard.writeText(text)
      message.success('已复制到剪贴板')
    } catch (err) {
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      message.success('已复制到剪贴板')
    }
  }

  const handleExportPDF = () => {
    if (!contentRef.current) {
      message.error('内容未就绪')
      return
    }

    const printWindow = window.open('', '_blank')
    if (!printWindow) {
      message.error('无法打开打印窗口，请允许弹窗')
      return
    }

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>${title}</title>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
            color: #333;
          }
          h1 {
            text-align: center;
            color: #1677ff;
            margin-bottom: 8px;
          }
          .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 32px;
          }
          .day-section {
            margin-bottom: 24px;
            border: 1px solid #e8e8e8;
            border-radius: 12px;
            overflow: hidden;
          }
          .day-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 20px;
            font-weight: 600;
          }
          .schedule-item {
            padding: 12px 20px;
            border-bottom: 1px solid #f0f0f0;
          }
          .schedule-item:last-child {
            border-bottom: none;
          }
          .time-tag {
            display: inline-block;
            background: #e6f7ff;
            color: #1677ff;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 8px;
          }
          .hotel-info {
            background: #e6f7ff;
            padding: 12px 20px;
          }
          .cost-section {
            background: #fff7e6;
            padding: 20px;
            border-radius: 12px;
            margin-top: 24px;
          }
          .tips-section {
            margin-top: 24px;
          }
          .summary-section {
            background: #f6ffed;
            padding: 16px 20px;
            border-radius: 12px;
            margin-bottom: 24px;
          }
          @media print {
            body { padding: 20px; }
          }
        </style>
      </head>
      <body>
        ${contentRef.current.innerHTML}
      </body>
      </html>
    `)
    
    printWindow.document.close()
    printWindow.onload = () => {
      printWindow.print()
    }
    
    message.success('已打开打印窗口')
  }

  const handleExportImage = async () => {
    if (!contentRef.current) {
      message.error('内容未就绪')
      return
    }

    setExporting(true)
    setExportProgress(10)

    try {
      const canvas = await html2canvas(contentRef.current, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#ffffff',
        logging: false,
        onclone: (clonedDoc) => {
          setExportProgress(30)
        }
      })

      setExportProgress(70)

      const link = document.createElement('a')
      link.download = `${title}_${new Date().toISOString().slice(0, 10)}.png`
      link.href = canvas.toDataURL('image/png')
      link.click()

      setExportProgress(100)
      message.success('图片已下载')
    } catch (err) {
      console.error('导出图片失败:', err)
      message.error('导出图片失败，请重试')
    } finally {
      setExporting(false)
      setExportProgress(0)
    }
  }

  const renderExportContent = () => {
    if (!itineraryData) {
      return <Empty description="暂无可导出的行程内容" />
    }

    const summary = itineraryData.summary || []
    const days = itineraryData.days || []
    const totalCost = itineraryData.total_cost_estimate || {}
    const tips = itineraryData.tips || []

    return (
      <div ref={contentRef} style={{ background: '#fff', padding: 24, borderRadius: 12, maxWidth: 700, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <h1 style={{ color: '#1677ff', margin: 0, fontSize: 24 }}>{title}</h1>
          <p style={{ color: '#666', margin: '8px 0 0', fontSize: 14 }}>
            {new Date().toLocaleDateString('zh-CN')} 生成
          </p>
        </div>

        {summary.length > 0 && (
          <div style={{ background: '#f6ffed', padding: 16, borderRadius: 12, marginBottom: 24 }}>
            <h3 style={{ margin: '0 0 12px', color: '#389e0d' }}>行程概览</h3>
            {summary.map((item, i) => (
              <p key={i} style={{ margin: '4px 0', fontSize: 14 }}>{i + 1}. {item}</p>
            ))}
          </div>
        )}

        {days.map((day, dayIdx) => (
          <div key={dayIdx} style={{ marginBottom: 20, border: '1px solid #e8e8e8', borderRadius: 12, overflow: 'hidden' }}>
            <div style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '12px 16px', fontWeight: 600 }}>
              第 {day.day || dayIdx + 1} 天 - {day.title || ''}
            </div>
            <div style={{ padding: '8px 0' }}>
              {day.schedule?.map((item, itemIdx) => (
                <div key={itemIdx} style={{ padding: '10px 16px', borderBottom: itemIdx < day.schedule.length - 1 ? '1px solid #f0f0f0' : 'none' }}>
                  <span style={{ background: '#e6f7ff', color: '#1677ff', padding: '2px 8px', borderRadius: 4, fontSize: 12, marginRight: 8 }}>
                    {item.time}
                  </span>
                  <span style={{ fontWeight: 500 }}>{item.item?.name || item.description || ''}</span>
                  {item.description && item.item?.name && (
                    <div style={{ fontSize: 12, color: '#666', marginTop: 4 }}>{item.description}</div>
                  )}
                  {item.item?.rating && (
                    <span style={{ fontSize: 12, color: '#faad14', marginLeft: 8 }}>评分: {item.item.rating}</span>
                  )}
                </div>
              ))}
              {day.hotel && (
                <div style={{ background: '#e6f7ff', padding: '10px 16px' }}>
                  <strong>🏨 住宿: {day.hotel.name}</strong>
                  {day.hotel.address && <div style={{ fontSize: 12, color: '#666', marginTop: 4 }}>{day.hotel.address}</div>}
                </div>
              )}
            </div>
          </div>
        ))}

        {totalCost.total > 0 && (
          <div style={{ background: '#fff7e6', padding: 16, borderRadius: 12, marginTop: 20 }}>
            <h3 style={{ margin: '0 0 12px', color: '#d46b08' }}>费用估算</h3>
            <div style={{ fontSize: 20, fontWeight: 'bold', color: '#ff6b6b', marginBottom: 8 }}>
              总计: ¥{totalCost.total?.toLocaleString() || 0}
            </div>
            <div style={{ display: 'flex', gap: 24, fontSize: 14, color: '#666' }}>
              <span>🏨 住宿: ¥{totalCost.hotel || 0}</span>
              <span>🍜 餐饮: ¥{totalCost.food || 0}</span>
              <span>🎫 门票: ¥{totalCost.attraction || 0}</span>
            </div>
          </div>
        )}

        {tips.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <h3 style={{ margin: '0 0 12px', color: '#1677ff' }}>温馨提示</h3>
            {tips.map((tip, i) => (
              <p key={i} style={{ margin: '4px 0', fontSize: 14 }}>💡 {tip}</p>
            ))}
          </div>
        )}

        <div style={{ textAlign: 'center', marginTop: 24, paddingTop: 16, borderTop: '1px solid #f0f0f0', fontSize: 12, color: '#999' }}>
          🗺️ 由智能旅行规划助手生成
        </div>
      </div>
    )
  }

  return (
    <Modal
      title={
        <Space>
          <ExportOutlined style={{ color: '#1677ff' }} />
          <span>导出行程</span>
        </Space>
      }
      open={visible}
      onCancel={() => setVisible(false)}
      footer={null}
      width={720}
      centered
    >
      {exporting && (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Spin size="large" />
          <Progress percent={exportProgress} style={{ marginTop: 16, maxWidth: 300 }} />
          <div style={{ marginTop: 12, color: '#666' }}>正在导出，请稍候...</div>
        </div>
      )}

      {!exporting && (
        <>
          <Card style={{ marginBottom: 24, borderRadius: 12 }}>
            <Title level={5} style={{ marginBottom: 16 }}>选择导出格式</Title>
            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <Tooltip title="使用浏览器打印功能，可保存为 PDF">
                <Button
                  size="large"
                  icon={<PrinterOutlined />}
                  onClick={handleExportPDF}
                  style={{ height: 60, minWidth: 140, borderRadius: 12, border: '2px dashed #1677ff' }}
                >
                  <div>
                    <div style={{ fontWeight: 600 }}>PDF / 打印</div>
                    <div style={{ fontSize: 12, color: '#999' }}>浏览器打印</div>
                  </div>
                </Button>
              </Tooltip>

              <Tooltip title="将行程截图保存为图片">
                <Button
                  size="large"
                  icon={<FileImageOutlined />}
                  onClick={handleExportImage}
                  loading={exporting}
                  style={{ height: 60, minWidth: 140, borderRadius: 12, border: '2px dashed #52c41a' }}
                >
                  <div>
                    <div style={{ fontWeight: 600 }}>图片</div>
                    <div style={{ fontSize: 12, color: '#999' }}>PNG 格式</div>
                  </div>
                </Button>
              </Tooltip>

              <Tooltip title="导出为纯文本文件">
                <Button
                  size="large"
                  icon={<FileTextOutlined />}
                  onClick={handleExportText}
                  style={{ height: 60, minWidth: 140, borderRadius: 12, border: '2px dashed #faad14' }}
                >
                  <div>
                    <div style={{ fontWeight: 600 }}>文本</div>
                    <div style={{ fontSize: 12, color: '#999' }}>TXT 格式</div>
                  </div>
                </Button>
              </Tooltip>

              <Tooltip title="复制行程内容到剪贴板">
                <Button
                  size="large"
                  icon={<CopyOutlined />}
                  onClick={handleCopyText}
                  style={{ height: 60, minWidth: 140, borderRadius: 12, border: '2px dashed #722ed1' }}
                >
                  <div>
                    <div style={{ fontWeight: 600 }}>复制</div>
                    <div style={{ fontSize: 12, color: '#999' }}>剪贴板</div>
                  </div>
                </Button>
              </Tooltip>
            </div>
          </Card>

          <Card 
            title={
              <Space>
                <DownloadOutlined />
                <span>导出预览</span>
              </Space>
            }
            style={{ borderRadius: 12 }}
          >
            {renderExportContent()}
          </Card>
        </>
      )}
    </Modal>
  )
})

export default ExportModal
