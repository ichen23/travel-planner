import sys
sys.path.insert(0, '.')
import json

print("=== 问题诊断 ===\n")

# 1. 检查真实数据有多少
from app.services.real_city_data import REAL_CITY_ATTRACTIONS
print(f"1. real_city_data.py 中的真实城市: {len(REAL_CITY_ATTRACTIONS)} 个")
print(f"   城市列表: {list(REAL_CITY_ATTRACTIONS.keys())}")

# 2. 检查 city_database 中有多少真实数据
from app.services.city_database import CITY_BASIC_INFO, MASS_CITY_INFO, MEGA_CITY_INFO

def check_real_highlights(data, source):
    """检查数据源中有多少真实highlights"""
    real_count = 0
    total_count = 0
    real_cities = []
    
    for city, info in data.items():
        total_count += 1
        highlights = info.get('highlights', '')
        
        if not highlights:
            continue
            
        # 解析
        if isinstance(highlights, str):
            separator = '、' if '、' in highlights else (',' if ',' in highlights else '，')
            items = [h.strip() for h in highlights.split(separator) if h.strip()]
        else:
            items = highlights if isinstance(highlights, list) else []
        
        # 检查是否有真实的景点（包含具体的景点名）
        template_keywords = ['CBD', '摩天大楼', '主题乐园', '地', '标志', '购物中心']
        real_items = [item for item in items if not any(kw in item for kw in template_keywords)]
        
        if len(real_items) >= 3:
            real_count += 1
            real_cities.append((city, real_items[:3]))
    
    print(f"\n{source}:")
    print(f"  总城市数: {total_count}")
    print(f"  有真实highlights的城市: {real_count}")
    
    return real_cities

# 检查各个数据源
print("\n2. 检查 city_database 中的真实数据:")
real_from_basic = check_real_highlights(CITY_BASIC_INFO, "CITY_BASIC_INFO")
real_from_mass = check_real_highlights(MASS_CITY_INFO, "MASS_CITY_INFO")
real_from_mega = check_real_highlights(MEGA_CITY_INFO, "MEGA_CITY_INFO")

# 合并所有真实数据
all_real_cities = {}
for city, items in real_from_basic:
    all_real_cities[city] = items
for city, items in real_from_mass:
    if city not in all_real_cities:
        all_real_cities[city] = items
for city, items in real_from_mega:
    if city not in all_real_cities:
        all_real_cities[city] = items

print(f"\n所有有真实highlights的城市(不重复): {len(all_real_cities)} 个")
print(f"\n详细列表:")
for city, items in sorted(all_real_cities.items()):
    print(f"  {city}: {', '.join(items)}")

# 3. 测试 generate_full_day_plan 是否工作
print("\n\n3. 测试 generate_full_day_plan:")
from app.services.multi_city_service import generate_full_day_plan

# 测试真实数据城市
test_cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '西安', '厦门', '青岛', '三亚', '桂林', '丽江']
for city in test_cities[:5]:
    result = generate_full_day_plan(city, 1)
    if result:
        schedule = result.get('schedule', [])
        print(f"  {city}: ✓ {len(schedule)} 个活动")
    else:
        print(f"  {city}: ✗ 返回 None")

# 测试非真实数据城市
unknown_cities = ['郑州', '武汉', '南京', '苏州', '长沙']
print(f"\n测试其他城市:")
for city in unknown_cities:
    result = generate_full_day_plan(city, 1)
    if result:
        schedule = result.get('schedule', [])
        print(f"  {city}: ✓ {len(schedule)} 个活动")
    else:
        print(f"  {city}: ✗ 返回 None")
