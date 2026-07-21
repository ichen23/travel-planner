from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.multi_city_service import generate_multi_city_itinerary, get_train_info, CITY_STATIC_DATA

router = APIRouter(prefix="/multi-city", tags=["多城市行程"])


class CityInfo(BaseModel):
    name: str
    days: int


class MultiCityRequest(BaseModel):
    cities: List[str]
    day_allocation: Optional[List[int]] = None
    total_days: int
    budget: float
    preference: str = ""


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
        budget=request.budget,
        preference=request.preference
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "生成失败"))
    
    return result


@router.get("/cities", summary="获取支持的城市列表")
async def get_supported_cities():
    cities_data = []
    for city_name, data in CITY_STATIC_DATA.items():
        cities_data.append({
            "name": city_name,
            "has_attractions": len(data.get("attractions", [])),
            "has_food": len(data.get("food", [])),
            "tips": data.get("tips", "")
        })
    
    return {
        "success": True,
        "cities": cities_data,
        "total": len(cities_data)
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
        budget=request.budget,
        preference=request.preference
    )
    
    return result


@router.get("/city-detail/{city}", summary="获取城市详情")
async def get_city_detail_multi(city: str):
    city_data = CITY_STATIC_DATA.get(city)
    if not city_data:
        return {"success": False, "message": f"未找到城市 {city} 的数据"}
    
    return {
        "success": True,
        "city": city,
        "data": city_data
    }
