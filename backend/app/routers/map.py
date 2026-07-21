from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.amap_service import (
    driving_direction, transit_direction, walking_direction, 
    riding_direction, reverse_geocode, ip_location,
    get_weather, get_static_map_url, get_all_transport_modes,
    geocode_city
)

router = APIRouter(prefix="/map", tags=["地图服务"])


@router.get("/direction/driving", summary="驾车路线规划")
async def get_driving_direction(
    origin: str = Query(..., description="起点经纬度 lng,lat"),
    destination: str = Query(..., description="终点经纬度 lng,lat"),
    strategy: int = Query(32, description="策略: 32=推荐, 33=躲避拥堵, 34=高速优先")
):
    result = await driving_direction(origin, destination, strategy)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/direction/transit", summary="公交路线规划")
async def get_transit_direction(
    origin: str = Query(..., description="起点经纬度 lng,lat"),
    destination: str = Query(..., description="终点经纬度 lng,lat"),
    city: str = Query(..., description="城市名称或adcode"),
    strategy: int = Query(0, description="策略: 0=推荐, 1=最少换乘, 2=最少步行")
):
    result = await transit_direction(origin, destination, city, strategy)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/direction/walking", summary="步行路线规划")
async def get_walking_direction(
    origin: str = Query(..., description="起点经纬度 lng,lat"),
    destination: str = Query(..., description="终点经纬度 lng,lat")
):
    result = await walking_direction(origin, destination)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/direction/riding", summary="骑行路线规划")
async def get_riding_direction(
    origin: str = Query(..., description="起点经纬度 lng,lat"),
    destination: str = Query(..., description="终点经纬度 lng,lat")
):
    result = await riding_direction(origin, destination)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/direction/all", summary="所有交通方式路线规划")
async def get_all_directions(
    origin: str = Query(..., description="起点经纬度 lng,lat"),
    destination: str = Query(..., description="终点经纬度 lng,lat"),
    city: str = Query("", description="城市名称(用于公交规划)")
):
    result = await get_all_transport_modes(origin, destination, city)
    return result


@router.get("/reverse-geocode", summary="逆地理编码(经纬度转地址)")
async def get_reverse_geocode(
    lng: float = Query(..., description="经度"),
    lat: float = Query(..., description="纬度")
):
    result = await reverse_geocode(lng, lat)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/ip-location", summary="IP定位")
async def get_ip_location(
    ip: str = Query("", description="IP地址(留空使用服务器IP)")
):
    result = await ip_location(ip)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


@router.get("/weather", summary="获取天气")
async def get_weather_info(
    city: str = Query("", description="城市名称"),
    adcode: str = Query("", description="行政区划代码")
):
    if not adcode and city:
        geo = await geocode_city(city)
        if geo:
            adcode = geo.get("adcode", "")
    
    if not adcode:
        raise HTTPException(status_code=400, detail="需要提供城市名称或adcode")
    
    result = await get_weather(adcode)
    if not result.get("status"):
        raise HTTPException(status_code=400, detail="获取天气失败")
    return result


@router.get("/static-map", summary="获取静态地图URL")
async def get_static_map(
    lng: float = Query(..., description="中心经度"),
    lat: float = Query(..., description="中心纬度"),
    zoom: int = Query(11, description="缩放级别 1-18"),
    width: int = Query(750, description="宽度(px)"),
    height: int = Query(400, description="高度(px)"),
    markers: str = Query("", description="标注点"),
    paths: str = Query("", description="路径")
):
    url = get_static_map_url(lng, lat, zoom, width, height, markers, paths)
    return {"url": url}


@router.get("/route-compare", summary="路线对比(多种交通方式)")
async def compare_routes(
    from_city: str = Query(..., description="出发城市"),
    to_city: str = Query(..., description="目的城市"),
    transport_types: str = Query("driving,transit,walking", description="交通方式(driving,transit,walking,riding)")
):
    from app.services.train_service import get_train_info
    from_city_geo = await geocode_city(from_city)
    to_city_geo = await geocode_city(to_city)
    
    if not from_city_geo or not to_city_geo:
        raise HTTPException(status_code=400, detail="无法定位城市")
    
    origin = f"{from_city_geo['lng']},{from_city_geo['lat']}"
    destination = f"{to_city_geo['lng']},{to_city_geo['lat']}"
    types = transport_types.split(",")
    
    result = {
        "from": {"name": from_city, "geo": from_city_geo},
        "to": {"name": to_city, "geo": to_city_geo},
        "routes": {}
    }
    
    if "driving" in types:
        result["routes"]["driving"] = await driving_direction(origin, destination)
    
    if "transit" in types:
        result["routes"]["transit"] = await transit_direction(origin, destination, from_city)
    
    if "walking" in types:
        result["routes"]["walking"] = await walking_direction(origin, destination)
    
    if "riding" in types:
        result["routes"]["riding"] = await riding_direction(origin, destination)
    
    train_info = get_train_info(from_city, to_city)
    if train_info:
        result["routes"]["train"] = {
            "status": True,
            "train_number": train_info.get("train_number"),
            "duration_min": train_info.get("duration_min"),
            "price": train_info.get("price"),
            "train_type": train_info.get("type_name", "高铁")
        }
    
    return result
