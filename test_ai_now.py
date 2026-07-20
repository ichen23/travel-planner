import requests
import json

BASE_URL = "http://localhost:8000/api/ai/generate"

test_cases = [
    ("故宫博物院", "古建筑", "北京"),
    ("长城", "古建筑", "北京"),
    ("西湖", "自然", "杭州"),
    ("布达拉宫", "古建筑", "拉萨"),
    ("黄山", "自然", "黄山"),
    ("张家界", "自然", "张家界"),
    ("外滩", "风景名胜", "上海"),
    ("丽江古城", "风景名胜", "丽江"),
]

templates = ["travel_copy", "punch_card", "photo_spots"]

for title, ptype, city in test_cases:
    print(f"\n{'='*60}")
    print(f"测试: {title} ({ptype}, {city})")
    print(f"{'='*60}")
    for template in templates:
        try:
            r = requests.post(BASE_URL, json={
                "template_type": template,
                "context": {
                    "title": title,
                    "type": ptype,
                    "city": city,
                }
            }, timeout=10)
            data = r.json()
            content = data.get("data", {}).get("content", "")
            title_result = data.get("data", {}).get("title", "")
            is_ok = data.get("success", False) and len(content) > 100
            status = "PASS" if is_ok else "FAIL"
            print(f"  [{status}] {template}: title='{title_result}', content_len={len(content)}, success={data.get('success')}")
            if not is_ok:
                print(f"         Error: {data.get('error', 'content too short')}")
                print(f"         Content preview: {content[:100]}")
        except Exception as e:
            print(f"  [ERROR] {template}: {e}")

print("\n\nDone!")
