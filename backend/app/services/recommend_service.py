import asyncio
from app.services.city_database import (
    get_recommendations, get_city_info, get_destinations_count,
    CITY_COORDS, get_high_speed_routes
)
from app.services.amap_service import get_city_content_full, geocode_city


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
    
    return recommendations


async def get_city_detail(city: str, use_realtime: bool = True):
    city_info = get_city_info(city)
    tips = city_info.get("tips", {})
    
    geo = None
    if city in CITY_COORDS:
        geo = {"lng": CITY_COORDS[city][0], "lat": CITY_COORDS[city][1], "name": city}
    elif use_realtime:
        real_geo = await geocode_city(city)
        if real_geo:
            geo = {"lng": real_geo["lng"], "lat": real_geo["lat"], "name": city}
    
    high_speed_routes = get_high_speed_routes(city)
    
    result = {
        "success": True,
        "city": city_info.get("name", city),
        "info": city_info,
        "static_data": {
            "attractions": tips.get("attractions", []),
            "foods": tips.get("food", []),
            "hotels": tips.get("hotels", []),
        },
        "realtime_data": {
            "attractions": [],
            "foods": [],
            "hotels": [],
        },
        "itinerary": tips.get("itinerary_suggestion", []),
        "geo": geo,
        "description": city_info.get("description", ""),
        "tags": city_info.get("tags", []),
        "rating": city_info.get("rating", 4.5),
        "image": city_info.get("image", ""),
        "best_time": city_info.get("best_time", ""),
        "weather_tips": city_info.get("weather_tips", ""),
        "transport": city_info.get("transport", ""),
        "high_speed_routes": high_speed_routes,
        "tips": tips,
    }
    
    if geo:
        try:
            realtime = await get_city_content_full(city)
            result["realtime_data"] = realtime
            result["attractions"] = realtime.get("attractions", []) or tips.get("attractions", [])
            result["foods"] = realtime.get("foods", []) or tips.get("food", [])
            result["hotels"] = realtime.get("hotels", []) or tips.get("hotels", [])
        except Exception as e:
            result["attractions"] = tips.get("attractions", [])
            result["foods"] = tips.get("food", [])
            result["hotels"] = tips.get("hotels", [])
            result["realtime_error"] = str(e)
    else:
        result["attractions"] = tips.get("attractions", [])
        result["foods"] = tips.get("food", [])
        result["hotels"] = tips.get("hotels", [])
    
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
