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
    
    static_recommendations = {
        "北京": {"attractions": ["故宫博物院", "八达岭长城", "颐和园", "天坛公园", "天安门广场"], "food": ["北京烤鸭", "炸酱面", "涮羊肉", "豆汁焦圈"]},
        "上海": {"attractions": ["外滩", "东方明珠", "豫园", "迪士尼乐园", "南京路"], "food": ["小笼包", "生煎", "蟹粉豆腐", "本帮红烧肉"]},
        "广州": {"attractions": ["广州塔", "白云山", "陈家祠", "长隆欢乐世界", "沙面"], "food": ["早茶", "烧腊", "肠粉", "双皮奶"]},
        "成都": {"attractions": ["宽窄巷子", "锦里", "都江堰", "大熊猫繁育研究基地", "武侯祠"], "food": ["火锅", "串串香", "川菜", "钟水饺"]},
        "杭州": {"attractions": ["西湖", "灵隐寺", "千岛湖", "宋城", "西溪湿地"], "food": ["龙井虾仁", "东坡肉", "叫花鸡", "片儿川"]},
        "西安": {"attractions": ["兵马俑", "大雁塔", "回民街", "华清池", "城墙"], "food": ["肉夹馍", "羊肉泡馍", "凉皮", "biangbiang面"]},
        "重庆": {"attractions": ["洪崖洞", "解放碑", "武隆天生三桥", "磁器口", "长江索道"], "food": ["火锅", "小面", "酸辣粉", "毛血旺"]},
        "南京": {"attractions": ["中山陵", "夫子庙", "玄武湖", "总统府", "明孝陵"], "food": ["盐水鸭", "鸭血粉丝汤", "小笼包", "狮子头"]},
        "武汉": {"attractions": ["黄鹤楼", "东湖", "户部巷", "武汉大学", "长江大桥"], "food": ["热干面", "鸭脖", "三鲜豆皮", "糊汤粉"]},
        "厦门": {"attractions": ["鼓浪屿", "南普陀寺", "厦门大学", "中山路", "曾厝垵"], "food": ["沙茶面", "土笋冻", "海蛎煎", "花生汤"]},
        "苏州": {"attractions": ["拙政园", "留园", "虎丘", "周庄", "金鸡湖"], "food": ["松鼠桂鱼", "阳澄湖大闸蟹", "响油鳝糊", "苏式糕点"]},
        "青岛": {"attractions": ["栈桥", "八大关", "崂山", "金沙滩", "五四广场"], "food": ["海鲜", "青岛啤酒", "锅贴", "鲅鱼水饺"]},
        "长沙": {"attractions": ["岳麓山", "橘子洲", "张家界", "凤凰古城", "湖南省博物馆"], "food": ["臭豆腐", "剁椒鱼头", "糖油粑粑", "口味虾"]},
        "天津": {"attractions": ["五大道", "古文化街", "意大利风情区", "塘沽", "独乐寺"], "food": ["狗不理包子", "煎饼果子", "麻花", "锅巴菜"]},
        "大理": {"attractions": ["洱海", "苍山", "大理古城", "双廊", "喜洲"], "food": ["白族烤鱼", "乳扇", "饵丝", "砂锅鱼"]},
        "丽江": {"attractions": ["丽江古城", "玉龙雪山", "束河古镇", "蓝月谷", "泸沽湖"], "food": ["纳西烤鱼", "腊排骨火锅", "鸡豆凉粉", "丽江粑粑"]},
        "桂林": {"attractions": ["漓江", "阳朔", "龙脊梯田", "象鼻山", "遇龙河"], "food": ["桂林米粉", "啤酒鱼", "荔浦芋扣肉", "田螺酿"]},
        "三亚": {"attractions": ["亚龙湾", "天涯海角", "蜈支洲岛", "南山", "大东海"], "food": ["海鲜大餐", "椰子鸡", "清补凉", "和乐蟹"]},
        "深圳": {"attractions": ["世界之窗", "欢乐谷", "大小梅沙", "莲花山", "东部华侨城"], "food": ["潮汕牛肉火锅", "客家菜", "肠粉", "烧鹅"]},
        "郑州": {"attractions": ["少林寺", "黄河风景名胜区", "二七纪念塔", "清明上河园", "龙门石窟"], "food": ["烩面", "胡辣汤", "道口烧鸡", "灌汤包"]},
    }
    
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
        
        static_data = static_recommendations.get(rec["city"], {
            "attractions": [f"{rec['city']}著名景点", f"{rec['city']}特色街区", f"{rec['city']}文化遗址"],
            "food": [f"{rec['city']}特色美食", f"{rec['city']}传统小吃"]
        })
        
        rec["tips"] = {
            "attractions": [{"name": a, "address": ""} for a in static_data["attractions"]],
            "food": [{"name": f, "address": ""} for f in static_data["food"]]
        }

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
