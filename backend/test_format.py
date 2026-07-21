import requests
import json

base_url = "http://localhost:8000/api"

def test_data_format():
    print("测试后端返回数据格式：")
    print("=" * 60)
    
    # 测试城市详情
    for city in ["北京", "三亚"]:
        r = requests.get(f"{base_url}/destination/detail/{city}")
        data = r.json()
        
        print(f"\n{city} 详情返回结构：")
        print(f"  - 顶级键: {list(data.keys())[:8]}...")
        
        if "attractions" in data and data["attractions"]:
            first = data["attractions"][0]
            print(f"  - attractions[0] 类型: {type(first)}")
            if isinstance(first, dict):
                print(f"  - attractions[0] 键: {list(first.keys())[:10]}")
                print(f"  - attractions[0] 示例: {json.dumps({k: first[k] for k in list(first.keys())[:3]}, ensure_ascii=False)[:100]}")
        
        if "realtime_data" in data:
            realtime = data["realtime_data"]
            print(f"  - realtime_data 键: {list(realtime.keys())}")
            if realtime.get("attractions"):
                first = realtime["attractions"][0]
                print(f"  - realtime_data.attractions[0] 类型: {type(first)}")
                if isinstance(first, dict):
                    print(f"  - realtime_data.attractions[0] 键: {list(first.keys())[:10]}")

if __name__ == "__main__":
    test_data_format()
