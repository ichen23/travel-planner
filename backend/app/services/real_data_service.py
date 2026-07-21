"""
真实数据服务 - 使用高德地图API获取真实景点
"""
import asyncio
from typing import List, Dict, Optional

async def get_real_attractions(city: str, limit: int = 10) -> List[Dict]:
    """
    获取城市真实景点
    
    Args:
        city: 城市名称
        limit: 返回数量限制
        
    Returns:
        景点列表，每个景点包含 name, address, rating, etc.
    """
    try:
        from app.services.amap_service import search_attractions
        pois = await search_attractions(city, limit=limit)
        
        result = []
        for poi in pois[:limit]:
            if poi.get('name'):
                result.append({
                    'name': poi['name'],
                    'address': poi.get('address', ''),
                    'rating': poi.get('rating', 0),
                    'cost': poi.get('cost', 0),
                    'lng': poi.get('lng'),
                    'lat': poi.get('lat'),
                    'type': poi.get('type', ''),
                    'source': 'amap',
                    'is_real': True
                })
        
        return result
    except Exception as e:
        print(f"获取{city}真实景点失败: {e}")
        return []

async def get_real_foods(city: str, limit: int = 8) -> List[Dict]:
    """
    获取城市真实美食
    
    Args:
        city: 城市名称
        limit: 返回数量限制
        
    Returns:
        美食列表
    """
    try:
        from app.services.amap_service import search_foods
        pois = await search_foods(city, limit=limit)
        
        result = []
        for poi in pois[:limit]:
            if poi.get('name'):
                result.append({
                    'name': poi['name'],
                    'address': poi.get('address', ''),
                    'rating': poi.get('rating', 0),
                    'cost': poi.get('cost', 0),
                    'lng': poi.get('lng'),
                    'lat': poi.get('lat'),
                    'type': poi.get('type', ''),
                    'source': 'amap',
                    'is_real': True
                })
        
        return result
    except Exception as e:
        print(f"获取{city}真实美食失败: {e}")
        return []

async def get_city_real_data(city: str) -> Dict:
    """
    获取城市完整真实数据
    
    Args:
        city: 城市名称
        
    Returns:
        包含 attractions 和 foods 的字典
    """
    attractions, foods = await asyncio.gather(
        get_real_attractions(city, 10),
        get_real_foods(city, 8),
        return_exceptions=True
    )
    
    if isinstance(attractions, Exception):
        attractions = []
    if isinstance(foods, Exception):
        foods = []
    
    return {
        'attractions': attractions,
        'foods': foods,
        'source': 'amap',
        'is_real': True
    }
