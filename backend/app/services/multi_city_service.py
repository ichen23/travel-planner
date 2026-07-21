import asyncio
import random
from datetime import datetime, timedelta
from app.services.city_database import (
    CITY_COORDS, CITY_BASIC_INFO, get_high_speed_routes, 
    get_city_info, BEIJING_3HR_COORDS
)


CITY_STATIC_DATA = {
    "开封": {
        "attractions": [
            {"name": "清明上河园", "morning_start": "09:00", "duration_hours": 3, "ticket": "120元", "tips": "门票包含演出《东京梦华》非常震撼，建议下午场"},
            {"name": "龙亭公园", "morning_start": "13:30", "duration_hours": 2, "ticket": "50元", "tips": "皇家园林，可俯瞰开封古城"},
            {"name": "天波杨府", "morning_start": "15:30", "duration_hours": 1.5, "ticket": "60元", "tips": "杨家将府邸，了解北宋历史"},
            {"name": "大相国寺", "morning_start": "17:00", "duration_hours": 1, "ticket": "40元", "tips": "千年古刹，鲁智深倒拔垂杨柳旧址"},
        ],
        "food": [
            {"name": "第一楼灌汤包", "location": "寺后街", "price_range": "30-50元", "recommend": "猪肉灌汤包、蟹黄包"},
            {"name": "黄家老店", "location": "中山路", "price_range": "25-40元", "recommend": "开封传统小笼包"},
            {"name": "州桥夜市", "location": "中山路与自由路交叉口", "price_range": "20-30元", "recommend": "炒凉粉、花生糕、冰糖梨"},
        ],
        "transport": "市内公交发达，推荐购买公交卡；景点间距离不远，打车约10-20元",
        "tips": "开封景区集中在老城区，步行游览最方便；清明上河园建议游玩5-6小时"
    },
    "焦作": {
        "attractions": [
            {"name": "云台山", "morning_start": "07:00", "duration_hours": 6, "ticket": "210元（含观光车）", "tips": "世界地质公园，红石峡最美，建议早上出发避开人流"},
            {"name": "红石峡", "morning_start": "09:00", "duration_hours": 2.5, "ticket": "含在云台山门票内", "tips": "丹霞地貌，红色峡谷非常震撼"},
            {"name": "茱萸峰", "morning_start": "13:00", "duration_hours": 3, "ticket": "含在云台山门票内", "tips": "云台山主峰，海拔1308米，有玻璃栈道"},
            {"name": "陈家沟", "morning_start": "10:00", "duration_hours": 4, "ticket": "80元", "tips": "太极拳发源地，可体验太极文化"},
        ],
        "food": [
            {"name": "焦作老烩面", "location": "解放区", "price_range": "15-25元", "recommend": "羊汤烩面、牛肉烩面"},
            {"name": "武陟油茶", "location": "武陟县", "price_range": "10-15元", "recommend": "传统早餐，香浓可口"},
            {"name": "云台山野菜馆", "location": "景区门口", "price_range": "50-80元", "recommend": "山野菜、土鸡、土鸡蛋"},
        ],
        "transport": "云台山距市区40公里，有旅游专线车；景区内需乘观光车",
        "tips": "云台山建议玩2天，第一天红石峡+子房湖，第二天茱萸峰+玻璃栈道"
    },
    "洛阳": {
        "attractions": [
            {"name": "龙门石窟", "morning_start": "07:30", "duration_hours": 4, "ticket": "90元", "tips": "中国四大石窟之一，卢舍那大佛最壮观，早上光线好"},
            {"name": "白马寺", "morning_start": "12:30", "duration_hours": 2.5, "ticket": "50元", "tips": "中国第一古刹，佛教传入中原后建立的第一座寺庙"},
            {"name": "关林", "morning_start": "15:30", "duration_hours": 2, "ticket": "40元", "tips": "关羽陵庙，三国文化圣地"},
            {"name": "洛阳博物馆", "morning_start": "09:00", "duration_hours": 3, "ticket": "免费（需预约）", "tips": "馆藏丰富，唐三彩、青铜器、壁画是特色"},
            {"name": "应天门", "morning_start": "19:00", "duration_hours": 1.5, "ticket": "30元", "tips": "隋唐洛阳城的正南门，夜景很美"},
            {"name": "老君山", "morning_start": "06:30", "duration_hours": 6, "ticket": "100元", "tips": "道教名山，金顶日出非常震撼"}
        ],
        "food": [
            {"name": "真不同水席", "location": "老城区", "price_range": "80-120元/人", "recommend": "洛阳水席代表，牡丹燕菜、焦炸丸子"},
            {"name": "马杰山牛肉汤", "location": "瀍河区", "price_range": "15-25元", "recommend": "洛阳牛肉汤配烧饼"},
            {"name": "西工小街锅贴", "location": "西工区", "price_range": "10-15元", "recommend": "地道的洛阳锅贴"},
            {"name": "老城十字街夜市", "location": "老城区十字街", "price_range": "20-50元", "recommend": "不翻汤、炒酸奶、牡丹饼"},
        ],
        "transport": "地铁1、2号线覆盖主要景点；景区直通车串联龙门、关林、白马寺；共享单车适合短途",
        "tips": "洛阳博物馆周一闭馆；龙门石窟卢舍那大佛最佳观赏时间10-14点；4月牡丹花会期间人多"
    },
    "北京": {
        "attractions": [
            {"name": "天安门广场", "morning_start": "06:30", "duration_hours": 1, "ticket": "免费", "tips": "升旗仪式根据季节调整时间，提前查好"},
            {"name": "故宫博物院", "morning_start": "08:30", "duration_hours": 4, "ticket": "60元（需提前预约）", "tips": "必须提前7天预约，午门进神武门出"},
            {"name": "八达岭长城", "morning_start": "07:00", "duration_hours": 5, "ticket": "40元", "tips": "最经典的长城段，可乘缆车；提前在德胜门乘877路直达"},
            {"name": "颐和园", "morning_start": "09:00", "duration_hours": 3, "ticket": "30元联票60元", "tips": "皇家园林，长廊、佛香阁、十七孔桥是精华"},
            {"name": "天坛公园", "morning_start": "09:00", "duration_hours": 2, "ticket": "34元联票", "tips": "祈年殿、回音壁、圜丘坛是三大景点"},
            {"name": "南锣鼓巷", "morning_start": "14:00", "duration_hours": 2, "ticket": "免费", "tips": "北京最古老的胡同，有特色小店和美食"},
        ],
        "food": [
            {"name": "全聚德烤鸭", "location": "前门店", "price_range": "200-300元/人", "recommend": "挂炉烤鸭，配荷叶饼和甜面酱"},
            {"name": "炸酱面", "location": "海碗居", "price_range": "30-50元", "recommend": "老北京风味，六种菜码"},
            {"name": "簋街麻辣小龙虾", "location": "东城区簋街", "price_range": "80-120元", "recommend": "晚上最热闹，24小时营业"},
        ],
        "transport": "地铁发达，推荐购买亿通行APP；景点多在地铁沿线；打车高峰难拦",
        "tips": "故宫必须预约；长城建议早上出发避免人流；景区周边消费高"
    },
    "西安": {
        "attractions": [
            {"name": "秦始皇兵马俑", "morning_start": "07:30", "duration_hours": 4, "ticket": "120元", "tips": "必看一号坑，推荐请讲解（200元）；可乘地铁9号线直达"},
            {"name": "大雁塔", "morning_start": "13:30", "duration_hours": 2, "ticket": "40元", "tips": "西安地标，晚上有音乐喷泉表演"},
            {"name": "西安城墙", "morning_start": "15:30", "duration_hours": 2.5, "ticket": "54元", "tips": "可租自行车骑行一圈（1小时）；南门夜景最美"},
            {"name": "回民街", "morning_start": "18:00", "duration_hours": 2, "ticket": "免费", "tips": "西安最著名的美食街，晚上最热闹"},
            {"name": "华清宫", "morning_start": "08:30", "duration_hours": 3, "ticket": "120元", "tips": "唐玄宗与杨贵妃的行宫，骊山脚下"},
        ],
        "food": [
            {"name": "老孙家泡馍", "location": "回民街", "price_range": "25-35元", "recommend": "牛羊肉泡馍，馍要自己掰"},
            {"name": "肉夹馍", "location": "子午路张记", "price_range": "10-15元", "recommend": "腊汁肉夹馍，白吉馍夹腊汁肉"},
            {"name": "回民街小吃", "location": "北院门", "price_range": "20-50元", "recommend": "镜糕、柿子饼、甑糕、黄桂稠酒"},
        ],
        "transport": "地铁覆盖主要景点；景区直通车串联兵马俑、华清宫；市内打车方便",
        "tips": "兵马俑建议请讲解；回民街美食多但要注意卫生；城墙骑行看个人体力"
    },
    "郑州": {
        "attractions": [
            {"name": "少林寺", "morning_start": "07:00", "duration_hours": 6, "ticket": "80元", "tips": "天下武功出少林，塔林、藏经阁是重点；距市区70公里"},
            {"name": "黄河风景名胜区", "morning_start": "08:00", "duration_hours": 4, "ticket": "60元", "tips": "看黄河奔流，炎黄二帝雕像壮观；可乘索道上山"},
            {"name": "河南博物院", "morning_start": "09:00", "duration_hours": 3, "ticket": "免费（需预约）", "tips": "馆藏丰富，莲鹤方壶、妇好鸮尊是镇馆之宝"},
            {"name": "二七纪念塔", "morning_start": "15:00", "duration_hours": 1, "ticket": "免费", "tips": "郑州地标，可登塔俯瞰市区"},
        ],
        "food": [
            {"name": "合记烩面", "location": "人民路", "price_range": "20-30元", "recommend": "郑州烩面代表，羊肉烩面"},
            {"name": "老蔡记蒸饺", "location": "德化街", "price_range": "25-40元", "recommend": "郑州传统名吃，皮薄馅大"},
            {"name": "方中山胡辣汤", "location": "紫荆山", "price_range": "15-20元", "recommend": "河南胡辣汤代表，配油条吃"},
        ],
        "transport": "地铁1、2号线覆盖市区；少林寺有旅游专线车；黄河景区在北郊",
        "tips": "少林寺距市区远，建议一日游；河南博物院周一闭馆"
    },
    "杭州": {
        "attractions": [
            {"name": "西湖", "morning_start": "07:00", "duration_hours": 4, "ticket": "免费", "tips": "断桥残雪、苏堤春晓、三潭印月必看；可租自行车环湖"},
            {"name": "灵隐寺", "morning_start": "06:30", "duration_hours": 3, "ticket": "75元（含飞来峰）", "tips": "江南著名古刹，飞来峰石窟艺术精美"},
            {"name": "千岛湖", "morning_start": "07:00", "duration_hours": 8, "ticket": "150元（含船票）", "tips": "国家5A级景区，坐船游览多个岛屿；距市区150公里"},
            {"name": "龙井村", "morning_start": "10:00", "duration_hours": 2, "ticket": "免费", "tips": "龙井茶原产地，可品茶看茶园"},
            {"name": "河坊街", "morning_start": "14:00", "duration_hours": 2, "ticket": "免费", "tips": "杭州特色商业街，有传统小吃和工艺品"},
        ],
        "food": [
            {"name": "楼外楼", "location": "孤山路", "price_range": "150-250元/人", "recommend": "西湖醋鱼、东坡肉、龙井虾仁"},
            {"name": "知味观", "location": "仁和路", "price_range": "50-80元", "recommend": "片儿川、定胜糕、猫耳朵"},
            {"name": "外婆家", "location": "湖滨银泰", "price_range": "60-100元", "recommend": "杭州家常菜代表"},
        ],
        "transport": "地铁覆盖主要景点；西湖景区内有观光车；共享单车适合短途",
        "tips": "西湖景区大，建议分2天玩；千岛湖建议跟团或自驾"
    },
    "成都": {
        "attractions": [
            {"name": "宽窄巷子", "morning_start": "09:00", "duration_hours": 2, "ticket": "免费", "tips": "成都老巷子改造，有茶馆和小吃"},
            {"name": "锦里", "morning_start": "11:00", "duration_hours": 2, "ticket": "免费", "tips": "三国文化主题街区，晚上有表演"},
            {"name": "大熊猫繁育研究基地", "morning_start": "07:30", "duration_hours": 4, "ticket": "55元", "tips": "必去！建议早上看熊猫最活跃；距市区10公里"},
            {"name": "都江堰", "morning_start": "07:00", "duration_hours": 6, "ticket": "80元", "tips": "世界文化遗产，古代水利工程；距市区60公里"},
            {"name": "武侯祠", "morning_start": "14:00", "duration_hours": 2, "ticket": "50元", "tips": "三国文化圣地，纪念诸葛亮"},
        ],
        "food": [
            {"name": "陈麻婆豆腐", "location": "青华路", "price_range": "30-50元", "recommend": "正宗麻婆豆腐，麻辣鲜香"},
            {"name": "龙抄手", "location": "春熙路", "price_range": "20-30元", "recommend": "红油抄手、清汤抄手"},
            {"name": "宽窄巷子小吃", "location": "宽窄巷子", "price_range": "20-40元", "recommend": "三大炮、糖油果子、蛋烘糕"},
            {"name": "小龙坎火锅", "location": "春熙路", "price_range": "100-150元/人", "recommend": "成都火锅代表，排队火爆"},
        ],
        "transport": "地铁覆盖市区主要景点；大熊猫基地有旅游专线；都江堰可乘城际铁路",
        "tips": "熊猫基地早上熊猫最活跃；成都美食多但偏辣，注意肠胃"
    }
}

TRAIN_TEMPLATES = [
    {"type": "G", "name": "高速动车组"},
    {"type": "D", "name": "动车组"},
    {"type": "C", "name": "城际列车"},
]

CITY_PAIR_TRAINS = {
    ("开封", "郑州"): {"duration_min": 30, "price": 50, "train_types": ["G", "C"]},
    ("郑州", "开封"): {"duration_min": 30, "price": 50, "train_types": ["G", "C"]},
    ("郑州", "焦作"): {"duration_min": 40, "price": 70, "train_types": ["G", "C"]},
    ("焦作", "郑州"): {"duration_min": 40, "price": 70, "train_types": ["G", "C"]},
    ("郑州", "洛阳"): {"duration_min": 45, "price": 80, "train_types": ["G", "D"]},
    ("洛阳", "郑州"): {"duration_min": 45, "price": 80, "train_types": ["G", "D"]},
    ("开封", "洛阳"): {"duration_min": 60, "price": 100, "train_types": ["G"]},
    ("洛阳", "开封"): {"duration_min": 60, "price": 100, "train_types": ["G"]},
    ("焦作", "洛阳"): {"duration_min": 90, "price": 150, "train_types": ["G", "D"]},
    ("洛阳", "焦作"): {"duration_min": 90, "price": 150, "train_types": ["G", "D"]},
    ("北京", "郑州"): {"duration_min": 150, "price": 300, "train_types": ["G"]},
    ("郑州", "北京"): {"duration_min": 150, "price": 300, "train_types": ["G"]},
    ("北京", "开封"): {"duration_min": 180, "price": 350, "train_types": ["G"]},
    ("开封", "北京"): {"duration_min": 180, "price": 350, "train_types": ["G"]},
    ("北京", "西安"): {"duration_min": 240, "price": 500, "train_types": ["G"]},
    ("西安", "北京"): {"duration_min": 240, "price": 500, "train_types": ["G"]},
    ("北京", "济南"): {"duration_min": 90, "price": 200, "train_types": ["G"]},
    ("济南", "北京"): {"duration_min": 90, "price": 200, "train_types": ["G"]},
    ("上海", "杭州"): {"duration_min": 45, "price": 70, "train_types": ["G", "C"]},
    ("杭州", "上海"): {"duration_min": 45, "price": 70, "train_types": ["G", "C"]},
    ("上海", "苏州"): {"duration_min": 30, "price": 50, "train_types": ["G", "C"]},
    ("苏州", "上海"): {"duration_min": 30, "price": 50, "train_types": ["G", "C"]},
    ("广州", "深圳"): {"duration_min": 30, "price": 80, "train_types": ["G", "C"]},
    ("深圳", "广州"): {"duration_min": 30, "price": 80, "train_types": ["G", "C"]},
    ("成都", "重庆"): {"duration_min": 120, "price": 250, "train_types": ["G"]},
    ("重庆", "成都"): {"duration_min": 120, "price": 250, "train_types": ["G"]},
    ("西安", "洛阳"): {"duration_min": 90, "price": 180, "train_types": ["G"]},
    ("洛阳", "西安"): {"duration_min": 90, "price": 180, "train_types": ["G"]},
}


def get_train_info(from_city: str, to_city: str) -> dict:
    key = (from_city, to_city)
    if key in CITY_PAIR_TRAINS:
        info = CITY_PAIR_TRAINS[key]
        train_type = random.choice(info["train_types"])
        train_num = f"{train_type}{random.randint(1, 9999)}"
        return {
            "train_number": train_num,
            "type": TRAIN_TEMPLATES[0]["type"] if train_type == "G" else 
                   TRAIN_TEMPLATES[1]["type"] if train_type == "D" else "C",
            "type_name": "高铁" if train_type == "G" else "动车" if train_type == "D" else "城际",
            "duration_min": info["duration_min"],
            "duration_text": f"{info['duration_min'] // 60}小时{info['duration_min'] % 60}分" if info['duration_min'] >= 60 else f"{info['duration_min']}分钟",
            "price": info["price"],
        }
    else:
        estimated_min = random.randint(90, 240)
        return {
            "train_number": f"G{random.randint(1, 9999)}",
            "type": "G",
            "type_name": "高铁",
            "duration_min": estimated_min,
            "duration_text": f"{estimated_min // 60}小时{estimated_min % 60}分",
            "price": estimated_min * 2,
            "note": "建议在12306查询准确车次"
        }


def format_time(hour: int, minute: int = 0) -> str:
    return f"{int(hour):02d}:{int(minute):02d}"


def add_minutes(time_str: str, minutes: int) -> str:
    h, m = map(int, time_str.split(":"))
    total_min = h * 60 + m + minutes
    return format_time(total_min // 60 % 24, total_min % 60)


def generate_city_day_plan(city: str, day_index: int, attractions_count: int = 3) -> dict:
    city_data = CITY_STATIC_DATA.get(city, {})
    attractions = city_data.get("attractions", [])
    
    if not attractions:
        return None
    
    selected_attractions = random.sample(attractions, min(attractions_count, len(attractions)))
    
    schedule = []
    current_time = 8
    
    for i, attr in enumerate(selected_attractions):
        start_time_str = attr.get("morning_start", format_time(current_time))
        h, m = map(int, start_time_str.split(":"))
        duration = attr.get("duration_hours", 2)
        
        schedule.append({
            "type": "attraction",
            "name": attr["name"],
            "start_time": start_time_str,
            "end_time": format_time(h + duration, m),
            "duration_hours": duration,
            "ticket": attr.get("ticket", "以实际为准"),
            "tips": attr.get("tips", ""),
            "icon": "🏛️"
        })
        
        current_time = h + duration + 1
    
    foods = city_data.get("food", [])
    if foods:
        lunch = foods[0]
        dinner = foods[-1] if len(foods) > 1 else foods[0]
        
        schedule.insert(1, {
            "type": "food",
            "name": f"午餐：{lunch['name']}",
            "start_time": "12:00",
            "end_time": "13:00",
            "location": lunch.get("location", ""),
            "price_range": lunch.get("price_range", ""),
            "recommend": lunch.get("recommend", ""),
            "icon": "🍜"
        })
        
        schedule.append({
            "type": "food",
            "name": f"晚餐：{dinner['name']}",
            "start_time": "18:00",
            "end_time": "19:30",
            "location": dinner.get("location", ""),
            "price_range": dinner.get("price_range", ""),
            "recommend": dinner.get("recommend", ""),
            "icon": "🍲"
        })
    
    schedule.sort(key=lambda x: x["start_time"])
    
    return {
        "day": day_index,
        "city": city,
        "date_label": f"第{day_index}天",
        "transport_tips": city_data.get("transport", ""),
        "city_tips": city_data.get("tips", ""),
        "schedule": schedule
    }


def calculate_city_budget(city: str, days: int, budget_per_day: float = 400) -> dict:
    city_data = CITY_STATIC_DATA.get(city, {})
    attractions = city_data.get("attractions", [])
    
    ticket_cost = 0
    for attr in attractions[:days * 2]:
        ticket = attr.get("ticket", "")
        if ticket and ticket != "免费" and ticket != "免费（需预约）":
            clean_ticket = ticket.replace("元", "").replace("（含观光车）", "").replace("（需预约）", "0").split("(")[0].strip()
            try:
                ticket_cost += int(clean_ticket)
            except:
                pass
    
    return {
        "ticket": ticket_cost,
        "food": budget_per_day * days * 0.4,
        "transport": budget_per_day * days * 0.2,
        "other": budget_per_day * days * 0.4,
        "total": ticket_cost + budget_per_day * days
    }


async def generate_multi_city_itinerary(cities: list, day_allocation: list, 
                                         budget: float, preference: str = "") -> dict:
    if len(cities) < 2:
        return {"success": False, "message": "至少需要2个城市"}
    
    total_days = sum(day_allocation)
    budget_per_day = budget / total_days
    days_schedule = []
    transfer_segments = []
    day_counter = 1
    
    city_budgets = {}
    
    for i, city in enumerate(cities):
        city_days = day_allocation[i]
        city_budgets[city] = calculate_city_budget(city, city_days, budget_per_day)
        
        if i > 0:
            prev_city = cities[i-1]
            train_info = get_train_info(prev_city, city)
            
            prev_day = days_schedule[-1]
            prev_end_time = "19:30" if prev_day["schedule"][-1]["type"] == "food" else "18:00"
            
            transfer_start = "20:00"
            train_end_min = train_info["duration_min"]
            train_end_h = 20 + train_end_min // 60
            train_end_m = train_end_min % 60
            transfer_end = f"{train_end_h:02d}:{train_end_m:02d}" if train_end_h < 24 else f"{train_end_h - 24:02d}:{train_end_m:02d}"
            
            transfer_segments.append({
                "from_city": prev_city,
                "to_city": city,
                "day": day_counter,
                "departure": transfer_start,
                "arrival": transfer_end,
                **train_info
            })
            
            days_schedule.append({
                "day": day_counter,
                "city": prev_city,
                "date_label": f"第{day_counter}天",
                "is_transfer_day": True,
                "transfer_info": transfer_segments[-1],
                "schedule": [
                    {"type": "food", "name": f"在{prev_city}的最后一晚", "start_time": "17:30", "end_time": "19:00", "icon": "🍜"},
                    {"type": "transport", "name": f"{prev_city}站集合乘车", "start_time": "19:30", "end_time": transfer_start, "icon": "🚄"},
                    {"type": "transport", "name": f"{train_info['train_number']}次 {prev_city}→{city}", "start_time": transfer_start, "end_time": transfer_end, "duration": train_info["duration_text"], "icon": "🚄"},
                ]
            })
            day_counter += 1
            city_days -= 1
        
        for d in range(city_days):
            day_plan = generate_city_day_plan(city, day_counter, min(3 + d, 5))
            if day_plan:
                day_plan["is_transfer_day"] = False
                days_schedule.append(day_plan)
                day_counter += 1
    
    total_transfer_cost = sum(t["price"] for t in transfer_segments)
    
    return {
        "success": True,
        "cities": cities,
        "day_allocation": day_allocation,
        "total_days": total_days,
        "total_budget": budget,
        "budget_breakdown": {
            "accommodation": budget * 0.4,
            "food": budget * 0.25,
            "transport": budget * 0.2 + total_transfer_cost,
            "tickets": budget * 0.1,
            "other": budget * 0.05
        },
        "city_budgets": city_budgets,
        "transfer_segments": transfer_segments,
        "days": days_schedule,
        "tips": [
            "提前7-14天预订高铁票可享受优惠",
            "携带舒适的鞋子，每天步行较多",
            "准备充电宝，随时拍照记录",
            "关注天气预报，合理安排室内外景点",
            "每个城市推荐1-2个必去景点，不要贪多"
        ],
        "packing_list": get_packing_suggestions(cities),
        "generated_at": datetime.now().isoformat()
    }


def get_packing_suggestions(cities: list) -> dict:
    base_items = ["身份证/护照", "手机充电器/充电宝", "舒适的步行鞋", "轻便外套", "洗漱用品", "常用药品", "雨伞"]
    seasonal_items = []
    optional_items = []
    
    hot_cities = ["郑州", "武汉", "重庆", "杭州", "成都"]
    cultural_cities = ["洛阳", "西安", "开封", "北京", "南京"]
    nature_cities = ["焦作", "杭州", "成都", "张家界", "桂林"]
    
    has_hot = any(c in hot_cities for c in cities)
    has_cultural = any(c in cultural_cities for c in cities)
    has_nature = any(c in nature_cities for c in cities)
    
    if has_hot:
        seasonal_items.extend(["防晒霜", "遮阳帽", "清凉衣物"])
    if has_cultural:
        optional_items.extend(["汉服/古装（拍照用）", "文化书籍/攻略"])
    if has_nature:
        optional_items.extend(["登山鞋", "背包", "相机/望远镜"])
    
    return {
        "必带物品": base_items,
        "季节推荐": seasonal_items,
        "可选物品": optional_items
    }
