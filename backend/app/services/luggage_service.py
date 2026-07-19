from datetime import datetime, timedelta


SEASON_CLOTHING = {
    "spring": {
        "months": [3, 4, 5],
        "outer": ["薄外套", "风衣", "针织衫"],
        "inner": ["长袖T恤", "衬衫"],
        "bottom": ["长裤", "牛仔裤"],
        "shoes": ["休闲鞋", "运动鞋"],
        "accessories": ["薄围巾"]
    },
    "summer": {
        "months": [6, 7, 8],
        "outer": ["防晒外套(可选)"],
        "inner": ["短袖T恤", "衬衫", "吊带"],
        "bottom": ["短裤", "薄长裤", "裙子"],
        "shoes": ["凉鞋", "拖鞋", "运动鞋"],
        "accessories": ["遮阳帽", "太阳镜", "防晒霜"]
    },
    "autumn": {
        "months": [9, 10, 11],
        "outer": ["厚外套", "夹克", "风衣"],
        "inner": ["长袖T恤", "衬衫", "毛衣"],
        "bottom": ["长裤", "牛仔裤", "裙子+打底裤"],
        "shoes": ["休闲鞋", "短靴"],
        "accessories": ["薄围巾"]
    },
    "winter": {
        "months": [12, 1, 2],
        "outer": ["羽绒服", "厚棉服", "大衣"],
        "inner": ["保暖内衣", "厚毛衣", "卫衣"],
        "bottom": ["厚长裤", "牛仔裤(加厚)", "保暖裤"],
        "shoes": ["雪地靴", "加绒运动鞋"],
        "accessories": ["厚围巾", "手套", "暖宝宝", "帽子"]
    }
}

PERSONAL_ITEMS = {
    "essential": ["身份证", "手机充电器", "充电宝", "钥匙", "钱包"],
    "toiletries": ["牙刷/牙膏", "洗面奶", "护肤品", "洗发水(旅行装)", "毛巾", "梳子"],
    "health": ["常用药品", "晕车药", "创可贴", "口罩", "洗手液"],
    "documents": ["行程单", "机票/车票", "酒店预订凭证", "保险单"],
    "electronics": ["耳机", "转换插头", "数据线", "相机"],
}

SCENARIO_EXTRAS = {
    "beach": ["泳衣", "泳镜", "沙滩鞋", "防水袋", "防晒衣", "潜水装备"],
    "mountain": ["登山鞋", "冲锋衣", "登山杖", "头灯", "保温水壶", "防滑手套"],
    "business": ["西装/正装", "领带", "商务鞋", "笔记本电脑", "U盘", "名片"],
    "family": ["儿童衣物", "尿不湿", "奶瓶/奶粉", "儿童药物", "玩具", "推车"],
    "elderly": ["保暖衣物", "护膝", "手杖", "常用慢性病药物", "血压计", "保温杯"],
    "hiking": ["登山靴", "速干衣", "背包(40L+)", "登山杖", "水壶", "急救包", "头灯"],
    "photography": ["相机", "备用电池", "内存卡", "三脚架", "镜头", "清洁套装"],
    "night_out": ["漂亮服装", "高跟鞋", "手包", "化妆品", "香水"],
}


def get_season(month: int) -> str:
    for season, data in SEASON_CLOTHING.items():
        if month in data["months"]:
            return season
    return "spring"


def generate_luggage_checklist(
    days: int = 3,
    season: str = "",
    scenario: str = "",
    weather_temp: float = 20,
    has_rain: bool = False,
    people_count: int = 1,
    special_needs: list = None
) -> dict:
    now = datetime.now()
    
    if not season:
        season = get_season(now.month)
    
    if weather_temp <= 0:
        season = "winter"
    elif weather_temp <= 10:
        season = "winter"
    elif weather_temp <= 18:
        season = "autumn"
    elif weather_temp >= 28:
        season = "summer"
    
    checklist = {
        "season": season,
        "generated_at": now.strftime("%Y-%m-%d %H:%M"),
        "days": days,
        "summary": _generate_summary(days, season, weather_temp, has_rain, scenario),
        "categories": [],
        "tips": _generate_tips(days, season, weather_temp, has_rain),
    }
    
    clothing = SEASON_CLOTHING.get(season, SEASON_CLOTHING["spring"])
    days_multiplier = max(2, days + 1)
    
    clothing_items = []
    for item in clothing["inner"]:
        clothing_items.append({"name": item, "quantity": days_multiplier, "checked": False, "category": "穿着"})
    for item in clothing["bottom"]:
        clothing_items.append({"name": item, "quantity": max(2, (days + 2) // 2), "checked": False, "category": "穿着"})
    for item in clothing["outer"]:
        clothing_items.append({"name": item, "quantity": 1, "checked": False, "category": "穿着"})
    for item in clothing["shoes"]:
        clothing_items.append({"name": item, "quantity": 1, "checked": False, "category": "穿着"})
    for item in clothing["accessories"]:
        clothing_items.append({"name": item, "quantity": 1, "checked": False, "category": "配饰"})
    
    checklist["categories"].append({
        "name": "穿着衣物",
        "icon": "👕",
        "items": clothing_items,
    })
    
    personal_items = []
    for category, items in PERSONAL_ITEMS.items():
        for item in items:
            personal_items.append({"name": item, "quantity": 1, "checked": False, "category": "个人"})
    
    checklist["categories"].append({
        "name": "个人物品",
        "icon": "🎒",
        "items": personal_items,
    })
    
    if has_rain:
        rain_items = [
            {"name": "折叠雨伞", "quantity": 1, "checked": False, "category": "雨具"},
            {"name": "雨衣", "quantity": 1, "checked": False, "category": "雨具"},
            {"name": "防水鞋套", "quantity": 1, "checked": False, "category": "雨具"},
        ]
        checklist["categories"].append({
            "name": "雨具装备",
            "icon": "☔",
            "items": rain_items,
        })
    
    if scenario and scenario in SCENARIO_EXTRAS:
        scenario_items = []
        for item in SCENARIO_EXTRAS[scenario]:
            scenario_items.append({"name": item, "quantity": 1, "checked": False, "category": "特殊"})
        checklist["categories"].append({
            "name": f"{_scenario_label(scenario)}装备",
            "icon": _scenario_icon(scenario),
            "items": scenario_items,
        })
    
    if special_needs:
        special_items = []
        for need in special_needs:
            special_items.append({"name": need, "quantity": 1, "checked": False, "category": "特殊需求"})
        checklist["categories"].append({
            "name": "特殊需求",
            "icon": "✨",
            "items": special_items,
        })
    
    checklist["total_items"] = sum(len(cat["items"]) for cat in checklist["categories"])
    checklist["estimated_weight"] = _estimate_weight(checklist)
    
    return checklist


def _scenario_label(scenario: str) -> str:
    labels = {
        "beach": "海滩度假",
        "mountain": "登山徒步",
        "business": "商务出行",
        "family": "亲子家庭",
        "elderly": "老人随行",
        "hiking": "户外徒步",
        "photography": "摄影采风",
        "night_out": "夜生活",
    }
    return labels.get(scenario, scenario)


def _scenario_icon(scenario: str) -> str:
    icons = {
        "beach": "🏖️",
        "mountain": "🏔️",
        "business": "💼",
        "family": "👨‍👩‍👧",
        "elderly": "👴",
        "hiking": "🥾",
        "photography": "📷",
        "night_out": "🌃",
    }
    return icons.get(scenario, "✨")


def _generate_summary(days, season, weather_temp, has_rain, scenario):
    season_desc = {"spring": "春季", "summer": "夏季", "autumn": "秋季", "winter": "冬季"}
    summary = f"根据您{days}天的{season_desc.get(season, season)}出行"
    
    if weather_temp:
        summary += f"（预计气温{weather_temp}°C左右）"
    if has_rain:
        summary += "，有降雨可能"
    if scenario:
        summary += f"，{_scenario_label(scenario)}场景"
    
    return summary + "，为您智能生成以下行李清单"


def _generate_tips(days, season, weather_temp, has_rain):
    tips = [
        f"行程{days}天，建议选择24-28寸行李箱",
        "重要证件建议拍照备份到手机云端",
        "预留20%行李空间购买纪念品",
    ]
    
    if season == "summer" and weather_temp and weather_temp >= 30:
        tips.append("夏季衣物轻便，注意防晒降温")
    elif season == "winter":
        tips.append("冬季衣物厚重，建议使用真空压缩袋节省空间")
    
    if has_rain:
        tips.append("雨天出行，多备一双鞋和干袜子")
    
    if days >= 5:
        tips.append("行程较长，可带折叠洗衣袋和少量洗衣液")
    
    return tips


def _estimate_weight(checklist):
    total = 0
    for cat in checklist["categories"]:
        for item in cat["items"]:
            name = item["name"]
            if any(kw in name for kw in ["羽绒服", "棉服", "大衣"]):
                total += 2
            elif any(kw in name for kw in ["外套", "夹克"]):
                total += 1
            elif any(kw in name for kw in ["笔记本", "电脑", "相机"]):
                total += 1.5
            elif any(kw in name for kw in ["行李箱", "背包"]):
                total += 0
            else:
                total += 0.3
    return round(total, 1)
