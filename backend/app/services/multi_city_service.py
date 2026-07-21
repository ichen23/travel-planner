import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.services.city_database import (
    CITY_COORDS, CITY_BASIC_INFO, get_high_speed_routes, 
    get_city_info, BEIJING_3HR_COORDS, ALL_CITY_COORDS,
    MASS_CITY_INFO, MEGA_CITY_INFO, EXTENDED_CITY_BASIC_INFO
)


def normalize_city_name(city: str) -> str:
    """规范化城市名称，处理'市'、'省'、'特别行政区'等后缀"""
    if not city:
        return city
    
    suffixes = ['特别行政区', '自治区', '自治州', '地区', '盟', '省', '市', '区', '县']
    normalized = city
    
    for suffix in suffixes:
        if normalized.endswith(suffix) and len(normalized) > len(suffix):
            normalized = normalized[:-len(suffix)]
            break
    
    if normalized in CITY_STATIC_DATA:
        return normalized
    if normalized in CITY_BASIC_INFO:
        return normalized
    if normalized in MASS_CITY_INFO:
        return normalized
    if normalized in MEGA_CITY_INFO:
        return normalized
    if normalized in EXTENDED_CITY_BASIC_INFO:
        return normalized
    
    return city


CITY_STATIC_DATA = {
    "开封": {
        "attractions": [
            {"name": "清明上河园", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "120元", "rating": 5, "tags": ["历史", "必去", "拍照"], "tips": "门票包含《东京梦华》演出，下午场更精彩，建议下午2点后进入"},
            {"name": "龙亭公园", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["园林", "历史"], "tips": "皇家园林，可俯瞰开封古城，傍晚光线好适合拍照"},
            {"name": "天波杨府", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "60元", "rating": 4, "tags": ["历史", "文化"], "tips": "杨家将府邸，了解北宋抗辽历史"},
            {"name": "大相国寺", "start_time": "15:00", "duration_hours": 1.5, "best_period": "afternoon", "ticket": "40元", "rating": 4, "tags": ["寺庙", "历史"], "tips": "千年古刹，鲁智深倒拔垂杨柳旧址"},
            {"name": "开封府", "start_time": "13:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "65元", "rating": 4, "tags": ["历史", "必去"], "tips": "包公开府办案之地，有开衙仪式表演"},
            {"name": "鼓楼", "start_time": "18:00", "duration_hours": 1, "best_period": "evening", "ticket": "30元", "rating": 3, "tags": ["夜景", "地标"], "tips": "开封地标建筑，夜景很美"},
            {"name": "西司夜市", "start_time": "19:30", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["美食", "夜市"], "tips": "本地人的夜市，比鼓楼夜市更地道"}
        ],
        "food": [
            {"name": "第一楼灌汤包", "location": "寺后街", "price_range": "30-80元", "recommend": "猪肉灌汤包、蟹黄包、虾包", "type": "正餐"},
            {"name": "黄家老店", "location": "中山路中段", "price_range": "25-60元", "recommend": "开封传统小笼包、鲤鱼焙面", "type": "正餐"},
            {"name": "州桥夜市小吃", "location": "中山路与自由路交叉口", "price_range": "20-40元", "recommend": "炒凉粉、花生糕、冰糖梨、杏仁茶", "type": "小吃"},
            {"name": "河大夜市", "location": "明伦街", "price_range": "15-35元", "recommend": "烧饼夹鸡腿、炒冰、麻辣烫", "type": "小吃"},
            {"name": "老河大西门店", "location": "河大西门", "price_range": "20-50元", "recommend": "烩面、大盘鸡", "type": "正餐"}
        ],
        "transport": "市内公交发达，推荐购买公交卡或使用支付宝乘车码；景点间距离较近，打车约10-20元",
        "tips": "开封景区集中在老城区，步行游览最方便；清明上河园建议游玩5-6小时；避开节假日高峰"
    },
    "焦作": {
        "attractions": [
            {"name": "云台山红石峡", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "210元（含观光车）", "rating": 5, "tags": ["自然", "必去", "拍照"], "tips": "丹霞地貌，红色峡谷非常震撼，建议早上避开人流"},
            {"name": "云台山茱萸峰", "start_time": "13:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "含云台山门票", "rating": 4, "tags": ["自然", "登山"], "tips": "云台山主峰，海拔1308米，有玻璃栈道"},
            {"name": "云台山潭瀑峡", "start_time": "09:00", "duration_hours": 2.5, "best_period": "morning", "ticket": "含云台山门票", "rating": 4, "tags": ["自然", "亲子"], "tips": "三步一泉五步一瀑，适合带孩子玩水"},
            {"name": "陈家沟", "start_time": "10:00", "duration_hours": 4, "best_period": "morning", "ticket": "80元", "rating": 4, "tags": ["文化", "太极"], "tips": "太极拳发源地，可体验太极文化"},
            {"name": "青天河", "start_time": "08:30", "duration_hours": 4, "best_period": "morning", "ticket": "180元", "rating": 4, "tags": ["自然", "水上"], "tips": "北方小桂林，可乘船游览"},
            {"name": "云台天池", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "含云台山门票", "rating": 3, "tags": ["自然", "休闲"], "tips": "湖光山色，适合放松"}
        ],
        "food": [
            {"name": "焦作老烩面", "location": "解放区", "price_range": "15-35元", "recommend": "羊汤烩面、牛肉烩面", "type": "正餐"},
            {"name": "武陟油茶", "location": "武陟县", "price_range": "10-20元", "recommend": "传统早餐，香浓可口", "type": "早餐"},
            {"name": "云台山野菜馆", "location": "景区门口", "price_range": "50-100元", "recommend": "山野菜、土鸡、土鸡蛋、炒山药", "type": "特色"},
            {"name": "济源土馍", "location": "小吃店", "price_range": "5-15元", "recommend": "当地特色面食", "type": "小吃"},
            {"name": "博爱怀姜糖", "location": "特产店", "price_range": "20-40元", "recommend": "用怀姜制作的姜糖，暖胃驱寒", "type": "特产"}
        ],
        "transport": "云台山距市区40公里，有旅游专线车；景区内需乘观光车；陈家沟距市区30公里",
        "tips": "云台山建议玩2天，第一天红石峡+潭瀑峡，第二天茱萸峰+玻璃栈道；山上温度低，带件外套"
    },
    "洛阳": {
        "attractions": [
            {"name": "龙门石窟", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "90元", "rating": 5, "tags": ["历史", "必去", "拍照"], "tips": "中国四大石窟之一，卢舍那大佛最壮观，上午光线好适合拍照"},
            {"name": "白马寺", "start_time": "13:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["寺庙", "历史"], "tips": "中国第一古刹，佛教传入中原后建立的第一座寺庙"},
            {"name": "关林", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["历史", "三国"], "tips": "关羽陵庙，三国文化圣地"},
            {"name": "洛阳博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去", "免费"], "tips": "馆藏丰富，唐三彩、青铜器、壁画是特色，周一闭馆"},
            {"name": "应天门", "start_time": "19:00", "duration_hours": 2, "best_period": "evening", "ticket": "30元", "rating": 4, "tags": ["夜景", "地标"], "tips": "隋唐洛阳城的正南门，夜景很美，有灯光秀"},
            {"name": "老君山", "start_time": "06:30", "duration_hours": 6, "best_period": "morning", "ticket": "100元", "rating": 5, "tags": ["自然", "必去", "登山"], "tips": "道教名山，金顶日出非常震撼，山上温度低"},
            {"name": "隋唐大运河博物馆", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文化", "历史"], "tips": "了解大运河历史的好地方"},
            {"name": "洛邑古城", "start_time": "17:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["拍照", "汉服"], "tips": "穿汉服免费入园，夜景很美"}
        ],
        "food": [
            {"name": "真不同水席", "location": "老城区", "price_range": "80-150元/人", "recommend": "洛阳水席代表，牡丹燕菜、焦炸丸子", "type": "特色"},
            {"name": "马杰山牛肉汤", "location": "瀍河区", "price_range": "15-30元", "recommend": "洛阳牛肉汤配烧饼、油旋", "type": "早餐"},
            {"name": "西工小街锅贴", "location": "西工区", "price_range": "10-25元", "recommend": "地道的洛阳锅贴", "type": "小吃"},
            {"name": "老城十字街夜市", "location": "老城区十字街", "price_range": "20-50元", "recommend": "不翻汤、炒酸奶、牡丹饼、水席", "type": "夜市"},
            {"name": "管记水席", "location": "老城区", "price_range": "60-100元", "recommend": "洛阳水席老店，经济实惠", "type": "正餐"}
        ],
        "transport": "地铁1、2号线覆盖主要景点；景区直通车串联龙门、关林、白马寺；共享单车适合短途",
        "tips": "洛阳博物馆周一闭馆；龙门石窟卢舍那大佛最佳观赏时间10-14点；4月牡丹花会期间人多票难抢"
    },
    "北京": {
        "attractions": [
            {"name": "故宫博物院", "start_time": "08:30", "duration_hours": 5, "best_period": "morning", "ticket": "60元（需提前预约）", "rating": 5, "tags": ["历史", "必去", "地标"], "tips": "必须提前7天在官网预约，午门进神武门出，建议走中轴线"},
            {"name": "天安门广场", "start_time": "06:30", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "历史"], "tips": "升旗仪式根据季节调整时间，提前查好；周一不开放"},
            {"name": "八达岭长城", "start_time": "07:00", "duration_hours": 5, "best_period": "morning", "ticket": "40元", "rating": 5, "tags": ["必去", "历史", "户外"], "tips": "最经典的长城段，可乘缆车；提前在德胜门乘877路直达"},
            {"name": "颐和园", "start_time": "09:00", "duration_hours": 3.5, "best_period": "morning", "ticket": "30元（联票60元）", "rating": 5, "tags": ["园林", "历史"], "tips": "皇家园林，长廊、佛香阁、十七孔桥是精华"},
            {"name": "天坛公园", "start_time": "08:00", "duration_hours": 2.5, "best_period": "morning", "ticket": "15元（联票34元）", "rating": 4, "tags": ["历史", "地标"], "tips": "祈年殿、回音壁、圜丘坛是三大景点"},
            {"name": "北海公园", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "10元", "rating": 4, "tags": ["园林", "休闲"], "tips": "北京最古老的皇家园林，白塔是标志"},
            {"name": "南锣鼓巷", "start_time": "15:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "拍照"], "tips": "北京最古老的胡同，有特色小店和咖啡馆"},
            {"name": "什刹海", "start_time": "17:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "酒吧"], "tips": "湖光山色，周围有很多酒吧和特色餐厅"},
            {"name": "北京环球影城", "start_time": "09:00", "duration_hours": 7, "best_period": "all_day", "ticket": "418元起", "rating": 5, "tags": ["主题乐园", "亲子"], "tips": "热门项目需要优速通；开园就去排队哈利波特"},
            {"name": "798艺术区", "start_time": "10:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["艺术", "拍照"], "tips": "现代艺术聚集地，适合拍照和看展览"}
        ],
        "food": [
            {"name": "全聚德烤鸭", "location": "前门店", "price_range": "200-350元/人", "recommend": "挂炉烤鸭，配荷叶饼和甜面酱", "type": "特色"},
            {"name": "东来顺涮羊肉", "location": "王府井", "price_range": "150-250元/人", "recommend": "传统铜锅涮肉，手切羊肉", "type": "特色"},
            {"name": "海碗居炸酱面", "location": "甘家口", "price_range": "30-60元", "recommend": "老北京风味，六种菜码", "type": "小吃"},
            {"name": "簋街小龙虾", "location": "东城区簋街", "price_range": "100-200元", "recommend": "麻辣小龙虾、馋嘴蛙", "type": "夜市"},
            {"name": "护国寺小吃", "location": "西城区", "price_range": "20-40元", "recommend": "豆汁焦圈、艾窝窝、驴打滚", "type": "早餐"}
        ],
        "transport": "地铁发达，推荐使用亿通行APP；景点多在地铁沿线；打车高峰难拦，建议用网约车",
        "tips": "故宫必须预约；长城建议早上出发避开人流；景区周边消费高；北京交通拥堵，地铁最可靠"
    },
    "西安": {
        "attractions": [
            {"name": "秦始皇兵马俑", "start_time": "07:30", "duration_hours": 4, "best_period": "morning", "ticket": "120元", "rating": 5, "tags": ["历史", "必去", "地标"], "tips": "必看一号坑，推荐请讲解（200元）；可乘地铁9号线直达"},
            {"name": "大雁塔", "start_time": "13:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "40元", "rating": 4, "tags": ["历史", "地标"], "tips": "西安地标，晚上有音乐喷泉表演"},
            {"name": "西安城墙", "start_time": "16:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "54元", "rating": 5, "tags": ["历史", "必去", "拍照"], "tips": "可租自行车骑行一圈（1小时约45元）；南门夜景最美"},
            {"name": "回民街", "start_time": "18:00", "duration_hours": 2.5, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["美食", "夜市"], "tips": "西安最著名的美食街，晚上最热闹"},
            {"name": "华清宫", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "120元", "rating": 4, "tags": ["历史", "园林"], "tips": "唐玄宗与杨贵妃的行宫，骊山脚下"},
            {"name": "陕西历史博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "馆藏丰富，何家村遗宝、唐代壁画是亮点"},
            {"name": "大唐不夜城", "start_time": "19:30", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "拍照"], "tips": "仿唐文化步行街，有不倒翁小姐姐表演"},
            {"name": "华山", "start_time": "05:00", "duration_hours": 8, "best_period": "all_day", "ticket": "160元", "rating": 5, "tags": ["登山", "必去", "户外"], "tips": "西峰索道上山，东峰看日出；山上温度低"}
        ],
        "food": [
            {"name": "老孙家泡馍", "location": "回民街", "price_range": "25-50元", "recommend": "牛羊肉泡馍，馍要自己掰", "type": "特色"},
            {"name": "子午路张记肉夹馍", "location": "子午路", "price_range": "10-25元", "recommend": "腊汁肉夹馍，白吉馍夹腊汁肉", "type": "小吃"},
            {"name": "回民街小吃", "location": "北院门", "price_range": "20-60元", "recommend": "镜糕、柿子饼、甑糕、黄桂稠酒", "type": "夜市"},
            {"name": "魏家凉皮", "location": "多家分店", "price_range": "15-30元", "recommend": "秘制凉皮、米皮", "type": "快餐"},
            {"name": "长安大牌档", "location": "钟楼", "price_range": "80-150元", "recommend": "葫芦鸡、长安六小时、毛笔酥", "type": "特色"}
        ],
        "transport": "地铁覆盖主要景点；景区直通车串联兵马俑、华清宫；市内打车方便",
        "tips": "兵马俑建议请讲解；回民街美食多但要注意卫生；城墙骑行看个人体力；陕西历史博物馆需提前预约"
    },
    "郑州": {
        "attractions": [
            {"name": "少林寺", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "80元", "rating": 5, "tags": ["必去", "文化", "武术"], "tips": "天下武功出少林，塔林、藏经阁是重点；距市区70公里"},
            {"name": "黄河风景名胜区", "start_time": "08:30", "duration_hours": 4, "best_period": "morning", "ticket": "60元", "rating": 4, "tags": ["自然", "必去"], "tips": "看黄河奔流，炎黄二帝雕像壮观；可乘索道上山"},
            {"name": "河南博物院", "start_time": "09:00", "duration_hours": 3.5, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "馆藏丰富，莲鹤方壶、妇好鸮尊是镇馆之宝，周一闭馆"},
            {"name": "二七纪念塔", "start_time": "14:00", "duration_hours": 1.5, "best_period": "afternoon", "ticket": "免费", "rating": 3, "tags": ["地标"], "tips": "郑州地标，可登塔俯瞰市区"},
            {"name": "只有河南戏剧幻城", "start_time": "10:00", "duration_hours": 6, "best_period": "all_day", "ticket": "290元", "rating": 5, "tags": ["文化", "必去"], "tips": "沉浸式戏剧体验，3大主题剧场值得一看"},
            {"name": "皇帝千古情", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "280元", "rating": 4, "tags": ["演出", "文化"], "tips": "大型演出，讲述中原文化"},
            {"name": "中原福塔", "start_time": "16:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "90元", "rating": 3, "tags": ["地标", "观景"], "tips": "郑州最高建筑，可俯瞰全城"}
        ],
        "food": [
            {"name": "合记烩面", "location": "人民路", "price_range": "25-40元", "recommend": "郑州烩面代表，羊肉烩面", "type": "特色"},
            {"name": "老蔡记蒸饺", "location": "德化街", "price_range": "25-50元", "recommend": "郑州传统名吃，皮薄馅大", "type": "特色"},
            {"name": "方中山胡辣汤", "location": "紫荆山", "price_range": "15-25元", "recommend": "河南胡辣汤代表，配油条吃", "type": "早餐"},
            {"name": "阿利茄汁面", "location": "多家分店", "price_range": "20-35元", "recommend": "茄汁面、担担面", "type": "快餐"},
            {"name": "萧记三鲜烩面", "location": "多家分店", "price_range": "25-45元", "recommend": "三鲜烩面，汤鲜味美", "type": "特色"}
        ],
        "transport": "地铁1、2号线覆盖市区；少林寺有旅游专线车；黄河景区在北郊",
        "tips": "少林寺距市区远，建议安排一日游；河南博物院周一闭馆；烩面是郑州特色必尝"
    },
    "杭州": {
        "attractions": [
            {"name": "西湖", "start_time": "07:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["必去", "自然", "拍照"], "tips": "断桥残雪、苏堤春晓、三潭印月必看；可租自行车环湖"},
            {"name": "灵隐寺", "start_time": "06:30", "duration_hours": 3, "best_period": "morning", "ticket": "75元（含飞来峰）", "rating": 5, "tags": ["寺庙", "必去"], "tips": "江南著名古刹，飞来峰石窟艺术精美"},
            {"name": "千岛湖", "start_time": "07:00", "duration_hours": 8, "best_period": "all_day", "ticket": "150元（含船票）", "rating": 5, "tags": ["必去", "自然"], "tips": "国家5A级景区，坐船游览多个岛屿；距市区150公里"},
            {"name": "龙井村", "start_time": "10:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文化", "休闲"], "tips": "龙井茶原产地，可品茶看茶园"},
            {"name": "河坊街", "start_time": "14:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "拍照"], "tips": "杭州特色商业街，有传统小吃和工艺品"},
            {"name": "宋城", "start_time": "14:30", "duration_hours": 4, "best_period": "afternoon", "ticket": "310元（含千古情）", "rating": 5, "tags": ["演出", "文化"], "tips": "给我一天，还你千年；千古情演出必看"},
            {"name": "西溪湿地", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "80元", "rating": 4, "tags": ["自然", "休闲"], "tips": "城市湿地，可乘船游览"},
            {"name": "京杭大运河", "start_time": "17:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "文化"], "tips": "运河夜景很美，可乘夜游船"}
        ],
        "food": [
            {"name": "楼外楼", "location": "孤山路", "price_range": "150-300元/人", "recommend": "西湖醋鱼、东坡肉、龙井虾仁", "type": "特色"},
            {"name": "知味观", "location": "仁和路", "price_range": "50-120元", "recommend": "片儿川、定胜糕、猫耳朵", "type": "特色"},
            {"name": "外婆家", "location": "湖滨银泰", "price_range": "60-120元", "recommend": "杭州家常菜代表，茶香鸡", "type": "正餐"},
            {"name": "杭儿风", "location": "多家分店", "price_range": "80-150元", "recommend": "杭帮菜，西湖牛肉羹", "type": "正餐"},
            {"name": "小龙坎火锅", "location": "湖滨", "price_range": "120-200元", "recommend": "川味火锅，毛肚、鸭肠", "type": "火锅"}
        ],
        "transport": "地铁覆盖主要景点；西湖景区内有观光车；共享单车适合短途；景区间打车",
        "tips": "西湖景区大，建议分2天玩；千岛湖建议跟团或自驾；宋城千古情值得一看"
    },
    "成都": {
        "attractions": [
            {"name": "宽窄巷子", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "拍照"], "tips": "成都老巷子改造，有茶馆和小吃"},
            {"name": "锦里", "start_time": "11:00", "duration_hours": 2.5, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "夜景"], "tips": "三国文化主题街区，晚上有表演"},
            {"name": "大熊猫繁育研究基地", "start_time": "07:30", "duration_hours": 4, "best_period": "morning", "ticket": "55元", "rating": 5, "tags": ["必去", "亲子", "可爱"], "tips": "必去！建议早上看熊猫最活跃；距市区10公里"},
            {"name": "都江堰", "start_time": "07:00", "duration_hours": 5, "best_period": "morning", "ticket": "80元", "rating": 5, "tags": ["历史", "必去"], "tips": "世界文化遗产，古代水利工程奇迹；距市区60公里"},
            {"name": "武侯祠", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["历史", "三国"], "tips": "三国文化圣地，纪念诸葛亮"},
            {"name": "杜甫草堂", "start_time": "15:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["文化", "历史"], "tips": "诗圣杜甫故居，环境清幽"},
            {"name": "文殊院", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 3, "tags": ["寺庙"], "tips": "成都著名古刹，香火旺盛"},
            {"name": "春熙路", "start_time": "16:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "美食"], "tips": "成都最繁华的商业街"},
            {"name": "成都欢乐谷", "start_time": "10:00", "duration_hours": 6, "best_period": "all_day", "ticket": "230元", "rating": 4, "tags": ["主题乐园", "亲子"], "tips": "大型主题乐园，适合年轻人"}
        ],
        "food": [
            {"name": "陈麻婆豆腐", "location": "青华路", "price_range": "40-80元", "recommend": "正宗麻婆豆腐，麻辣鲜香", "type": "特色"},
            {"name": "龙抄手", "location": "春熙路", "price_range": "25-50元", "recommend": "红油抄手、清汤抄手", "type": "特色"},
            {"name": "宽窄巷子小吃", "location": "宽窄巷子", "price_range": "20-50元", "recommend": "三大炮、糖油果子、蛋烘糕", "type": "小吃"},
            {"name": "小龙坎火锅", "location": "春熙路", "price_range": "120-200元", "recommend": "成都火锅代表，毛肚、黄喉", "type": "火锅"},
            {"name": "老妈蹄花", "location": "人民公园", "price_range": "35-60元", "recommend": "芸豆蹄花汤，招牌菜", "type": "特色"}
        ],
        "transport": "地铁覆盖市区主要景点；大熊猫基地有旅游专线；都江堰可乘城际铁路",
        "tips": "熊猫基地早上熊猫最活跃；成都美食多但偏辣，注意肠胃；都江堰建议跟团"
    },
    "南京": {
        "attractions": [
            {"name": "中山陵", "start_time": "08:00", "duration_hours": 2.5, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["历史", "必去"], "tips": "孙中山先生陵墓，气势恢宏"},
            {"name": "夫子庙", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "30元", "rating": 4, "tags": ["古街", "文化"], "tips": "秦淮河畔，夜游更美"},
            {"name": "总统府", "start_time": "09:00", "duration_hours": 2.5, "best_period": "morning", "ticket": "35元", "rating": 4, "tags": ["历史"], "tips": "民国时期总统府，历史建筑保护完好"},
            {"name": "明孝陵", "start_time": "10:00", "duration_hours": 3, "best_period": "morning", "ticket": "70元", "rating": 4, "tags": ["历史", "必去"], "tips": "明朝开国皇帝陵墓，世界文化遗产"},
            {"name": "南京博物院", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "中国三大博物馆之一，周一闭馆"},
            {"name": "老门东", "start_time": "16:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["古街", "夜景"], "tips": "南京传统街区，有很多特色小店"},
            {"name": "燕子矶", "start_time": "15:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "10元", "rating": 3, "tags": ["自然", "夜景"], "tips": "长江三大名矶之一，看长江好地方"},
            {"name": "牛首山", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "98元", "rating": 5, "tags": ["必去", "拍照"], "tips": "网红打卡地，佛顶宫非常震撼"}
        ],
        "food": [
            {"name": "南京大牌档", "location": "多家分店", "price_range": "60-120元", "recommend": "盐水鸭、狮子头、美龄粥", "type": "特色"},
            {"name": "尹氏鸡汁汤包", "location": "湖南路", "price_range": "25-50元", "recommend": "鸡汁汤包、鸭血粉丝汤", "type": "特色"},
            {"name": "莲湖糕团店", "location": "夫子庙", "price_range": "15-30元", "recommend": "赤豆元宵、糖芋苗、桂花糕", "type": "小吃"},
            {"name": "回味鸭血粉丝汤", "location": "多家分店", "price_range": "20-35元", "recommend": "招牌鸭血粉丝汤", "type": "快餐"},
            {"name": "赤豆元宵店", "location": "老门东", "price_range": "10-20元", "recommend": "赤豆元宵，甜糯可口", "type": "小吃"}
        ],
        "transport": "地铁覆盖主要景点；中山陵有观光车；市内打车方便",
        "tips": "南京博物院周一闭馆；夫子庙夜游值得；牛首山建议早上避免人流"
    },
    "郑州": {
        "attractions": [
            {"name": "少林寺", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "100元", "rating": 5, "tags": ["历史", "必去", "武术"], "tips": "禅宗祖庭，少林武术发源地"},
            {"name": "河南博物院", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "中国九大博物院之一，文物丰富"},
            {"name": "二七纪念塔", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["历史", "地标"], "tips": "郑州标志性建筑，可登顶观景"},
            {"name": "黄河风景名胜区", "start_time": "14:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "60元", "rating": 4, "tags": ["自然", "必去"], "tips": "黄河岸边，可看到浊浪滔天"},
            {"name": "方特欢乐世界", "start_time": "10:00", "duration_hours": 6, "best_period": "afternoon", "ticket": "260元", "rating": 4, "tags": ["娱乐", "亲子"], "tips": "大型主题乐园，适合年轻人"},
            {"name": "中原大佛", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "120元", "rating": 4, "tags": ["宗教", "打卡"], "tips": "世界最大的露天大佛"}
        ],
        "food": [
            {"name": "合记烩面", "location": "人民路", "price_range": "20-40元", "recommend": "羊肉烩面、牛肉烩面", "type": "特色"},
            {"name": "葛记焖饼", "location": "黄河路", "price_range": "15-30元", "recommend": "金丝焖饼", "type": "特色"},
            {"name": "萧记三鲜烩面", "location": "多家分店", "price_range": "25-45元", "recommend": "三鲜烩面", "type": "特色"},
            {"name": "郑州烤鸭店", "location": "紫荆山", "price_range": "50-100元", "recommend": "烤鸭、黄河鲤鱼", "type": "中餐"}
        ],
        "transport": "地铁1-5号线，公交覆盖全城",
        "tips": "河南博物院周一闭馆；少林寺建议上午去；方特适合年轻人"
    },
    "济南": {
        "attractions": [
            {"name": "趵突泉", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 5, "tags": ["自然", "必去"], "tips": "天下第一泉，济南标志性景点"},
            {"name": "大明湖", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["自然", "必去"], "tips": "济南三大名胜之一，可乘船游览"},
            {"name": "千佛山", "start_time": "07:00", "duration_hours": 3, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["自然", "登山"], "tips": "俯瞰济南全城，早上空气好"},
            {"name": "黑虎泉", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["自然", "免费"], "tips": "济南名泉之一，可接泉水饮用"},
            {"name": "芙蓉街", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "古街"], "tips": "济南特色小吃一条街"},
            {"name": "红叶谷", "start_time": "10:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "100元", "rating": 4, "tags": ["自然", "秋季"], "tips": "秋季看红叶的好地方"}
        ],
        "food": [
            {"name": "草包包子铺", "location": "普利街", "price_range": "15-30元", "recommend": "猪肉包子、素馅包子", "type": "特色"},
            {"name": "油旋张", "location": "芙蓉街", "price_range": "5-10元", "recommend": "油旋", "type": "小吃"},
            {"name": "甜沫唐", "location": "多家分店", "price_range": "10-20元", "recommend": "甜沫、油条", "type": "早餐"},
            {"name": "老济南把子肉", "location": "经十路", "price_range": "25-50元", "recommend": "把子肉、米饭", "type": "特色"}
        ],
        "transport": "地铁1-3号线，公交发达",
        "tips": "趵突泉和大明湖相邻，可一起游览；黑虎泉可以接泉水喝"
    },
    "青岛": {
        "attractions": [
            {"name": "栈桥", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "免费"], "tips": "青岛标志性建筑，可喂海鸥"},
            {"name": "八大关", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["建筑", "拍照"], "tips": "万国建筑博览会，适合拍照"},
            {"name": "五四广场", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "夜景"], "tips": "青岛新城区中心，夜景漂亮"},
            {"name": "崂山", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "130元", "rating": 5, "tags": ["自然", "必去"], "tips": "海上名山第一，建议一日游"},
            {"name": "金沙滩", "start_time": "14:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["海滩", "夏季"], "tips": "亚洲第一滩，适合夏季游泳"},
            {"name": "极地海洋世界", "start_time": "10:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "220元", "rating": 4, "tags": ["亲子", "娱乐"], "tips": "大型海洋主题公园"},
            {"name": "啤酒博物馆", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["文化", "打卡"], "tips": "了解青岛啤酒历史，可品尝新鲜啤酒"}
        ],
        "food": [
            {"name": "船歌鱼水饺", "location": "多家分店", "price_range": "50-100元", "recommend": "鲅鱼水饺、墨鱼水饺", "type": "特色"},
            {"name": "青岛啤酒街", "location": "登州路", "price_range": "30-80元", "recommend": "原浆啤酒、海鲜烧烤", "type": "特色"},
            {"name": "春和楼", "location": "中山路", "price_range": "80-150元", "recommend": "香酥鸡、海鲜", "type": "中餐"},
            {"name": "辣炒蛤蜊", "location": "大排档", "price_range": "30-50元", "recommend": "辣炒蛤蜊、烤鱿鱼", "type": "小吃"}
        ],
        "transport": "地铁1-4号线，沿海公交专线",
        "tips": "崂山建议包车或跟团；啤酒博物馆可以喝到新鲜原浆啤酒；夏季海边注意防晒"
    },
    "西安": {
        "attractions": [
            {"name": "秦始皇兵马俑", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "120元", "rating": 5, "tags": ["历史", "必去"], "tips": "世界第八大奇迹，必去！"},
            {"name": "大雁塔", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["历史", "地标"], "tips": "唐代佛教建筑，可登塔观景"},
            {"name": "西安城墙", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "54元", "rating": 5, "tags": ["历史", "必去"], "tips": "中国现存最完整的古城墙，可骑自行车"},
            {"name": "华清宫", "start_time": "10:00", "duration_hours": 3, "best_period": "morning", "ticket": "120元", "rating": 4, "tags": ["历史", "温泉"], "tips": "唐明皇与杨贵妃的行宫"},
            {"name": "陕西历史博物馆", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "国家级博物馆，文物丰富"},
            {"name": "回民街", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "夜景"], "tips": "西安美食聚集地，晚上热闹"},
            {"name": "大唐不夜城", "start_time": "18:00", "duration_hours": 3, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "打卡"], "tips": "盛唐主题街区，夜景壮观"}
        ],
        "food": [
            {"name": "老孙家泡馍", "location": "东大街", "price_range": "30-60元", "recommend": "羊肉泡馍、牛肉泡馍", "type": "特色"},
            {"name": "回民街小吃", "location": "北院门", "price_range": "20-50元", "recommend": "肉夹馍、凉皮、甑糕", "type": "小吃"},
            {"name": "魏家凉皮", "location": "多家分店", "price_range": "15-30元", "recommend": "秘制凉皮", "type": "小吃"},
            {"name": "西安饭庄", "location": "东大街", "price_range": "80-150元", "recommend": "葫芦鸡、水晶饼", "type": "中餐"}
        ],
        "transport": "地铁1-4号线，公交发达",
        "tips": "兵马俑建议早上早去避开人流；陕博周一闭馆；城墙骑车一圈约2小时"
    },
    "重庆": {
        "attractions": [
            {"name": "洪崖洞", "start_time": "18:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "打卡"], "tips": "千与千寻原型，夜景必看"},
            {"name": "解放碑", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "购物"], "tips": "重庆地标，周边商圈繁华"},
            {"name": "磁器口古镇", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "千年古镇，小吃众多"},
            {"name": "长江索道", "start_time": "09:00", "duration_hours": 1, "best_period": "morning", "ticket": "单程20元", "rating": 4, "tags": ["体验", "打卡"], "tips": "空中看重庆，网红项目"},
            {"name": "武隆天坑", "start_time": "07:00", "duration_hours": 8, "best_period": "morning", "ticket": "175元", "rating": 5, "tags": ["自然", "必去"], "tips": "世界自然遗产，建议一日游"},
            {"name": "鹅岭二厂", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "拍照"], "tips": "网红打卡地，文艺范"},
            {"name": "李子坝轻轨", "start_time": "08:00", "duration_hours": 1, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["打卡", "交通"], "tips": "轻轨穿楼，网红景点"}
        ],
        "food": [
            {"name": "小天鹅火锅", "location": "解放碑", "price_range": "80-150元", "recommend": "毛肚、鸭肠、黄喉", "type": "火锅"},
            {"name": "重庆小面", "location": "街边摊", "price_range": "10-20元", "recommend": "麻辣小面、豌杂面", "type": "小吃"},
            {"name": "酸辣粉", "location": "解放碑", "price_range": "15-25元", "recommend": "手工酸辣粉", "type": "小吃"},
            {"name": "泉水鸡", "location": "南山", "price_range": "60-120元", "recommend": "泉水鸡、烧鸡公", "type": "特色"}
        ],
        "transport": "地铁1-10号线，轻轨特色",
        "tips": "洪崖洞晚上最美；长江索道排队久可买往返票；武隆建议包车"
    },
    "成都": {
        "attractions": [
            {"name": "宽窄巷子", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "文化"], "tips": "成都慢生活体验地"},
            {"name": "锦里古街", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "三国文化主题街区"},
            {"name": "大熊猫繁育研究基地", "start_time": "07:30", "duration_hours": 4, "best_period": "morning", "ticket": "55元", "rating": 5, "tags": ["必去", "亲子"], "tips": "看大熊猫，早上活跃"},
            {"name": "武侯祠", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["历史", "文化"], "tips": "三国文化圣地"},
            {"name": "杜甫草堂", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["文化", "园林"], "tips": "诗圣故居"},
            {"name": "都江堰", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "80元", "rating": 5, "tags": ["历史", "必去"], "tips": "世界遗产，古代水利工程"},
            {"name": "春熙路", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "夜景"], "tips": "成都最繁华商业街"}
        ],
        "food": [
            {"name": "小龙坎火锅", "location": "春熙路", "price_range": "80-150元", "recommend": "毛肚、鹅肠、酥肉", "type": "火锅"},
            {"name": "陈麻婆豆腐", "location": "青华路", "price_range": "40-80元", "recommend": "麻婆豆腐、回锅肉", "type": "川菜"},
            {"name": "龙抄手", "location": "春熙路", "price_range": "20-40元", "recommend": "红油抄手、钟水饺", "type": "小吃"},
            {"name": "担担面", "location": "街边店", "price_range": "10-20元", "recommend": "麻辣担担面", "type": "小吃"}
        ],
        "transport": "地铁1-7号线，公交发达",
        "tips": "熊猫基地早上熊猫最活跃；都江堰建议一日游；宽窄巷子比锦里清静"
    },
    "杭州": {
        "attractions": [
            {"name": "西湖", "start_time": "07:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["必去", "自然"], "tips": "杭州灵魂，绕湖步行或骑车"},
            {"name": "灵隐寺", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "75元", "rating": 5, "tags": ["历史", "宗教"], "tips": "千年古刹，飞来峰石刻"},
            {"name": "千岛湖", "start_time": "07:00", "duration_hours": 8, "best_period": "morning", "ticket": "150元", "rating": 5, "tags": ["自然", "必去"], "tips": "天下第一秀水，建议一日游"},
            {"name": "宋城", "start_time": "14:00", "duration_hours": 5, "best_period": "afternoon", "ticket": "310元", "rating": 5, "tags": ["主题", "演出"], "tips": "宋城千古情必看"},
            {"name": "西溪湿地", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "80元", "rating": 4, "tags": ["自然", "生态"], "tips": "城市湿地，乘船游览"},
            {"name": "雷峰塔", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["地标", "夜景"], "tips": "登塔看西湖全景"},
            {"name": "河坊街", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "南宋御街，特色小吃"}
        ],
        "food": [
            {"name": "楼外楼", "location": "孤山", "price_range": "150-300元", "recommend": "西湖醋鱼、龙井虾仁、东坡肉", "type": "浙菜"},
            {"name": "知味观", "location": "湖滨", "price_range": "60-120元", "recommend": "片儿川、小笼包", "type": "特色"},
            {"name": "外婆家", "location": "多家分店", "price_range": "50-100元", "recommend": "茶香鸡、麻婆豆腐", "type": "杭帮菜"},
            {"name": "葱包桧", "location": "河坊街", "price_range": "10-20元", "recommend": "葱包桧、定胜糕", "type": "小吃"}
        ],
        "transport": "地铁1-5号线，公交发达",
        "tips": "西湖早晚最美；千岛湖建议跟团或包车；灵隐寺早上人少"
    },
    "北京": {
        "attractions": [
            {"name": "故宫博物院", "start_time": "08:30", "duration_hours": 5, "best_period": "morning", "ticket": "60元", "rating": 5, "tags": ["历史", "必去"], "tips": "紫禁城，建议提前预约门票"},
            {"name": "八达岭长城", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "40元", "rating": 5, "tags": ["历史", "必去"], "tips": "万里长城，建议早去避人流"},
            {"name": "天安门广场", "start_time": "06:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["地标", "必去"], "tips": "看升旗仪式，需安检"},
            {"name": "颐和园", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "30元", "rating": 5, "tags": ["历史", "园林"], "tips": "皇家园林，昆明湖游船"},
            {"name": "天坛", "start_time": "07:30", "duration_hours": 3, "best_period": "morning", "ticket": "15元", "rating": 5, "tags": ["历史", "必去"], "tips": "明清皇帝祭天之所"},
            {"name": "圆明园", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "25元", "rating": 4, "tags": ["历史", "教育"], "tips": "遗址公园，勿忘国耻"},
            {"name": "南锣鼓巷", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "文艺"], "tips": "老北京胡同文化"},
            {"name": "什刹海", "start_time": "15:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["自然", "夜景"], "tips": "后海酒吧街，夜景热闹"}
        ],
        "food": [
            {"name": "全聚德烤鸭", "location": "前门", "price_range": "200-400元", "recommend": "挂炉烤鸭", "type": "京菜"},
            {"name": "东来顺涮羊肉", "location": "王府井", "price_range": "150-300元", "recommend": "铜锅涮肉", "type": "火锅"},
            {"name": "炸酱面", "location": "老北京面馆", "price_range": "20-40元", "recommend": "北京炸酱面", "type": "特色"},
            {"name": "豆汁焦圈", "location": "老北京小吃", "price_range": "10-20元", "recommend": "豆汁、焦圈、咸菜", "type": "小吃"}
        ],
        "transport": "地铁1-16号线，公交发达",
        "tips": "故宫、长城建议提前预约；天安门需安检；颐和园和圆明园可一起游览"
    },
    "上海": {
        "attractions": [
            {"name": "外滩", "start_time": "17:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "地标"], "tips": "上海地标，晚上灯光最美"},
            {"name": "东方明珠", "start_time": "10:00", "duration_hours": 3, "best_period": "morning", "ticket": "160元", "rating": 5, "tags": ["地标", "必去"], "tips": "上海标志建筑，可俯瞰全城"},
            {"name": "豫园", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["园林", "古街"], "tips": "江南古典园林，城隍庙紧邻"},
            {"name": "上海博物馆", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "中国四大博物馆之一"},
            {"name": "南京路", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "地标"], "tips": "中华商业第一街"},
            {"name": "迪士尼乐园", "start_time": "09:00", "duration_hours": 8, "best_period": "day", "ticket": "475元", "rating": 5, "tags": ["主题", "必去"], "tips": "中国首座迪士尼，建议一整天"},
            {"name": "田子坊", "start_time": "13:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "打卡"], "tips": "老弄堂改造的艺术区"},
            {"name": "朱家角", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "60元", "rating": 4, "tags": ["古镇", "江南"], "tips": "上海水乡古镇，可一日游"}
        ],
        "food": [
            {"name": "小杨生煎", "location": "多家分店", "price_range": "30-60元", "recommend": "鲜肉生煎、蟹粉生煎", "type": "特色"},
            {"name": "南翔馒头店", "location": "豫园", "price_range": "50-100元", "recommend": "小笼包、蟹粉小笼", "type": "特色"},
            {"name": "本帮红烧肉", "location": "上海老饭店", "price_range": "80-150元", "recommend": "红烧肉、响油鳝糊", "type": "本帮菜"},
            {"name": "鲜肉月饼", "location": "光明邨", "price_range": "10-20元", "recommend": "鲜肉月饼、榨菜鲜肉", "type": "小吃"}
        ],
        "transport": "地铁1-18号线，公交发达",
        "tips": "外滩晚上灯光最美；博物馆周一闭馆；迪士尼建议一整天游玩"
    },
    "天津": {
        "attractions": [
            {"name": "古文化街", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "文化"], "tips": "天津民俗文化街"},
            {"name": "天津之眼", "start_time": "18:00", "duration_hours": 1, "best_period": "evening", "ticket": "170元", "rating": 5, "tags": ["地标", "夜景"], "tips": "世界最大摩天轮，夜景最美"},
            {"name": "意大利风情区", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["建筑", "拍照"], "tips": "欧洲风情建筑群"},
            {"name": "瓷房子", "start_time": "10:00", "duration_hours": 1, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["打卡", "建筑"], "tips": "瓷器装饰的特色建筑"},
            {"name": "五大道", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["建筑", "骑行"], "tips": "租界建筑区，可骑行游览"},
            {"name": "大沽口炮台", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["历史", "海边"], "tips": "鸦片战争遗址，海边风景"},
            {"name": "盘山", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "100元", "rating": 4, "tags": ["自然", "登山"], "tips": "京东第一山，可一日游"}
        ],
        "food": [
            {"name": "狗不理包子", "location": "多家分店", "price_range": "50-100元", "recommend": "猪肉包、三鲜包", "type": "特色"},
            {"name": "煎饼果子", "location": "街边摊", "price_range": "10-20元", "recommend": "绿豆面煎饼、鸡蛋", "type": "小吃"},
            {"name": "耳朵眼炸糕", "location": "多家分店", "price_range": "10-20元", "recommend": "红豆馅、豆沙馅", "type": "小吃"},
            {"name": "水爆肚", "location": "天津老菜馆", "price_range": "30-60元", "recommend": "水爆肚、红烧牛尾", "type": "特色"}
        ],
        "transport": "地铁1-5号线，公交发达",
        "tips": "天津之眼晚上最美；煎饼果子配豆浆是天津早餐；五大道可以骑行"
    },
    "苏州": {
        "attractions": [
            {"name": "拙政园", "start_time": "08:30", "duration_hours": 2, "best_period": "morning", "ticket": "90元", "rating": 5, "tags": ["园林", "必去"], "tips": "中国四大园林之首"},
            {"name": "狮子林", "start_time": "10:30", "duration_hours": 1.5, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["园林", "假山"], "tips": "以假山闻名的园林"},
            {"name": "虎丘", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "80元", "rating": 5, "tags": ["历史", "必去"], "tips": "吴中第一名胜"},
            {"name": "周庄古镇", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "100元", "rating": 5, "tags": ["古镇", "江南"], "tips": "中国第一水乡，可一日游"},
            {"name": "同里古镇", "start_time": "07:30", "duration_hours": 6, "best_period": "day", "ticket": "100元", "rating": 4, "tags": ["古镇", "江南"], "tips": "小桥流水人家"},
            {"name": "平江路", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "苏州历史街区"},
            {"name": "金鸡湖", "start_time": "16:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "现代"], "tips": "苏州工业园区地标，夜景好美"},
            {"name": "寒山寺", "start_time": "15:00", "duration_hours": 1.5, "best_period": "afternoon", "ticket": "20元", "rating": 4, "tags": ["寺庙", "文化"], "tips": "枫桥夜泊诗中寺庙"}
        ],
        "food": [
            {"name": "松鹤楼", "location": "观前街", "price_range": "100-200元", "recommend": "松鼠桂鱼、蟹粉豆腐", "type": "苏帮菜"},
            {"name": "哑巴生煎", "location": "临顿路", "price_range": "30-50元", "recommend": "鲜肉生煎", "type": "特色"},
            {"name": "奥灶面", "location": "多家分店", "price_range": "20-30元", "recommend": "红油爆鱼面、卤鸭面", "type": "面食"},
            {"name": "采芝斋", "location": "观前街", "price_range": "20-50元", "recommend": "粽子糖、薄荷糖", "type": "特产"}
        ],
        "transport": "地铁1-4号线，公交发达",
        "tips": "拙政园和狮子林可一起游览；古镇建议早去避人流；苏帮菜偏甜"
    },
    "武汉": {
        "attractions": [
            {"name": "黄鹤楼", "start_time": "08:30", "duration_hours": 2, "best_period": "morning", "ticket": "70元", "rating": 5, "tags": ["地标", "必去"], "tips": "江南三大名楼之一"},
            {"name": "东湖", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["自然", "骑行"], "tips": "武汉城中湖，可骑行或划船"},
            {"name": "户部巷", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "古街"], "tips": "武汉小吃街"},
            {"name": "湖北省博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "越王勾践剑、曾侯乙编钟"},
            {"name": "江滩", "start_time": "16:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "散步"], "tips": "长江岸边，夜景好美"},
            {"name": "武汉大学", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["名校", "樱花"], "tips": "樱花大道，春季最美"},
            {"name": "黄鹤楼", "start_time": "08:30", "duration_hours": 2, "best_period": "morning", "ticket": "70元", "rating": 5, "tags": ["地标", "必去"], "tips": "江南三大名楼之一"}
        ],
        "food": [
            {"name": "热干面", "location": "街边店", "price_range": "10-20元", "recommend": "芝麻酱热干面", "type": "早餐"},
            {"name": "武昌鱼", "location": "艳阳天", "price_range": "60-120元", "recommend": "清蒸武昌鱼、红烧排骨", "type": "鄂菜"},
            {"name": "小龙虾", "location": "万松园", "price_range": "100-200元", "recommend": "油焖大虾、蒜蓉小龙虾", "type": "特色"},
            {"name": "面窝", "location": "街边摊", "price_range": "5-10元", "recommend": "面窝、糯米鸡", "type": "小吃"}
        ],
        "transport": "地铁1-8号线，公交发达",
        "tips": "东湖可以骑行；樱花季武大很美；小龙虾夏季最美味"
    },
    "长沙": {
        "attractions": [
            {"name": "岳麓书院", "start_time": "08:30", "duration_hours": 3, "best_period": "morning", "ticket": "50元", "rating": 5, "tags": ["文化", "必去"], "tips": "千年学府，岳麓山下"},
            {"name": "橘子洲头", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["地标", "必去"], "tips": "湘江中央，可坐小火车"},
            {"name": "太平街", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "古街"], "tips": "长沙小吃街"},
            {"name": "湖南省博物馆", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "马王堆汉墓陈列"},
            {"name": "坡子街", "start_time": "15:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "商圈"], "tips": "火宫殿在这边"},
            {"name": "黑麋峰", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "60元", "rating": 4, "tags": ["自然", "登山"], "tips": "长沙近郊最高峰"},
            {"name": "世界之窗", "start_time": "09:00", "duration_hours": 6, "best_period": "day", "ticket": "150元", "rating": 4, "tags": ["主题", "亲子"], "tips": "主题乐园，老少皆宜"}
        ],
        "food": [
            {"name": "火宫殿", "location": "坡子街", "price_range": "60-120元", "recommend": "臭豆腐、糖油粑粑、口味虾", "type": "小吃"},
            {"name": "文和友", "location": "海信广场", "price_range": "80-150元", "recommend": "油爆虾、口味蟹", "type": "湘菜馆"},
            {"name": "茶颜悦色", "location": "多家分店", "price_range": "15-25元", "recommend": "幽兰拿铁、声声乌龙", "type": "奶茶"},
            {"name": "剁椒鱼头", "location": "辣椒炒肉", "price_range": "80-150元", "recommend": "剁椒鱼头、小炒黄牛肉", "type": "湘菜"}
        ],
        "transport": "地铁1-6号线，公交发达",
        "tips": "臭豆腐、小龙虾必吃；茶颜悦色到处都有；岳麓书院在湖南大学内"
    },
    "福州": {
        "attractions": [
            {"name": "三坊七巷", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["古街", "文化"], "tips": "福州历史文化街区"},
            {"name": "鼓山", "start_time": "07:00", "duration_hours": 5, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["自然", "登山"], "tips": "福州名山，可看日出"},
            {"name": "西湖公园", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["自然", "散步"], "tips": "福州城中湖"},
            {"name": "青云山", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "130元", "rating": 4, "tags": ["自然", "一日游"], "tips": "福州近郊景区，可一日游"},
            {"name": "平潭岛", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["海边", "一日游"], "tips": "福建最美海岛"},
            {"name": "林则徐故居", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "20元", "rating": 4, "tags": ["历史", "文化"], "tips": "民族英雄林则徐故居"}
        ],
        "food": [
            {"name": "聚春园", "location": "东街口", "price_range": "100-200元", "recommend": "佛跳墙、荔枝肉", "type": "闽菜"},
            {"name": "鱼丸", "location": "街边店", "price_range": "15-30元", "recommend": "鲨鱼丸、鳗鱼丸", "type": "小吃"},
            {"name": "同利肉燕", "location": "三坊七巷", "price_range": "20-40元", "recommend": "肉燕、燕皮", "type": "特色"},
            {"name": "锅边糊", "location": "街边摊", "price_range": "5-15元", "recommend": "锅边糊、油条", "type": "早餐"}
        ],
        "transport": "地铁1-2号线，公交发达",
        "tips": "三坊七巷晚上有灯光；平潭岛可看蓝眼泪；佛跳墙是闽菜代表"
    },
    "合肥": {
        "attractions": [
            {"name": "包公园", "start_time": "08:30", "duration_hours": 2, "best_period": "morning", "ticket": "20元", "rating": 4, "tags": ["历史", "公园"], "tips": "包公祠、包公墓园"},
            {"name": "三河古镇", "start_time": "07:30", "duration_hours": 6, "best_period": "day", "ticket": "免费", "rating": 4, "tags": ["古镇", "一日游"], "tips": "合肥近郊古镇"},
            {"name": "李鸿章故居", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "25元", "rating": 4, "tags": ["历史", "文化"], "tips": "晚清重臣李鸿章故居"},
            {"name": "巢湖", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "免费", "rating": 4, "tags": ["自然", "一日游"], "tips": "中国五大淡水湖之一"},
            {"name": "岱山湖", "start_time": "07:30", "duration_hours": 8, "best_period": "day", "ticket": "40元", "rating": 4, "tags": ["自然", "一日游"], "tips": "合肥近郊山水景区"},
            {"name": "合肥海洋世界", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "150元", "rating": 4, "tags": ["亲子", "主题"], "tips": "海洋主题乐园"}
        ],
        "food": [
            {"name": "同庆楼", "location": "多家分店", "price_range": "100-200元", "recommend": "臭鳜鱼、毛豆腐", "type": "徽菜"},
            {"name": "老乡鸡", "location": "多家分店", "price_range": "20-40元", "recommend": "肥西老母鸡汤", "type": "快餐"},
            {"name": "肥东老母鸡", "location": "肥东", "price_range": "30-60元", "recommend": "老母鸡汤", "type": "特色"},
            {"name": "庐州烤鸭", "location": "宿州路", "price_range": "50-100元", "recommend": "烤鸭、鸭油烧饼", "type": "特色"}
        ],
        "transport": "地铁1-4号线，公交发达",
        "tips": "三河古镇免费；巢湖可一日游；臭鳜鱼是徽菜代表"
    },
    "南昌": {
        "attractions": [
            {"name": "滕王阁", "start_time": "08:30", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 5, "tags": ["地标", "必去"], "tips": "江南三大名楼之一"},
            {"name": "八一起义纪念馆", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费（需预约）", "rating": 4, "tags": ["历史", "红色"], "tips": "南昌起义旧址"},
            {"name": "梅岭", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "45元", "rating": 4, "tags": ["自然", "登山"], "tips": "南昌近郊名山"},
            {"name": "秋水广场", "start_time": "18:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["夜景", "音乐喷泉"], "tips": "有音乐喷泉表演"},
            {"name": "绳金塔", "start_time": "10:00", "duration_hours": 1, "best_period": "morning", "ticket": "20元", "rating": 4, "tags": ["历史", "地标"], "tips": "南昌古塔"},
            {"name": "天香园", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["自然", "观鸟"], "tips": "城市湿地，可看候鸟"}
        ],
        "food": [
            {"name": "民间饭庄", "location": "榕门路", "price_range": "80-150元", "recommend": "瓦罐汤、三杯鸡", "type": "赣菜"},
            {"name": "绳金塔夜市", "location": "绳金塔", "price_range": "20-50元", "recommend": "烤串、炒粉", "type": "小吃"},
            {"name": "黄庆仁药店", "location": "多家分店", "price_range": "15-30元", "recommend": "绿豆汤、龟苓膏", "type": "特色"},
            {"name": "南昌炒粉", "location": "街边店", "price_range": "10-20元", "recommend": "牛肉炒粉、鸡蛋炒粉", "type": "面食"}
        ],
        "transport": "地铁1-4号线，公交发达",
        "tips": "秋水广场有音乐喷泉；瓦罐汤是南昌特色；滕王阁晚上有灯光"
    }
}


def format_time(hour: int, minute: int = 0) -> str:
    h = hour % 24
    return f"{h:02d}:{minute:02d}"


def get_city_attractions(city: str) -> list:
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]["attractions"]
    
    city_info = {}
    if city in CITY_BASIC_INFO:
        city_info = CITY_BASIC_INFO[city]
    elif city in MASS_CITY_INFO:
        city_info = MASS_CITY_INFO[city]
    elif city in MEGA_CITY_INFO:
        city_info = MEGA_CITY_INFO[city]
    elif city in EXTENDED_CITY_BASIC_INFO:
        city_info = EXTENDED_CITY_BASIC_INFO[city]
    elif city in ALL_CITY_COORDS:
        city_info = {
            'name': city,
            'highlights': '',
            'description': f'{city}是一个值得探索的城市',
            'transport': '建议使用当地公共交通或打车服务'
        }
    else:
        return []
    
    highlights = city_info.get('highlights', '')
    if isinstance(highlights, str):
        separator = '、' if '、' in highlights else (',' if ',' in highlights else '，')
        attractions_list = [h.strip() for h in highlights.split(separator) if h.strip()]
    elif isinstance(highlights, list):
        attractions_list = highlights
    else:
        attractions_list = []
    
    if not attractions_list:
        attractions_list = [f"{city}市中心游览", f"{city}博物馆/纪念馆", f"{city}特色街区"]
    
    attractions = []
    for i, attr_name in enumerate(attractions_list[:8]):
        periods = ["morning", "afternoon", "evening"]
        base_hour = 8 + (i % 4) * 2 + (i // 4) * 2
        duration = 2.5 if i < 4 else 2
        
        attraction = {
            "name": attr_name,
            "start_time": format_time(base_hour, 0),
            "duration_hours": duration,
            "best_period": periods[i % 3],
            "ticket": f"{random.choice([0, 30, 50, 80, 100])}元",
            "rating": random.randint(3, 5),
            "tags": ["推荐"],
            "tips": f"{attr_name}是{city}的热门景点，值得一看"
        }
        attractions.append(attraction)
    
    return attractions


def get_city_food(city: str) -> list:
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]["food"]
    
    return [
        {"name": f"{city}特色美食", "location": "市中心", "price_range": "30-60元", "recommend": "当地特色菜", "type": "正餐"},
        {"name": f"{city}小吃街", "location": "老城区", "price_range": "20-40元", "recommend": "各种特色小吃", "type": "小吃"},
        {"name": f"{city}老字号", "location": "商业街", "price_range": "40-80元", "recommend": "传统名菜", "type": "特色"}
    ]


def get_city_info_data(city: str) -> dict:
    city = normalize_city_name(city)
    
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]
    
    city_info = {}
    if city in CITY_BASIC_INFO:
        city_info = CITY_BASIC_INFO[city]
    elif city in MASS_CITY_INFO:
        city_info = MASS_CITY_INFO[city]
    elif city in MEGA_CITY_INFO:
        city_info = MEGA_CITY_INFO[city]
    elif city in EXTENDED_CITY_BASIC_INFO:
        city_info = EXTENDED_CITY_BASIC_INFO[city]
    elif city in ALL_CITY_COORDS:
        city_info = {
            'name': city,
            'highlights': '',
            'description': f'{city}是一个值得探索的城市',
            'transport': '建议使用当地公共交通或打车服务'
        }
    else:
        return {"attractions": [], "food": [], "transport": "", "tips": ""}
    
    return {
        "attractions": get_city_attractions(city),
        "food": get_city_food(city),
        "transport": city_info.get('transport', '建议使用当地公共交通或打车服务'),
        "tips": city_info.get('description', f'{city}是一个值得探索的城市')[:100]
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
            "type": train_type,
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


def time_to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def minutes_to_time(minutes: int) -> str:
    h = (minutes // 60) % 24
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def parse_duration_to_minutes(duration_str: str) -> int:
    try:
        if isinstance(duration_str, (int, float)):
            return int(duration_str * 60)
        
        duration_str = str(duration_str).strip()
        total_minutes = 0
        
        if "小时" in duration_str:
            parts = duration_str.split("小时")
            total_minutes += int(parts[0]) * 60
            if len(parts) > 1 and "分" in parts[1]:
                mins = parts[1].replace("分", "").strip()
                if mins:
                    total_minutes += int(mins)
        elif "时" in duration_str:
            parts = duration_str.split("时")
            total_minutes += int(parts[0]) * 60
            if len(parts) > 1 and "分" in parts[1]:
                mins = parts[1].replace("分", "").strip()
                if mins:
                    total_minutes += int(mins)
        elif "分钟" in duration_str or "分" in duration_str:
            mins = duration_str.replace("分钟", "").replace("分", "").strip()
            if mins:
                total_minutes += int(mins)
        else:
            total_minutes = int(float(duration_str) * 60)
        
        return max(total_minutes, 30)
    except:
        return 120


def generate_full_day_plan(city: str, day_index: int, user_selected_attractions: list = None) -> dict:
    city_data = get_city_info_data(city)
    all_attractions = city_data.get("attractions", [])
    foods = city_data.get("food", [])
    
    if not all_attractions:
        return None
    
    user_selected = user_selected_attractions or []
    
    morning_attrs = []
    afternoon_attrs = []
    evening_attrs = []
    
    used_attr_names = set()
    
    if user_selected:
        for attr_name in user_selected:
            for attr in all_attractions:
                if attr_name in attr["name"] or attr["name"] in attr_name:
                    period = attr.get("best_period", "afternoon")
                    used_attr_names.add(attr["name"])
                    if period == "morning":
                        morning_attrs.append(attr)
                    elif period == "afternoon":
                        afternoon_attrs.append(attr)
                    else:
                        evening_attrs.append(attr)
                    break
    
    available_attrs = [a for a in all_attractions if a["name"] not in used_attr_names]
    random.shuffle(available_attrs)
    
    for attr in available_attrs[:4]:
        period = attr.get("best_period", "afternoon")
        if period == "morning" and len(morning_attrs) < 2:
            morning_attrs.append(attr)
            used_attr_names.add(attr["name"])
        elif period == "afternoon" and len(afternoon_attrs) < 2:
            afternoon_attrs.append(attr)
            used_attr_names.add(attr["name"])
        elif period == "evening" and len(evening_attrs) < 1:
            evening_attrs.append(attr)
            used_attr_names.add(attr["name"])
    
    for attr in available_attrs:
        if attr["name"] not in used_attr_names:
            if len(morning_attrs) < 2:
                morning_attrs.append(attr)
                used_attr_names.add(attr["name"])
            elif len(afternoon_attrs) < 2:
                afternoon_attrs.append(attr)
                used_attr_names.add(attr["name"])
            elif len(evening_attrs) < 1:
                evening_attrs.append(attr)
                used_attr_names.add(attr["name"])
    
    schedule = []
    
    morning_start = 8 * 60
    morning_end = 12 * 60
    current_time = morning_start
    
    for attr in morning_attrs[:2]:
        attr_start = max(current_time, time_to_minutes(attr.get("start_time", "09:00")))
        attr_duration = parse_duration_to_minutes(attr.get("duration_hours", 2))
        attr_end = min(attr_start + attr_duration, morning_end)
        
        if attr_start >= morning_end:
            break
        
        schedule.append({
            "type": "attraction",
            "name": attr["name"],
            "start_time": minutes_to_time(attr_start),
            "end_time": minutes_to_time(attr_end),
            "duration_minutes": attr_end - attr_start,
            "ticket": attr.get("ticket", "以实际为准"),
            "rating": attr.get("rating", 4),
            "tags": attr.get("tags", []),
            "tips": attr.get("tips", ""),
            "icon": "🏛️"
        })
        
        current_time = attr_end + 15
    
    if foods:
        lunch = foods[0]
        schedule.append({
            "type": "food",
            "name": f"午餐：{lunch['name']}",
            "start_time": minutes_to_time(morning_end),
            "end_time": minutes_to_time(morning_end + 90),
            "duration_minutes": 90,
            "location": lunch.get("location", ""),
            "price_range": lunch.get("price_range", ""),
            "recommend": lunch.get("recommend", ""),
            "icon": "🍜"
        })
    
    afternoon_start = morning_end + 90
    afternoon_end = 18 * 60
    current_time = afternoon_start
    
    for attr in afternoon_attrs[:2]:
        attr_start = max(current_time, time_to_minutes(attr.get("start_time", "14:00")))
        attr_duration = parse_duration_to_minutes(attr.get("duration_hours", 2))
        attr_end = min(attr_start + attr_duration, afternoon_end)
        
        if attr_start >= afternoon_end:
            break
        
        schedule.append({
            "type": "attraction",
            "name": attr["name"],
            "start_time": minutes_to_time(attr_start),
            "end_time": minutes_to_time(attr_end),
            "duration_minutes": attr_end - attr_start,
            "ticket": attr.get("ticket", "以实际为准"),
            "rating": attr.get("rating", 4),
            "tags": attr.get("tags", []),
            "tips": attr.get("tips", ""),
            "icon": "🏛️"
        })
        
        current_time = attr_end + 15
    
    if foods:
        dinner = foods[-1] if len(foods) > 1 else foods[0]
        schedule.append({
            "type": "food",
            "name": f"晚餐：{dinner['name']}",
            "start_time": minutes_to_time(afternoon_end),
            "end_time": minutes_to_time(afternoon_end + 90),
            "duration_minutes": 90,
            "location": dinner.get("location", ""),
            "price_range": dinner.get("price_range", ""),
            "recommend": dinner.get("recommend", ""),
            "icon": "🍲"
        })
    
    evening_start = afternoon_end + 90
    evening_end = 21 * 60
    current_time = evening_start
    
    for attr in evening_attrs[:1]:
        attr_start = max(current_time, time_to_minutes(attr.get("start_time", "19:30")))
        attr_duration = parse_duration_to_minutes(attr.get("duration_hours", 1.5))
        attr_end = min(attr_start + attr_duration, evening_end)
        
        if attr_start >= evening_end:
            break
        
        schedule.append({
            "type": "attraction",
            "name": attr["name"],
            "start_time": minutes_to_time(attr_start),
            "end_time": minutes_to_time(attr_end),
            "duration_minutes": attr_end - attr_start,
            "ticket": attr.get("ticket", "以实际为准"),
            "rating": attr.get("rating", 4),
            "tags": attr.get("tags", []),
            "tips": attr.get("tips", ""),
            "icon": "🌃"
        })
        
        current_time = attr_end
    
    schedule.sort(key=lambda x: x["start_time"])
    
    if not schedule:
        return None
    
    return {
        "day": day_index,
        "city": city,
        "date_label": f"第{day_index}天",
        "transport_tips": city_data.get("transport", ""),
        "city_tips": city_data.get("tips", ""),
        "total_duration_minutes": sum(item["duration_minutes"] for item in schedule),
        "schedule": schedule
    }


async def generate_multi_city_itinerary(cities: list, day_allocation: list,
                                         total_days: int, budget: float, 
                                         preference: str = "",
                                         user_attractions: dict = None) -> dict:
    try:
        if len(cities) < 2:
            return {"success": False, "message": "至少需要2个城市"}
        
        if sum(day_allocation) != total_days:
            if sum(day_allocation) > 0:
                total_days = sum(day_allocation)
            else:
                day_allocation = [total_days // len(cities)] * len(cities)
                day_allocation[0] += total_days % len(cities)
        
        user_attractions = user_attractions or {}
        budget_per_day = budget / total_days if total_days > 0 else budget
        
        days_schedule = []
        transfer_segments = []
        day_counter = 1
        city_budgets = {}
        last_day_index_by_city = {}
        
        for i, city in enumerate(cities):
            city_days = day_allocation[i]
            
            user_selected = user_attractions.get(city, [])
            
            city_attractions = get_city_attractions(city)
            city_budget = estimate_city_budget(city, city_days, budget_per_day, city_attractions)
            city_budgets[city] = city_budget
            
            for d in range(city_days):
                day_user_selected = user_selected if d == 0 else []
                
                day_plan = generate_full_day_plan(city, day_counter, day_user_selected)
                if day_plan:
                    days_schedule.append(day_plan)
                    day_counter += 1
                    last_day_index_by_city[city] = len(days_schedule) - 1
        
        for i in range(len(cities) - 1):
            from_city = cities[i]
            to_city = cities[i + 1]
            
            train_info = get_train_info(from_city, to_city)
            
            transfer_segment = {
                "from_city": from_city,
                "to_city": to_city,
                "train_number": train_info.get("train_number", "未知"),
                "train_type": train_info.get("type", "G"),
                "train_type_name": train_info.get("type_name", "高铁"),
                "departure": "19:00",
                "arrival": calculate_arrival_time("19:00", train_info.get("duration_min", 120)),
                "duration": train_info.get("duration_text", "2小时"),
                "duration_minutes": train_info.get("duration_min", 120),
                "price": train_info.get("price", 100),
                "icon": "🚄"
            }
            transfer_segments.append(transfer_segment)
            
            last_idx = last_day_index_by_city.get(from_city)
            if last_idx is not None and last_idx < len(days_schedule):
                add_transfer_to_day(days_schedule[last_idx], from_city, to_city, transfer_segment)
        
        total_transfer_cost = sum(t.get("price", 0) for t in transfer_segments)
        total_ticket_cost = sum(b.get("ticket", 0) for b in city_budgets.values())
        
        return {
            "success": True,
            "cities": cities,
            "day_allocation": day_allocation,
            "total_days": total_days,
            "total_budget": budget,
            "budget_breakdown": {
                "accommodation": round(budget * 0.3),
                "food": round(budget * 0.25),
                "transport": round(budget * 0.2) + total_transfer_cost,
                "tickets": total_ticket_cost,
                "other": round(budget * 0.1)
            },
            "city_budgets": city_budgets,
            "transfer_segments": transfer_segments,
            "days": days_schedule,
            "tips": [
                "提前7-14天预订高铁票可享受优惠",
                "建议每天8:00开始行程，晚上21:00左右结束",
                "携带舒适的鞋子，每天步行较多",
                "准备充电宝，随时拍照记录",
                "关注天气预报，合理安排室内外景点",
                "每个城市推荐1-2个必去景点，不要贪多"
            ],
            "packing_list": get_packing_suggestions(cities),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"生成行程失败: {str(e)}",
            "error": str(e)
        }


def calculate_arrival_time(departure_time: str, duration_minutes: int) -> str:
    dep_hour, dep_minute = map(int, departure_time.split(":"))
    total_minutes = dep_hour * 60 + dep_minute + duration_minutes
    total_minutes = total_minutes % (24 * 60)
    return minutes_to_time(total_minutes)


def add_transfer_to_day(day_plan: dict, from_city: str, to_city: str, transfer_info: dict):
    schedule = day_plan["schedule"]
    
    evening_start = 18 * 60
    evening_items = [item for item in schedule if time_to_minutes(item["start_time"]) >= evening_start]
    morning_items = [item for item in schedule if time_to_minutes(item["start_time"]) < evening_start]
    
    new_evening = [
        {
            "type": "food",
            "name": f"在{from_city}的最后晚餐",
            "start_time": "18:00",
            "end_time": "19:00",
            "duration_minutes": 60,
            "tips": "提前准备好行李，吃完晚饭去车站",
            "icon": "🍜"
        },
        {
            "type": "transport",
            "name": f"前往{from_city}火车站",
            "start_time": "19:00",
            "end_time": "19:30",
            "duration_minutes": 30,
            "tips": "建议打车或地铁，预留足够时间",
            "icon": "🚖"
        },
        {
            "type": "transport",
            "name": f"{transfer_info['train_number']}次 {from_city}→{to_city}",
            "start_time": transfer_info["departure"],
            "end_time": transfer_info["arrival"],
            "duration_minutes": transfer_info["duration_minutes"],
            "tips": f"{transfer_info['duration']}到达{to_city}，票价{transfer_info['price']}元",
            "icon": "🚄"
        }
    ]
    
    day_plan["schedule"] = morning_items + new_evening
    day_plan["is_transfer_day"] = True
    day_plan["transfer_info"] = transfer_info
    day_plan["date_label"] = f"{day_plan['date_label']}（离开{from_city}）"


def estimate_city_budget(city: str, days: int, budget_per_day: float, attractions: list) -> dict:
    ticket_cost = 0
    ticket_attractions = []
    
    for attr in attractions[:days * 3]:
        ticket = attr.get("ticket", "0元")
        if ticket and ticket != "免费":
            try:
                clean = str(ticket).replace("元", "").replace("（含观光车）", "").replace("含", "").split("/")[0].strip()
                if clean:
                    price = int(clean)
                    ticket_cost += price
                    ticket_attractions.append({"name": attr["name"], "ticket": price})
            except:
                pass
    
    return {
        "ticket": ticket_cost,
        "ticket_attractions": ticket_attractions,
        "food": round(budget_per_day * days * 0.4),
        "local_transport": round(budget_per_day * days * 0.2),
        "accommodation": round(budget_per_day * days * 0.3),
        "misc": round(budget_per_day * days * 0.1),
        "total": round(budget_per_day * days)
    }


def get_packing_suggestions(cities: list) -> dict:
    base_items = ["身份证/护照", "手机充电器/充电宝", "舒适的步行鞋", "轻便外套", "洗漱用品", "常用药品", "雨伞"]
    seasonal_items = []
    optional_items = []
    
    hot_cities = ["郑州", "武汉", "重庆", "杭州", "成都", "南京"]
    cold_cities = ["北京", "西安"]
    cultural_cities = ["洛阳", "西安", "开封", "北京", "南京"]
    nature_cities = ["焦作", "杭州", "成都", "桂林"]
    
    has_hot = any(c in hot_cities for c in cities)
    has_cold = any(c in cold_cities for c in cities)
    has_cultural = any(c in cultural_cities for c in cities)
    has_nature = any(c in nature_cities for c in cities)
    
    if has_hot:
        seasonal_items.extend(["防晒霜", "遮阳帽", "清凉衣物"])
    if has_cold:
        seasonal_items.extend(["保暖内衣", "厚外套", "暖宝宝"])
    if has_cultural:
        optional_items.extend(["汉服/古装（拍照用）", "文化书籍/攻略"])
    if has_nature:
        optional_items.extend(["登山鞋", "背包", "相机/望远镜"])
    
    return {
        "必带物品": base_items,
        "季节推荐": list(set(seasonal_items)),
        "可选物品": list(set(optional_items))
    }


def get_city_all_attractions(city: str) -> list:
    return get_city_attractions(city)


def get_city_all_food(city: str) -> list:
    return get_city_food(city)


def generate_city_data(city: str) -> dict:
    city_info = get_city_info_data(city)
    
    if not city_info:
        return None
    
    basic_info = city_info.get("basic_info", {})
    attractions = city_info.get("attractions", [])
    food = city_info.get("food", [])
    
    return {
        "name": city,
        "basic_info": basic_info,
        "attractions": attractions,
        "food": food,
        "transport": city_info.get("transport", ""),
        "tips": city_info.get("tips", ""),
        "recommended_days": basic_info.get("recommended_days", 2),
        "best_season": basic_info.get("best_season", "")
    }
