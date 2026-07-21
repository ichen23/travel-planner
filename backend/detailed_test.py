import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("详细功能测试")
print("=" * 60)

print("\n1. 测试城市搜索返回完整数据...")
response = requests.get(f"{BASE_URL}/api/destination/search-city", params={"keyword": "北京", "limit": 3})
if response.status_code == 200:
    data = response.json()
    print(f"   返回格式: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    if isinstance(data, dict):
        if "data" in data:
            print(f"   数据数量: {len(data['data'])}")
            if data['data']:
                print(f"   第一个结果: {data['data'][0]}")
        elif "results" in data:
            print(f"   结果数量: {len(data['results'])}")
        else:
            print(f"   完整数据: {json.dumps(data, ensure_ascii=False)[:200]}")

print("\n2. 测试推荐目的地（带完整参数）...")
response = requests.get(f"{BASE_URL}/api/destination/recommend", params={
    "from_city": "北京市", 
    "days": 3,
    "travel_date": "2025-08-01"
})
if response.status_code == 200:
    data = response.json()
    print(f"   状态: 成功")
    if isinstance(data, dict):
        if "data" in data:
            print(f"   推荐数量: {len(data['data'])}")
        print(f"   返回数据结构: {list(data.keys())}")
else:
    print(f"   状态码: {response.status_code}")
    print(f"   错误信息: {response.text[:200]}")

print("\n3. 测试AI模板列表详情...")
response = requests.get(f"{BASE_URL}/api/ai/templates")
if response.status_code == 200:
    data = response.json()
    if isinstance(data, dict):
        print(f"   模板数量: {len(data)}")
        for key in list(data.keys())[:3]:
            print(f"   - {key}: {str(data[key])[:30]}...")
    else:
        print(f"   返回类型: {type(data)}")
        print(f"   数据: {str(data)[:100]}")

print("\n4. 测试北京市完整内容（检查是否有景点、美食等）...")
response = requests.get(f"{BASE_URL}/api/destination/full-content/北京市")
if response.status_code == 200:
    data = response.json()
    if isinstance(data, dict) and "data" in data:
        content = data["data"]
        print(f"   城市: {content.get('name', 'N/A')}")
        print(f"   省份: {content.get('province', 'N/A')}")
        if "coords" in content:
            print(f"   坐标: {content['coords']}")
        if "attractions" in content:
            print(f"   景点数量: {len(content['attractions'])}")
        if "foods" in content:
            print(f"   美食数量: {len(content['foods'])}")
        if "tips" in content:
            print(f"   贴士数量: {len(content['tips'])}")

print("\n5. 测试特殊地区（西藏、新疆、香港、台湾）...")
test_cities = [
    ("拉萨市", "西藏"),
    ("乌鲁木齐市", "新疆"), 
    ("香港", "香港"),
    ("台北市", "台湾"),
    ("银川市", "宁夏"),
    ("贵阳市", "贵州")
]
for city, region in test_cities:
    response = requests.get(f"{BASE_URL}/api/destination/full-content/{city}")
    status = "✓" if response.status_code == 200 else "✗"
    print(f"   {status} {city}({region}): {response.status_code}")

print("\n6. 测试AI内容生成...")
response = requests.post(f"{BASE_URL}/api/ai/generate", json={
    "template": "poetic",
    "city": "拉萨市",
    "days": 2
})
if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        print(f"   ✓ AI生成成功")
        content = data.get("data", {})
        print(f"   标题: {content.get('title', 'N/A')}")
        print(f"   内容长度: {len(content.get('content', ''))}")
    else:
        print(f"   ✗ AI生成失败: {data.get('error')}")
else:
    print(f"   ✗ 请求失败: {response.status_code}")

print("\n7. 测试统计信息...")
response = requests.get(f"{BASE_URL}/api/destination/stats")
if response.status_code == 200:
    data = response.json()
    print(f"   统计数据: {json.dumps(data, ensure_ascii=False)[:200]}")

print("\n" + "=" * 60)
print("详细测试完成")
print("=" * 60)
