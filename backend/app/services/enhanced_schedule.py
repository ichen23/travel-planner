"""
增强版多城市行程生成服务
- 智能时间安排（根据景区开放时间和游玩时长）
- 完整行程（起床、睡觉、酒店、美食等）
- 景点详情
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random


ATTRACTION_DETAILS = {
    "故宫博物院": {
        "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一。",
        "best_time": "上午8:30-11:30",
        "visit_duration": "3-4小时",
        "tips": "需提前预约，建议走午门进入，神武门出。避开节假日人流高峰。",
        "ticket": "旺季60元/淡季40元",
        "open_hours": "旺季8:30-17:00/淡季8:30-16:30"
    },
    "天安门广场": {
        "description": "世界上最大的城市广场之一，是中华人民共和国的象征。",
        "best_time": "清晨或傍晚",
        "visit_duration": "1-2小时",
        "tips": "可观看升旗仪式，需提前查询时间。安检严格，建议轻装前往。",
        "ticket": "免费（需预约）",
        "open_hours": "全天开放"
    },
    "长城": {
        "description": "万里长城是世界上最伟大的建筑奇迹之一，北京段包括八达岭、慕田峪、司马台等。",
        "best_time": "上午9:00-12:00或下午14:00-17:00",
        "visit_duration": "3-5小时",
        "tips": "推荐慕田峪，人少景美。长城陡峭处多，穿舒适鞋子。带足够水和防晒。",
        "ticket": "40-60元不等",
        "open_hours": "7:30-17:30"
    },
    "西湖": {
        "description": "杭州西湖是世界文化遗产，以秀丽的湖光山色和众多的名胜古迹闻名中外。",
        "best_time": "清晨或傍晚",
        "visit_duration": "半天到一天",
        "tips": "可租自行车环湖，推荐雷峰塔、三潭印月、断桥残雪等景点。",
        "ticket": "免费（部分景点收费）",
        "open_hours": "全天开放"
    },
    "灵隐寺": {
        "description": "杭州最早的名刹，被誉为东南佛国第一名刹。",
        "best_time": "上午8:00-11:00",
        "visit_duration": "2-3小时",
        "tips": "需购买飞来峰门票后入寺，早上人少清净。",
        "ticket": "飞来峰45元+灵隐寺香花券30元",
        "open_hours": "7:00-18:00"
    },
    "拙政园": {
        "description": "中国四大名园之一，世界文化遗产，江南园林的典范。",
        "best_time": "上午8:30-11:30",
        "visit_duration": "2-3小时",
        "tips": "淡季人少，可细细品味园林之美。",
        "ticket": "旺季80元/淡季50元",
        "open_hours": "7:30-17:30"
    },
    "兵马俑": {
        "description": "世界第八大奇迹，秦始皇陵的陪葬坑，已发掘三个坑。",
        "best_time": "上午8:30-12:00",
        "visit_duration": "3-4小时",
        "tips": "建议请讲解，1号坑最大最壮观，3号坑是指挥所。",
        "ticket": "120元",
        "open_hours": "3月-11月 8:30-18:00/12月-2月 8:30-17:30"
    },
    "大雁塔": {
        "description": "西安地标，唐代玄奘法师为保存经卷而建。",
        "best_time": "傍晚看音乐喷泉",
        "visit_duration": "1-2小时",
        "tips": "北广场有亚洲最大的音乐喷泉，晚上表演值得一看。",
        "ticket": "50元/登塔30元",
        "open_hours": "8:00-17:30"
    },
    "外滩": {
        "description": "上海地标，万国建筑博览群，与陆家嘴隔江相望。",
        "best_time": "傍晚或夜景",
        "visit_duration": "1-2小时",
        "tips": "晚上灯光最美，可坐渡轮过江到浦东。",
        "ticket": "免费",
        "open_hours": "全天开放"
    },
    "东方明珠": {
        "description": "上海标志性建筑，观光塔高468米。",
        "best_time": "傍晚看日落和夜景",
        "visit_duration": "1-2小时",
        "tips": "推荐上旋转餐厅或悬空观光廊。",
        "ticket": "160-220元",
        "open_hours": "8:00-21:30"
    },
    "布达拉宫": {
        "description": "世界屋脊上的宫殿，藏传佛教的圣地，世界文化遗产。",
        "best_time": "上午9:00-12:00",
        "visit_duration": "3-4小时",
        "tips": "需提前1天预约，带身份证，殿内不能拍照。高反严重者慎入。",
        "ticket": "200元",
        "open_hours": "9:00-16:30（闭馆前1小时停止进入）"
    },
    "鼓浪屿": {
        "description": "厦门必去，素有海上花园之称，万国建筑博物馆。",
        "best_time": "全天",
        "visit_duration": "半天到一天",
        "tips": "需从东渡邮轮码头坐船，岛上无车，步行游览。",
        "ticket": "船票35元/景点套票90元",
        "open_hours": "全天开放"
    },
    "九寨沟": {
        "description": "人间仙境，世界自然遗产，以翠海、叠瀑、彩林、雪峰、藏情、蓝冰六绝著称。",
        "best_time": "10月金秋",
        "visit_duration": "1-2天",
        "tips": "实行单日进沟，建议住沟口或漳扎镇。海拔较高，注意防高反。",
        "ticket": "旺季190元/淡季80元+观光车90元",
        "open_hours": "7:00-17:00"
    },
    "香格里拉": {
        "description": "世外桃源，有普达措、松赞林寺等景点。",
        "best_time": "5-7月或9-10月",
        "visit_duration": "2-3天",
        "tips": "海拔3300米，注意高原反应。可包车或跟团游。",
        "ticket": "普达措100元/松赞林寺90元",
        "open_hours": "8:00-18:00"
    },
    "丽江古城": {
        "description": "世界文化遗产，纳西族文化古镇，家家流水户户种花。",
        "best_time": "晚上逛古城",
        "visit_duration": "半天到一天",
        "tips": "需缴纳古城维护费50元。推荐去黑龙潭、木府。",
        "ticket": "免费（需古城维护费）",
        "open_hours": "全天开放"
    },
    "大理古城": {
        "description": "风花雪月之城，苍山洱海相伴。",
        "best_time": "全天",
        "visit_duration": "1-2天",
        "tips": "可租电动车环洱海，推荐喜洲古镇、双廊。",
        "ticket": "免费",
        "open_hours": "全天开放"
    },
    "张家界": {
        "description": "世界自然遗产，以石英砂岩峰林地貌闻名，阿凡达取景地。",
        "best_time": "雨后或日出",
        "visit_duration": "2-3天",
        "tips": "推荐森林公园、天门山、大峡谷玻璃桥。",
        "ticket": "225元（4天有效）",
        "open_hours": "7:00-18:00"
    },
    "黄山": {
        "description": "天下第一奇山，以奇松、怪石、云海、温泉四绝著称。",
        "best_time": "日出日落",
        "visit_duration": "2天",
        "tips": "建议山顶住宿看日出，冬季有雪景。",
        "ticket": "旺季190元/淡季150元",
        "open_hours": "6:00-18:00"
    },
    "泰山": {
        "description": "五岳之首，历代帝王封禅之地。",
        "best_time": "日出",
        "visit_duration": "1-2天",
        "tips": "可夜爬看日出，红门登山口最经典。",
        "ticket": "115元",
        "open_hours": "全天开放"
    },
    "峨眉山": {
        "description": "佛教名山，与乐山大佛一起列入世界文化与自然双重遗产。",
        "best_time": "云海日出",
        "visit_duration": "2-3天",
        "tips": "推荐住山顶金顶看日出，可能遇到野生猴子。",
        "ticket": "160元",
        "open_hours": "6:00-18:00"
    },
    "平遥古城": {
        "description": "保存最完整的古代县城，世界文化遗产，晋商文化发源地。",
        "best_time": "全天",
        "visit_duration": "1-2天",
        "tips": "购买通票可游览城内20多个景点。",
        "ticket": "125元",
        "open_hours": "8:00-18:00"
    },
    "周庄": {
        "description": "中国第一水乡，江南六大古镇之首。",
        "best_time": "清晨或傍晚",
        "visit_duration": "1天",
        "tips": "推荐乘船游览，品尝万三蹄。",
        "ticket": "100元",
        "open_hours": "8:00-21:00"
    },
    "乌镇": {
        "description": "枕水人家，江南水乡典范，分东西栅。",
        "best_time": "西栅夜景",
        "visit_duration": "1-2天",
        "tips": "东栅原汁原味，西栅夜景最美。",
        "ticket": "东栅110元/西栅150元",
        "open_hours": "7:00-18:00（西栅到22:00）"
    },
    "凤凰古城": {
        "description": "中国最美小城，沱江边的苗族古镇。",
        "best_time": "晚上",
        "visit_duration": "1-2天",
        "tips": "推荐坐沱江游船，体验苗族风情。",
        "ticket": "免费",
        "open_hours": "全天开放"
    },
    "鼓浪屿": {
        "description": "海上花园，万国建筑博物馆。",
        "best_time": "全天",
        "visit_duration": "1天",
        "tips": "需坐船前往，岛上无车。",
        "ticket": "船票35元",
        "open_hours": "全天开放"
    },
    "武夷山": {
        "description": "世界文化与自然双重遗产，丹霞地貌典范。",
        "best_time": "九曲溪漂流",
        "visit_duration": "2天",
        "tips": "推荐九曲溪竹筏漂流，晚上看《印象大红袍》。",
        "ticket": "140元+竹筏100元",
        "open_hours": "6:30-18:00"
    },
    "桂林漓江": {
        "description": "桂林山水甲天下，漓江是精华。",
        "best_time": "晴天",
        "visit_duration": "4-5小时",
        "tips": "推荐杨堤到兴坪精华段，或竹筏游览。",
        "ticket": "215元（含餐）",
        "open_hours": "8:00-18:00"
    },
    "三亚亚龙湾": {
        "description": "天下第一湾，拥有7千米长的银白色海滩。",
        "best_time": "10月-次年4月",
        "visit_duration": "半天到一天",
        "tips": "沙白水清，适合潜水、游泳。",
        "ticket": "免费",
        "open_hours": "全天开放"
    },
    "香格里拉普达措": {
        "description": "国家公园，中国第一个国家公园，高原湖泊、草甸、森林。",
        "best_time": "5-7月",
        "visit_duration": "4-5小时",
        "tips": "海拔3700米，注意高反。穿防水鞋。",
        "ticket": "100元+观光车120元",
        "open_hours": "7:30-16:00"
    },
    "千岛湖": {
        "description": "天下第一秀水，1078个岛屿星罗棋布。",
        "best_time": "晴天",
        "visit_duration": "1-2天",
        "tips": "推荐中心湖区，坐船游览各岛屿。",
        "ticket": "150元（含船票）",
        "open_hours": "8:00-17:00"
    },
    "莫干山": {
        "description": "江南第一山，避暑胜地，民国老别墅群。",
        "best_time": "夏季",
        "visit_duration": "1-2天",
        "tips": "推荐住特色民宿，体验竹海风光。",
        "ticket": "80元",
        "open_hours": "8:00-17:00"
    },
    "雁荡山": {
        "description": "东南第一山，海上名山。",
        "best_time": "灵峰夜景",
        "visit_duration": "2天",
        "tips": "推荐灵峰、灵岩、大龙湫景区。",
        "ticket": "各景点30-50元",
        "open_hours": "8:00-17:00"
    },
    "横店影视城": {
        "description": "东方好莱坞，世界最大的影视拍摄基地。",
        "best_time": "全天",
        "visit_duration": "2-3天",
        "tips": "推荐买联票，明清宫苑、清明上河图、秦王宫必去。",
        "ticket": "联票480元",
        "open_hours": "8:00-17:00"
    },
    "普陀山": {
        "description": "中国四大佛教名山之一，观音道场。",
        "best_time": "早上烧香",
        "visit_duration": "1-2天",
        "tips": "需坐船前往，推荐住岛上。",
        "ticket": "160元（旺季）",
        "open_hours": "6:00-21:00"
    },
    "千岛湖": {
        "description": "天下第一秀水",
        "best_time": "晴天",
        "visit_duration": "1天",
        "tips": "推荐坐船游中心湖区",
        "ticket": "150元含船票",
        "open_hours": "8:00-17:00"
    },
    "鼓浪屿菽庄花园": {
        "description": "海上花园，钢琴博物馆所在地。",
        "best_time": "下午",
        "visit_duration": "1小时",
        "tips": "拍照好去处，面朝大海。",
        "ticket": "30元",
        "open_hours": "8:00-17:30"
    },
}


HOTELS_BY_CITY = {
    "北京": {"luxury": "北京饭店/王府半岛/瑰丽", "mid_range": "全季/桔子水晶/如家精选", "budget": "7天/汉庭"},
    "上海": {"luxury": "外滩华尔道夫/丽思卡尔顿/和平饭店", "mid_range": "亚朵/桔子水晶", "budget": "7天/锦江之星"},
    "杭州": {"luxury": "西湖国宾馆/安缦法云", "mid_range": "亚朵/全季", "budget": "7天/汉庭"},
    "西安": {"luxury": "W酒店/威斯汀", "mid_range": "全季/如家精选", "budget": "7天/锦江之星"},
    "成都": {"luxury": "丽思卡尔顿/香格里拉", "mid_range": "亚朵/全季", "budget": "7天/汉庭"},
    "重庆": {"luxury": "解放碑威斯汀/洲际", "mid_range": "亚朵/全季", "budget": "7天"},
    "厦门": {"luxury": "厦门希尔顿/康莱德", "mid_range": "全季/桔子", "budget": "7天"},
    "广州": {"luxury": "四季/丽思卡尔顿", "mid_range": "亚朵/全季", "budget": "7天"},
    "深圳": {"luxury": "四季/柏悦", "mid_range": "亚朵/全季", "budget": "7天"},
    "南京": {"luxury": "金陵饭店/威斯汀", "mid_range": "全季/桔子水晶", "budget": "7天"},
    "苏州": {"luxury": "金鸡湖凯宾斯基/香格里拉", "mid_range": "全季/亚朵", "budget": "7天"},
    "丽江": {"luxury": "悦榕庄/古城花间堂", "mid_range": "精品客栈", "budget": "青旅"},
    "大理": {"luxury": "洱海天域/安缦", "mid_range": "海景客栈", "budget": "青旅"},
    "三亚": {"luxury": "亚特兰蒂斯/太阳湾柏悦", "mid_range": "全季/海景酒店", "budget": "家庭旅馆"},
    "桂林": {"luxury": "香格里拉/阳朔悦榕庄", "mid_range": "全季/精选酒店", "budget": "7天"},
    "拉萨": {"luxury": "瑞吉/洲际", "mid_range": "全季/阳光酒店", "budget": "青旅"},
    "洛阳": {"luxury": "钼都利豪/友谊宾馆", "mid_range": "全季/如家精选", "budget": "7天"},
    "开封": {"luxury": "开元名都/中州国际", "mid_range": "全季/如家", "budget": "7天"},
    "郑州": {"luxury": "建业艾美/JW万豪", "mid_range": "全季/亚朵", "budget": "7天"},
    "杭州": {"luxury": "西湖国宾馆/安缦法云", "mid_range": "亚朵/全季", "budget": "7天/汉庭"},
}


LOCAL_FOOD = {
    "北京": ["北京烤鸭", "炸酱面", "豆汁焦圈", "涮羊肉", "卤煮火烧"],
    "上海": ["小笼包", "本帮红烧肉", "生煎", "蟹黄面", "上海菜饭"],
    "杭州": ["西湖醋鱼", "东坡肉", "龙井虾仁", "叫花鸡", "片儿川"],
    "成都": ["火锅", "串串香", "川菜", "担担面", "龙抄手"],
    "重庆": ["火锅", "小面", "酸辣粉", "江湖菜", "毛血旺"],
    "西安": ["肉夹馍", "羊肉泡馍", "凉皮", "biangbiang面", "甑糕"],
    "广州": ["早茶", "烧腊", "肠粉", "糖水", "煲仔饭"],
    "厦门": ["沙茶面", "土笋冻", "海蛎煎", "花生汤", "姜母鸭"],
    "南京": ["盐水鸭", "鸭血粉丝汤", "小笼包", "酸菜鱼", "牛肉锅贴"],
    "苏州": ["松鼠桂鱼", "响油鳝糊", "苏式汤面", "生煎", "奥灶面"],
    "洛阳": ["洛阳水席", "牛肉汤", "驴肉汤", "不翻汤", "牡丹饼"],
    "开封": ["灌汤包", "桶子鸡", "花生糕", "炒凉粉", "大宋切糕"],
    "郑州": ["烩面", "胡辣汤", "油馍头", "蒸饺", "大盘鸡"],
    "长沙": ["臭豆腐", "辣椒炒肉", "糖油粑粑", "口味虾", "剁椒鱼头"],
    "武汉": ["热干面", "周黑鸭", "三鲜豆皮", "武昌鱼", "面窝"],
    "丽江": ["纳西烤鱼", "腊排骨火锅", "丽江粑粑", "鸡豆凉粉", "米灌肠"],
    "大理": ["白族土八碗", "生皮", "乳扇", "饵丝", "砂锅鱼"],
    "三亚": ["海南鸡饭", "海鲜", "椰子鸡", "清补凉", "竹筒饭"],
    "桂林": ["桂林米粉", "啤酒鱼", "荔浦芋扣肉", "田螺酿", "恭城油茶"],
    "拉萨": ["藏面", "酥油茶", "糌粑", "藏猪", "牦牛肉"],
}


TRANSPORT_TIPS = {
    "北京": "地铁发达，办交通卡或用APP乘车码。景点间地铁方便。",
    "上海": "地铁覆盖全，外滩、陆家嘴步行可达。",
    "杭州": "地铁+公交，西湖周边可骑行。",
    "西安": "地铁覆盖主要景点，兵马俑需坐专线车。",
    "成都": "地铁发达，熊猫基地可坐地铁3号线。",
    "重庆": "轻轨穿楼很有特色，注意导航（山城高低差）。",
    "厦门": "公交方便，鼓浪屿需坐船。",
    "广州": "地铁发达，早茶文化丰富。",
    "深圳": "地铁+公交，市区景点集中。",
    "南京": "地铁发达，景点多在市区。",
    "苏州": "地铁+公交，古镇可坐大巴。",
    "洛阳": "公交覆盖主要景点，龙门石窟可坐专线。",
    "开封": "景点集中，步行或公交可达。",
    "郑州": "地铁+公交，少林寺可坐大巴。",
    "丽江": "古城内步行，束河、玉龙雪山需打车或包车。",
    "大理": "推荐租电动车环洱海，或包车。",
    "三亚": "景点分散，推荐打车或包车。",
    "桂林": "市区公交方便，漓江游需坐船。",
    "拉萨": "市区公交可达，纳木错、羊湖需包车。",
}


def generate_smart_schedule(attractions: List[str], day_num: int, 
                             city: str, budget_level: str = "mid_range") -> List[Dict]:
    """
    生成智能行程安排
    - 早上7:30起床，8:00早餐
    - 上午安排景点（光线好）
    - 午餐+休息
    - 下午继续景点
    - 晚餐+夜景或休闲
    - 22:30睡觉
    """
    schedule = []
    base_hour = 7
    
    schedule.append({
        "time": "07:30",
        "activity": "起床洗漱",
        "location": f"{city}酒店",
        "type": "作息",
        "details": "早睡早起，精神饱满开启一天"
    })
    
    schedule.append({
        "time": "08:00",
        "activity": "早餐",
        "location": f"{city}酒店或附近餐馆",
        "type": "餐饮",
        "details": f"推荐品尝当地特色：{', '.join(LOCAL_FOOD.get(city, ['当地小吃'])[:2])}"
    })
    
    morning_attractions = attractions[:2]
    afternoon_attractions = attractions[2:4] if len(attractions) > 2 else attractions[-1:] if len(attractions) > 1 else []
    
    current_time = 9
    for i, attr in enumerate(morning_attractions):
        details = ATTRACTION_DETAILS.get(attr, {})
        visit_hours = details.get("visit_duration", "2小时")
        
        duration_match = re.search(r'(\d+)', visit_hours)
        duration = int(duration_match.group(1)) if duration_match else 2
        
        start_hour = current_time
        end_hour = start_hour + duration
        
        schedule.append({
            "time": f"{start_hour:02d}:00",
            "activity": attr,
            "location": city,
            "type": "景点",
            "duration": visit_hours,
            "details": details.get("description", f"{city}著名景点"),
            "best_time": details.get("best_time", ""),
            "tips": details.get("tips", ""),
            "ticket": details.get("ticket", ""),
            "open_hours": details.get("open_hours", "")
        })
        
        current_time = end_hour
    
    schedule.append({
        "time": f"{current_time:02d}:00",
        "activity": "午餐休息",
        "location": city,
        "type": "餐饮",
        "details": f"推荐美食：{', '.join(random.sample(LOCAL_FOOD.get(city, ['当地美食']), min(3, len(LOCAL_FOOD.get(city, ['当地美食'])))))}"
    })
    
    current_time += 1
    
    for i, attr in enumerate(afternoon_attractions):
        details = ATTRACTION_DETAILS.get(attr, {})
        visit_hours = details.get("visit_duration", "2小时")
        
        duration_match = re.search(r'(\d+)', visit_hours)
        duration = int(duration_match.group(1)) if duration_match else 2
        
        start_hour = current_time
        end_hour = start_hour + duration
        
        schedule.append({
            "time": f"{start_hour:02d}:00",
            "activity": attr,
            "location": city,
            "type": "景点",
            "duration": visit_hours,
            "details": details.get("description", f"{city}著名景点"),
            "best_time": details.get("best_time", ""),
            "tips": details.get("tips", ""),
            "ticket": details.get("ticket", ""),
            "open_hours": details.get("open_hours", "")
        })
        
        current_time = end_hour
    
    schedule.append({
        "time": f"{current_time:02d}:00",
        "activity": "晚餐",
        "location": city,
        "type": "餐饮",
        "details": f"推荐餐厅：当地特色餐厅"
    })
    
    current_time += 1
    
    schedule.append({
        "time": f"{current_time:02d}:00",
        "activity": "自由活动/夜景欣赏",
        "location": city,
        "type": "休闲",
        "details": f"可逛{city}夜景、买特产、泡温泉或看演出"
    })
    
    schedule.append({
        "time": "22:30",
        "activity": "休息",
        "location": f"{city}酒店",
        "type": "作息",
        "details": "保证充足睡眠，为明天做准备"
    })
    
    return schedule


def get_hotel_recommendation(city: str, budget_level: str = "mid_range") -> str:
    """获取酒店推荐"""
    hotels = HOTELS_BY_CITY.get(city, {})
    level_map = {
        "luxury": "豪华型",
        "mid_range": "经济型",
        "budget": "实惠型"
    }
    hotel_names = hotels.get(budget_level, "推荐在携程/美团搜索当地酒店")
    level_name = level_map.get(budget_level, "经济型")
    return f"【{level_name}】{hotel_names}"


def get_city_transport_tips(city: str) -> str:
    """获取城市交通提示"""
    return TRANSPORT_TIPS.get(city, "推荐使用高德地图导航，根据实际情况选择交通方式")


def get_city_food(city: str) -> List[str]:
    """获取城市美食推荐"""
    return LOCAL_FOOD.get(city, ["当地特色美食"])


def enrich_attraction_info(attraction_name: str) -> Dict:
    """丰富景点信息"""
    return ATTRACTION_DETAILS.get(attraction_name, {
        "description": f"{attraction_name}是当地著名景点",
        "best_time": "全天",
        "visit_duration": "2小时",
        "tips": "建议穿舒适鞋子，带水和防晒用品",
        "ticket": "以景区实际为准",
        "open_hours": "以景区实际为准"
    })
