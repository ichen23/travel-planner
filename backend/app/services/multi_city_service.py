import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.services.city_database import (
    CITY_COORDS, CITY_BASIC_INFO, get_high_speed_routes, 
    get_city_info, BEIJING_3HR_COORDS, ALL_CITY_COORDS,
    MASS_CITY_INFO, MEGA_CITY_INFO, EXTENDED_CITY_BASIC_INFO
)


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
    }
}


def format_time(hour: int, minute: int = 0) -> str:
    h = hour % 24
    return f"{h:02d}:{minute:02d}"


def get_city_attractions(city: str) -> list:
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
    if city in CITY_STATIC_DATA:
        return CITY_STATIC_DATA[city]["food"]
    
    return [
        {"name": f"{city}特色美食", "location": "市中心", "price_range": "30-60元", "recommend": "当地特色菜", "type": "正餐"},
        {"name": f"{city}小吃街", "location": "老城区", "price_range": "20-40元", "recommend": "各种特色小吃", "type": "小吃"},
        {"name": f"{city}老字号", "location": "商业街", "price_range": "40-80元", "recommend": "传统名菜", "type": "特色"}
    ]


def get_city_info_data(city: str) -> dict:
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
            "train_number": train_info["train_number"],
            "train_type": train_info["type"],
            "train_type_name": train_info["type_name"],
            "departure": "19:00",
            "arrival": calculate_arrival_time("19:00", train_info["duration_min"]),
            "duration": train_info["duration_text"],
            "duration_minutes": train_info["duration_min"],
            "price": train_info["price"],
            "icon": "🚄"
        }
        transfer_segments.append(transfer_segment)
        
        last_idx = last_day_index_by_city[from_city]
        if last_idx is not None:
            add_transfer_to_day(days_schedule[last_idx], from_city, to_city, transfer_segment)
    
    total_transfer_cost = sum(t["price"] for t in transfer_segments)
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
