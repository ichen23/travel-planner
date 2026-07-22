import { useState } from 'react';
import { Card, Row, Col, Button, Input, Tabs, message, Spin, Typography, Tag, Alert } from 'antd';
import { CarOutlined, CloudOutlined, EnvironmentOutlined, SwapOutlined, SearchOutlined, ArrowRightOutlined, GlobalOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { compareRoutes, getRealPoi, getMapWeather } from '../services/mapService';

const { Title, Text } = Typography;
const { TabPane } = Tabs;

const weatherIcons = {
  '晴': '☀️',
  '多云': '⛅',
  '阴': '☁️',
  '小雨': '🌧️',
  '中雨': '🌧️',
  '大雨': '🌧️',
  '雷阵雨': '⛈️',
  '雪': '❄️',
};

const getWeatherIcon = (weather) => {
  for (const [key, icon] of Object.entries(weatherIcons)) {
    if (weather?.includes(key)) return icon;
  }
  return '🌤️';
};

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
      message.success('路线对比完成');
    } catch (error) {
      message.error('查询失败: ' + (error?.message || '未知错误'));
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
      message.success('天气查询完成');
    } catch (error) {
      message.error('查询失败: ' + (error?.message || '未知错误'));
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
      message.success(`获取到 ${result?.total_attractions || 0} 个真实景点`);
    } catch (error) {
      message.error('查询失败: ' + (error?.message || '未知错误'));
    } finally {
      setPoiLoading(false);
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '-';
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return h > 0 ? `${h}小时${m}分` : `${m}分`;
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${month}月${day}日`;
  };

  const getWeekDay = (index) => {
    const days = ['今天', '明天', '后天', '第四天'];
    return days[index] || `第${index + 1}天`;
  };

  const renderRouteCard = (title, icon, color, data, subtitle) => {
    if (!data || data.status === false) return null;
    return (
      <Card
        size="small"
        style={{
          borderRadius: 12,
          borderTop: `4px solid ${color}`,
          textAlign: 'center',
          height: '100%',
        }}
        bodyStyle={{ padding: '20px 16px' }}
      >
        <div style={{ fontSize: 28, marginBottom: 8 }}>{icon}</div>
        <div style={{ fontWeight: 600, marginBottom: 12, color: '#333' }}>{title}</div>
        <div style={{ fontSize: 24, fontWeight: 'bold', color, marginBottom: 4 }}>{subtitle}</div>
        {data.price !== undefined && (
          <div style={{ fontSize: 18, color: '#ff4d4f', fontWeight: 500 }}>¥{data.price}</div>
        )}
      </Card>
    );
  };

  const renderRoutes = () => {
    if (!routeResult?.routes) return null;
    const { routes } = routeResult;
    
    const cards = [];
    
    if (routes.train?.status) {
      cards.push(renderRouteCard(
        routes.train.train_number || '高铁',
        '🚄',
        '#1890ff',
        routes.train,
        formatDuration(routes.train.duration_min)
      ));
    }
    
    if (routes.driving?.status && routes.driving.paths?.length > 0) {
      const path = routes.driving.paths[0];
      cards.push(renderRouteCard(
        '驾车',
        '🚗',
        '#52c41a',
        routes.driving,
        path.duration ? formatDuration(path.duration / 60) : '-',
        `${path.distance ? (path.distance / 1000).toFixed(0) + '公里' : ''}`
      ));
    }
    
    if (routes.transit?.status && routes.transit.transits?.length > 0) {
      const transit = routes.transit.transits[0];
      cards.push(renderRouteCard(
        '公交',
        '🚇',
        '#722ed1',
        routes.transit,
        transit.duration ? formatDuration(parseInt(transit.duration) / 60) : '-',
        transit.fare ? `¥${transit.fare}` : ''
      ));
    }
    
    if (routes.walking?.status && routes.walking.paths?.length > 0) {
      const path = routes.walking.paths[0];
      cards.push(renderRouteCard(
        '步行',
        '🚶',
        '#fa8c16',
        routes.walking,
        path.duration ? formatDuration(path.duration / 60) : '-'
      ));
    }
    
    return <Row gutter={[16, 16]}>{cards.map((card, i) => <Col key={i} xs={12} sm={6}>{card}</Col>)}</Row>;
  };

  const renderWeather = () => {
    if (!weatherResult?.current) return null;
    const { current, forecast } = weatherResult;
    
    return (
      <div>
        <Card
          style={{
            borderRadius: 12,
            marginBottom: 20,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
          }}
          bodyStyle={{ padding: '28px 32px' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 24, color: '#fff' }}>
            <div style={{ fontSize: 64 }}>{getWeatherIcon(current.weather)}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 48, fontWeight: 'bold', lineHeight: 1 }}>{current.temperature}°</div>
              <div style={{ fontSize: 20, marginTop: 4, opacity: 0.9 }}>{current.weather}</div>
              <div style={{ fontSize: 14, marginTop: 8, opacity: 0.8 }}>
                {current.province} {current.city} · 湿度 {current.humidity}% · {current.wind_direction}风 {current.wind_power}级
              </div>
            </div>
          </div>
        </Card>
        
        {forecast?.length > 0 && (
          <Row gutter={[12, 12]}>
            {forecast.map((day, index) => (
              <Col key={index} xs={12} sm={6}>
                <Card
                  size="small"
                  style={{ borderRadius: 10, textAlign: 'center' }}
                  bodyStyle={{ padding: '16px 12px' }}
                >
                  <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>
                    {getWeekDay(index)}
                  </div>
                  <div style={{ fontSize: 12, color: '#999', marginBottom: 8 }}>
                    {formatDate(day.date)}
                  </div>
                  <div style={{ fontSize: 32, marginBottom: 8 }}>
                    {getWeatherIcon(day.weather_day)}
                  </div>
                  <div style={{ fontSize: 12, color: '#666', marginBottom: 8 }}>
                    {day.weather_day || '-'}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'center', gap: 8 }}>
                    {day.temp_max && <span style={{ color: '#f5222d', fontWeight: 600 }}>{day.temp_max}°</span>}
                    {day.temp_min && <span style={{ color: '#1890ff', fontWeight: 600 }}>{day.temp_min}°</span>}
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
    const { attractions = [], foods = [], total_attractions = 0, total_foods = 0 } = poiResult;
    
    return (
      <div>
        <Alert
          message={`共找到 ${total_attractions} 个景点，${total_foods} 个美食`}
          description="数据来源：高德地图实时POI"
          type="success"
          showIcon
          style={{ marginBottom: 16 }}
        />
        
        {attractions.length > 0 && (
          <div style={{ marginBottom: 24 }}>
            <Title level={5} style={{ marginBottom: 16 }}>🏛️ 热门景点</Title>
            <Row gutter={[12, 12]}>
              {attractions.slice(0, 12).map((poi, i) => (
                <Col key={i} xs={24} sm={12} md={8}>
                  <Card
                    size="small"
                    style={{ borderRadius: 10 }}
                    bodyStyle={{ padding: 16 }}
                  >
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 8, color: '#333' }}>
                      {poi.name}
                    </div>
                    {poi.address && (
                      <div style={{ fontSize: 12, color: '#999', marginBottom: 8, minHeight: 32 }}>
                        📍 {poi.address}
                      </div>
                    )}
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      {poi.rating > 0 && (
                        <Tag color="gold" style={{ margin: 0 }}>⭐ {poi.rating}</Tag>
                      )}
                      {poi.source === 'amap' && (
                        <Tag color="blue" style={{ margin: 0 }}>高德</Tag>
                      )}
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        )}
        
        {foods.length > 0 && (
          <div>
            <Title level={5} style={{ marginBottom: 16 }}>🍜 特色美食</Title>
            <Row gutter={[12, 12]}>
              {foods.slice(0, 8).map((food, i) => (
                <Col key={i} xs={24} sm={12} md={6}>
                  <Card
                    size="small"
                    style={{ borderRadius: 10 }}
                    bodyStyle={{ padding: 14 }}
                  >
                    <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 6 }}>
                      {food.name}
                    </div>
                    {food.address && (
                      <div style={{ fontSize: 11, color: '#999' }}>
                        📍 {food.address}
                      </div>
                    )}
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
    <div style={{ minHeight: '100vh', background: '#f5f7fa', padding: '24px 16px' }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <div style={{ marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>🗺️ 地图服务</Title>
          <Text type="secondary">基于高德地图的真实数据服务</Text>
        </div>

        <Card style={{ borderRadius: 16, marginBottom: 24, boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }} bodyStyle={{ padding: 0 }}>
          <Tabs
            activeKey={activeTab}
            onChange={setActiveTab}
            size="large"
            style={{ padding: '0 24px' }}
            tabBarStyle={{ marginBottom: 24 }}
          >
            <TabPane tab={<span><SwapOutlined /> 路线对比</span>} key="routes">
              <div style={{ padding: '0 24px 24px' }}>
                <Row gutter={[16, 16]} align="middle" style={{ marginBottom: 24 }}>
                  <Col xs={24} sm={10}>
                    <Input
                      prefix={<CarOutlined style={{ color: '#bfbfbf' }} />}
                      placeholder="输入出发城市"
                      value={fromCity}
                      onChange={(e) => setFromCity(e.target.value)}
                      size="large"
                      style={{ borderRadius: 8 }}
                    />
                  </Col>
                  <Col xs={24} sm={4} style={{ textAlign: 'center' }}>
                    <ArrowRightOutlined style={{ fontSize: 20, color: '#1890ff' }} />
                  </Col>
                  <Col xs={24} sm={10}>
                    <Input
                      prefix={<EnvironmentOutlined style={{ color: '#bfbfbf' }} />}
                      placeholder="输入目的城市"
                      value={toCity}
                      onChange={(e) => setToCity(e.target.value)}
                      size="large"
                      style={{ borderRadius: 8 }}
                    />
                  </Col>
                </Row>
                <div style={{ textAlign: 'center', marginBottom: 24 }}>
                  <Button
                    type="primary"
                    size="large"
                    icon={<ThunderboltOutlined />}
                    onClick={handleCompareRoutes}
                    loading={loading}
                    style={{ minWidth: 180, height: 44, borderRadius: 8, fontSize: 15 }}
                  >
                    查询路线
                  </Button>
                </div>
                {loading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
                {!loading && routeResult && renderRoutes()}
                {!loading && !routeResult && (
                  <div style={{ textAlign: 'center', padding: 60, color: '#999' }}>
                    <CarOutlined style={{ fontSize: 48, marginBottom: 16, opacity: 0.5 }} />
                    <div>输入城市后点击查询</div>
                  </div>
                )}
              </div>
            </TabPane>

            <TabPane tab={<span><CloudOutlined /> 天气预报</span>} key="weather">
              <div style={{ padding: '0 24px 24px' }}>
                <Row gutter={[12, 12]} style={{ marginBottom: 24 }}>
                  <Col xs={24} sm={16}>
                    <Input
                      prefix={<GlobalOutlined style={{ color: '#bfbfbf' }} />}
                      placeholder="输入城市名称，如：北京、上海"
                      value={weatherCity}
                      onChange={(e) => setWeatherCity(e.target.value)}
                      size="large"
                      onPressEnter={handleGetWeather}
                      style={{ borderRadius: 8 }}
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
                      style={{ height: 44, borderRadius: 8 }}
                    >
                      查询天气
                    </Button>
                  </Col>
                </Row>
                {weatherLoading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
                {!weatherLoading && weatherResult?.current && renderWeather()}
                {!weatherLoading && !weatherResult?.current && (
                  <div style={{ textAlign: 'center', padding: 60, color: '#999' }}>
                    <CloudOutlined style={{ fontSize: 48, marginBottom: 16, opacity: 0.5 }} />
                    <div>输入城市后点击查询</div>
                  </div>
                )}
              </div>
            </TabPane>

            <TabPane tab={<span><EnvironmentOutlined /> 探索景点</span>} key="poi">
              <div style={{ padding: '0 24px 24px' }}>
                <Row gutter={[12, 12]} style={{ marginBottom: 24 }}>
                  <Col xs={24} sm={16}>
                    <Input
                      prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
                      placeholder="输入城市名称，探索真实景点"
                      value={poiCity}
                      onChange={(e) => setPoiCity(e.target.value)}
                      size="large"
                      onPressEnter={handleGetPoi}
                      style={{ borderRadius: 8 }}
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
                      style={{ height: 44, borderRadius: 8 }}
                    >
                      探索
                    </Button>
                  </Col>
                </Row>
                {poiLoading && <div style={{ textAlign: 'center', padding: 40 }}><Spin size="large" /></div>}
                {!poiLoading && poiResult && renderPoiList()}
                {!poiLoading && !poiResult && (
                  <div style={{ textAlign: 'center', padding: 60, color: '#999' }}>
                    <EnvironmentOutlined style={{ fontSize: 48, marginBottom: 16, opacity: 0.5 }} />
                    <div>输入城市后点击探索</div>
                  </div>
                )}
              </div>
            </TabPane>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
