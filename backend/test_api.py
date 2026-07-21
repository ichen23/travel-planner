import requests
import json
import time

print("等待服务启动...")
time.sleep(3)

BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, url, params=None, expected_status=200):
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        else:
            response = requests.post(url, json=params, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✓ {name}: {response.status_code}")
            try:
                return response.json()
            except:
                return {"raw": response.text[:100]}
        else:
            print(f"✗ {name}: 期望 {expected_status}, 实际 {response.status_code}")
            print(f"  响应: {response.text[:100]}")
            return None
    except Exception as e:
        print(f"✗ {name}: 连接失败 - {str(e)}")
        return None

print("=" * 60)
print("API端点测试")
print("=" * 60)

print("\n1. 测试城市搜索...")
result = test_endpoint("搜索北京", "GET", f"{BASE_URL}/api/destination/search-city", {"keyword": "北京", "limit": 5})
if result and result.get("success"):
    print(f"  找到 {result.get('total', 0)} 个结果")

test_endpoint("搜索拉萨", "GET", f"{BASE_URL}/api/destination/search-city", {"keyword": "拉萨", "limit": 5})
test_endpoint("搜索乌鲁木齐", "GET", f"{BASE_URL}/api/destination/search-city", {"keyword": "乌鲁木齐", "limit": 5})
test_endpoint("搜索香港", "GET", f"{BASE_URL}/api/destination/search-city", {"keyword": "香港", "limit": 5})
test_endpoint("搜索台北", "GET", f"{BASE_URL}/api/destination/search-city", {"keyword": "台北", "limit": 5})

print("\n2. 测试推荐目的地...")
test_endpoint("北京出发推荐", "GET", f"{BASE_URL}/api/destination/recommend", {"from_city": "北京市", "days": 3})

print("\n3. 测试AI模板列表...")
test_endpoint("获取模板", "GET", f"{BASE_URL}/api/ai/templates")

print("\n4. 测试完整城市内容...")
result = test_endpoint("北京市完整内容", "GET", f"{BASE_URL}/api/destination/full-content/北京市")
if result and result.get("success"):
    print(f"  城市: {result.get('city')}")

print("\n5. 测试POI搜索...")
test_endpoint("北京POI搜索", "GET", f"{BASE_URL}/api/destination/poi", {"city": "北京市", "keywords": "故宫"})

print("\n6. 测试7天天气预报...")
test_endpoint("北京天气预报", "GET", f"{BASE_URL}/api/destination/weather-forecast/北京市")

print("\n7. 测试所有真实行政区划...")
result = test_endpoint("获取所有行政区划", "GET", f"{BASE_URL}/api/destination/real-cities")
if result:
    data = result.get("data", [])
    if isinstance(data, list):
        print(f"  共 {len(data)} 个行政区划")
    elif isinstance(data, dict):
        print(f"  共 {len(data)} 个行政区划")

print("\n8. 测试统计信息...")
test_endpoint("获取统计", "GET", f"{BASE_URL}/api/destination/stats")

print("\n9. 测试生成行程...")
test_endpoint("AI生成行程", "POST", f"{BASE_URL}/api/destination/generate-itinerary", {
    "from_city": "北京市",
    "to_city": "上海市",
    "days": 3,
    "style": "经典"
})

print("\n" + "=" * 60)
print("API测试完成")
print("=" * 60)
