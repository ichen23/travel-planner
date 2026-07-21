import requests
import asyncio
import time

base_url = "http://localhost:8000/api"

def test_health():
    print("=" * 60)
    print("1. 测试健康检查")
    print("=" * 60)
    try:
        r = requests.get(f"{base_url}/health")
        data = r.json()
        print(f"✓ 服务状态: {data.get('status')}")
        print(f"✓ AMAP Key 已配置: {data.get('amap_key_in_env')}")
        return True
    except Exception as e:
        print(f"✗ 健康检查失败: {e}")
        return False

def test_weather():
    print("\n" + "=" * 60)
    print("2. 测试天气API（不同城市应有不同天气）")
    print("=" * 60)
    
    cities = ["北京", "上海", "广州", "哈尔滨", "三亚"]
    
    for city in cities:
        try:
            r = requests.get(f"{base_url}/weather/current", params={"city": city})
            data = r.json()
            if data.get("success"):
                weather = data.get("weather", {})
                print(f"✓ {city}: {weather.get('weather')}, {weather.get('temperature')}°C, 湿度{weather.get('humidity')}%")
            else:
                print(f"✗ {city}: {data.get('message')}")
        except Exception as e:
            print(f"✗ {city}: {e}")

def test_city_detail():
    print("\n" + "=" * 60)
    print("3. 测试城市详情（每个城市应有不同景点）")
    print("=" * 60)
    
    cities = ["北京", "上海", "广州", "成都", "西安", "塞罕坝", "丽江", "哈尔滨"]
    
    for city in cities:
        try:
            r = requests.get(f"{base_url}/destination/detail/{city}")
            data = r.json()
            if data.get("success"):
                attractions = data.get("attractions", [])
                real_data = data.get("realtime_data", {})
                real_attrs = real_data.get("attractions", [])
                
                if real_attrs:
                    first_attr = real_attrs[0]
                    if isinstance(first_attr, dict):
                        print(f"✓ {city}: 实时景点={first_attr.get('name')}, 归属={first_attr.get('cityname')}")
                    else:
                        print(f"✓ {city}: 实时景点={str(first_attr)[:30]}")
                elif attractions:
                    print(f"✓ {city}: 静态景点={str(attractions[0])[:30]}")
                else:
                    print(f"✗ {city}: 无景点数据")
            else:
                print(f"✗ {city}: 获取失败")
        except Exception as e:
            print(f"✗ {city}: {e}")

def test_geocode():
    print("\n" + "=" * 60)
    print("4. 测试地理编码")
    print("=" * 60)
    
    cities = ["北京", "上海", "塞罕坝", "丽江古城", "三亚"]
    
    for city in cities:
        try:
            r = requests.get(f"{base_url}/destination/geocode", params={"city": city})
            data = r.json()
            if data.get("success"):
                geo = data.get("geo", {})
                print(f"✓ {city}: 经纬度=[{geo.get('lng')}, {geo.get('lat')}], 标准名={geo.get('name')[:30]}")
            else:
                print(f"✗ {city}: 地理编码失败")
        except Exception as e:
            print(f"✗ {city}: {e}")

def test_blind_box():
    print("\n" + "=" * 60)
    print("5. 测试盲盒功能")
    print("=" * 60)
    
    try:
        r = requests.post(f"{base_url}/blindbox/generate")
        data = r.json()
        if data.get("success"):
            city = data.get("city")
            content = data.get("content", {})
            real_data = data.get("real_data", {})
            weather = data.get("weather", {})
            
            print(f"✓ 随机城市: {city}")
            
            if weather and weather.get("current"):
                w = weather["current"]
                print(f"✓ 天气: {w.get('weather')}, {w.get('temperature')}°C")
            
            if real_data.get("attractions"):
                first = real_data["attractions"][0]
                if isinstance(first, dict):
                    print(f"✓ 推荐景点: {first.get('name')}")
            
            if content.get("data"):
                content_data = content["data"]
                print(f"✓ 文案类型: {content_data.get('type')}")
        else:
            print(f"✗ 盲盒生成失败: {data.get('message')}")
    except Exception as e:
        print(f"✗ 盲盒测试失败: {e}")

def test_recommendations():
    print("\n" + "=" * 60)
    print("6. 测试推荐功能")
    print("=" * 60)
    
    try:
        r = requests.get(f"{base_url}/destination/recommend", params={
            "from_city": "北京",
            "travel_date": "2026-07-25",
            "max_duration": 3
        })
        data = r.json()
        if data.get("success"):
            destinations = data.get("destinations", [])
            print(f"✓ 推荐数量: {len(destinations)}")
            for dest in destinations[:3]:
                print(f"  - {dest.get('city')}: 有景点={len(dest.get('tips', {}).get('attractions', [])) > 0}")
        else:
            print(f"✗ 推荐失败")
    except Exception as e:
        print(f"✗ 推荐测试失败: {e}")

def main():
    print("\n" + "#" * 60)
    print("# 综合功能测试")
    print("#" * 60)
    
    test_health()
    test_weather()
    test_city_detail()
    test_geocode()
    test_blind_box()
    test_recommendations()
    
    print("\n" + "#" * 60)
    print("# 测试完成")
    print("#" * 60)

if __name__ == "__main__":
    main()
