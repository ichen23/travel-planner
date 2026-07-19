import json

CITY_COORDS = {
    "北京": (116.4074, 39.9042),
    "上海": (121.4737, 31.2304),
    "广州": (113.2644, 23.1291),
    "深圳": (114.0579, 22.5431),
    "杭州": (120.1551, 30.2741),
    "成都": (104.0665, 30.5728),
    "南京": (118.7674, 32.0415),
    "武汉": (114.3055, 30.5931),
    "西安": (108.9402, 34.3416),
    "重庆": (106.5516, 29.5630),
    "苏州": (120.5853, 31.2989),
    "天津": (117.2009, 39.1256),
    "长沙": (112.9388, 28.2282),
    "青岛": (120.3826, 36.0671),
    "大连": (121.6147, 38.9140),
    "厦门": (118.0894, 24.4798),
    "昆明": (102.8329, 24.8801),
    "贵阳": (106.7135, 26.5783),
    "桂林": (110.2992, 25.2742),
    "三亚": (109.5082, 18.2479),
    "海口": (110.1999, 20.0444),
    "福州": (119.2965, 26.0745),
    "宁波": (121.5498, 29.8684),
    "合肥": (117.2272, 31.8206),
    "郑州": (113.6254, 34.7466),
    "济南": (117.0009, 36.6758),
    "石家庄": (114.5149, 38.0428),
    "太原": (112.5489, 37.8706),
    "沈阳": (123.4315, 41.8057),
    "长春": (125.3235, 43.8171),
    "哈尔滨": (126.6424, 45.7567),
    "呼和浩特": (111.7491, 40.8425),
    "乌鲁木齐": (87.6168, 43.8256),
    "兰州": (103.8343, 36.0611),
    "西宁": (101.7782, 36.6232),
    "银川": (106.2730, 38.4872),
    "拉萨": (91.1409, 29.6500),
    "南昌": (115.8579, 28.6820),
    "南宁": (108.3200, 22.8240),
}

CITY_HIGH_SPEED_DATA = {
    "北京": [
        {"to": "天津", "duration": "30分钟", "price": 54.5},
        {"to": "济南", "duration": "1小时40分", "price": 184},
        {"to": "上海", "duration": "4小时40分", "price": 662},
        {"to": "南京", "duration": "3小时20分", "price": 443},
        {"to": "郑州", "duration": "2小时30分", "price": 321},
    ],
    "上海": [
        {"to": "苏州", "duration": "25分钟", "price": 59},
        {"to": "南京", "duration": "1小时15分", "price": 134},
        {"to": "杭州", "duration": "50分钟", "price": 73},
        {"to": "合肥", "duration": "2小时30分", "price": 199},
        {"to": "武汉", "duration": "4小时", "price": 301},
    ],
    "广州": [
        {"to": "深圳", "duration": "30分钟", "price": 74.5},
        {"to": "长沙", "duration": "2小时30分", "price": 314},
        {"to": "桂林", "duration": "3小时", "price": 294},
        {"to": "贵阳", "duration": "4小时", "price": 323},
        {"to": "南宁", "duration": "3小时", "price": 236},
    ],
    "杭州": [
        {"to": "上海", "duration": "50分钟", "price": 73},
        {"to": "南京", "duration": "1小时20分", "price": 142},
        {"to": "苏州", "duration": "1小时", "price": 110},
        {"to": "合肥", "duration": "2小时15分", "price": 180},
        {"to": "福州", "duration": "3小时", "price": 260},
    ],
    "成都": [
        {"to": "重庆", "duration": "1小时30分", "price": 97},
        {"to": "西安", "duration": "3小时", "price": 263},
        {"to": "贵阳", "duration": "3小时30分", "price": 258},
        {"to": "昆明", "duration": "4小时30分", "price": 294},
        {"to": "武汉", "duration": "7小时", "price": 472},
    ],
}

EXTENDED_HIGH_SPEED = {
    "北京": ["沈阳", "长春", "哈尔滨", "太原", "石家庄"],
    "上海": ["无锡", "常州", "合肥", "武汉", "福州"],
    "广州": ["厦门", "福州", "海口", "三亚"],
    "杭州": ["宁波", "南昌", "合肥", "上海"],
    "成都": ["乐山", "绵阳", "重庆", "南充"],
    "南京": ["镇江", "扬州", "苏州", "上海"],
    "武汉": ["长沙", "合肥", "南昌", "郑州"],
    "西安": ["洛阳", "郑州", "兰州", "银川"],
    "重庆": ["成都", "贵阳", "昆明", "南宁"],
    "苏州": ["无锡", "常州", "上海", "南京"],
    "天津": ["北京", "济南", "石家庄", "唐山"],
    "长沙": ["武汉", "贵阳", "桂林", "广州"],
    "青岛": ["济南", "烟台", "大连", "天津"],
    "大连": ["沈阳", "长春", "青岛", "天津"],
    "厦门": ["福州", "泉州", "广州", "深圳"],
    "昆明": ["大理", "丽江", "贵阳", "成都"],
    "贵阳": ["桂林", "长沙", "昆明", "成都"],
    "桂林": ["南宁", "广州", "贵阳", "长沙"],
    "南宁": ["昆明", "贵阳", "广州", "桂林"],
    "郑州": ["西安", "武汉", "济南", "石家庄"],
}

CITY_TAGS = {
    "北京": ["历史名城", "世界遗产", "皇家园林", "胡同文化", "都市"],
    "上海": ["国际都市", "外滩夜景", "主题乐园", "购物天堂", "海派文化"],
    "广州": ["美食之都", "千年商都", "岭南文化", "主题乐园"],
    "深圳": ["创新城市", "主题乐园", "海滨", "现代都市"],
    "杭州": ["西湖美景", "江南水乡", "茶文化", "世界遗产", "互联网"],
    "成都": ["熊猫基地", "美食天堂", "慢生活", "历史文化"],
    "南京": ["六朝古都", "秦淮河", "历史遗迹", "民国风情"],
    "武汉": ["樱花之都", "江城", "历史名城", "美食"],
    "西安": ["十三朝古都", "兵马俑", "历史文化", "美食"],
    "重庆": ["8D魔幻", "火锅之都", "网红城市", "夜景"],
    "苏州": ["园林之都", "江南水乡", "世界遗产", "历史文化"],
    "天津": ["曲艺之乡", "欧式风情", "美食", "海河"],
    "长沙": ["美食之都", "娱乐之城", "网红城市", "历史文化"],
    "青岛": ["海滨城市", "啤酒之都", "德式建筑", "山海"],
    "大连": ["海滨城市", "浪漫", "海鲜", "雪景"],
    "厦门": ["海上花园", "文艺清新", "鼓浪屿", "海岛"],
    "昆明": ["春城", "民族风情", "鲜花", "美食"],
    "贵阳": ["避暑之都", "少数民族", "美食"],
    "桂林": ["山水甲天下", "漓江", "少数民族", "自然景观"],
    "三亚": ["海岛度假", "热带风光", "潜水", "度假"],
    "海口": ["椰城", "海岛", "历史文化", "美食"],
    "福州": ["榕城", "历史文化", "美食", "海滨"],
    "宁波": ["港口城市", "历史文化", "海鲜", "现代"],
    "合肥": ["科技创新", "历史文化"],
    "郑州": ["铁路枢纽", "历史文化", "少林寺"],
    "济南": ["泉城", "历史文化", "趵突泉"],
    "石家庄": ["省会", "历史文化"],
    "太原": ["龙城", "历史文化", "晋商"],
    "沈阳": ["东北", "历史文化", "工业"],
    "长春": ["汽车城", "冰雪", "电影"],
    "哈尔滨": ["冰雪之都", "俄式建筑", "冰雪大世界"],
    "呼和浩特": ["草原", "蒙古族", "昭君"],
    "乌鲁木齐": ["西域", "天山", "民族风情"],
    "兰州": ["黄河", "拉面", "丝绸之路"],
    "西宁": ["青藏高原", "湖光山色", "藏文化"],
    "银川": ["塞上江南", "西夏文化", "沙漠"],
    "拉萨": ["雪域高原", "藏文化", "布达拉宫"],
    "南昌": ["英雄城", "滕王阁", "历史文化"],
    "南宁": ["绿城", "少数民族", "东盟"],
}

CITY_IMAGES = {
    "北京": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800",
    "上海": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=800",
    "广州": "https://images.unsplash.com/photo-1559286456-b6976a7f4f64?w=800",
    "深圳": "https://images.unsplash.com/photo-1536599018102-9f803c140fc1?w=800",
    "杭州": "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=800",
    "成都": "https://images.unsplash.com/photo-1533106418989-88406c7cc8ca?w=800",
    "南京": "https://images.unsplash.com/photo-1528164344705-47542687000d?w=800",
    "武汉": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800",
    "西安": "https://images.unsplash.com/photo-1591247947424-42d8e2c63f8e?w=800",
    "重庆": "https://images.unsplash.com/photo-1555217851-6141535bd771?w=800",
    "苏州": "https://images.unsplash.com/photo-1518544801976-3e188ea7a631?w=800",
    "天津": "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=800",
    "长沙": "https://images.unsplash.com/photo-1566991585629-f71f768fd07c?w=800",
    "青岛": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
    "大连": "https://images.unsplash.com/photo-1571184243053-f7d7c80f0f7b?w=800",
    "厦门": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800",
    "昆明": "https://images.unsplash.com/photo-1508873699372-7aeab60b44ab?w=800",
    "桂林": "https://images.unsplash.com/photo-1513415277900-a62401e19be4?w=800",
    "三亚": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
}

with open("app/services/city_database.py", "w", encoding="utf-8") as f:
    f.write('"""城市数据库 - 核心数据来自静态库，实时内容通过高德API获取"""\n\n')
    f.write(f"CITY_COORDS = {json.dumps(CITY_COORDS, ensure_ascii=False, indent=4)}\n\n")
    f.write(f"CITY_HIGH_SPEED_DATA = {json.dumps(CITY_HIGH_SPEED_DATA, ensure_ascii=False, indent=4)}\n\n")
    f.write(f"EXTENDED_HIGH_SPEED = {json.dumps(EXTENDED_HIGH_SPEED, ensure_ascii=False, indent=4)}\n\n")
    f.write(f"CITY_TAGS = {json.dumps(CITY_TAGS, ensure_ascii=False, indent=4)}\n\n")
    f.write(f"CITY_IMAGES = {json.dumps(CITY_IMAGES, ensure_ascii=False, indent=4)}\n\n")
    
    f.write("""
CITY_BASIC_INFO = {
    "北京": {
        "name": "北京",
        "province": "北京",
        "description": "千年古都，中国政治文化中心，拥有故宫、长城等世界文化遗产。",
        "rating": 4.8,
        "best_time": "9月-11月（秋季），4月-5月（春季）",
        "weather_tips": "冬季寒冷需保暖，夏季炎热注意防晒，春秋最舒适",
        "transport": "地铁发达，建议使用交通卡或支付宝乘车码",
        "highlights": "故宫、长城、天安门、颐和园",
    },
    "上海": {
        "name": "上海",
        "province": "上海",
        "description": "东方明珠，国际金融中心，海派文化与现代都市完美结合。",
        "rating": 4.7,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "梅雨季节(6-7月)多雨潮湿，四季分明",
        "transport": "地铁密集，建议metro大都会APP",
        "highlights": "外滩、东方明珠、迪士尼、豫园",
    },
    "广州": {
        "name": "广州",
        "province": "广东",
        "description": "千年商都，南国明珠，美食之都，岭南文化中心。",
        "rating": 4.6,
        "best_time": "10月-次年4月",
        "weather_tips": "夏季炎热多雨，冬季温暖干燥",
        "transport": "地铁发达，覆盖所有主要景点",
        "highlights": "广州塔、长隆、陈家祠、沙面",
    },
    "深圳": {
        "name": "深圳",
        "province": "广东",
        "description": "创新之都，主题乐园丰富，现代感强。",
        "rating": 4.5,
        "best_time": "10月-次年4月",
        "weather_tips": "夏季炎热潮湿，冬季温暖",
        "transport": "地铁完善，建议深圳通",
        "highlights": "世界之窗、欢乐谷、东部华侨城",
    },
    "杭州": {
        "name": "杭州",
        "province": "浙江",
        "description": "人间天堂，西湖美景闻名天下，龙井茶产地。",
        "rating": 4.8,
        "best_time": "3月-5月，10月-11月",
        "weather_tips": "4月梅雨，7-8月高温",
        "transport": "地铁公交覆盖，西湖景区有观光车",
        "highlights": "西湖、灵隐寺、千岛湖、宋城",
    },
    "成都": {
        "name": "成都",
        "province": "四川",
        "description": "天府之国，熊猫故乡，慢生活之都，美食天堂。",
        "rating": 4.7,
        "best_time": "3月-6月，9月-11月",
        "weather_tips": "气候温和湿润，四季分明",
        "transport": "地铁发达，推荐滴滴",
        "highlights": "熊猫基地、宽窄巷子、都江堰",
    },
    "南京": {
        "name": "南京",
        "province": "江苏",
        "description": "六朝古都，秦淮河畔，历史文化名城。",
        "rating": 4.6,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "春秋最佳，夏季炎热",
        "transport": "地铁覆盖主要景点",
        "highlights": "中山陵、夫子庙、明孝陵",
    },
    "武汉": {
        "name": "武汉",
        "province": "湖北",
        "description": "九省通衢，江城武汉，樱花之都，热干面故乡。",
        "rating": 4.5,
        "best_time": "3月（樱花季），9月-11月",
        "weather_tips": "夏季炎热（火炉），冬季湿冷",
        "transport": "地铁发达",
        "highlights": "黄鹤楼、东湖、武汉大学樱花",
    },
    "西安": {
        "name": "西安",
        "province": "陕西",
        "description": "十三朝古都，兵马俑世界第八大奇迹，丝绸之路起点。",
        "rating": 4.7,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "春秋干燥，夏季炎热，冬季寒冷",
        "transport": "地铁覆盖市区，去兵马俑坐景区直通车",
        "highlights": "兵马俑、大雁塔、西安城墙、华山",
    },
    "重庆": {
        "name": "重庆",
        "province": "重庆",
        "description": "山城雾都，8D魔幻城市，火锅之都，夜景媲美香港。",
        "rating": 4.7,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "夏季炎热，冬季潮湿多雾",
        "transport": "地铁复杂，推荐高德地图导航",
        "highlights": "洪崖洞、解放碑、武隆、长江索道",
    },
    "苏州": {
        "name": "苏州",
        "province": "江苏",
        "description": "上有天堂下有苏杭，园林之都，江南水乡。",
        "rating": 4.7,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "梅雨季(6-7月)多雨",
        "transport": "地铁公交覆盖市区",
        "highlights": "拙政园、留园、周庄、虎丘",
    },
    "天津": {
        "name": "天津",
        "province": "天津",
        "description": "九河下梢天津卫，曲艺之乡，中西合璧。",
        "rating": 4.5,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "春秋短暂，夏季炎热",
        "transport": "地铁覆盖主要景点",
        "highlights": "五大道、天津之眼、古文化街",
    },
    "长沙": {
        "name": "长沙",
        "province": "湖南",
        "description": "星城长沙，娱乐之都，美食之城。",
        "rating": 4.6,
        "best_time": "3月-5月，9月-11月",
        "weather_tips": "夏季炎热，冬季湿冷",
        "transport": "地铁覆盖主要景点",
        "highlights": "橘子洲、岳麓山、坡子街",
    },
    "青岛": {
        "name": "青岛",
        "province": "山东",
        "description": "海滨城市，啤酒之都，德式建筑，红瓦绿树。",
        "rating": 4.6,
        "best_time": "5月-10月",
        "weather_tips": "夏季凉爽多海雾",
        "transport": "地铁公交覆盖",
        "highlights": "栈桥、八大关、崂山、啤酒博物馆",
    },
    "大连": {
        "name": "大连",
        "province": "辽宁",
        "description": "浪漫海滨城市，海鲜美食，雪景迷人。",
        "rating": 4.5,
        "best_time": "5月-10月",
        "weather_tips": "夏季凉爽",
        "transport": "地铁完善",
        "highlights": "星海广场、老虎滩、金石滩",
    },
    "厦门": {
        "name": "厦门",
        "province": "福建",
        "description": "海上花园，浪漫海岛，文艺清新。",
        "rating": 4.6,
        "best_time": "10月-次年4月",
        "weather_tips": "5-9月多雨台风",
        "transport": "地铁公交覆盖",
        "highlights": "鼓浪屿、环岛路、曾厝垵",
    },
    "昆明": {
        "name": "昆明",
        "province": "云南",
        "description": "春城昆明，四季如春，民族风情。",
        "rating": 4.5,
        "best_time": "全年",
        "weather_tips": "四季如春，年温差小",
        "transport": "地铁公交覆盖",
        "highlights": "滇池、石林、翠湖",
    },
    "桂林": {
        "name": "桂林",
        "province": "广西",
        "description": "山水甲天下，漓江风光，少数民族风情。",
        "rating": 4.7,
        "best_time": "4月-10月",
        "weather_tips": "4-6月雨季",
        "transport": "建议包车或跟团",
        "highlights": "漓江、阳朔、龙脊梯田",
    },
    "三亚": {
        "name": "三亚",
        "province": "海南",
        "description": "海岛度假天堂，热带风光，潜水胜地。",
        "rating": 4.6,
        "best_time": "10月-次年4月",
        "weather_tips": "5-9月炎热多雨",
        "transport": "机场有直达巴士",
        "highlights": "亚龙湾、天涯海角、蜈支洲岛",
    },
}
""")
    
    f.write("""
def get_all_start_cities():
    """获取所有出发城市"""
    cities = list(CITY_COORDS.keys())
    cities.sort()
    return cities


def get_destinations_count():
    """获取目的地数量"""
    return len(CITY_COORDS)


def get_city_info(city: str) -> dict:
    """获取城市基础信息"""
    basic = CITY_BASIC_INFO.get(city, {})
    coords = CITY_COORDS.get(city)
    tags = CITY_TAGS.get(city, [])
    image = CITY_IMAGES.get(city, "")
    
    return {
        "name": basic.get("name", city),
        "province": basic.get("province", ""),
        "description": basic.get("description", ""),
        "rating": basic.get("rating", 4.5),
        "best_time": basic.get("best_time", ""),
        "weather_tips": basic.get("weather_tips", ""),
        "transport": basic.get("transport", ""),
        "highlights": basic.get("highlights", ""),
        "tags": tags,
        "image": image,
        "coords": coords,
    }


def get_high_speed_routes(city: str) -> list:
    """获取城市的高铁线路"""
    routes = CITY_HIGH_SPEED_DATA.get(city, [])
    extended = EXTENDED_HIGH_SPEED.get(city, [])
    for dest in extended[:5]:
        if dest not in [r.get("to") for r in routes]:
            routes.append({
                "to": dest,
                "duration": "约2-4小时",
                "price": "以实际为准",
            })
    return routes[:10]


def get_recommendations(from_city: str, max_duration_hours: float = 8) -> list:
    """获取推荐目的地"""
    recommendations = []
    
    direct_routes = CITY_HIGH_SPEED_DATA.get(from_city, [])
    for route in direct_routes:
        dest = route["to"]
        if dest in CITY_COORDS:
            city_info = get_city_info(dest)
            recommendations.append({
                "city": dest,
                "duration": route.get("duration", ""),
                "price": route.get("price", 0),
                "tags": city_info.get("tags", []),
                "image": city_info.get("image", ""),
                "rating": city_info.get("rating", 4.5),
            })
    
    extended_routes = EXTENDED_HIGH_SPEED.get(from_city, [])
    for dest in extended_routes:
        if dest in CITY_COORDS and dest not in [r["city"] for r in recommendations]:
            city_info = get_city_info(dest)
            recommendations.append({
                "city": dest,
                "duration": "约2-4小时",
                "price": "以实际为准",
                "tags": city_info.get("tags", []),
                "image": city_info.get("image", ""),
                "rating": city_info.get("rating", 4.5),
            })
    
    if len(recommendations) < 15:
        all_cities = list(CITY_COORDS.keys())
        import random
        random.shuffle(all_cities)
        for dest in all_cities:
            if len(recommendations) >= 20:
                break
            if dest != from_city and dest not in [r["city"] for r in recommendations]:
                city_info = get_city_info(dest)
                recommendations.append({
                    "city": dest,
                    "duration": "约3-6小时",
                    "price": "以实际为准",
                    "tags": city_info.get("tags", []),
                    "image": city_info.get("image", ""),
                    "rating": city_info.get("rating", 4.5),
                })
    
    recommendations.sort(key=lambda x: x.get("rating", 0), reverse=True)
    return recommendations[:25]
""")

print("city_database.py generated successfully!")
