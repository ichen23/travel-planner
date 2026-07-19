import sys
sys.path.insert(0, '.')

from app.services.city_database import get_recommendations

for hours in [1, 2, 3, 4, 5, 6, 7]:
    print(f"\n{'='*60}")
    print(f"北京出发，{hours}小时{'内' if hours < 7 else '以上'}推荐")
    print(f"{'='*60}")
    r = get_recommendations("北京", hours)
    print(f"共 {len(r)} 个推荐目的地")
    for d in r[:10]:
        city = d['city']
        dur = d['duration']
        tags = d.get('tags', [])[:3]
        print(f"  {city}: {dur} | {tags}")
    if len(r) > 10:
        print(f"  ... 还有 {len(r)-10} 个")
