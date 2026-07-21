import requests
import time

base_url = "http://localhost:8000/api"

print("测试不同城市的实时数据：")
print("=" * 60)

cities = ["北京", "上海", "三亚", "塞罕坝", "丽江"]

for city in cities:
    try:
        r = requests.get(f"{base_url}/destination/detail/{city}")
        data = r.json()
        real_data = data.get("realtime_data", {})
        real_attrs = real_data.get("attractions", [])
        
        if real_attrs:
            first = real_attrs[0]
            if isinstance(first, dict):
                name = first.get("name", "未知")
                cityname = first.get("cityname", "")
                print(f"{city}: {name} (属于{cityname})")
            else:
                print(f"{city}: {str(first)[:50]}")
        else:
            static_attrs = data.get("static_data", {}).get("attractions", [])
            if static_attrs:
                print(f"{city}: {static_attrs[0]} (静态数据)")
            else:
                print(f"{city}: 无数据")
    except Exception as e:
        print(f"{city}: 错误 - {e}")

print("\n测试天气（不同城市）：")
print("=" * 60)

for city in ["北京", "哈尔滨", "三亚", "拉萨"]:
    try:
        r = requests.get(f"{base_url}/weather/current", params={"city": city})
        data = r.json()
        if data.get("success"):
            w = data.get("weather", {})
            print(f"{city}: {w.get('weather')}, {w.get('temperature')}°C, 湿度{w.get('humidity')}%")
    except Exception as e:
        print(f"{city}: 错误 - {e}")

print("\n测试完成！")
