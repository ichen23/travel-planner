import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.real_city_data import REAL_CITY_DATA
from app.services.city_database import REAL_CITY_COORDS

test_names = ["北京", "北京市", "上海", "上海市", "广州", "广州市", "深圳", "深圳市", "拉萨", "拉萨市", "乌鲁木齐", "乌鲁木齐市", "台北", "台北市"]

print("检查数据是否存在:")
for name in test_names:
    in_data = name in REAL_CITY_DATA
    in_coords = name in REAL_CITY_COORDS
    print(f"  {name}: 数据={'✓' if in_data else '✗'}, 坐标={'✓' if in_coords else '✗'}")

print("\n数据统计:")
print(f"  REAL_CITY_DATA: {len(REAL_CITY_DATA)} 条")
print(f"  REAL_CITY_COORDS: {len(REAL_CITY_COORDS)} 条")

print("\n检查重复键...")
keys = list(REAL_CITY_DATA.keys())
unique_keys = set(keys)
print(f"  总键数: {len(keys)}")
print(f"  唯一键数: {len(unique_keys)}")
if len(keys) != len(unique_keys):
    print("  警告: 存在重复键!")
