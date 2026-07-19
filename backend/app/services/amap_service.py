import httpx
from app.config import get_settings

settings = get_settings()

AMAP_POI_URL = "https://restapi.amap.com/v3/place/text"
AMAP_POI_DETAIL_URL = "https://restapi.amap.com/v3/place/detail"
AMAP_NEARBY_URL = "https://restapi.amap.com/v3/place/around"
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
AMAP_DISTRICT_URL = "https://restapi.amap.com/v3/config/district"
AMAP_TIP_URL = "https://restapi.amap.com/v3/assistant/inputtips"


async def _make_request(url: str, params: dict) -> dict:
    params["key"] = settings.AMAP_KEY
    params["output"] = "JSON"
    params.setdefault("extensions", "all")
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        return resp.json()


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
    data = await _make_request(AMAP_GEOCODE_URL, {"address": city_name})
    if data.get("status") == "1" and data.get("geocodes"):
        geo = data["geocodes"][0]
        lng, lat = geo["location"].split(",")
        return {"name": geo["formatted_address"], "lng": float(lng), "lat": float(lat),
                "adcode": geo.get("adcode"), "province": geo.get("province"),
                "city": geo.get("city"), "district": geo.get("district")}
    return None


async def search_poi(city: str, keywords: str, types: str = "", offset: int = 20) -> list:
    params = {"keywords": keywords, "city": city, "citylimit": "true", "offset": offset, "page": 1}
    if types:
        params["types"] = types
    data = await _make_request(AMAP_POI_URL, params)
    if data.get("status") != "1":
        return []
    return [_parse_poi(p) for p in data.get("pois", [])]


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
    return {
        "attractions": sorted([a for a in attractions if a.get("rating", 0) > 0],
                              key=lambda x: x.get("rating", 0), reverse=True),
        "foods": sorted([f for f in foods if f.get("rating", 0) > 0],
                       key=lambda x: x.get("rating", 0), reverse=True),
        "hotels": sorted([h for h in hotels if h.get("rating", 0) > 0],
                        key=lambda x: x.get("rating", 0), reverse=True),
    }


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
