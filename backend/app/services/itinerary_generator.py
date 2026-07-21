import asyncio
import random
import re
from datetime import datetime
from app.services.amap_service import search_attractions, search_foods, search_hotels, get_poi_detail
from app.services.poi_tips import get_poi_tips


def parse_natural_language(text: str) -> dict:
    params = {}
    
    days_patterns = [
        r'(\d+)\s*天', r'(\d+)\s*日', r'(\d+)\s*晚',
        r'三日', r'两日', r'一日', r'五日', r'七日'
    ]
    for pattern in days_patterns:
        match = re.search(pattern, text)
        if match:
            num_map = {'三': 3, '两': 2, '一': 1, '五': 5, '七': 7}
            if match.group(1):
                params['days'] = int(match.group(1))
            elif match.group(0)[:1] in num_map:
                params['days'] = num_map[match.group(0)[:1]]
            break
    
    budget_patterns = [
        r'(\d+)\s*元', r'(\d+)\s*块', r'预算\s*(\d+)',
        r'人均\s*(\d+)', r'(\d+)\s*以内'
    ]
    for pattern in budget_patterns:
        match = re.search(pattern, text)
        if match:
            params['budget'] = int(match.group(1))
            break
    
    people_patterns = [
        r'(\d+)\s*人', r'(\d+)\s*个', r'一行\s*(\d+)',
        r'两人', r'一家三口', r'一家四口'
    ]
    for pattern in people_patterns:
        match = re.search(pattern, text)
        if match:
            num_map = {'两': 2}
            if match.group(1):
                params['people'] = int(match.group(1))
            elif match.group(0)[:1] in num_map:
                params['people'] = num_map[match.group(0)[:1]]
            elif '三' in match.group(0):
                params['people'] = 3
            elif '四' in match.group(0):
                params['people'] = 4
            break
    
    city_patterns = [
        r'([\u4e00-\u9fa5]+)\s*出发', r'去\s*([\u4e00-\u9fa5]+)',
        r'到\s*([\u4e00-\u9fa5]+)', r'([\u4e00-\u9fa5]+)\s*旅游',
        r'([\u4e00-\u9fa5]+)\s*旅行'
    ]
    for pattern in city_patterns:
        match = re.search(pattern, text)
        if match:
            city = match.group(1)
            if city not in ['北京', '上海', '广州', '深圳', '杭州', '成都', '西安', '重庆', '南京', '武汉', '长沙', '厦门', '青岛', '大连', '苏州', '天津', '郑州', '济南', '沈阳', '哈尔滨', '合肥', '福州', '宁波', '无锡', '昆明', '丽江', '三亚', '桂林', '张家界']:
                continue
            if '出发' in pattern or '从' in text[:text.index(city)] if city in text else False:
                params['from_city'] = city
            else:
                params['city'] = city
            break
    
    preference_keywords = {
        '美食': ['吃', '美食', '餐厅', '小吃', '吃货', '饭'],
        '购物': ['逛', '购物', '商场', '买'],
        '亲子': ['带孩子', '亲子', '儿童', '小孩', '宝宝', '一家'],
        '自然': ['风景', '自然', '山', '水', '湖', '海', '森林'],
        '文化': ['历史', '文化', '古迹', '博物馆', '文物', '古'],
    }
    
    for pref, keywords in preference_keywords.items():
        for kw in keywords:
            if kw in text:
                params['preference'] = pref
                break
        if 'preference' in params:
            break
    
    if '老人' in text or '父母' in text:
        params['elderly_friendly'] = True
    if '少走路' in text or '不累' in text or '轻松' in text:
        params['easy_walk'] = True
    if '辣' in text and ('不' in text or '忌' in text or '避免' in text):
        params['no_spicy'] = True
    if '拍照' in text or '摄影' in text:
        params['photo_focus'] = True
    if '民宿' in text:
        params['homestay'] = True
    if '近' in text and ('站' in text or '高铁' in text):
        params['near_station'] = True
    if '近' in text and ('景' in text or '景区' in text):
        params['near_attraction'] = True
    
    if '浪漫' in text or '情侣' in text or '蜜月' in text:
        params['is_couple'] = True
    if '徒步' in text or '户外' in text:
        params['is_hiking'] = True
    
    return params


async def generate_smart_itinerary(
    city: str, 
    days: int, 
    budget: float, 
    preference: str = '',
    people: int = 2,
    elderly_friendly: bool = False,
    easy_walk: bool = False,
    no_spicy: bool = False,
    photo_focus: bool = False,
    homestay: bool = False,
    near_station: bool = False,
    near_attraction: bool = False,
    max_walk_per_day: int = 10000,
    max_travel_time: int = 60,
    wake_up_time: str = '08:00',
    sleep_time: str = '22:00',
    include_night: bool = True,
    is_couple: bool = False,
    is_hiking: bool = False
):
    attractions, foods, hotels = await asyncio.gather(
        search_attractions(city, limit=50),
        search_foods(city, limit=50),
        search_hotels(city, limit=25),
        return_exceptions=True
    )
    
    if isinstance(attractions, Exception):
        attractions = []
    if isinstance(foods, Exception):
        foods = []
    if isinstance(hotels, Exception):
        hotels = []
    
    attractions = [a for a in attractions if a.get("rating", 0) > 0]
    foods = [f for f in foods if f.get("rating", 0) > 0]
    hotels = [h for h in hotels if h.get("rating", 0) > 0]
    
    attractions.sort(key=lambda x: x.get("rating", 0), reverse=True)
    foods.sort(key=lambda x: x.get("rating", 0), reverse=True)
    hotels.sort(key=lambda x: x.get("rating", 0), reverse=True)
    
    if len(attractions) < 2 and len(foods) < 2:
        return {
            "days": [],
            "total_cost_estimate": budget,
            "summary": f"抱歉，暂时没有足够的{city}本地数据来生成详细行程。建议您选择较大的城市或稍后再试。",
            "tips": [
                "小贴士：较大城市的景点、美食数据更丰富，生成的行程会更详细",
                "您可以尝试搜索北京、上海、杭州等热门旅游城市"
            ],
            "hotel_recommendations": [],
            "config": {
                "city": city, "days": days, "budget": budget, "people": people
            },
            "warning": "数据不足"
        }
    
    filtered_attractions = _filter_attractions(attractions, preference, elderly_friendly, easy_walk, photo_focus, is_hiking)
    filtered_foods = _filter_foods(foods, no_spicy)
    filtered_hotels = _filter_hotels(hotels, homestay, near_station, near_attraction, budget, days)
    
    itinerary = []
    attractions_queue = filtered_attractions.copy()
    foods_queue = filtered_foods.copy()
    hotels_queue = filtered_hotels.copy()
    
    if easy_walk:
        attractions_queue = _interleave_indoor_outdoor(attractions_queue)
    
    for day_num in range(1, days + 1):
        day_plan = {
            "day": day_num,
            "title": f"第 {day_num} 天",
            "date_hint": _get_date_hint(day_num),
            "schedule": [],
            "tips": [],
            "estimated_walk": 0,
            "estimated_travel_time": 0,
            "weather_hint": ""
        }
        
        morning_start = wake_up_time
        morning_end = "11:30"
        lunch_start = "12:00"
        lunch_end = "13:30"
        afternoon_start = "14:00"
        afternoon_end = "17:00"
        dinner_start = "18:00"
        dinner_end = "19:30"
        
        morning_attraction = None
        if attractions_queue:
            morning_attraction = attractions_queue.pop(0)
            day_plan["schedule"].append({
                "time": f"{morning_start}-{morning_end}",
                "type": "attraction",
                "item": morning_attraction,
                "description": _get_attraction_description(morning_attraction, 'morning'),
                "transport": _estimate_transport(),
                "walk_estimate": _estimate_walk()
            })
            day_plan["estimated_walk"] += 2000
            day_plan["estimated_travel_time"] += 15
        
        lunch = None
        if foods_queue:
            lunch = foods_queue.pop(0)
            day_plan["schedule"].append({
                "time": f"{lunch_start}-{lunch_end}",
                "type": "food",
                "item": lunch,
                "description": _get_food_description(lunch),
                "transport": _estimate_transport(),
                "walk_estimate": _estimate_walk()
            })
            day_plan["estimated_walk"] += 500
            day_plan["estimated_travel_time"] += 10
        
        afternoon_attraction = None
        if attractions_queue:
            afternoon_attraction = attractions_queue.pop(0)
            day_plan["schedule"].append({
                "time": f"{afternoon_start}-{afternoon_end}",
                "type": "attraction",
                "item": afternoon_attraction,
                "description": _get_attraction_description(afternoon_attraction, 'afternoon'),
                "transport": _estimate_transport(),
                "walk_estimate": _estimate_walk()
            })
            day_plan["estimated_walk"] += 3000
            day_plan["estimated_travel_time"] += 15
        
        dinner = None
        if foods_queue:
            dinner = foods_queue.pop(0)
            day_plan["schedule"].append({
                "time": f"{dinner_start}-{dinner_end}",
                "type": "food",
                "item": dinner,
                "description": _get_food_description(dinner),
                "transport": _estimate_transport(),
                "walk_estimate": _estimate_walk()
            })
            day_plan["estimated_walk"] += 500
            day_plan["estimated_travel_time"] += 10
        
        if include_night and day_num % 2 == 0 and attractions_queue:
            evening_activity = attractions_queue.pop(0)
            day_plan["schedule"].append({
                "time": f"20:00-21:30",
                "type": "attraction",
                "item": evening_activity,
                "description": _get_attraction_description(evening_activity, 'evening'),
                "transport": _estimate_transport(),
                "walk_estimate": _estimate_walk()
            })
            day_plan["estimated_walk"] += 1500
            day_plan["estimated_travel_time"] += 10
        
        if day_num < days and hotels_queue:
            hotel = hotels_queue.pop(0)
            day_plan["hotel"] = hotel
            day_plan["tips"].append(f"入住: {hotel.get('name', '')}")
        
        day_plan["tips"].extend(_generate_day_tips(day_num, city, easy_walk, elderly_friendly, photo_focus))
        itinerary.append(day_plan)
    
    total_cost = calculate_cost(itinerary, hotels, budget, people, days)
    itinerary_summary = generate_summary(itinerary, city, people, days)
    
    return {
        "days": itinerary,
        "total_cost_estimate": total_cost,
        "summary": itinerary_summary,
        "tips": generate_tips(city, days, budget, people, elderly_friendly, easy_walk, no_spicy, photo_focus),
        "hotel_recommendations": hotels[:5],
        "config": {
            "city": city, "days": days, "budget": budget, "people": people,
            "preference": preference, "elderly_friendly": elderly_friendly,
            "easy_walk": easy_walk, "no_spicy": no_spicy,
            "photo_focus": photo_focus, "homestay": homestay
        }
    }


async def generate_multiple_itineraries(
    city: str, 
    days: int, 
    budget: float, 
    preference: str = '',
    people: int = 2,
    version_count: int = 3
):
    versions = []
    strategies = [
        {"name": "舒适省心", "desc": "节奏轻松，交通便利", "easy_walk": True, "elderly_friendly": False},
        {"name": "经济实惠", "desc": "性价比之选，深度体验", "easy_walk": False, "elderly_friendly": False},
        {"name": "深度文化", "desc": "历史古迹，人文体验", "easy_walk": False, "elderly_friendly": False, "culture_focus": True},
        {"name": "自然风光", "desc": "山水之美，户外探索", "easy_walk": False, "elderly_friendly": False, "nature_focus": True},
        {"name": "美食之旅", "desc": "舌尖盛宴，地道风味", "easy_walk": False, "elderly_friendly": False},
        {"name": "购物休闲", "desc": "时尚购物，放松身心", "easy_walk": True, "elderly_friendly": False},
    ]
    
    selected_strategies = random.sample(strategies, min(version_count, len(strategies)))
    
    for strategy in selected_strategies:
        try:
            result = await generate_smart_itinerary(
                city=city, days=days, budget=budget,
                preference=preference or '',
                people=people,
                easy_walk=strategy.get('easy_walk', False),
                elderly_friendly=strategy.get('elderly_friendly', False),
                photo_focus=strategy.get('culture_focus', False) or strategy.get('nature_focus', False),
                include_night=True
            )
            result['version_name'] = strategy['name']
            result['version_desc'] = strategy['desc']
            result['strategy'] = strategy
            versions.append(result)
        except Exception as e:
            print(f"版本生成失败: {e}")
    
    return {"versions": versions, "total": len(versions)}


async def generate_from_natural_language(text: str):
    params = parse_natural_language(text)
    
    if 'city' not in params:
        return {"success": False, "message": "请告诉我您想去哪个城市", "parsed_params": params}
    
    result = await generate_smart_itinerary(
        city=params.get('city', ''),
        days=params.get('days', 3),
        budget=params.get('budget', 3000),
        preference=params.get('preference', ''),
        people=params.get('people', 2),
        elderly_friendly=params.get('elderly_friendly', False),
        easy_walk=params.get('easy_walk', False),
        no_spicy=params.get('no_spicy', False),
        photo_focus=params.get('photo_focus', False),
        homestay=params.get('homestay', False),
        near_station=params.get('near_station', False),
        near_attraction=params.get('near_attraction', False),
        is_couple=params.get('is_couple', False),
        is_hiking=params.get('is_hiking', False)
    )
    
    return {
        "success": True,
        "parsed_params": params,
        "itinerary": result,
        "message": f"已为您生成{params.get('city', '')}{params.get('days', 3)}天行程"
    }


def _filter_attractions(attractions, preference='', elderly_friendly=False, easy_walk=False, photo_focus=False, is_hiking=False):
    filtered = attractions
    
    if preference == '美食':
        filtered = filtered[:20]
    elif preference == '购物':
        shopping_keywords = ['购物', '商场', '步行街', '商业街', '奥莱', '广场']
        shopping = [a for a in filtered if any(kw in a.get('name', '') or kw in a.get('type', '') for kw in shopping_keywords)]
        filtered = shopping + [a for a in filtered if a not in shopping][:15]
    elif preference == '亲子':
        family_keywords = ['乐园', '儿童', '动物园', '海洋馆', '博物馆', '公园', '游乐场']
        family = [a for a in filtered if any(kw in a.get('name', '') or kw in a.get('type', '') for kw in family_keywords)]
        filtered = family + filtered[:10]
    elif preference == '自然':
        nature_keywords = ['山', '水', '湖', '海', '森林', '公园', '自然', '风景', '峡谷', '瀑布']
        nature = [a for a in filtered if any(kw in a.get('type', '') for kw in nature_keywords)]
        filtered = nature + filtered[:10]
    elif preference == '文化':
        culture_keywords = ['博物馆', '古', '遗址', '故居', '历史', '寺庙', '教堂', '纪念馆']
        culture = [a for a in filtered if any(kw in a.get('name', '') or kw in a.get('type', '') for kw in culture_keywords)]
        filtered = culture + filtered[:10]
    
    if easy_walk:
        indoor_keywords = ['博物馆', '室内', '展览馆', '美术馆', '科技馆']
        indoor = [a for a in filtered if any(kw in a.get('type', '') or kw in a.get('name', '') for kw in indoor_keywords)]
        outdoor = [a for a in filtered if a not in indoor]
        filtered = indoor[:10] + outdoor[:10]
    elif is_hiking:
        outdoor_keywords = ['山', '公园', '自然', '徒步', '森林']
        outdoor = [a for a in filtered if any(kw in a.get('type', '') or kw in a.get('name', '') for kw in outdoor_keywords)]
        filtered = outdoor + filtered[:10]
    
    if photo_focus:
        photo_keywords = ['塔', '楼', '广场', '公园', '古镇', '古街', '江', '湖']
        photo = [a for a in filtered if any(kw in a.get('name', '') or kw in a.get('type', '') for kw in photo_keywords)]
        filtered = photo + filtered[:10]
    
    return filtered[:25]


def _filter_foods(foods, no_spicy=False):
    if no_spicy:
        non_spicy = [f for f in foods if '辣' not in f.get('type', '') and '川菜' not in f.get('type', '') and '湘菜' not in f.get('type', '')]
        return non_spicy[:25] + foods[:5]
    return foods[:30]


def _filter_hotels(hotels, homestay=False, near_station=False, near_attraction=False, budget=3000, days=3):
    per_day_budget = budget / days / 2
    
    affordable = [h for h in hotels if h.get('cost', 0) <= per_day_budget * 1.5]
    if affordable:
        hotels = affordable
    
    if near_station:
        station = [h for h in hotels if '站' in h.get('address', '') or '火车站' in h.get('address', '') or '高铁' in h.get('address', '')]
        hotels = station + [h for h in hotels if h not in station]
    elif near_attraction:
        hotels = hotels
    
    return hotels[:15]


def _interleave_indoor_outdoor(attractions):
    indoor = []
    outdoor = []
    indoor_keywords = ['博物馆', '室内', '展览馆', '美术馆', '科技馆', '纪念馆']
    for a in attractions:
        if any(kw in a.get('type', '') or kw in a.get('name', '') for kw in indoor_keywords):
            indoor.append(a)
        else:
            outdoor.append(a)
    
    result = []
    max_len = max(len(indoor), len(outdoor))
    for i in range(max_len):
        if i < len(outdoor):
            result.append(outdoor[i])
        if i < len(indoor):
            result.append(indoor[i])
    
    return result if result else attractions


def _get_attraction_description(attraction, time_period='morning'):
    if time_period == 'morning':
        return f"上午游览{attraction.get('name', '')}"
    elif time_period == 'afternoon':
        return f"下午深度游览{attraction.get('name', '')}"
    elif time_period == 'evening':
        return f"夜间游览{attraction.get('name', '')}，欣赏夜景"
    return f"游览{attraction.get('name', '')}"


def _get_food_description(food):
    desc = f"品尝{food.get('name', '')}"
    if food.get('cost', 0) > 0:
        desc += f"（人均约¥{food['cost']}）"
    return desc


def _estimate_transport():
    return random.choice(['步行约15分钟', '打车约10分钟', '地铁约8分钟', '公交约20分钟'])


def _estimate_walk():
    return random.choice(['约500米', '约800米', '约1000米', '约1200米'])


def _get_date_hint(day_num):
    today = datetime.now()
    from datetime import timedelta
    date = today + timedelta(days=day_num - 1)
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return f"{date.month}月{date.day}日 {weekdays[date.weekday()]}"


def _generate_day_tips(day_num, city, easy_walk, elderly_friendly, photo_focus):
    tips = []
    if day_num == 1:
        tips.append(f"抵达{city}后建议先休息适应")
        tips.append("提前准备好健康码和身份证")
    if easy_walk:
        tips.append("今日行程较为轻松，适合慢慢游览")
    if elderly_friendly:
        tips.append("注意休息，建议每小时休息10-15分钟")
    if photo_focus:
        tips.append("注意捕捉精彩瞬间，光线好的时段拍照更佳")
    if day_num % 2 == 0:
        tips.append("可以尝试当地特色夜生活")
    if easy_walk:
        tips.append("穿着舒适的鞋子，减少步行负担")
    return tips[:3]


def calculate_cost(itinerary, hotels, budget, people=2, days=3):
    hotel_cost = 0
    if hotels:
        avg_hotel = sum(h.get("cost", 200) for h in hotels[:5] if h.get("cost", 0) > 0) / max(1, len([h for h in hotels[:5] if h.get("cost", 0) > 0]))
        hotel_cost = avg_hotel * (days - 1)
    
    food_per_day = 150
    food_cost = food_per_day * days * people
    
    attraction_cost = 0
    for day in itinerary:
        for item in day.get('schedule', []):
            if item['type'] == 'attraction':
                attraction_cost += 50 * people
    
    local_transport = 30 * days * people
    
    total = hotel_cost + food_cost + attraction_cost + local_transport
    
    budget_per_person = budget * people if budget < 100 else budget
    if budget_per_person > 0:
        ratio = total / budget_per_person
        if ratio > 1.2:
            level = "high"
        elif ratio > 0.8:
            level = "medium"
        else:
            level = "low"
    else:
        level = "unknown"
    
    return {
        "total": round(total, 0),
        "hotel": round(hotel_cost, 0),
        "food": round(food_cost, 0),
        "attraction": round(attraction_cost, 0),
        "local_transport": round(local_transport, 0),
        "per_person": round(total / max(1, people), 0),
        "budget_level": level,
        "budget_match": round((budget_per_person - total) / budget_per_person * 100, 1) if budget_per_person > 0 else 0
    }


def generate_summary(itinerary, city, people=2, days=3):
    total_attractions = sum(1 for day in itinerary for item in day["schedule"] if item["type"] == "attraction")
    total_foods = sum(1 for day in itinerary for item in day["schedule"] if item["type"] == "food")
    total_walk = sum(day.get('estimated_walk', 0) for day in itinerary)
    
    summary = [
        f"本次行程共 {days} 天，{people}人，游览 {city}",
        f"安排 {total_attractions} 个景点/活动，{total_foods} 家餐厅",
        f"预计总步行约 {total_walk} 米，平均每天 {total_walk // max(1, days)} 米",
        "行程已按劳逸结合原则安排，包含早晚时段的合理分配"
    ]
    
    return summary


def generate_tips(city, days, budget, people, elderly_friendly, easy_walk, no_spicy, photo_focus):
    tips = [
        f"提前预订{city}酒店，尤其是节假日或旅游旺季",
        "景点门票建议提前在官方渠道预约，避免现场排队",
        "穿着舒适的鞋子，方便游览",
        "随身携带水杯、充电宝和少量现金",
        f"关注{city}实时天气预报，合理安排行程",
        "保存好紧急联系电话和当地医院地址",
        "购买旅行保险，保障出行安全"
    ]
    
    if budget and budget > 5000:
        tips.append("预算充足，可考虑升级住宿或体验特色项目")
    elif budget and budget < 2000:
        tips.append("预算有限，建议选择性价比高的快捷酒店和本地餐饮")
    
    if days <= 2:
        tips.append("行程紧凑，建议重点游玩核心景点")
    elif days >= 5:
        tips.append("时间充裕，可安排周边一日游或深度体验活动")
    
    if elderly_friendly:
        tips.append("注意老人身体状况，避免过度疲劳")
        tips.append("建议准备常用药品，注意保暖防暑")
    
    if easy_walk:
        tips.append("行程以室内和轻松景点为主，减少步行量")
    
    if no_spicy:
        tips.append("点菜时可告知服务员不要放辣，选择清淡口味")
    
    if photo_focus:
        tips.append("建议早上或傍晚拍摄，光线柔和效果更佳")
        tips.append("备好相机和充电宝，多拍精选")
    
    tips.append("合理规划每日预算，保留部分灵活资金")
    
    return tips
