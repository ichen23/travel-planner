"""
扩展城市数据加载器
从JSON文件加载215个城市的详细数据
"""
import json
import os

# 查找数据文件的多个可能位置
def find_data_file():
    """查找数据文件"""
    # 获取项目根目录 (backend/)
    current_file = os.path.abspath(__file__)  # app/services/extended_data_loader.py
    backend_dir = os.path.dirname(os.path.dirname(current_file))  # backend/
    
    possible_paths = [
        os.path.join(backend_dir, "all_cities_data.json"),  # backend/all_cities_data.json
        os.path.join(os.path.dirname(current_file), "all_cities_data.json"),  # app/services/all_cities_data.json
        os.path.join(os.getcwd(), "all_cities_data.json"),  # 工作目录
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

# 加载所有城市数据
def load_extended_cities_data():
    """从JSON文件加载扩展城市数据"""
    data_file = find_data_file()
    
    if data_file:
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"从 {data_file} 加载了 {len(data)} 个城市数据")
                return data
        except Exception as e:
            print(f"加载数据文件失败: {e}")
    return {}

# 扩展城市数据（运行时加载）
EXTENDED_CITIES_DATA = load_extended_cities_data()

# 获取所有可用城市列表
def get_all_available_cities():
    """获取所有有详细数据的城市"""
    from app.services.multi_city_service import CITY_STATIC_DATA
    all_cities = set(CITY_STATIC_DATA.keys())
    all_cities.update(EXTENDED_CITIES_DATA.keys())
    return sorted(all_cities)

# 获取城市景点（扩展版）
def get_city_attractions_extended(city):
    """获取城市景点，包括扩展数据"""
    from app.services.multi_city_service import CITY_STATIC_DATA, normalize_city_name
    
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]["attractions"]
    
    if city in EXTENDED_CITIES_DATA:
        return EXTENDED_CITIES_DATA[city]["attractions"]
    
    return None

# 获取城市美食（扩展版）
def get_city_food_extended(city):
    """获取城市美食，包括扩展数据"""
    from app.services.multi_city_service import CITY_STATIC_DATA, normalize_city_name
    
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]["food"]
    
    if city in EXTENDED_CITIES_DATA:
        return EXTENDED_CITIES_DATA[city]["food"]
    
    return None

# 获取城市完整数据（扩展版）
def get_city_full_data(city):
    """获取城市完整数据，包括扩展数据"""
    from app.services.multi_city_service import CITY_STATIC_DATA, normalize_city_name
    
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]
    
    if city in EXTENDED_CITIES_DATA:
        return EXTENDED_CITIES_DATA[city]
    
    return None

print(f"扩展城市数据加载成功：{len(EXTENDED_CITIES_DATA)} 个城市")
