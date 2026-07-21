import asyncio
import random
from app.services.city_database import (
    get_recommendations, get_city_info, get_destinations_count,
    CITY_COORDS, get_high_speed_routes
)
from app.services.amap_service import get_city_content_full, geocode_city
from app.services.poi_tips import POI_TIPS


async def get_city_real_data(city: str) -> dict:
    try:
        real_content = await get_city_content_full(city)
        return real_content
    except Exception as e:
        return {"attractions": [], "foods": [], "hotels": []}


async def get_city_complete_info(city: str) -> dict:
    city_info = get_city_info(city)
    real_data = await get_city_real_data(city)
    geo = await geocode_city(city)
    
    city_pois = []
    for poi_id, poi_info in POI_TIPS.items():
        if poi_info.get('city') == city:
            city_pois.append(poi_info)
    
    static_attractions = [p.get('name', '') for p in city_pois[:5]]
    static_foods = []
    
    if real_data.get('attractions'):
        real_names = [a.get('name', '') if isinstance(a, dict) else str(a) for a in real_data['attractions'][:5]]
        attractions = real_names + static_attractions
    else:
        attractions = static_attractions
    
    if real_data.get('foods'):
        static_foods = [f.get('name', '') if isinstance(f, dict) else str(f) for f in real_data['foods'][:5]]
    
    static_hotels = []
    if real_data.get('hotels'):
        static_hotels = [h.get('name', '') if isinstance(h, dict) else str(h) for h in real_data['hotels'][:3]]
    
    return {
        "attractions": list(dict.fromkeys(attractions))[:8],
        "food": list(dict.fromkeys(static_foods))[:5],
        "hotels": list(dict.fromkeys(static_hotels))[:3],
        "geo": geo,
        "real_data": real_data,
        "static_data": city_pois,
    }


async def recommend_destinations(from_city: str, travel_date: str,
                                   max_duration_hours: float = 3, preference: str = ""):
    recommendations = get_recommendations(from_city, max_duration_hours)
    
    from app.services.beijing_3hr_data import BEIJING_3HR_COORDS
    
    for rec in recommendations:
        rec["source"] = "database"
        if rec["city"] in CITY_COORDS:
            rec["lng"] = CITY_COORDS[rec["city"]][0]
            rec["lat"] = CITY_COORDS[rec["city"]][1]
        elif rec["city"] in BEIJING_3HR_COORDS:
            rec["lng"] = BEIJING_3HR_COORDS[rec["city"]][0]
            rec["lat"] = BEIJING_3HR_COORDS[rec["city"]][1]
        
        city_info = get_city_info(rec["city"])
        rec["tags"] = city_info.get("tags", [])
        rec["image"] = city_info.get("image", "")
        rec["rating"] = city_info.get("rating", 4.5)
        rec["description"] = city_info.get("description", f"{rec['city']}是中国一座具有独特魅力的城市")
        rec["avg_daily_budget"] = city_info.get("avg_daily_budget", 400)
        rec["highlights"] = city_info.get("highlights", "")
        rec["tips"] = {"attractions": [], "food": []}

    return recommendations


async def get_city_detail(city: str, use_realtime: bool = True):
    city_info = get_city_info(city)
    
    geo = None
    province = city_info.get("province", "")
    parent = city_info.get("parent", "")
    district = city_info.get("district", "")
    
    if city in CITY_COORDS:
        geo = {"lng": CITY_COORDS[city][0], "lat": CITY_COORDS[city][1], "name": city}
    elif use_realtime:
        real_geo = await geocode_city(city)
        if real_geo:
            geo = {
                "lng": real_geo["lng"], 
                "lat": real_geo["lat"], 
                "name": real_geo.get("name", city),
                "province": real_geo.get("province", ""),
                "city": real_geo.get("city", ""),
                "district": real_geo.get("district", ""),
                "adcode": real_geo.get("adcode")
            }
            if not province and real_geo.get("province"):
                province = real_geo["province"]
            if not parent and real_geo.get("city") and real_geo["city"] != city:
                parent = real_geo["city"]
            if not district and real_geo.get("district"):
                district = real_geo["district"]
    
    high_speed_routes = get_high_speed_routes(city)
    
    realtime = None
    if use_realtime:
        try:
            realtime = await get_city_content_full(city)
        except Exception:
            pass
    
    if not realtime:
        realtime = {"attractions": [], "foods": [], "hotels": []}
    
    def to_poi_list(items, max_count=8):
        if not items:
            return []
        result = []
        for item in items[:max_count]:
            if isinstance(item, dict):
                result.append({
                    "name": item.get("name", ""),
                    "address": item.get("address", ""),
                    "lng": item.get("lng"),
                    "lat": item.get("lat"),
                    "rating": item.get("rating", 0),
                    "type": item.get("type", ""),
                    "photos": item.get("photos", []),
                })
            else:
                result.append({
                    "name": str(item),
                    "address": "",
                    "lng": None,
                    "lat": None,
                    "rating": 0,
                    "type": "",
                    "photos": [],
                })
        return result
    
    real_attractions = to_poi_list(realtime.get("attractions", []), 8)
    real_foods = to_poi_list(realtime.get("foods", []), 5)
    real_hotels = to_poi_list(realtime.get("hotels", []), 3)
    
    if not real_attractions or len(real_attractions) == 0:
        real_attractions = []
    if not real_foods or len(real_foods) == 0:
        real_foods = []
    if not real_hotels or len(real_hotels) == 0:
        real_hotels = []
    
    final_info = dict(city_info)
    if not final_info.get("province") and province:
        final_info["province"] = province
    if not final_info.get("parent") and parent:
        final_info["parent"] = parent
    if not final_info.get("district") and district:
        final_info["district"] = district
    
    full_address_parts = []
    if final_info.get("province"):
        full_address_parts.append(final_info["province"])
    if final_info.get("parent") and final_info["parent"] != final_info.get("name"):
        full_address_parts.append(final_info["parent"])
    if final_info.get("district") and final_info["district"] != final_info.get("name"):
        full_address_parts.append(final_info["district"])
    final_info["full_address"] = " ".join(full_address_parts) if full_address_parts else ""
    
    result = {
        "success": True,
        "city": final_info.get("name", city),
        "info": final_info,
        "geo": geo,
        "description": final_info.get("description", f"{city}是中国一座具有独特魅力的城市"),
        "tags": city_info.get("tags", []),
        "rating": city_info.get("rating", 4.5),
        "image": city_info.get("image", ""),
        "best_time": city_info.get("best_time", ""),
        "weather_tips": city_info.get("weather_tips", ""),
        "transport": city_info.get("transport", ""),
        "high_speed_routes": high_speed_routes,
        "itinerary": city_info.get("tips", {}).get("itinerary_suggestion", []) or [
            f"Day1: 抵达{city}，入住酒店，逛逛当地夜景",
            f"Day2: 游览{city}主要景点，品尝当地美食",
            f"Day3: 休闲购物，体验{city}生活",
        ],
        "tips": {
            "attractions": real_attractions,
            "food": real_foods,
            "hotels": real_hotels,
        },
        "attractions": real_attractions,
        "foods": real_foods,
        "hotels": real_hotels,
        "realtime_data": realtime,
    }
    
    return result


async def get_city_realtime_only(city: str):
    realtime = await get_city_content_full(city)
    geo = await geocode_city(city)
    return {
        "success": True,
        "city": city,
        "geo": geo,
        **realtime,
    }


async def get_all_cities_count():
    return {"total": get_destinations_count()}
