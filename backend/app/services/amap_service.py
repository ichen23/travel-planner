import httpx
import logging
import os
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

AMAP_POI_URL = "https://restapi.amap.com/v3/place/text"
AMAP_POI_DETAIL_URL = "https://restapi.amap.com/v3/place/detail"
AMAP_NEARBY_URL = "https://restapi.amap.com/v3/place/around"
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
AMAP_DISTRICT_URL = "https://restapi.amap.com/v3/config/district"
AMAP_TIP_URL = "https://restapi.amap.com/v3/assistant/inputtips"

_cache = {}
_CACHE_TTL = 3600
_cache_lock = asyncio.Lock()

def _get_cache(key):
    if key in _cache:
        entry = _cache[key]
        if time.time() - entry['time'] < _CACHE_TTL:
            return entry['data']
    return None

def _set_cache(key, data):
    _cache[key] = {'data': data, 'time': time.time()}

def clear_cache():
    global _cache
    _cache = {}
    logger.info("Cache cleared")


async def _make_request(url: str, params: dict) -> dict:
    amap_key = os.environ.get('AMAP_KEY', '')
    if not amap_key:
        logger.error("AMAP_KEY is not configured")
        return {"status": "0", "info": "AMAP_KEY not configured"}
    
    params["key"] = amap_key
    params["output"] = "JSON"
    params.setdefault("extensions", "all")
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            result = resp.json()
            if result.get("status") != "1":
                logger.warning(f"Amap API error: {result.get('info')}, url: {url}")
            return result
    except Exception as e:
        logger.error(f"Amap API request failed: {str(e)}")
        return {"status": "0", "info": str(e)}


def _parse_poi(poi: dict) -> dict:
    location = poi.get("location", "")
    parts = location.split(",") if location else ["", ""]
    try:
        lng = float(parts[0]) if parts[0] else None
        lat = float(parts[1]) if parts[1] else None
    except ValueError:
        lng, lat = None, None
    biz = poi.get("biz_ext") or {}
    try:
        rating = float(biz.get("rating", 0) or 0) if biz else 0
    except (ValueError, TypeError):
        rating = 0
    try:
        cost = float(biz.get("cost", 0) or 0) if biz else 0
    except (ValueError, TypeError):
        cost = 0
    photos = [p.get("url", "") for p in (poi.get("photos") or []) if p.get("url")]
    return {
        "id": poi.get("id"),
        "name": poi.get("name", ""),
        "address": poi.get("address") or f"{poi.get('pname', '')}{poi.get('cityname', '')}{poi.get('adname', '')}",
        "lng": lng,
        "lat": lat,
        "type": poi.get("type", ""),
        "tel": poi.get("tel", ""),
        "rating": rating,
        "cost": cost,
        "open_time": biz.get("open_time", "") if biz else "",
        "photos": photos,
        "adcode": poi.get("adcode"),
        "cityname": poi.get("cityname", ""),
        "area": poi.get("area", ""),
    }


async def geocode_city(city_name: str):
    cache_key = f"geocode:{city_name}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    data = await _make_request(AMAP_GEOCODE_URL, {"address": city_name})
    if data.get("status") == "1" and data.get("geocodes"):
        geo = data["geocodes"][0]
        lng, lat = geo["location"].split(",")
        result = {"name": geo["formatted_address"], "lng": float(lng), "lat": float(lat),
                  "adcode": geo.get("adcode"), "province": geo.get("province"),
                  "city": geo.get("city"), "district": geo.get("district")}
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, None)
    return None


async def search_poi(city: str, keywords: str, types: str = "", offset: int = 20) -> list:
    cache_key = f"poi:{city}:{keywords}:{types}:{offset}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    geo = await geocode_city(city)
    
    if geo:
        search_keywords = keywords
        district = geo.get("district", "")
        city_name = geo.get("city") or city
        
        if district and district != city_name:
            search_keywords = f"{district}{keywords}"
        
        params = {"keywords": search_keywords, "city": city_name, "citylimit": "true", "offset": offset, "page": 1}
        if types:
            params["types"] = types
        data = await _make_request(AMAP_POI_URL, params)
        
        if data.get("status") == "1" and data.get("pois"):
            result = [_parse_poi(p) for p in data.get("pois", [])]
            if district and district != city_name:
                filtered = [p for p in result if district in p.get("address", "") or district in p.get("name", "")]
                if filtered:
                    result = filtered
            _set_cache(cache_key, result)
            return result
        
        if geo.get("lng") and geo.get("lat"):
            nearby_radius = 5000 if district and district != city_name else 10000
            nearby = await search_nearby(geo["lng"], geo["lat"], keywords, nearby_radius, offset, types)
            if nearby:
                _set_cache(cache_key, nearby)
                return nearby
    
    params = {"keywords": keywords, "city": city, "citylimit": "true", "offset": offset, "page": 1}
    if types:
        params["types"] = types
    data = await _make_request(AMAP_POI_URL, params)
    if data.get("status") == "1":
        result = [_parse_poi(p) for p in data.get("pois", [])]
        _set_cache(cache_key, result)
        return result
    
    _set_cache(cache_key, [])
    return []


async def search_nearby(lng: float, lat: float, keywords: str = "",
                        radius: int = 3000, offset: int = 20, types: str = "") -> list:
    params = {"location": f"{lng},{lat}", "radius": radius, "offset": offset, "page": 1}
    if keywords:
        params["keywords"] = keywords
    if types:
        params["types"] = types
    data = await _make_request(AMAP_NEARBY_URL, params)
    if data.get("status") != "1":
        return []
    return [_parse_poi(p) for p in data.get("pois", [])]


async def get_poi_detail(poi_id: str):
    from app.services.poi_tips import get_poi_tips
    data = await _make_request(AMAP_POI_DETAIL_URL, {"id": poi_id})
    if data.get("status") == "1" and data.get("pois"):
        poi = _parse_poi(data["pois"][0])
        tips = get_poi_tips(poi_id, poi.get("name", ""))
        if tips:
            poi["tips"] = tips.get("tips", [])
            poi["tickets"] = tips.get("tickets", [])
            poi["best_time"] = tips.get("best_time", "")
            poi["transport"] = tips.get("transport", "")
            poi["photos_hint"] = tips.get("photos_hint", "")
        else:
            poi["tips"] = []
            poi["tickets"] = []
            poi["best_time"] = ""
            poi["transport"] = ""
            poi["photos_hint"] = ""
        return poi
    return None


async def search_attractions(city: str, keyword: str = "", limit: int = 20) -> list:
    if keyword:
        return await search_poi(city, keyword, "", limit)
    return await search_poi(city, "景点", "风景名胜", limit)


async def search_foods(city: str, keyword: str = "", limit: int = 20) -> list:
    if keyword:
        return await search_poi(city, keyword, "", limit)
    return await search_poi(city, "美食", "餐饮服务", limit)


async def search_hotels(city: str, keyword: str = "", limit: int = 20) -> list:
    if keyword:
        return await search_poi(city, keyword, "", limit)
    return await search_poi(city, "酒店", "住宿服务", limit)


async def get_city_hot_content(city: str) -> dict:
    return await get_city_content_full(city)


async def get_city_content_full(city: str) -> dict:
    cache_key = f"city_content:{city}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    import asyncio
    attractions, foods, hotels = await asyncio.gather(
        search_attractions(city, limit=15),
        search_foods(city, limit=15),
        search_hotels(city, limit=10),
        return_exceptions=True
    )
    if isinstance(attractions, Exception):
        attractions = []
    if isinstance(foods, Exception):
        foods = []
    if isinstance(hotels, Exception):
        hotels = []
    
    if not attractions and not foods:
        geo = await geocode_city(city)
        if geo:
            nearby = await get_nearby_content(geo["lng"], geo["lat"], 10000)
            if not attractions:
                attractions = nearby["attractions"]
            if not foods:
                foods = nearby["foods"]
            if not hotels:
                hotels = nearby["hotels"]
    
    result = {
        "attractions": sorted([a for a in attractions if a.get("rating", 0) > 0],
                              key=lambda x: x.get("rating", 0), reverse=True),
        "foods": sorted([f for f in foods if f.get("rating", 0) > 0],
                       key=lambda x: x.get("rating", 0), reverse=True),
        "hotels": sorted([h for h in hotels if h.get("rating", 0) > 0],
                        key=lambda x: x.get("rating", 0), reverse=True),
    }
    _set_cache(cache_key, result)
    return result


async def get_nearby_content(lng: float, lat: float, radius: int = 3000) -> dict:
    import asyncio
    attractions, foods, hotels = await asyncio.gather(
        search_nearby(lng, lat, "景点", radius, 10, "风景名胜"),
        search_nearby(lng, lat, "美食", radius, 10, "餐饮服务"),
        search_nearby(lng, lat, "酒店", radius, 8, "住宿服务"),
        return_exceptions=True
    )
    if isinstance(attractions, Exception):
        attractions = []
    if isinstance(foods, Exception):
        foods = []
    if isinstance(hotels, Exception):
        hotels = []
    return {"attractions": attractions, "foods": foods, "hotels": hotels}


async def search_city_tips(keywords: str, city: str = "") -> list:
    params = {"keywords": keywords, "type": "poi"}
    if city:
        params["city"] = city
    data = await _make_request(AMAP_TIP_URL, params)
    if data.get("status") != "1":
        return []
    tips = []
    for tip in data.get("tips", []):
        loc = tip.get("location", "")
        lng, lat = (loc.split(",") + ["", ""])[:2] if loc else ["", ""]
        tips.append({
            "name": tip.get("name", ""), "address": tip.get("address", ""),
            "lng": float(lng) if lng else None, "lat": float(lat) if lat else None,
            "district": tip.get("district", ""),
        })
    return tips


async def get_city_districts(city_name: str):
    data = await _make_request(AMAP_DISTRICT_URL, {"keywords": city_name, "subdistrict": 0})
    if data.get("status") == "1" and data.get("districts"):
        return data["districts"][0]
    return None


async def get_city_adcode(city_name: str):
    district = await get_city_districts(city_name)
    if district:
        return district.get("adcode")
    return None


AMAP_DIRECTION_DRIVING_URL = "https://restapi.amap.com/v3/direction/driving"
AMAP_DIRECTION_TRANSIT_URL = "https://restapi.amap.com/v3/direction/transit/integrated"
AMAP_DIRECTION_WALKING_URL = "https://restapi.amap.com/v3/direction/walking"
AMAP_DIRECTION_RIDING_URL = "https://restapi.amap.com/v4/direction/bicycling"
AMAP_GEOCODE_REVERSE_URL = "https://restapi.amap.com/v3/geocode/regeo"
AMAP_IP_URL = "https://restapi.amap.com/v3/ip"
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"


async def driving_direction(origin: str, destination: str, strategy: int = 32) -> dict:
    """
    驾车路线规划
    origin: 起点经纬度 "lng,lat"
    destination: 终点经纬度 "lng,lat"
    strategy: 路线策略 (32=高德推荐, 33=躲避拥堵, 34=高速优先, 35=不走高速)
    """
    cache_key = f"driving:{origin}:{destination}:{strategy}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {
        "origin": origin,
        "destination": destination,
        "strategy": strategy,
        "extensions": "base"
    }
    data = await _make_request(AMAP_DIRECTION_DRIVING_URL, params)
    if data.get("status") == "1":
        route = data.get("route", {})
        paths = route.get("paths", [])
        result = {
            "status": True,
            "paths": [{
                "distance": float(p.get("distance", 0)),
                "duration": float(p.get("duration", 0)),
                "tolls": float(p.get("tolls", 0)),
                "toll_distance": float(p.get("toll_distance", 0)),
                "steps_count": len(p.get("steps", [])),
                "polyline": p.get("polyline", "")
            } for p in paths] if paths else [],
            "total_distance": float(route.get("distance", 0)) if route.get("distance") else 0,
            "taxi_cost": float(route.get("taxi_cost", 0)) if route.get("taxi_cost") else 0
        }
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, {"status": False, "message": data.get("info")})
    return {"status": False, "message": data.get("info")}


async def transit_direction(origin: str, destination: str, city: str, 
                             strategy: int = 0) -> dict:
    """
    公交路线规划
    origin: 起点经纬度 "lng,lat"
    destination: 终点经纬度 "lng,lat"
    city: 城市名称或adcode
    strategy: 0=推荐, 1=最少换乘, 2=最少步行, 3=最快捷
    """
    cache_key = f"transit:{origin}:{destination}:{city}:{strategy}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {
        "origin": origin,
        "destination": destination,
        "city": city,
        "strategy": strategy
    }
    data = await _make_request(AMAP_DIRECTION_TRANSIT_URL, params)
    if data.get("status") == "1":
        route = data.get("route", {})
        result = {
            "status": True,
            "transits": []
        }
        transits = route.get("transits", []) or []
        for transit in transits:
            segments = transit.get("segments", []) or []
            lines = []
            for seg in segments:
                bus_info = seg.get("bus", {}) or {}
                buslines = bus_info.get("buslines", []) or []
                for line in buslines:
                    lines.append({
                        "name": line.get("name"),
                        "type": line.get("type"),
                        "station_count": line.get("station_num"),
                        "departure_stop": (line.get("departure_stop") or {}).get("name"),
                        "arrival_stop": (line.get("arrival_stop") or {}).get("name")
                    })
            result["transits"].append({
                "duration": transit.get("duration"),
                "distance": transit.get("distance"),
                "fare": transit.get("fare"),
                "lines": lines
            })
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, {"status": False, "message": data.get("info")})
    return {"status": False, "message": data.get("info")}


async def walking_direction(origin: str, destination: str) -> dict:
    """
    步行路线规划
    origin: 起点经纬度 "lng,lat"
    destination: 终点经纬度 "lng,lat"
    """
    cache_key = f"walking:{origin}:{destination}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {
        "origin": origin,
        "destination": destination
    }
    data = await _make_request(AMAP_DIRECTION_WALKING_URL, params)
    if data.get("status") == "1":
        paths = data.get("route", {}).get("paths", [])
        result = {
            "status": True,
            "paths": [{
                "distance": float(p.get("distance", 0)),
                "duration": float(p.get("duration", 0)),
                "steps_count": len(p.get("steps", []))
            } for p in paths]
        }
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, {"status": False, "message": data.get("info")})
    return {"status": False, "message": data.get("info")}


async def riding_direction(origin: str, destination: str) -> dict:
    """
    骑行路线规划
    origin: 起点经纬度 "lng,lat"
    destination: 终点经纬度 "lng,lat"
    """
    cache_key = f"riding:{origin}:{destination}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {
        "origin": origin,
        "destination": destination
    }
    data = await _make_request(AMAP_DIRECTION_RIDING_URL, params)
    if data.get("status") == "1":
        paths = data.get("data", {}).get("paths", [])
        result = {
            "status": True,
            "paths": [{
                "distance": float(p.get("distance", 0)),
                "duration": float(p.get("duration", 0))
            } for p in paths]
        }
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, {"status": False, "message": data.get("info")})
    return {"status": False, "message": data.get("info")}


async def reverse_geocode(lng: float, lat: float) -> dict:
    """
    逆地理编码 - 经纬度转地址
    """
    cache_key = f"regeo:{lng}:{lat}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {"location": f"{lng},{lat}"}
    data = await _make_request(AMAP_GEOCODE_REVERSE_URL, params)
    if data.get("status") == "1":
        regeocode = data.get("regeocode", {})
        address_component = regeocode.get("addressComponent", {})
        result = {
            "status": True,
            "formatted_address": regeocode.get("formatted_address", ""),
            "province": address_component.get("province", ""),
            "city": address_component.get("city", ""),
            "district": address_component.get("district", ""),
            "township": address_component.get("township", ""),
            "street": address_component.get("street", ""),
            "number": address_component.get("number", ""),
            "adcode": address_component.get("adcode", ""),
            "building": address_component.get("building", {}).get("name", "")
        }
        _set_cache(cache_key, result)
        return result
    _set_cache(cache_key, {"status": False, "message": data.get("info")})
    return {"status": False, "message": data.get("info")}


async def ip_location(ip: str = "") -> dict:
    """
    IP定位 - 根据IP地址获取位置信息
    注意: 免费版Key可能不支持无参数调用
    """
    cache_key = f"ip:{ip}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    params = {}
    if ip:
        params["ip"] = ip
    
    try:
        data = await _make_request(AMAP_IP_URL, params)
        if data.get("status") == "1":
            result = {
                "status": True,
                "ip": data.get("ip", ""),
                "country": data.get("country", ""),
                "province": data.get("province", ""),
                "city": data.get("city", ""),
                "district": data.get("district", ""),
                "rectangle": data.get("rectangle", "")
            }
            _set_cache(cache_key, result)
            return result
    except Exception as e:
        pass
    
    _set_cache(cache_key, {"status": False, "message": "IP定位功能可能需要高级权限"})
    return {"status": False, "message": "IP定位功能可能需要高级权限"}


async def get_weather(adcode: str) -> dict:
    """
    获取天气信息
    extensions: base=实况天气, all=预报天气
    """
    cache_key = f"weather:{adcode}"
    cached = _get_cache(cache_key)
    if cached is not None:
        return cached
    
    current_data = await _make_request(AMAP_WEATHER_URL, {
        "city": adcode,
        "extensions": "base"
    })
    
    forecast_data = await _make_request(AMAP_WEATHER_URL, {
        "city": adcode,
        "extensions": "all"
    })
    
    result = {"status": False}
    
    if current_data.get("status") == "1":
        lives = current_data.get("lives", [])
        result["current"] = {
            "province": lives[0].get("province") if lives else "",
            "city": lives[0].get("city") if lives else "",
            "weather": lives[0].get("weather") if lives else "",
            "temperature": lives[0].get("temperature") if lives else "",
            "wind_direction": lives[0].get("winddirection") if lives else "",
            "wind_power": lives[0].get("windpower") if lives else "",
            "humidity": lives[0].get("humidity") if lives else "",
            "report_time": lives[0].get("reporttime") if lives else ""
        }
        result["status"] = True
    
    if forecast_data.get("status") == "1":
        forecasts = forecast_data.get("forecasts", [])
        if forecasts:
            result["forecast"] = [{
                "date": d.get("date"),
                "week": d.get("week"),
                "weather_day": d.get("weather_day"),
                "weather_night": d.get("weather_night"),
                "temp_max": d.get("temp_max"),
                "temp_min": d.get("temp_min"),
                "wind_direction_day": d.get("wind_direction_day"),
                "wind_power_day": d.get("wind_power_day")
            } for d in forecasts[0].get("casts", [])]
    
    _set_cache(cache_key, result)
    return result


def get_static_map_url(center_lng: float, center_lat: float, 
                       zoom: int = 11, width: int = 750, height: int = 400,
                       markers: str = "", paths: str = "") -> str:
    """
    生成静态地图URL
    """
    amap_key = os.environ.get('AMAP_KEY', '')
    if not amap_key:
        return ""
    
    base_url = "https://restapi.amap.com/v3/staticmap"
    params = {
        "location": f"{center_lng},{center_lat}",
        "zoom": zoom,
        "size": f"{width}*{height}",
        "key": amap_key
    }
    if markers:
        params["markers"] = markers
    if paths:
        params["paths"] = paths
    
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base_url}?{query}"


async def get_all_transport_modes(origin: str, destination: str, city: str = "") -> dict:
    """
    获取所有交通方式的路线规划
    """
    results = {}
    
    driving, walking = await asyncio.gather(
        driving_direction(origin, destination),
        walking_direction(origin, destination),
        return_exceptions=True
    )
    
    if isinstance(driving, Exception):
        driving = {"status": False, "message": str(driving)}
    if isinstance(walking, Exception):
        walking = {"status": False, "message": str(walking)}
    
    results["driving"] = driving
    results["walking"] = walking
    
    if city:
        transit = await transit_direction(origin, destination, city)
        results["transit"] = transit
    
    return results
