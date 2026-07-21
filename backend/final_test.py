import requests
import json

base_url = "http://localhost:8000/api"

def test_all_features():
    print("\n" + "#" * 70)
    print("# 完整功能测试报告")
    print("#" * 70)
    
    results = {"success": 0, "failed": 0, "details": []}
    
    def check(name, success, detail=""):
        status = "✓" if success else "✗"
        print(f"{status} {name}")
        if detail:
            print(f"  {detail}")
        results["success" if success else "failed"] += 1
        results["details"].append({"name": name, "success": success, "detail": detail})
    
    # 1. 健康检查
    print("\n【1. 基础功能】")
    try:
        r = requests.get(f"{base_url}/health")
        check("健康检查", r.status_code == 200)
    except Exception as e:
        check("健康检查", False, str(e))
    
    # 2. 天气API测试
    print("\n【2. 天气API测试】")
    cities = ["北京", "上海", "广州", "哈尔滨", "三亚", "拉萨"]
    weather_data = {}
    
    for city in cities:
        try:
            r = requests.get(f"{base_url}/weather/current", params={"city": city})
            data = r.json()
            if data.get("success"):
                weather = data.get("weather", {})
                weather_data[city] = weather
                check(f"{city}当前天气", True, f"{weather.get('weather')}, {weather.get('temperature')}°C")
            else:
                check(f"{city}当前天气", False, data.get("message"))
        except Exception as e:
            check(f"{city}当前天气", False, str(e))
    
    # 验证不同城市天气不同
    if len(weather_data) >= 2:
        temps = [w.get("temperature") for w in weather_data.values()]
        different = len(set(temps)) > 1
        check("不同城市天气不同", different, f"温度: {temps}")
    
    # 3. 城市详情测试
    print("\n【3. 城市详情测试】")
    detail_data = {}
    
    for city in ["北京", "上海", "三亚", "塞罕坝", "丽江古城", "哈尔滨"]:
        try:
            r = requests.get(f"{base_url}/destination/detail/{city}")
            data = r.json()
            if data.get("success"):
                realtime = data.get("realtime_data", {})
                attrs = realtime.get("attractions", [])
                detail_data[city] = {
                    "attrs_count": len(attrs),
                    "first_attr": attrs[0] if attrs else None
                }
                if attrs:
                    check(f"{city}城市详情", True, f"{len(attrs)}个景点, 第一个: {attrs[0].get('name')}")
                else:
                    check(f"{city}城市详情", True, "无实时景点")
            else:
                check(f"{city}城市详情", False)
        except Exception as e:
            check(f"{city}城市详情", False, str(e))
    
    # 验证不同城市有不同景点
    if len(detail_data) >= 2:
        attrs_names = set()
        for city, info in detail_data.items():
            if info["first_attr"]:
                attrs_names.add(info["first_attr"].get("name"))
        different = len(attrs_names) > 1
        check("不同城市有不同景点", different, f"景点名称: {attrs_names}")
    
    # 4. 地理编码测试
    print("\n【4. 地理编码测试】")
    for city in ["北京", "三亚", "塞罕坝"]:
        try:
            r = requests.get(f"{base_url}/destination/geocode", params={"city": city})
            data = r.json()
            if data.get("success"):
                geo = data.get("geo", {})
                check(f"{city}地理编码", True, f"[{geo.get('lng')}, {geo.get('lat')}]")
            else:
                check(f"{city}地理编码", False)
        except Exception as e:
            check(f"{city}地理编码", False, str(e))
    
    # 5. 天气预报测试
    print("\n【5. 天气预报测试】")
    for city in ["北京", "三亚"]:
        try:
            r = requests.get(f"{base_url}/destination/weather-forecast/{city}")
            data = r.json()
            if data.get("success"):
                forecast = data.get("forecast", {})
                forecast_list = forecast.get("forecast", [])
                check(f"{city}天气预报", True, f"{len(forecast_list)}天预报")
            else:
                check(f"{city}天气预报", False)
        except Exception as e:
            check(f"{city}天气预报", False, str(e))
    
    # 6. 推荐功能测试
    print("\n【6. 推荐功能测试】")
    try:
        r = requests.get(f"{base_url}/destination/recommend", params={
            "from_city": "北京",
            "travel_date": "2026-07-25",
            "max_duration": 3
        })
        data = r.json()
        if data.get("success"):
            dests = data.get("destinations", [])
            check("推荐功能", True, f"{len(dests)}个推荐目的地")
        else:
            check("推荐功能", False)
    except Exception as e:
        check("推荐功能", False, str(e))
    
    # 7. POI搜索测试
    print("\n【7. POI搜索测试】")
    for city in ["北京", "三亚"]:
        try:
            r = requests.get(f"{base_url}/destination/attractions", params={"city": city})
            data = r.json()
            attrs = data.get("attractions", [])
            check(f"{city}景点搜索", True if attrs else False, f"{len(attrs)}个结果")
        except Exception as e:
            check(f"{city}景点搜索", False, str(e))
    
    # 8. 完整城市内容测试
    print("\n【8. 完整城市内容测试】")
    for city in ["北京", "三亚"]:
        try:
            r = requests.get(f"{base_url}/destination/full-content/{city}")
            data = r.json()
            attrs = data.get("attractions", [])
            foods = data.get("foods", [])
            hotels = data.get("hotels", [])
            check(f"{city}完整内容", True, f"景点:{len(attrs)}, 美食:{len(foods)}, 酒店:{len(hotels)}")
        except Exception as e:
            check(f"{city}完整内容", False, str(e))
    
    # 9. 统计测试
    print("\n【9. 统计测试】")
    try:
        r = requests.get(f"{base_url}/destination/stats")
        data = r.json()
        check("统计信息", True, f"{data.get('total_destinations')}个目的地, {data.get('real_city_count')}个真实城市")
    except Exception as e:
        check("统计信息", False, str(e))
    
    # 10. 盲盒测试
    print("\n【10. 盲盒测试】")
    try:
        r = requests.post(f"{base_url}/ai/blindbox/generate")
        data = r.json()
        if data.get("city"):
            check("盲盒生成", True, f"随机城市: {data.get('city')}")
            if data.get("weather"):
                check("盲盒天气", True, "包含天气信息")
            if data.get("real_data", {}).get("attractions"):
                check("盲盒景点", True, "包含景点信息")
        else:
            check("盲盒生成", False, data.get("message", "响应格式错误"))
    except Exception as e:
        check("盲盒生成", False, str(e))
    
    # 总结
    print("\n" + "#" * 70)
    print("# 测试总结")
    print("#" * 70)
    print(f"成功: {results['success']}, 失败: {results['failed']}")
    print(f"成功率: {results['success'] / (results['success'] + results['failed']) * 100:.1f}%")
    
    if results["failed"] > 0:
        print("\n失败的测试:")
        for detail in results["details"]:
            if not detail["success"]:
                print(f"  - {detail['name']}: {detail['detail']}")
    
    return results["failed"] == 0

if __name__ == "__main__":
    success = test_all_features()
    exit(0 if success else 1)
