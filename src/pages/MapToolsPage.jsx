import { useState } from 'react';
import { Layout, Input, Button, Card, Row, Col, Statistic, Tag, Table, Divider, Tabs, message, Spin, Image, Typography, Space, Tooltip, Alert } from 'antd';
import { ThunderboltOutlined, EnvironmentOutlined, CarOutlined, BusOutlined, ManOutlined, ThunderOutlined, CloudOutlined, SearchOutlined, SwapOutlined, ArrowRightOutlined, GlobalOutlined } from '@ant-design/icons';
import { getDrivingDirection, getTransitDirection, getWalkingDirection, getWeather, compareRoutes, getRealPoi, getMapWeather } from '../services/mapService';

const { Title, Text, Paragraph } = Typography;
const { TabPane } = Tabs;

export default function MapToolsPage() {
  const [activeTab, setActiveTab] = useState('routes');
  
  const [fromCity, setFromCity] = useState('北京');
  const [toCity, setToCity] = useState('天津');
  const [loading, setLoading] = useState(false);
  const [routeResult, setRouteResult] = useState(null);
  
  const [weatherCity, setWeatherCity] = useState('北京');
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherResult, setWeatherResult] = useState(null);
  
  const [poiCity, setPoiCity] = useState('北京');
  const [poiLoading, setPoiLoading] = useState(false);
  const [poiResult, setPoiResult] = useState(null);

  const handleCompareRoutes = async () => {
    if (!fromCity || !toCity) {
      message.warning('请输入出发地和目的地');
      return;
    }
    
    setLoading(true);
    try {
      const result = await compareRoutes(fromCity, toCity);
      setRouteResult(result);
      message.success('路线对比完成！');
    } catch (error) {
      message.error('查询失败：' + (error?.message || '未知错误'));
    } finally {
      setLoading(false);
    }
  };

  const handleGetWeather = async () => {
    if (!weatherCity) {
      message.warning('请输入城市名称');
      return;
    }
    
    setWeatherLoading(true);
    try {
      const result = await getMapWeather(weatherCity);
      setWeatherResult(result);
      message.success('天气查询完成！');
    } catch (error) {
      message.error('查询失败：' + (error?.message || '未知错误'));
    } finally {
      setWeatherLoading(false);
    }
  };

  const handleGetPoi = async () => {
    if (!poiCity) {
      message.warning('请输入城市名称');
      return;
    }
    
    setPoiLoading(true);
    try {
      const result = await getRealPoi(poiCity);
      setPoiResult(result);
      message.success(`获取到 ${result?.total_attractions || 0} 个真实景点！`);
    } catch (error) {
      message.error('查询失败：' + (error?.message || '未知错误'));
    } finally {
      setPoiLoading(false);
    }
  };

  const formatTime = (seconds) => {
    if (!seconds) return '-';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) return `${hours}小时${minutes}分钟`;
    return `${minutes}分钟`;
  };

  const formatDistance = (meters) => {
    if (!meters) return '-';
    if (meters >= 1000) return `${(meters / 1000).toFixed(1)}公里`;
    return `${meters}米`;
  };

  const renderRouteCard = (type, icon, color, data) => {
    if (!data || !data.status) return null;
    
    const typeNames = {
      train: '🚄 高铁',
      driving: '🚗 驾车',
      transit: '🚇 公交',
      walking: '🚶 步行',
      riding: '🚴 骑行'
    };
    
    let content = null;
    
    if (type === 'train') {
      content = (
        <div>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: color }}>
            {data.duration_min ? `${Math.floor(data.duration_min / 60)}小时${data.duration_min % 60}分钟` : '-'}
          </div>
          <div style={{ color: '#666', marginBottom: 8 }}>
            {data.train_number} {data.train_type}
          </div>
          <div style={{ fontSize: 20, color: '#ff4d4f', fontWeight: 'bold' }}>
            ¥{data.price || '-'}
          </div>
        </div>
      );
    } else if (type === 'driving' && data.paths && data.paths.length > 0) {
      const path = data.paths[0];
      content = (
        <div>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: color }}>
            {formatTime(path.duration)}
          </div>
          <div style={{ color: '#666', marginBottom: 8 }}>
            {formatDistance(path.distance)} {path.tolls > 0 ? `| 过路费 ¥${path.tolls}` : ''}
          </div>
          <div style={{ fontSize: 14, color: '#999' }}>
            {path.steps_count} 个导航步骤
          </div>
        </div>
      );
    } else if (type === 'transit' && data.transits && data.transits.length > 0) {
      const transit = data.transits[0];
      content = (
        <div>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: color }}>
            {formatTime(transit.duration)}
          </div>
          <div style={{ color: '#666', marginBottom: 8 }}>
            {transit.lines?.length > 0 ? transit.lines.map((l, i) => (
              <Tag key={i} color="blue">{l.name}</Tag>
            )) : '换乘方案'}
          </div>
          <div style={{ fontSize: 20, color: '#ff4d4f', fontWeight: 'bold' }}>
            ¥{transit.fare || '-'}
          </div>
        </div>
      );
    } else if (type === 'walking' && data.paths && data.paths.length > 0) {
      const path = data.paths[0];
      content = (
        <div>
          <div style={{ fontSize: 32, fontWeight: 'bold', color: color }}>
            {formatTime(path.duration)}
          </div>
          <div style={{ color: '#666', marginBottom: 8 }}>
            {formatDistance(path.distance)}
          </div>
          <div style={{ fontSize: 14, color: '#999' }}>
            约 {Math.floor(path.distance / 800)} 步
          </div>
        </div>
      );
    } else {
      content = <div style={{ color: '#999' }}>暂无数据</div>;
    }
    
    return (
      <Card size="small" bordered={false} style={{ 
        borderRadius: 12, 
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        borderTop: `4px solid ${color}`
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 40, marginBottom: 12 }}>{icon}</div>
          <div style={{ fontWeight: 'bold', fontSize: 16, marginBottom: 16 }}>
            {typeNames[type]}
          </div>
          {content}
        </div>
      </Card>
    );
  };

  const renderWeather = () => {
    if (!weatherResult?.current) return null;
    
    const { current, forecast } = weatherResult;
    
    return (
      <div>
        <Card 
          style={{ borderRadius: 12, marginBottom: 16, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}
          bodyStyle={{ padding: 24 }}
        >
          <div style={{ display: 'flex', alignItems: 'center', color: 'white' }}>
            <CloudOutlined style={{ fontSize: 48, marginRight: 24 }} />
            <div>
              <div style={{ fontSize: 32, fontWeight: 'bold' }}>{current.temperature}°C</div>
              <div style={{ fontSize: 18 }}>{current.weather}</div>
              <div style={{ fontSize: 14, opacity: 0.8 }}>
                {current.province} {current.city} | 湿度 {current.humidity}% | {current.wind_direction}风 {current.wind_power}级
              </div>
            </div>
          </div>
        </Card>
        
        {forecast && forecast.length > 0 && (
          <Row gutter={[16, 16]}>
            {forecast.map((day, index) => (
              <Col key={index} xs={12} sm={8} md={6} lg={4}>
                <Card size="small" style={{ borderRadius: 8, textAlign: 'center' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: 8 }}>{index === 0 ? '今天' : index === 1 ? '明天' : day.week}</div>
                  <div style={{ fontSize: 14, color: '#666', marginBottom: 4 }}>{day.date}</div>
                  <div style={{ fontSize: 18, marginBottom: 4 }}>{day.weather_day}</div>
                  <div>
                    <Tag color="red">{day.temp_max}°</Tag>
                    <Tag color="blue">{day.temp_min}°</Tag>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </div>
    );
  };

  const renderPoiList = () => {
    if (!poiResult?.attractions) return null;
    
    const columns = [
      {
        title: '景点名称',
        dataIndex: 'name',
        key: 'name',
        render: (text) => <a>{text}</a>
      },
      {
        title: '地址',
        dataIndex: 'address',
        key: 'address',
        ellipsis: true,
        render: (text) => <Text type="secondary">{text || '暂无地址'}</Text>
      },
      {
        title: '评分',
        dataIndex: 'rating',
        key: 'rating',
        width: 100,
        render: (rating) => rating ? (
          <Tag color="gold">⭐ {rating}</Tag>
        ) : '-'
      },
      {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
        width: 150,
        render: (type) => {
          if (!type) return '-';
          const types = type.split(';').slice(0, 2);
          return types.map((t, i) => <Tag key={i}>{t}</Tag>);
        }
      },
    ];
    
    return (
      <div>
        <Alert
          message={`来自高德地图的真实数据 - ${poiResult.total_attractions} 个景点, ${poiResult.total_foods || 0} 个美食`}
          description="所有数据均来自高德地图实时POI，确保真实性和时效性"
          type="success"
          showIcon
          style={{ marginBottom: 16 }}
        />
        
        <Table
          columns={columns}
          dataSource={poiResult.attractions}
          rowKey="name"
          pagination={{ pageSize: 10 }}
          size="middle"
          scroll={{ x: 600 }}
        />
        
        {poiResult.foods && poiResult.foods.length > 0 && (
          <div style={{ marginTop: 24 }}>
            <Title level={4}>🍜 推荐美食</Title>
            <Row gutter={[16, 16]}>
              {poiResult.foods.slice(0, 8).map((food, index) => (
                <Col key={index} xs={12} sm={8} md={6}>
                  <Card size="small" style={{ borderRadius: 8 }}>
                    <div style={{ fontWeight: 'bold', marginBottom: 4 }}>{food.name}</div>
                    <Text type="secondary" style={{ fontSize: 12 }}>{food.address}</Text>
                    {food.rating > 0 && <div style={{ marginTop: 4 }}><Tag color="gold">⭐ {food.rating}</Tag></div>}
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        )}
      </div>
    );
  };

  return (
    <Layout style={{ minHeight: '100vh', background: '#f0f2f5' }}>
      <Layout.Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        <div style={{ marginBottom: 24 }}>
          <Title level={2} style={{ marginBottom: 8 }}>🗺️ 地图工具箱</Title>
          <Text type="secondary">基于高德地图的真实数据，提供路线规划、天气查询、景点探索等服务</Text>
        </div>

        <Card style={{ borderRadius: 12, marginBottom: 24 }}>
          <Tabs activeKey={activeTab} onChange={setActiveTab} size="large">
            <TabPane tab={<span><SwapOutlined /> 路线对比</span>} key="routes">
              <div style={{ marginBottom: 24 }}>
                <Row gutter={[16, 16]} align="middle">
                  <Col xs={24} sm={10}>
                    <Input
                      prefix={<EnvironmentOutlined />}
                      placeholder="出发城市"
                      value={fromCity}
                      onChange={(e) => setFromCity(e.target.value)}
                      size="large"
                    />
                  </Col>
                  <Col xs={24} sm={4} style={{ textAlign: 'center' }}>
                    <ArrowRightOutlined style={{ fontSize: 24, color: '#1890ff' }} />
                  </Col>
                  <Col xs={24} sm={10}>
                    <Input
                      prefix={<EnvironmentOutlined />}
                      placeholder="目的城市"
                      value={toCity}
                      onChange={(e) => setToCity(e.target.value)}
                      size="large"
                    />
                  </Col>
                </Row>
                <div style={{ marginTop: 16, textAlign: 'center' }}>
                  <Button
                    type="primary"
                    size="large"
                    icon={<ThunderboltOutlined />}
                    onClick={handleCompareRoutes}
                    loading={loading}
                    style={{ minWidth: 200, height: 48, fontSize: 16 }}
                  >
                    查询所有路线
                  </Button>
                </div>
              </div>

              {loading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
              
              {routeResult && routeResult.routes && (
                <Row gutter={[16, 16]}>
                  {renderRouteCard('train', '🚄', '#1890ff', routeResult.routes.train)}
                  {renderRouteCard('driving', '🚗', '#52c41a', routeResult.routes.driving)}
                  {renderRouteCard('transit', '🚇', '#722ed1', routeResult.routes.transit)}
                  {renderRouteCard('walking', '🚶', '#faad14', routeResult.routes.walking)}
                </Row>
              )}
            </TabPane>

            <TabPane tab={<span><CloudOutlined /> 天气预报</span>} key="weather">
              <div style={{ marginBottom: 24 }}>
                <Row gutter={[16, 16]} align="middle">
                  <Col xs={24} sm={16}>
                    <Input
                      prefix={<GlobalOutlined />}
                      placeholder="输入城市名称，如：北京、上海、广州..."
                      value={weatherCity}
                      onChange={(e) => setWeatherCity(e.target.value)}
                      size="large"
                      onPressEnter={handleGetWeather}
                    />
                  </Col>
                  <Col xs={24} sm={8}>
                    <Button
                      type="primary"
                      size="large"
                      icon={<CloudOutlined />}
                      onClick={handleGetWeather}
                      loading={weatherLoading}
                      block
                    >
                      查询天气
                    </Button>
                  </Col>
                </Row>
              </div>

              {weatherLoading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
              {weatherResult?.current && renderWeather()}
            </TabPane>

            <TabPane tab={<span><EnvironmentOutlined /> 探索景点</span>} key="poi">
              <div style={{ marginBottom: 24 }}>
                <Row gutter={[16, 16]} align="middle">
                  <Col xs={24} sm={16}>
                    <Input
                      prefix={<SearchOutlined />}
                      placeholder="输入城市名称，获取真实景点数据"
                      value={poiCity}
                      onChange={(e) => setPoiCity(e.target.value)}
                      size="large"
                      onPressEnter={handleGetPoi}
                    />
                  </Col>
                  <Col xs={24} sm={8}>
                    <Button
                      type="primary"
                      size="large"
                      icon={<EnvironmentOutlined />}
                      onClick={handleGetPoi}
                      loading={poiLoading}
                      block
                    >
                      探索景点
                    </Button>
                  </Col>
                </Row>
              </div>

              {poiLoading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
              {poiResult && renderPoiList()}
              
              {!poiResult && !poiLoading && (
                <div style={{ textAlign: 'center', padding: 60, color: '#999' }}>
                  <EnvironmentOutlined style={{ fontSize: 48, marginBottom: 16 }} />
                  <div style={{ fontSize: 16 }}>输入城市名称，探索真实景点数据</div>
                </div>
              )}
            </TabPane>
          </Tabs>
        </Card>

        <Card title="📚 使用说明" style={{ borderRadius: 12 }}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={8}>
              <div style={{ padding: 16, background: '#e6f7ff', borderRadius: 8 }}>
                <CarOutlined style={{ fontSize: 32, color: '#1890ff', marginBottom: 12 }} />
                <Title level={5}>路线对比</Title>
                <Text type="secondary">支持同时对比高铁、驾车、公交、步行等多种出行方式，帮助您选择最优路线</Text>
              </div>
            </Col>
            <Col xs={24} sm={8}>
              <div style={{ padding: 16, background: '#f6ffed', borderRadius: 8 }}>
                <CloudOutlined style={{ fontSize: 32, color: '#52c41a', marginBottom: 12 }} />
                <Title level={5}>天气预报</Title>
                <Text type="secondary">查询全国所有城市的实时天气和4天预报，出行前做好准备</Text>
              </div>
            </Col>
            <Col xs={24} sm={8}>
              <div style={{ padding: 16, background: '#fff7e6', borderRadius: 8 }}>
                <EnvironmentOutlined style={{ fontSize: 32, color: '#fa8c16', marginBottom: 12 }} />
                <Title level={5}>探索景点</Title>
                <Text type="secondary">获取全国城市的真实景点和美食数据，所有数据均来自高德地图</Text>
              </div>
            </Col>
          </Row>
        </Card>
      </Layout.Content>
    </Layout>
  );
}
