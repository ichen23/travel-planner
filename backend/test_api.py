import requests
import json

base = "http://localhost:8000/api/destination/recommend"

for hours in [1, 3, 7]:
    print(f"\n{'='*60}")
    print(f"北京出发 {hours}小时{'内' if hours < 7 else '以上'}")
    print(f"{'='*60}")
    
    resp = requests.get(base, params={
        "from_city": "北京",
        "travel_date": "2025-07-20",
        "max_duration": hours
    })
    
    data = resp.json()
    print(f"成功: {data['success']}")
    print(f"目的地数量: {len(data['destinations'])}")
    
    for d in data['destinations'][:5]:
        city = d['city']
        dur = d['duration']
        tags = d.get('tags', [])[:2]
        has_tips = bool(d.get('tips', {}).get('food'))
        print(f"  {city}: {dur} | 标签: {tags} | 有美食贴士: {has_tips}")
    
    if hours == 7:
        faraway = [d for d in data['destinations'] if d.get('travel_time_hours', 0) >= 7]
        print(f"\n7小时以上的远方城市: {len(faraway)}个")
        for d in faraway[:5]:
            print(f"  {d['city']}: {d['duration']}")
        if len(faraway) > 5:
            print(f"  ... 还有 {len(faraway)-5} 个")
