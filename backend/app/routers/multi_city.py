from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.multi_city_service import (
    generate_multi_city_itinerary, 
    get_train_info, 
    generate_city_data,
    get_city_all_attractions,
    get_city_all_food,
    get_city_info_data,
    fetch_city_real_data,
    generate_full_day_plan
)
from app.services.city_database import (
    CITY_BASIC_INFO, MASS_CITY_INFO, MEGA_CITY_INFO,
    EXTENDED_CITY_BASIC_INFO, ALL_CITY_COORDS
)
from app.services.complete_city_data import ALL_CITIES_BASIC

router = APIRouter(prefix="/multi-city", tags=["多城市游玩"])


class CityInfo(BaseModel):
    name: str
    days: int


class MultiCityRequest(BaseModel):
    cities: List[str]
    day_allocation: Optional[List[int]] = None
    total_days: int
    budget: float
    preference: str = ""
    user_attractions: Optional[Dict[str, List[str]]] = None


@router.post("/generate", summary="生成多城市详细行程")
async def generate_multi_city(request: MultiCityRequest):
    if len(request.cities) < 2:
        raise HTTPException(status_code=400, detail="至少需要2个城市")
    
    day_allocation = request.day_allocation
    if not day_allocation:
        remaining = request.total_days
        n = len(request.cities)
        day_allocation = [remaining // n] * n
        day_allocation[0] += remaining % n
    
    result = await generate_multi_city_itinerary(
        cities=request.cities,
        day_allocation=day_allocation,
        total_days=request.total_days,
        budget=request.budget,
        preference=request.preference,
        user_attractions=request.user_attractions
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "生成失败"))
    
    return result


@router.get("/cities", summary="获取支持的城市列表")
async def get_supported_cities():
    all_city_names = set()
    all_city_names.update(CITY_BASIC_INFO.keys())
    all_city_names.update(MASS_CITY_INFO.keys())
    all_city_names.update(MEGA_CITY_INFO.keys())
    all_city_names.update(EXTENDED_CITY_BASIC_INFO.keys())
    all_city_names.update(ALL_CITY_COORDS.keys())
    all_city_names.update(ALL_CITIES_BASIC.keys())
    
    all_city_names = sorted(all_city_names)
    
    cities_data = []
    for city_name in all_city_names:
        city_info = {}
        if city_name in ALL_CITIES_BASIC:
            city_info = ALL_CITIES_BASIC[city_name]
        elif city_name in CITY_BASIC_INFO:
            city_info = CITY_BASIC_INFO[city_name]
        elif city_name in MASS_CITY_INFO:
            city_info = MASS_CITY_INFO[city_name]
        elif city_name in MEGA_CITY_INFO:
            city_info = MEGA_CITY_INFO[city_name]
        elif city_name in EXTENDED_CITY_BASIC_INFO:
            city_info = EXTENDED_CITY_BASIC_INFO[city_name]
        
        cities_data.append({
            "name": city_name,
            "province": city_info.get("province", ""),
            "rating": city_info.get("rating", 0),
            "has_highlight": bool(city_info.get("highlights", "")),
            "highlights": str(city_info.get("highlights", ""))[:50],
            "coords": ALL_CITY_COORDS.get(city_name, [0, 0])
        })
    
    return {
        "success": True,
        "cities": cities_data,
        "total": len(cities_data)
    }


@router.get("/city-attractions/{city}", summary="获取城市的景点列表")
async def get_city_attractions(city: str):
    attractions = get_city_all_attractions(city)
    foods = get_city_all_food(city)
    
    if not attractions and city not in ALL_CITY_COORDS:
        return {"success": False, "message": f"未找到城市 {city} 的景点数据"}
    
    return {
        "success": True,
        "city": city,
        "attractions": attractions,
        "foods": foods,
        "total_attractions": len(attractions),
        "total_foods": len(foods)
    }


@router.get("/train-info/{from_city}/{to_city}", summary="获取两城市间的高铁信息")
async def get_train_info_route(from_city: str, to_city: str):
    train = get_train_info(from_city, to_city)
    return {
        "success": True,
        "from": from_city,
        "to": to_city,
        "train": train
    }


@router.post("/quick-plan", summary="快速生成多城市行程 (简化版)")
async def quick_plan(request: MultiCityRequest):
    if len(request.cities) < 2:
        raise HTTPException(status_code=400, detail="至少需要2个城市")
    
    day_allocation = request.day_allocation
    if not day_allocation:
        remaining = request.total_days
        n = len(request.cities)
        day_allocation = [max(1, remaining // n)] * n
        extra = remaining - sum(day_allocation)
        day_allocation[0] += extra
    
    result = await generate_multi_city_itinerary(
        cities=request.cities,
        day_allocation=day_allocation,
        total_days=request.total_days,
        budget=request.budget,
        preference=request.preference,
        user_attractions=request.user_attractions
    )
    
    return result


@router.get("/city-detail/{city}", summary="获取城市详情")
async def get_city_detail_multi(city: str):
    city_data = generate_city_data(city)
    
    if not city_data:
        return {"success": False, "message": f"无法生成城市 {city} 的数据"}
    
    return {
        "success": True,
        "city": city,
        "data": city_data
    }


@router.get("/real-poi/{city}", summary="获取城市真实POI数据(来自高德地图)")
async def get_real_poi(city: str):
    """
    从高德地图获取城市的真实景点和美食数据
    """
    try:
        real_data = await fetch_city_real_data(city)
        
        if real_data and real_data.get('attractions'):
            return {
                "success": True,
                "city": city,
                "source": "amap",
                "attractions": real_data.get('attractions', []),
                "foods": real_data.get('food', []),
                "transport": real_data.get('transport', ''),
                "tips": real_data.get('tips', ''),
                "total_attractions": len(real_data.get('attractions', [])),
                "total_foods": len(real_data.get('food', []))
            }
        else:
            static_data = get_city_info_data(city)
            return {
                "success": True,
                "city": city,
                "source": "static",
                "attractions": static_data.get('attractions', []),
                "foods": static_data.get('food', []),
                "transport": static_data.get('transport', ''),
                "tips": static_data.get('tips', ''),
                "total_attractions": len(static_data.get('attractions', [])),
                "total_foods": len(static_data.get('food', []))
            }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "city": city,
            "error": str(e),
            "message": f"获取真实数据失败: {str(e)}"
        }


class ModifyDayRequest(BaseModel):
    itinerary: dict
    day_index: int
    action: str
    params: dict = {}


@router.post("/modify-day", summary="修改某天的行程")
async def modify_day_itinerary(request: ModifyDayRequest):
    """
    修改某天的行程
    action: 
    - swap_attraction: 替换某个景点
    - remove_attraction: 删除某个景点
    - add_attraction: 添加一个景点
    - regenerate: 重新生成某天
    - adjust_time: 调整时间
    """
    try:
        itinerary = request.itinerary
        day_index = request.day_index
        action = request.action
        params = request.params
        
        if day_index < 0 or day_index >= len(itinerary.get("days", [])):
            return {"success": False, "message": "无效的天数索引"}
        
        day = itinerary["days"][day_index]
        city = day.get("city", "")
        
        if action == "swap_attraction":
            old_name = params.get("old_attraction", "")
            new_name = params.get("new_attraction", "")
            
            if not old_name or not new_name:
                return {"success": False, "message": "需要提供旧景点和新景点名称"}
            
            for item in day.get("schedule", []):
                if item.get("name") == old_name and item.get("type") == "attraction":
                    from app.services.enhanced_schedule import enrich_attraction_info
                    new_details = enrich_attraction_info(new_name)
                    
                    item["name"] = new_name
                    item["description"] = new_details.get("description", "")
                    item["best_visit_time"] = new_details.get("best_time", "")
                    item["visit_duration"] = new_details.get("visit_duration", "")
                    item["open_hours"] = new_details.get("open_hours", "")
                    item["tips"] = new_details.get("tips", item.get("tips", ""))
                    
                    return {"success": True, "message": f"已将 {old_name} 替换为 {new_name}", "day": day}
            
            return {"success": False, "message": f"未找到景点 {old_name}"}
        
        elif action == "remove_attraction":
            target_name = params.get("attraction", "")
            
            new_schedule = [item for item in day.get("schedule", []) 
                          if not (item.get("name") == target_name and item.get("type") == "attraction")]
            day["schedule"] = new_schedule
            
            return {"success": True, "message": f"已删除 {target_name}", "day": day}
        
        elif action == "regenerate":
            user_selected = params.get("selected_attractions", [])
            new_day = generate_full_day_plan(city, day_index + 1, user_selected)
            
            if new_day:
                itinerary["days"][day_index] = new_day
                return {"success": True, "message": "已重新生成该天行程", "day": new_day}
            
            return {"success": False, "message": "重新生成失败"}
        
        elif action == "adjust_time":
            target_name = params.get("item_name", "")
            new_start = params.get("new_start_time", "")
            new_end = params.get("new_end_time", "")
            
            for item in day.get("schedule", []):
                if item.get("name") == target_name:
                    if new_start:
                        item["start_time"] = new_start
                    if new_end:
                        item["end_time"] = new_end
                    
                    if new_start and new_end:
                        start_h, start_m = map(int, new_start.split(":"))
                        end_h, end_m = map(int, new_end.split(":"))
                        duration = (end_h * 60 + end_m) - (start_h * 60 + start_m)
                        if duration > 0:
                            item["duration_minutes"] = duration
                    
                    return {"success": True, "message": f"已调整 {target_name} 的时间", "day": day}
            
            return {"success": False, "message": f"未找到 {target_name}"}
        
        else:
            return {"success": False, "message": f"未知的操作类型: {action}"}
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"修改行程失败: {str(e)}"}


@router.get("/available-attractions/{city}", summary="获取可替换的景点列表")
async def get_available_attractions_for_modify(city: str):
    """获取城市的所有景点，用于行程修改"""
    try:
        import asyncio
        from app.services.multi_city_service import fetch_city_real_data
        
        real_data = await fetch_city_real_data(city)
        
        if real_data and real_data.get("attractions"):
            attractions = [{"name": a["name"], "address": a.get("address", ""), "rating": a.get("rating", 4)} 
                          for a in real_data["attractions"]]
            return {"success": True, "attractions": attractions}
        
        from app.services.multi_city_service import get_city_all_attractions
        attractions = get_city_all_attractions(city)
        attraction_list = [{"name": a["name"], "address": a.get("address", ""), "rating": a.get("rating", 4)} 
                          for a in attractions]
        
        return {"success": True, "attractions": attraction_list}
    
    except Exception as e:
        return {"success": False, "message": f"获取景点列表失败: {str(e)}"}
