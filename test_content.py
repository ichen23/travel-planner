import requests
import json

BASE_URL = "http://localhost:8000/api/ai/generate"

print("="*60)
print("测试1: 已知景点 - 故宫博物院 (所有模板)")
print("="*60)
for template in ["travel_copy", "punch_card", "photo_spots"]:
    r = requests.post(BASE_URL, json={
        "template_type": template,
        "context": {"title": "故宫博物院", "type": "古建筑", "city": "北京"}
    })
    data = r.json()
    content = data.get("data", {}).get("content", "")
    print(f"\n【{template}】长度: {len(content)}")
    print("-" * 40)
    print(content[:500])
    if len(content) > 500:
        print("...")
    print()

print("\n" + "="*60)
print("测试2: 未知景点 - XX乐园 (使用fallback)")
print("="*60)
for template in ["travel_copy", "punch_card", "photo_spots"]:
    r = requests.post(BASE_URL, json={
        "template_type": template,
        "context": {"title": "XX乐园", "type": "游乐园", "city": "上海"}
    })
    data = r.json()
    content = data.get("data", {}).get("content", "")
    print(f"\n【{template}】长度: {len(content)}")
    print("-" * 40)
    print(content[:500])
    if len(content) > 500:
        print("...")
    print()

print("\n" + "="*60)
print("测试3: 完全 generic - 人民公园")
print("="*60)
for template in ["travel_copy", "punch_card", "photo_spots"]:
    r = requests.post(BASE_URL, json={
        "template_type": template,
        "context": {"title": "人民公园", "type": "公园", "city": "成都"}
    })
    data = r.json()
    content = data.get("data", {}).get("content", "")
    print(f"\n【{template}】长度: {len(content)}")
    print("-" * 40)
    print(content[:500])
    if len(content) > 500:
        print("...")
    print()

print("\n所有测试完成!")
