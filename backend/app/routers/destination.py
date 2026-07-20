from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional, List
from app.services.amap_service import (
    search_poi, geocode_city, search_nearby,
    search_attractions, search_foods, search_hotels,
    get_city_content_full, get_nearby_content, search_city_tips, get_poi_detail
)
from app.services.recommend_service import (
    recommend_destinations, get_city_detail, get_city_realtime_only
)
from app.services.city_database import get_all_start_cities, get_destinations_count
from app.services.itinerary_generator import (
    generate_smart_itinerary, generate_multiple_itineraries, generate_from_natural_language,
    parse_natural_language
)
from app.services.compare_service import compare_cities
from app.services.luggage_service import generate_luggage_checklist
from app.services.weather_service import get_weather_forecast

router = APIRouter(prefix="/destination", tags=["目的地"])


@router.get("/recommend", summary="推荐目的地")
async def get_recommendations(
    from_city: str = Query(..., description="出发城市"),
    travel_date: str = Query(..., description="出行日期 YYYY-MM-DD"),
    max_duration: float = Query(3.0, description="最大高铁行程时间(小时)"),
    preference: str = Query("", description="偏好类型")
):
    destinations = await recommend_destinations(from_city, travel_date, max_duration, preference)
    return {"success": True, "destinations": destinations}


@router.get("/detail/{city}", summary="获取城市详情")
async def get_city_detail_endpoint(
    city: str = Path(..., description="城市名称"),
    realtime: bool = Query(True, description="是否启用高德实时数据")
):
    result = await get_city_detail(city, realtime)
    return result


@router.get("/realtime/{city}", summary="获取城市实时数据")
async def get_city_realtime_endpoint(
    city: str = Path(..., description="城市名称")
):
    result = await get_city_realtime_only(city)
    return result


@router.get("/start-cities", summary="获取所有出发城市")
async def get_start_cities():
    cities = get_all_start_cities()
    return {"success": True, "cities": cities, "count": len(cities)}


@router.get("/stats", summary="获取统计信息")
async def get_stats():
    count = get_destinations_count()
    start_cities = get_all_start_cities()
    return {
        "success": True,
        "total_destinations": count,
        "total_start_cities": len(start_cities),
        "start_cities": start_cities
    }


@router.get("/poi", summary="搜索POI")
async def get_pois(
    city: str = Query(..., description="城市名"),
    keywords: str = Query(..., description="搜索关键词"),
    types: str = Query("", description="POI类型编码"),
    offset: int = Query(20, description="返回数量")
):
    pois = await search_poi(city, keywords, types, offset)
    return {"success": True, "pois": pois}


@router.get("/nearby", summary="搜索附近POI")
async def get_nearby(
    lng: float = Query(..., description="经度"),
    lat: float = Query(..., description="纬度"),
    keywords: str = Query("", description="搜索关键词"),
    radius: int = Query(3000, description="搜索半径(米)"),
    types: str = Query("", description="POI类型编码"),
    offset: int = Query(20, description="返回数量")
):
    pois = await search_nearby(lng, lat, keywords, radius, offset, types)
    return {"success": True, "pois": pois}


@router.get("/attractions", summary="搜索景点")
async def get_attractions(
    city: str = Query(..., description="城市名"),
    keyword: str = Query("", description="关键词"),
    limit: int = Query(20, description="返回数量")
):
    attractions = await search_attractions(city, keyword, limit)
    return {"success": True, "attractions": attractions}


@router.get("/foods", summary="搜索美食")
async def get_foods(
    city: str = Query(..., description="城市名"),
    keyword: str = Query("", description="关键词"),
    limit: int = Query(20, description="返回数量")
):
    foods = await search_foods(city, keyword, limit)
    return {"success": True, "foods": foods}


@router.get("/hotels", summary="搜索酒店")
async def get_hotels(
    city: str = Query(..., description="城市名"),
    keyword: str = Query("", description="关键词"),
    limit: int = Query(20, description="返回数量")
):
    hotels = await search_hotels(city, keyword, limit)
    return {"success": True, "hotels": hotels}


@router.get("/full-content/{city}", summary="获取城市完整内容")
async def get_full_content(
    city: str = Path(..., description="城市名称")
):
    content = await get_city_content_full(city)
    return {"success": True, "city": city, **content}


@router.get("/poi-detail", summary="获取POI详情")
async def get_poi_detail_endpoint(
    poi_id: str = Query(..., description="POI ID")
):
    detail = await get_poi_detail(poi_id)
    return {"success": detail is not None, "poi": detail}


@router.get("/tips", summary="搜索POI提示")
async def get_tips(
    keywords: str = Query(..., description="搜索关键词"),
    city: str = Query("", description="城市名")
):
    tips = await search_city_tips(keywords, city)
    return {"success": True, "tips": tips}


@router.get("/geocode", summary="城市地理编码")
async def get_geocode(city: str = Query(..., description="城市名")):
    geo = await geocode_city(city)
    return {"success": geo is not None, "geo": geo}


@router.get("/weather-forecast/{city}", summary="获取7天天气预报")
async def get_weather_forecast_endpoint(
    city: str = Path(..., description="城市名称")
):
    result = await get_weather_forecast(city)
    if result:
        return {"success": True, "forecast": result}
    return {"success": False, "message": "获取天气预报失败"}


@router.post("/generate-itinerary", summary="生成智能行程")
async def generate_itinerary(
    request: dict
):
    city = request.get("city")
    days = request.get("days", 3)
    budget = request.get("budget", 3000)
    preference = request.get("preference", "")
    people = request.get("people", 2)
    
    extra_params = {
        "elderly_friendly": request.get("elderly_friendly", False),
        "easy_walk": request.get("easy_walk", False),
        "no_spicy": request.get("no_spicy", False),
        "photo_focus": request.get("photo_focus", False),
        "homestay": request.get("homestay", False),
        "near_station": request.get("near_station", False),
        "near_attraction": request.get("near_attraction", False),
        "max_walk_per_day": request.get("max_walk_per_day", 10000),
        "max_travel_time": request.get("max_travel_time", 60),
        "wake_up_time": request.get("wake_up_time", "08:00"),
        "sleep_time": request.get("sleep_time", "22:00"),
        "include_night": request.get("include_night", True),
        "is_couple": request.get("is_couple", False),
        "is_hiking": request.get("is_hiking", False),
    }
    
    if not city:
        return {"success": False, "message": "请选择目的地城市"}
    
    itinerary = await generate_smart_itinerary(city, days, budget, preference, people, **extra_params)
    return {"success": True, "city": city, "days": days, "budget": budget, "itinerary": itinerary}


@router.post("/generate-multiple", summary="生成多版本行程")
async def generate_multiple(
    request: dict
):
    city = request.get("city")
    days = request.get("days", 3)
    budget = request.get("budget", 3000)
    preference = request.get("preference", "")
    people = request.get("people", 2)
    version_count = request.get("version_count", 3)
    
    if not city:
        return {"success": False, "message": "请选择目的地城市"}
    
    result = await generate_multiple_itineraries(city, days, budget, preference, people, version_count)
    return {"success": True, "city": city, "versions": result}


@router.post("/generate-from-text", summary="自然语言生成行程")
async def generate_from_text(
    request: dict
):
    text = request.get("text", "")
    if not text:
        return {"success": False, "message": "请输入您的旅行需求"}
    
    result = await generate_from_natural_language(text)
    return result


@router.post("/parse-text", summary="解析自然语言参数")
async def parse_text(
    request: dict
):
    text = request.get("text", "")
    params = parse_natural_language(text)
    return {"success": True, "parsed_params": params}


@router.post("/compare-cities", summary="对比城市")
async def compare_cities_endpoint(
    request: dict
):
    cities = request.get("cities", [])
    if not cities or len(cities) < 2:
        return {"success": False, "message": "请至少选择2个城市"}
    
    result = await compare_cities(cities)
    return result


@router.post("/luggage-checklist", summary="生成行李清单")
async def get_luggage_checklist(
    request: dict
):
    days = request.get("days", 3)
    season = request.get("season", "")
    scenario = request.get("scenario", "")
    weather_temp = request.get("weather_temp", 20)
    has_rain = request.get("has_rain", False)
    people_count = request.get("people_count", 1)
    special_needs = request.get("special_needs", [])
    
    result = generate_luggage_checklist(
        days=days, season=season, scenario=scenario,
        weather_temp=weather_temp, has_rain=has_rain,
        people_count=people_count, special_needs=special_needs
    )
    return {"success": True, "checklist": result}
