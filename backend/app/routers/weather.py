from fastapi import APIRouter, Query
from app.services.weather_service import get_weather
from app.services.amap_service import geocode_city

router = APIRouter(prefix="/weather", tags=["天气"])

@router.get("/current", summary="获取天气")
async def get_city_weather(city: str = Query(..., description="城市名")):
    geo = await geocode_city(city)
    if not geo or not geo.get("adcode"):
        return {"success": False, "message": "无法获取城市信息"}
    
    weather = await get_weather(geo["adcode"])
    if weather:
        return {"success": True, "weather": weather}
    return {"success": False, "message": "天气数据获取失败"}
