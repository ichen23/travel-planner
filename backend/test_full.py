import sys
sys.path.insert(0, '.')

from app.services.city_database import get_recommendations
from app.services.beijing_3hr_data import get_beijing_3hr_destinations

all_dests = get_beijing_3hr_destinations(999)
print(f"7小时以上 总共 {len(all_dests)} 个目的地")

long_distance = [d for d in all_dests if d['travel_time_hours'] >= 7]
print(f"\n7小时以上的远方城市 ({len(long_distance)} 个):")
for d in long_distance:
    print(f"  {d['name']}: {d['travel_time_hours']}小时")

r = get_recommendations("北京", 7)
print(f"\nget_recommendations 返回 {len(r)} 个 (限制50个)")

faraway_in_results = [d for d in r if d.get('travel_time_hours', 0) >= 7]
print(f"\n其中7小时以上的远方城市有 {len(faraway_in_results)} 个:")
for d in faraway_in_results:
    print(f"  {d['city']}: {d['duration']}")

tags_problem = [d['name'] for d in all_dests if not d['info'] and not d['name'] in ['上海', '杭州', '南京', '成都', '重庆', '西安', '广州', '深圳', '厦门']]
print(f"\n没有详细信息的城市: {len(tags_problem)} 个")
if tags_problem:
    print(f"  {tags_problem[:10]}...")
