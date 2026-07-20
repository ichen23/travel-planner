import asyncio
from app.services.amap_service import (
    geocode_city, search_attractions, search_foods, search_hotels
)
from app.services.weather_service import get_weather_forecast


CITY_TAGS = {
    "北京": ["历史名城", "古都", "文化", "政治中心"],
    "上海": ["现代都市", "金融中心", "时尚", "国际化"],
    "广州": ["美食", "南方都市", "商贸", "早茶"],
    "深圳": ["科技", "年轻", "海滨", "现代化"],
    "杭州": ["西湖", "江南水乡", "电商", "美景"],
    "成都": ["美食", "休闲", "熊猫", "火锅"],
    "西安": ["古都", "历史", "兵马俑", "西北"],
    "重庆": ["山城", "火锅", "夜景", "网红"],
    "南京": ["六朝古都", "历史", "江南", "民国"],
    "武汉": ["江城", "樱花", "热干面", "大学"],
    "长沙": ["美食", "娱乐", "烟花", "青春"],
    "厦门": ["海滨", "文艺", "鼓浪屿", "慢生活"],
    "青岛": ["海滨", "啤酒", "八大关", "海鲜"],
    "大连": ["海滨", "浪漫", "樱花", "海鲜"],
    "苏州": ["园林", "江南水乡", "古镇", "丝绸"],
    "天津": ["历史", "美食", "洋楼", "相声"],
    "昆明": ["春城", "四季如春", "石林", "民族"],
    "丽江": ["古城", "雪山", "古镇", "文艺"],
    "三亚": ["海滨", "度假", "热带", "潜水"],
    "桂林": ["山水", "漓江", "喀斯特", "田园"],
}

CITY_BEST_SEASON = {
    "北京": ["春秋(3-5月,9-11月)"],
    "上海": ["春秋(3-5月,9-11月)"],
    "广州": ["秋冬(10月-次年3月)"],
    "深圳": ["秋冬(10月-次年3月)"],
    "杭州": ["春秋(3-5月,9-11月)"],
    "成都": ["春秋(3-6月,9-11月)"],
    "西安": ["春秋(3-5月,9-11月)"],
    "重庆": ["春秋(3-5月,9-11月)"],
    "南京": ["春秋(3-5月,9-11月)"],
    "武汉": ["春秋(3-5月,9-11月)"],
    "长沙": ["春秋(3-5月,9-11月)"],
    "厦门": ["秋冬(10月-次年4月)"],
    "青岛": ["夏季(6-9月)"],
    "大连": ["夏季(6-9月)"],
    "苏州": ["春秋(3-5月,9-11月)"],
    "天津": ["春秋(3-5月,9-11月)"],
    "昆明": ["全年"],
    "丽江": ["春秋(3-5月,9-11月)"],
    "三亚": ["冬季(10月-次年4月)"],
    "桂林": ["春秋(3-5月,9-11月)"],
}


async def compare_cities(cities: list) -> dict:
    if len(cities) < 2:
        return {"success": False, "message": "请至少选择2个城市进行比较"}
    if len(cities) > 4:
        return {"success": False, "message": "最多比较4个城市"}
    
    city_data = []
    tasks = [_fetch_city_info(city) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        city = cities[i]
        if isinstance(result, Exception):
            city_data.append(_get_default_city_data(city))
        else:
            city_data.append(result)
    
    comparison = _build_comparison(city_data, cities)
    
    return {
        "success": True,
        "cities": city_data,
        "comparison": comparison,
        "recommendation": _generate_recommendation(city_data, cities)
    }


async def _fetch_city_info(city: str) -> dict:
    geo, attractions, foods, hotels, forecast = await asyncio.gather(
        geocode_city(city),
        search_attractions(city, limit=20),
        search_foods(city, limit=20),
        search_hotels(city, limit=15),
        get_weather_forecast(city),
        return_exceptions=True
    )
    
    if isinstance(geo, Exception):
        geo = None
    if isinstance(attractions, Exception):
        attractions = []
    if isinstance(foods, Exception):
        foods = []
    if isinstance(hotels, Exception):
        hotels = []
    if isinstance(forecast, Exception):
        forecast = None
    
    avg_attraction_rating = sum(a.get("rating", 0) for a in attractions) / max(1, len(attractions))
    avg_food_rating = sum(f.get("rating", 0) for f in foods) / max(1, len(foods))
    avg_hotel_rating = sum(h.get("rating", 0) for h in hotels) / max(1, len(hotels))
    
    hotel_prices = [h.get("cost", 0) for h in hotels if h.get("cost", 0) > 0]
    avg_hotel_price = sum(hotel_prices) / max(1, len(hotel_prices)) if hotel_prices else 0
    
    food_prices = [f.get("cost", 0) for f in foods if f.get("cost", 0) > 0]
    avg_food_price = sum(food_prices) / max(1, len(food_prices)) if food_prices else 0
    
    best_temp = None
    if forecast and forecast.get("forecast"):
        temps = [float(d.get("daytemp", 25)) for d in forecast["forecast"]]
        best_temp = round(sum(temps) / len(temps), 1) if temps else None
    
    return {
        "name": city,
        "tags": CITY_TAGS.get(city, []),
        "best_season": CITY_BEST_SEASON.get(city, []),
        "geo": geo,
        "stats": {
            "attraction_count": len([a for a in attractions if a.get("rating", 0) > 0]),
            "food_count": len([f for f in foods if f.get("rating", 0) > 0]),
            "hotel_count": len([h for h in hotels if h.get("rating", 0) > 0]),
            "avg_attraction_rating": round(avg_attraction_rating, 2),
            "avg_food_rating": round(avg_food_rating, 2),
            "avg_hotel_rating": round(avg_hotel_rating, 2),
            "avg_hotel_price": round(avg_hotel_price, 0),
            "avg_food_price": round(avg_food_price, 0),
        },
        "weather": {
            "current": forecast.get("current") if forecast else None,
            "best_temp": best_temp,
            "rain_days_7d": len(forecast.get("rain_alert", {}).get("rainy_days", [])) if forecast else 0,
        },
        "total_score": _calculate_total_score(
            avg_attraction_rating, avg_food_rating, avg_hotel_rating,
            avg_hotel_price, best_temp, city
        ),
    }


def _get_default_city_data(city: str) -> dict:
    return {
        "name": city,
        "tags": CITY_TAGS.get(city, []),
        "best_season": CITY_BEST_SEASON.get(city, []),
        "geo": None,
        "stats": {
            "attraction_count": 0,
            "food_count": 0,
            "hotel_count": 0,
            "avg_attraction_rating": 0,
            "avg_food_rating": 0,
            "avg_hotel_rating": 0,
            "avg_hotel_price": 0,
            "avg_food_price": 0,
        },
        "weather": {
            "current": None,
            "best_temp": None,
            "rain_days_7d": 0,
        },
        "total_score": 0,
    }


def _calculate_total_score(attr_rating, food_rating, hotel_rating, hotel_price, best_temp, city):
    score = 0
    
    score += attr_rating * 20
    score += food_rating * 15
    score += hotel_rating * 10
    
    if hotel_price > 0 and hotel_price <= 300:
        score += 20
    elif hotel_price <= 500:
        score += 15
    elif hotel_price <= 800:
        score += 10
    else:
        score += 5
    
    if best_temp and 18 <= best_temp <= 28:
        score += 20
    elif best_temp and (10 <= best_temp < 18 or 28 < best_temp <= 32):
        score += 10
    
    score += len(CITY_TAGS.get(city, [])) * 2
    
    return round(score, 1)


def _build_comparison(city_data, cities):
    dimensions = [
        {"key": "stats.attraction_count", "label": "景点数量", "type": "number"},
        {"key": "stats.avg_attraction_rating", "label": "景点评分", "type": "rating"},
        {"key": "stats.food_count", "label": "美食数量", "type": "number"},
        {"key": "stats.avg_food_rating", "label": "美食评分", "type": "rating"},
        {"key": "stats.avg_food_price", "label": "人均消费", "type": "price", "lower_better": True},
        {"key": "stats.avg_hotel_rating", "label": "酒店评分", "type": "rating"},
        {"key": "stats.avg_hotel_price", "label": "酒店均价", "type": "price", "lower_better": True},
        {"key": "weather.best_temp", "label": "平均气温", "type": "temp"},
        {"key": "weather.rain_days_7d", "label": "7天雨日", "type": "number", "lower_better": True},
        {"key": "total_score", "label": "综合评分", "type": "score"},
    ]
    
    comparison = {"dimensions": []}
    
    for dim in dimensions:
        values = []
        for data in city_data:
            keys = dim["key"].split(".")
            val = data
            for k in keys:
                val = val.get(k, 0) if isinstance(val, dict) else 0
            if val is None:
                val = 0
            values.append(val)
        
        if dim.get("lower_better"):
            winner_idx = values.index(min(values)) if all(v > 0 for v in values) else -1
        else:
            winner_idx = values.index(max(values)) if any(v > 0 for v in values) else -1
        
        comparison["dimensions"].append({
            "label": dim["label"],
            "type": dim["type"],
            "values": [{"city": cities[i], "value": values[i], "is_winner": i == winner_idx} for i in range(len(cities))],
        })
    
    return comparison


def _generate_recommendation(city_data, cities):
    if not city_data:
        return []
    
    sorted_data = sorted(city_data, key=lambda x: x.get("total_score", 0), reverse=True)
    
    recommendations = []
    for i, data in enumerate(sorted_data):
        rank = i + 1
        strengths = []
        
        if data["stats"]["avg_attraction_rating"] >= 4.5:
            strengths.append("景点质量高")
        if data["stats"]["avg_food_rating"] >= 4.5:
            strengths.append("美食出色")
        if data["stats"]["avg_hotel_rating"] >= 4.5:
            strengths.append("住宿优质")
        if data["stats"]["avg_hotel_price"] > 0 and data["stats"]["avg_hotel_price"] <= 400:
            strengths.append("性价比高")
        if data["weather"]["best_temp"] and 20 <= data["weather"]["best_temp"] <= 26:
            strengths.append("气候宜人")
        if len(data.get("tags", [])) >= 3:
            strengths.append("特色鲜明")
        
        best_season = data.get("best_season", ["四季皆宜"])
        if isinstance(best_season, list) and len(best_season) > 0:
            season = best_season[0]
        else:
            season = "四季皆宜"
        
        recommendations.append({
            "rank": rank,
            "city": data["name"],
            "score": data.get("total_score", 0),
            "tags": data.get("tags", [])[:4],
            "best_season": season,
            "strengths": strengths[:3] or ["综合表现均衡"],
        })
    
    return recommendations
