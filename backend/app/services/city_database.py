"""城市数据库 - 全国主要城市 + 详细旅游贴士"""
import random
import os
from app.services.beijing_3hr_data import (
    BEIJING_3HR_COORDS, BEIJING_3HR_DESTINATIONS, DEFAULT_EXTENDED_INFO,
    DESTINATION_TRAVEL_TIMES, get_travel_time_hours, time_category,
    get_beijing_3hr_destinations, get_beijing_3hr_info, format_travel_time
)

EXTENDED_CITY_COORDS = {}
EXTENDED_CITY_TIPS = {}
EXTENDED_CITY_TAGS = {}
EXTENDED_CITY_BASIC_INFO = {}

try:
    import importlib.util
    _module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expanded_city_data.py')
    if os.path.exists(_module_path):
        _spec = importlib.util.spec_from_file_location("expanded_city_data", _module_path)
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        if hasattr(_module, 'EXTENDED_CITY_COORDS'):
            EXTENDED_CITY_COORDS = _module.EXTENDED_CITY_COORDS
        if hasattr(_module, 'EXTENDED_CITY_TIPS'):
            EXTENDED_CITY_TIPS = _module.EXTENDED_CITY_TIPS
        if hasattr(_module, 'EXTENDED_CITY_TAGS'):
            EXTENDED_CITY_TAGS = _module.EXTENDED_CITY_TAGS
        if hasattr(_module, 'EXTENDED_CITY_BASIC_INFO'):
            EXTENDED_CITY_BASIC_INFO = _module.EXTENDED_CITY_BASIC_INFO
except Exception as e:
    pass

MASS_CITY_COORDS = {}
MASS_CITY_TIPS = {}
MASS_CITY_TAGS = {}
MASS_CITY_INFO = {}

try:
    import importlib.util
    _mass_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mass_city_data.py')
    if os.path.exists(_mass_path):
        _spec = importlib.util.spec_from_file_location("mass_city_data", _mass_path)
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        if hasattr(_module, 'MASS_CITY_COORDS'):
            MASS_CITY_COORDS = _module.MASS_CITY_COORDS
        if hasattr(_module, 'MASS_CITY_TIPS'):
            MASS_CITY_TIPS = _module.MASS_CITY_TIPS
        if hasattr(_module, 'MASS_CITY_TAGS'):
            MASS_CITY_TAGS = _module.MASS_CITY_TAGS
        if hasattr(_module, 'MASS_CITY_INFO'):
            MASS_CITY_INFO = _module.MASS_CITY_INFO
except Exception as e:
    pass

MEGA_CITY_COORDS = {}
MEGA_CITY_TIPS = {}
MEGA_CITY_TAGS = {}
MEGA_CITY_INFO = {}

try:
    import importlib.util
    _mega_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mega_city_data.py')
    if os.path.exists(_mega_path):
        _spec = importlib.util.spec_from_file_location("mega_city_data", _mega_path)
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        if hasattr(_module, 'MEGA_CITY_COORDS'):
            MEGA_CITY_COORDS = _module.MEGA_CITY_COORDS
        if hasattr(_module, 'MEGA_CITY_TIPS'):
            MEGA_CITY_TIPS = _module.MEGA_CITY_TIPS
        if hasattr(_module, 'MEGA_CITY_TAGS'):
            MEGA_CITY_TAGS = _module.MEGA_CITY_TAGS
        if hasattr(_module, 'MEGA_CITY_INFO'):
            MEGA_CITY_INFO = _module.MEGA_CITY_INFO
except Exception as e:
    pass

CITY_COORDS = {
    "北京": (116.4074, 39.9042), "上海": (121.4737, 31.2304),
    "广州": (113.2644, 23.1291), "深圳": (114.0579, 22.5431),
    "杭州": (120.1551, 30.2741), "成都": (104.0665, 30.5728),
    "南京": (118.7674, 32.0415), "武汉": (114.3055, 30.5931),
    "西安": (108.9402, 34.3416), "重庆": (106.5516, 29.5630),
    "苏州": (120.5853, 31.2989), "天津": (117.2009, 39.1256),
    "长沙": (112.9388, 28.2282), "青岛": (120.3826, 36.0671),
    "大连": (121.6147, 38.9140), "厦门": (118.0894, 24.4798),
    "昆明": (102.8329, 24.8801), "贵阳": (106.7135, 26.5783),
    "桂林": (110.2992, 25.2742), "三亚": (109.5082, 18.2479),
    "福州": (119.2965, 26.0745), "宁波": (121.5498, 29.8684),
    "合肥": (117.2272, 31.8206), "郑州": (113.6254, 34.7466),
    "济南": (117.0009, 36.6758), "石家庄": (114.5149, 38.0428),
    "太原": (112.5489, 37.8706), "沈阳": (123.4315, 41.8057),
    "哈尔滨": (126.6424, 45.7567), "南昌": (115.8579, 28.6820),
    "南宁": (108.3665, 22.8170), "海口": (110.3494, 20.0174),
    "兰州": (103.8343, 36.0611), "银川": (106.2309, 38.4872),
    "西宁": (101.7782, 36.6232), "拉萨": (91.1322, 29.6500),
    "乌鲁木齐": (87.6168, 43.8256), "呼和浩特": (111.6756, 40.8428),
    "无锡": (120.3119, 31.4912), "常州": (119.9741, 31.8106),
    "南通": (120.8667, 32.0170), "徐州": (117.2847, 34.2616),
    "扬州": (119.4129, 32.3936), "绍兴": (120.5833, 30.0000),
    "嘉兴": (120.7555, 30.7469), "湖州": (120.0938, 30.8946),
    "金华": (119.6494, 29.0795), "台州": (121.4400, 28.6563),
    "温州": (120.6994, 28.0006), "泉州": (118.6758, 24.8741),
    "漳州": (117.6471, 24.5127), "洛阳": (112.4540, 34.6197),
    "开封": (114.3416, 34.7972), "南阳": (112.5328, 33.0042),
    "襄阳": (112.1400, 32.0420), "宜昌": (111.2864, 30.6919),
    "岳阳": (113.1289, 29.3562), "常德": (111.6856, 29.0318),
    "张家界": (110.4792, 29.1179), "绵阳": (104.7344, 31.4676),
    "德阳": (104.4058, 31.1279), "乐山": (103.7619, 29.5521),
    "宜宾": (104.5656, 28.7734), "遵义": (106.9073, 27.7254),
    "六盘水": (104.8333, 26.5944), "曲靖": (103.7961, 25.4890),
    "大理": (100.2676, 25.6065), "丽江": (100.2299, 26.8721),
    "咸阳": (108.7089, 34.3296), "宝鸡": (107.2370, 34.3550),
    "天水": (105.7249, 34.5809), "酒泉": (98.4941, 39.7321),
    "赤峰": (118.8870, 42.2579), "包头": (109.8403, 40.6571),
    "鞍山": (122.9956, 41.1087), "抚顺": (123.9736, 41.8819),
    "吉林": (126.5549, 43.8380), "四平": (124.3506, 43.1666),
    "齐齐哈尔": (123.9741, 47.3542), "牡丹江": (129.5968, 44.5527),
}

ALL_CITY_COORDS = {**CITY_COORDS, **EXTENDED_CITY_COORDS, **MASS_CITY_COORDS, **MEGA_CITY_COORDS}

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
    ],
    "杭州": [
        {"to": "上海", "duration": "50分钟", "price": 73},
        {"to": "南京", "duration": "1小时20分", "price": 142},
        {"to": "苏州", "duration": "1小时", "price": 110},
        {"to": "合肥", "duration": "2小时15分", "price": 180},
    ],
    "成都": [
        {"to": "重庆", "duration": "1小时30分", "price": 97},
        {"to": "西安", "duration": "3小时", "price": 263},
        {"to": "贵阳", "duration": "3小时30分", "price": 258},
        {"to": "昆明", "duration": "4小时30分", "price": 294},
    ],
    "南京": [
        {"to": "苏州", "duration": "1小时", "price": 110},
        {"to": "上海", "duration": "1小时15分", "price": 134},
        {"to": "合肥", "duration": "1小时", "price": 80},
        {"to": "杭州", "duration": "1小时20分", "price": 142},
    ],
    "武汉": [
        {"to": "长沙", "duration": "1小时30分", "price": 164},
        {"to": "合肥", "duration": "2小时", "price": 190},
        {"to": "南京", "duration": "3小时", "price": 260},
        {"to": "郑州", "duration": "2小时30分", "price": 240},
    ],
    "西安": [
        {"to": "郑州", "duration": "2小时", "price": 210},
        {"to": "成都", "duration": "3小时", "price": 263},
        {"to": "重庆", "duration": "3小时30分", "price": 280},
    ],
    "重庆": [
        {"to": "成都", "duration": "1小时30分", "price": 97},
        {"to": "贵阳", "duration": "2小时", "price": 160},
        {"to": "昆明", "duration": "4小时", "price": 280},
    ],
    "天津": [
        {"to": "北京", "duration": "30分钟", "price": 54.5},
        {"to": "济南", "duration": "1小时", "price": 110},
    ],
    "深圳": [
        {"to": "广州", "duration": "30分钟", "price": 74.5},
    ],
}

EXTENDED_HIGH_SPEED = {
    "北京": ["济南", "郑州", "太原", "沈阳", "哈尔滨"],
    "上海": ["苏州", "南京", "杭州", "合肥", "武汉"],
    "广州": ["深圳", "长沙", "桂林", "贵阳", "南宁"],
    "杭州": ["上海", "南京", "苏州", "宁波", "合肥"],
    "成都": ["重庆", "西安", "贵阳", "昆明", "武汉"],
    "南京": ["苏州", "上海", "合肥", "杭州", "武汉"],
    "武汉": ["长沙", "合肥", "南京", "郑州", "西安"],
    "西安": ["郑州", "成都", "重庆", "武汉", "太原"],
    "重庆": ["成都", "贵阳", "昆明", "西安", "武汉"],
    "苏州": ["上海", "南京", "杭州", "无锡", "合肥"],
    "天津": ["北京", "济南", "石家庄", "沈阳", "大连"],
    "长沙": ["武汉", "广州", "贵阳", "桂林", "南昌"],
    "郑州": ["北京", "西安", "武汉", "济南", "合肥"],
    "济南": ["北京", "上海", "郑州", "南京", "合肥"],
    "合肥": ["上海", "南京", "武汉", "杭州", "郑州"],
    "福州": ["厦门", "泉州", "温州", "宁波", "南昌"],
    "厦门": ["福州", "泉州", "漳州", "汕头", "深圳"],
    "青岛": ["济南", "烟台", "威海", "大连", "天津"],
    "大连": ["沈阳", "天津", "烟台", "威海"],
    "沈阳": ["哈尔滨", "大连", "长春", "锦州"],
    "哈尔滨": ["沈阳", "长春", "齐齐哈尔", "牡丹江"],
    "昆明": ["成都", "贵阳", "重庆", "大理", "丽江"],
    "贵阳": ["成都", "重庆", "昆明", "南宁", "长沙"],
    "桂林": ["长沙", "贵阳", "南宁", "广州"],
    "南宁": ["广州", "桂林", "贵阳", "昆明", "长沙"],
    "南昌": ["长沙", "武汉", "杭州", "福州", "合肥"],
    "太原": ["北京", "郑州", "西安", "石家庄"],
    "石家庄": ["北京", "济南", "太原", "郑州"],
    "宁波": ["杭州", "上海", "温州", "福州"],
    "温州": ["福州", "宁波", "杭州", "上海"],
    "无锡": ["上海", "南京", "苏州", "常州"],
    "常州": ["南京", "上海", "苏州", "无锡"],
    "南通": ["上海", "南京", "苏州", "泰州"],
    "扬州": ["南京", "镇江", "泰州", "淮安"],
    "绍兴": ["杭州", "宁波", "上海", "嘉兴"],
    "嘉兴": ["杭州", "上海", "宁波", "苏州"],
    "金华": ["杭州", "宁波", "温州", "义乌"],
    "台州": ["温州", "宁波", "绍兴", "金华"],
    "泉州": ["厦门", "福州", "漳州", "汕头"],
    "漳州": ["厦门", "泉州", "福州", "汕头"],
    "洛阳": ["郑州", "西安", "开封", "三门峡"],
    "开封": ["郑州", "洛阳", "商丘", "周口"],
    "襄阳": ["武汉", "南阳", "十堰", "西安"],
    "宜昌": ["武汉", "荆州", "荆门", "恩施"],
    "岳阳": ["长沙", "武汉", "常德", "益阳"],
    "常德": ["长沙", "岳阳", "益阳", "张家界"],
    "张家界": ["长沙", "常德", "湘西", "宜昌"],
    "绵阳": ["成都", "德阳", "广元", "江油"],
    "德阳": ["成都", "绵阳", "资阳", "遂宁"],
    "乐山": ["成都", "眉山", "宜宾", "自贡"],
    "宜宾": ["成都", "乐山", "自贡", "泸州"],
    "遵义": ["贵阳", "重庆", "成都", "泸州"],
    "六盘水": ["贵阳", "昆明", "遵义"],
    "曲靖": ["昆明", "贵阳", "六盘水"],
    "大理": ["昆明", "丽江", "楚雄", "保山"],
    "丽江": ["昆明", "大理", "香格里拉"],
    "咸阳": ["西安", "宝鸡", "渭南"],
    "宝鸡": ["西安", "咸阳", "天水"],
    "天水": ["西安", "宝鸡", "兰州"],
    "兰州": ["天水", "西宁", "银川", "酒泉"],
    "西宁": ["兰州", "银川", "拉萨"],
    "银川": ["兰州", "西宁", "呼和浩特"],
    "呼和浩特": ["银川", "包头", "大同"],
    "包头": ["呼和浩特", "鄂尔多斯", "大同"],
    "大同": ["太原", "呼和浩特", "包头"],
    "赤峰": ["沈阳", "通辽", "承德"],
    "承德": ["北京", "唐山", "赤峰"],
    "秦皇岛": ["唐山", "沈阳", "锦州"],
    "鞍山": ["沈阳", "大连", "营口"],
    "抚顺": ["沈阳", "本溪", "丹东"],
    "吉林": ["长春", "延吉", "四平"],
    "四平": ["长春", "沈阳", "辽源"],
    "齐齐哈尔": ["哈尔滨", "大庆", "牡丹江"],
    "牡丹江": ["哈尔滨", "鸡西", "七台河"],
    "海口": ["三亚", "文昌", "琼海"],
    "三亚": ["海口", "万宁", "陵水"],
}

CITY_TIPS = {
    "北京": {
        "food": ["北京烤鸭（全聚德、大董）", "炸酱面", "豆汁焦圈", "涮羊肉", "爆肚冯", "卤煮火烧", "驴打滚"],
        "food_spots": ["簋街（宵夜）", "王府井美食街", "南锣鼓巷小吃", "护国寺小吃街", "牛街（清真美食）"],
        "hotels": ["王府井附近（步行景点）", "前门附近（性价比高）", "国贸CBD（高档商务）", "三里屯（潮流聚集地）"],
        "attractions": ["故宫博物院（需预约）", "八达岭长城", "颐和园", "天坛公园", "天安门广场", "国家博物馆（免费）", "圆明园", "景山公园（俯瞰故宫）"],
        "attraction_tips": ["故宫8:30开门，建议提前半小时排队", "长城建议去八达岭或慕田峪，避免居庸关人多", "国家博物馆需提前1-7天预约", "升旗仪式时间每天不同，提前查好"],
        "avoid_traps": ["景区附近10元3个的便宜玉石多为假货", "不要在天坛、故宫门口找野导游", "火车站附近拉客住宿的要小心", "便宜的一日游多有购物陷阱"],
        "transport_tips": ["办一张交通卡或用支付宝乘车码", "早晚高峰地铁拥挤，错峰出行", "去八达岭可坐S2线火车", "市区景点地铁基本都能到"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-50", "total_daily": "200-400"},
            "mid": {"hotel": "400-800", "meal": "80-150", "transport": "50-100", "total_daily": "600-1000"},
            "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：天安门广场-故宫-景山-北海", "Day2：八达岭长城一日游", "Day3：颐和园-圆明园-清华北大", "Day4：天坛-国家博物馆-前门"],
        "best_photo_spots": ["景山山顶（拍故宫全景）", "角楼护城河（古建筑倒影）", "798艺术区（文艺打卡）", "后海（胡同风光）", "CBD观景台（城市夜景）"],
    },
    "上海": {
        "food": ["小笼包（南翔）", "生煎包（小杨生煎）", "红烧肉", "蟹粉面", "本帮菜（老吉士）", "葱油拌面", "粢饭糕"],
        "food_spots": ["城隍庙小吃广场", "黄河路美食街", "云南南路美食街", "寿宁路小龙虾", "新天地餐厅"],
        "hotels": ["外滩附近（江景房）", "南京路步行街（交通方便）", "陆家嘴（高端商务）", "田子坊附近（文艺小店）"],
        "attractions": ["外滩（必看）", "东方明珠", "上海中心（观景台）", "豫园", "迪士尼乐园", "博物馆（免费）", "田子坊", "新天地", "朱家角古镇"],
        "attraction_tips": ["外滩最佳观看时间：19:00-21:00", "上海中心118层观景台需提前购票", "迪士尼建议玩一整天，早9点到晚10点", "豫园灯会期间特别美"],
        "avoid_traps": ["外滩附近的拉客餐厅价格高", "豫园小商品多为义乌货", "陆家嘴地下通道有假古董", "不要坐无牌照黑车"],
        "transport_tips": ["地铁网络发达，推荐Metro大都会APP", "过江推荐坐地铁，避开大桥堵车", "朱家角可坐旅游专线", "市区骑行共享单车方便"],
        "budget": {
            "economy": {"hotel": "200-400", "meal": "40-80", "transport": "20-40", "total_daily": "300-500"},
            "mid": {"hotel": "500-1000", "meal": "100-200", "transport": "50-100", "total_daily": "700-1300"},
            "luxury": {"hotel": "1500+", "meal": "300+", "transport": "打车为主", "total_daily": "2000+"}
        },
        "itinerary_suggestion": ["Day1：外滩-南京路-豫园", "Day2：陆家嘴-东方明珠-上海中心", "Day3：迪士尼一日游", "Day4：田子坊-新天地-朱家角"],
        "best_photo_spots": ["外滩观景台（拍陆家嘴）", "上海中心118层（俯瞰上海）", "武康路（老洋房街拍）", "迪士尼城堡（日落时分）", "陆家嘴天桥（金融中心）"],
    },
    "广州": {
        "food": ["早茶（必试）", "煲仔饭", "肠粉", "叉烧", "双皮奶", "艇仔粥", "白切鸡", "虾饺"],
        "food_spots": ["上下九步行街", "北京路美食街", "江南西美食区", "建设六马路", "广州酒家（老字号）"],
        "hotels": ["珠江新城（高端商务）", "北京路附近（交通方便）", "上下九附近（性价比高）", "长隆附近（亲子）"],
        "attractions": ["广州塔（小蛮腰）", "长隆欢乐世界", "陈家祠", "沙面岛", "北京路步行街", "上下九", "越秀公园", "广东省博物馆（免费）"],
        "attraction_tips": ["广州塔建议17:30左右上，看日落+夜景", "长隆建议玩2天，动物世界+欢乐世界", "陈家祠木雕精美，值得细看", "沙面岛适合拍照，欧式建筑"],
        "avoid_traps": ["上下九步行街的名贵药材多为假货", "珠江夜游选正规码头", "不要相信地铁口拉客的低价一日游", "吃早茶选老字号，避免小店"],
        "transport_tips": ["地铁覆盖广，推荐广州地铁APP", "APM线直达珠江新城", "去长隆有旅游专线", "市区打车便宜"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-40", "total_daily": "200-400"},
            "mid": {"hotel": "400-800", "meal": "80-150", "transport": "40-80", "total_daily": "600-1000"},
            "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：广州塔-珠江夜游", "Day2：长隆一日游", "Day3：陈家祠-沙面-上下九", "Day4：北京路-越秀公园"],
        "best_photo_spots": ["广州塔底（仰拍）", "沙面岛欧式建筑", "石室圣心大教堂", "珠江两岸夜景", "岭南新天地"],
    },
    "杭州": {
        "food": ["西湖醋鱼", "东坡肉", "龙井虾仁", "片儿川", "叫花鸡", "定胜糕", "桂花糖藕", "小笼包"],
        "food_spots": ["河坊街", "胜利河美食街", "高银街", "南宋御街", "湖滨银泰"],
        "hotels": ["西湖边（湖景房）", "武林广场（交通方便）", "灵隐附近（禅意民宿）", "宋城附近（亲子）"],
        "attractions": ["西湖（必游）", "灵隐寺", "千岛湖", "宋城", "西溪湿地", "六和塔", "清河坊", "浙江省博物馆"],
        "attraction_tips": ["西湖骑共享单车游玩最佳", "灵隐寺门票30元，飞来峰45元", "千岛湖建议坐船游中心湖区", "宋城千古情演出必看"],
        "avoid_traps": ["河坊街的廉价丝绸多为假货", "西湖边拉客划船的价格虚高", "不要在景区门口买茶叶", "农家菜餐厅看人下菜"],
        "transport_tips": ["西湖景区公交车方便", "推荐杭州地铁APP", "去千岛湖可坐大巴", "市区共享单车多"],
        "budget": {
            "economy": {"hotel": "200-400", "meal": "40-80", "transport": "20-40", "total_daily": "300-500"},
            "mid": {"hotel": "500-1000", "meal": "100-180", "transport": "40-80", "total_daily": "700-1200"},
            "luxury": {"hotel": "1200+", "meal": "250+", "transport": "打车+游艇", "total_daily": "1800+"}
        },
        "itinerary_suggestion": ["Day1：西湖环湖-雷峰塔-河坊街", "Day2：灵隐寺-飞来峰-龙井村", "Day3：千岛湖一日游", "Day4：宋城-西溪湿地"],
        "best_photo_spots": ["断桥残雪（冬季）", "苏堤春晓（春季）", "三潭印月（月夜）", "雷峰塔（俯瞰西湖）", "龙井村茶园"],
    },
    "成都": {
        "food": ["火锅（必试）", "麻辣烫", "担担面", "龙抄手", "钟水饺", "夫妻肺片", "麻婆豆腐", "冰粉"],
        "food_spots": ["宽窄巷子", "锦里", "春熙路", "玉林路", "建设路小吃街"],
        "hotels": ["春熙路附近（商圈核心）", "太古里附近（时尚）", "宽窄巷子附近（文化）", "高新区（商务）"],
        "attractions": ["大熊猫繁育基地", "宽窄巷子", "锦里", "都江堰", "武侯祠", "杜甫草堂", "春熙路", "太古里", "青城山"],
        "attraction_tips": ["熊猫基地早上8点去看活泼的熊猫", "都江堰建议请讲解，了解水利工程", "青城山建议坐索道，节省体力", "武侯祠和锦里在一起"],
        "avoid_traps": ["景区门口的玉器、茶叶多为假货", "拉客去偏僻火锅店的要小心", "景区餐厅价格贵味道一般", "出租车推荐的店有回扣"],
        "transport_tips": ["地铁覆盖广，推荐成都地铁APP", "去熊猫基地坐地铁3号线", "去都江堰坐城际铁路30分钟", "市区打车方便"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-40", "total_daily": "200-400"},
            "mid": {"hotel": "400-800", "meal": "80-150", "transport": "40-80", "total_daily": "600-1000"},
            "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：熊猫基地-春熙路-太古里", "Day2：宽窄巷子-锦里-武侯祠", "Day3：都江堰一日游", "Day4：杜甫草堂-青城山"],
        "best_photo_spots": ["熊猫基地（熊猫特写）", "宽窄巷子（老成都）", "太古里（时尚街拍）", "都江堰（水利工程）", "锦里夜景"],
    },
    "重庆": {
        "food": ["火锅（必试）", "小面", "酸辣粉", "毛血旺", "烤鱼", "江湖菜", "凉虾", "蛋炒饭"],
        "food_spots": ["解放碑", "洪崖洞", "磁器口", "观音桥", "南滨路"],
        "hotels": ["解放碑附近（核心商圈）", "洪崖洞附近（夜景）", "观音桥附近（潮流）", "江北机场附近（中转）"],
        "attractions": ["洪崖洞（8D魔幻）", "解放碑", "磁器口古镇", "长江索道", "武隆天坑", "大足石刻", "鹅岭二厂", "李子坝轻轨"],
        "attraction_tips": ["洪崖洞最佳时间：19:00-21:00亮灯", "长江索道建议网上购票免排队", "武隆建议2天，天生三桥+地缝", "李子坝轻轨观景台人多"],
        "avoid_traps": ["景区门口的珠宝、古玩多为假货", "出租车不打表的别坐", "网红火锅店排队几小时的不值得", "磁器口的陈麻花有多家分店"],
        "transport_tips": ["地铁网络发达，但站点间距离远", "过江推荐坐索道或地铁", "武隆坐大巴约2小时", "市区打车便宜"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-40", "total_daily": "200-400"},
            "mid": {"hotel": "400-800", "meal": "80-150", "transport": "40-80", "total_daily": "600-1000"},
            "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：解放碑-洪崖洞-长江索道", "Day2：磁器口-鹅岭二厂-李子坝", "Day3：武隆一日游", "Day4：大足石刻一日游"],
        "best_photo_spots": ["洪崖洞夜景（千与千寻感）", "长江索道轿厢内", "李子坝轻轨穿楼", "鹅岭二厂天台", "南滨路看渝中半岛"],
    },
    "西安": {
        "food": ["肉夹馍", "羊肉泡馍", "凉皮", "biangbiang面", "葫芦头", "甑糕", "柿子饼", "油泼面"],
        "food_spots": ["回民街", "永兴坊", "小寨", "大雁塔南广场", "洒金桥"],
        "hotels": ["钟楼附近（交通方便）", "大雁塔附近（景点多）", "回民街附近（美食）", "高新区（商务）"],
        "attractions": ["兵马俑（世界奇迹）", "大雁塔", "古城墙（骑行）", "华清宫", "回民街", "陕西历史博物馆（免费）", "大唐不夜城", "华山"],
        "attraction_tips": ["兵马俑建议请讲解，分三个坑", "古城墙租自行车骑行13.7公里", "陕西博物馆需提前预约", "华山建议一日游或两日游"],
        "avoid_traps": ["兵马俑门口的假兵马俑要小心", "回民街的低价玉器是假货", "不要相信野导游带你看'优惠兵马俑'", "景区门口的石榴多为催熟"],
        "transport_tips": ["地铁覆盖主要景点", "去兵马俑坐游5路公交", "去华山坐高铁30分钟", "市区打车方便"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-40", "total_daily": "200-400"},
            "mid": {"hotel": "400-800", "meal": "80-150", "transport": "40-80", "total_daily": "600-1000"},
            "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：兵马俑-华清宫", "Day2：古城墙-大雁塔-大唐不夜城", "Day3：陕西博物馆-回民街-钟鼓楼", "Day4：华山一日游"],
        "best_photo_spots": ["兵马俑一号坑（军阵）", "古城墙骑行（黄昏）", "大唐不夜城（穿汉服）", "大雁塔音乐喷泉", "华山日出"],
    },
    "厦门": {
        "food": ["沙茶面", "海蛎煎", "土笋冻", "花生汤", "烧肉粽", "面线糊", "姜母鸭", "椰子饼"],
        "food_spots": ["中山路", "曾厝垵", "八市海鲜市场", "沙坡尾", "鼓浪屿龙头路"],
        "hotels": ["曾厝垵附近（文艺民宿）", "中山路附近（交通方便）", "鼓浪屿（岛上酒店）", "环岛路附近（海景）"],
        "attractions": ["鼓浪屿（必游）", "环岛路（骑行）", "曾厝垵", "厦门大学（需预约）", "南普陀寺", "万石植物园", "沙坡尾", "漳州火山岛"],
        "attraction_tips": ["鼓浪屿船票提前15天公众号买", "环岛路租自行车骑行2-3小时", "厦门大学需预约，周一闭馆", "万石植物园建议早上凉快"],
        "avoid_traps": ["鼓浪屿的低价海鲜餐要小心", "不要在景区门口买高仿奢侈品", "曾厝垵的网红餐厅排队久", "乘船去鼓浪屿选轮渡码头"],
        "transport_tips": ["地铁覆盖主要区域", "鼓浪屿船票要预约", "环岛路骑共享单车", "市区打车便宜"],
        "budget": {
            "economy": {"hotel": "200-400", "meal": "40-80", "transport": "30-50", "total_daily": "300-550"},
            "mid": {"hotel": "500-1000", "meal": "100-200", "transport": "50-100", "total_daily": "700-1300"},
            "luxury": {"hotel": "1200+", "meal": "250+", "transport": "打车+船票", "total_daily": "1800+"}
        },
        "itinerary_suggestion": ["Day1：鼓浪屿一日游", "Day2：环岛路-曾厝垵-厦门大学", "Day3：南普陀-万石植物园-沙坡尾", "Day4：漳州火山岛一日游"],
        "best_photo_spots": ["鼓浪屿龙头路", "环岛路海滩", "厦门大学芙蓉隧道", "沙坡尾艺术西区", "曾厝垵海边"],
    },
    "青岛": {
        "food": ["辣炒蛤蜊", "鲅鱼饺子", "原浆啤酒", "海鲜大排档", "葱烧海参", "三鲜水饺", "烤鱿鱼", "青岛啤酒"],
        "food_spots": ["台东步行街", "登州路啤酒街", "营口路海鲜市场", "中山路", "闽江路美食街"],
        "hotels": ["栈桥附近（海景）", "八大关附近（文艺）", "台东附近（性价比高）", "黄岛附近（新开发区）"],
        "attractions": ["栈桥", "八大关", "崂山", "青岛啤酒博物馆", "五四广场", "金沙滩", "中山公园", "石老人"],
        "attraction_tips": ["栈桥人多，建议早上或傍晚去", "崂山建议坐索道，节省体力", "啤酒博物馆了解青岛历史", "金沙滩比第一海水浴场好"],
        "avoid_traps": ["海鲜大排档的秤可能不准", "景区门口的崂山茶多为假货", "不要坐黑车去崂山", "游泳注意安全"],
        "transport_tips": ["地铁覆盖主要景点", "去崂山坐旅游专线", "市区公交车方便", "打车比上海便宜"],
        "budget": {
            "economy": {"hotel": "150-300", "meal": "40-80", "transport": "20-40", "total_daily": "250-500"},
            "mid": {"hotel": "400-800", "meal": "100-180", "transport": "40-80", "total_daily": "600-1100"},
            "luxury": {"hotel": "1000+", "meal": "250+", "transport": "打车为主", "total_daily": "1500+"}
        },
        "itinerary_suggestion": ["Day1：栈桥-八大关-五四广场", "Day2：崂山一日游", "Day3：啤酒博物馆-台东-金沙滩", "Day4：中山公园-石老人"],
        "best_photo_spots": ["栈桥回澜阁", "八大关花石楼", "五四广场五月的风", "崂山海边", "金沙滩日落"],
    },
    "三亚": {
        "food": ["海鲜（必吃）", "椰子鸡", "清补凉", "抱罗粉", "文昌鸡", "和乐蟹", "东山羊", "加积鸭"],
        "food_spots": ["第一市场", "林旺夜市", "海棠湾68美食街", "外贸路海鲜大排档", "商品街"],
        "hotels": ["亚龙湾（高档度假）", "海棠湾（新开发区）", "大东海（性价比高）", "三亚湾（海景便宜）"],
        "attractions": ["亚龙湾", "蜈支洲岛", "天涯海角", "南山寺", "大东海", "呀诺达雨林", "分界洲岛", "凤凰岛"],
        "attraction_tips": ["蜈支洲岛船票+门票约144元", "亚龙湾是最美海湾", "南山寺海上观音很震撼", "呀诺达雨林建议跟团"],
        "avoid_traps": ["海鲜市场缺斤少两严重，用公平秤", "不要在景区门口买高价水果", "潜水项目选正规公司", "出租车可能绕路"],
        "transport_tips": ["市区打车方便", "景点之间距离远，建议包车", "机场到市区有机场大巴", "共享单车少"],
        "budget": {
            "economy": {"hotel": "300-600", "meal": "60-120", "transport": "50-100", "total_daily": "500-900"},
            "mid": {"hotel": "800-1500", "meal": "150-300", "transport": "100-200", "total_daily": "1200-2000"},
            "luxury": {"hotel": "2000+", "meal": "400+", "transport": "包车游艇", "total_daily": "3000+"}
        },
        "itinerary_suggestion": ["Day1：亚龙湾-大东海", "Day2：蜈支洲岛一日游", "Day3：天涯海角-南山寺", "Day4：呀诺达雨林-第一市场"],
        "best_photo_spots": ["亚龙湾海滩", "蜈支洲岛情人桥", "天涯海角石碑", "南山寺海上观音", "三亚湾椰梦长廊日落"],
    },
    "桂林": {
        "food": ["桂林米粉（必试）", "啤酒鱼", "田螺酿", "荔浦芋扣肉", "桂花糕", "白果炖鸡", "油茶", "螺蛳粉"],
        "food_spots": ["东西巷", "正阳步行街", "尚水美食街", "椿记烧鹅", "小南国"],
        "hotels": ["两江四湖附近（市区）", "阳朔西街附近（热闹）", "兴坪古镇（幽静）", "龙脊梯田（民宿）"],
        "attractions": ["漓江（必游）", "阳朔西街", "龙脊梯田", "遇龙河", "银子岩", "两江四湖", "兴坪古镇", "十里画廊"],
        "attraction_tips": ["漓江游船建议坐4小时竹筏", "龙脊梯田建议住一晚看日出", "遇龙河比漓江人少", "十里画廊租自行车"],
        "avoid_traps": ["景区门口的玉石多为假货", "不要相信低价'漓江游'", "阳朔酒吧消费高", "出租车推荐的店有回扣"],
        "transport_tips": ["桂林到阳朔坐大巴约1.5小时", "漓江游船选正规码头", "龙脊梯田坐班车约2小时", "市区打车便宜"],
        "budget": {
            "economy": {"hotel": "200-400", "meal": "40-80", "transport": "50-100", "total_daily": "350-600"},
            "mid": {"hotel": "500-1000", "meal": "100-200", "transport": "100-200", "total_daily": "800-1500"},
            "luxury": {"hotel": "1500+", "meal": "300+", "transport": "包车竹筏", "total_daily": "2000+"}
        },
        "itinerary_suggestion": ["Day1：市区-两江四湖-东西巷", "Day2：漓江游船-阳朔西街", "Day3：遇龙河-十里画廊", "Day4：龙脊梯田一日游"],
        "best_photo_spots": ["漓江竹筏（二十元背景）", "龙脊梯田日出", "遇龙河田园风光", "阳朔西街夜景", "银子岩溶洞"],
    },
    "丽江": {
        "food": ["腊排骨火锅", "丽江粑粑", "纳西烤鱼", "鸡豆凉粉", "酥油茶", "奶锅", "黑山羊火锅", "野生菌火锅"],
        "food_spots": ["四方街", "五一街", "七一街", "忠义市场", "束河古镇"],
        "hotels": ["丽江古城内（客栈）", "束河古镇（清静）", "玉龙雪山附近", "大理古城（可选）"],
        "attractions": ["丽江古城（大研古镇）", "玉龙雪山", "束河古镇", "蓝月谷", "黑龙潭", "木府", "大理古城", "洱海"],
        "attraction_tips": ["玉龙雪山建议提前买票", "蓝月谷像小九寨", "古城维护费50元，7天有效", "大理洱海环湖一日游"],
        "avoid_traps": ["古城门口的低价玉器多为假货", "不要在古城门口买氧气瓶", "租车环湖有陷阱", "古城里拉客的要小心"],
        "transport_tips": ["丽江到大理坐火车约2小时", "玉龙雪山坐大巴约1小时", "古城内步行或骑电动车", "市区打车方便"],
        "budget": {
            "economy": {"hotel": "200-400", "meal": "50-100", "transport": "50-100", "total_daily": "400-700"},
            "mid": {"hotel": "500-1200", "meal": "120-250", "transport": "100-200", "total_daily": "800-1500"},
            "luxury": {"hotel": "1500+", "meal": "300+", "transport": "包车游艇", "total_daily": "2000+"}
        },
        "itinerary_suggestion": ["Day1：丽江古城-木府-黑龙潭", "Day2：玉龙雪山-蓝月谷", "Day3：束河古镇-忠义市场", "Day4：大理洱海一日游"],
        "best_photo_spots": ["四方街古城夜景", "玉龙雪山山顶", "蓝月谷湖水", "洱海倒影", "束河古镇"],
    },
}

ALL_CITY_TIPS = {**CITY_TIPS, **EXTENDED_CITY_TIPS}

DEFAULT_CITY_TIPS = {
    "food": ["当地特色小吃", "老字号餐厅", "夜市美食", "网红餐厅", "本地人的私房菜"],
    "food_spots": ["市中心步行街", "美食街", "老字号聚集区", "网红打卡餐厅"],
    "hotels": ["市中心附近（交通方便）", "景区附近（节省时间）", "商圈附近（购物方便）", "特色民宿"],
    "attractions": ["当地著名景点", "博物馆", "公园", "古镇", "自然风景区"],
    "attraction_tips": ["建议早上早去避开人流高峰", "请个讲解能了解更多历史", "提前查好开放时间", "穿舒适的鞋子"],
    "avoid_traps": ["景区门口的低价商品多为假货", "不要相信无牌照黑车", "注意保管好随身物品", "热门景点建议网上购票"],
    "transport_tips": ["推荐下载当地地铁APP", "市区打车比坐地铁方便", "景点之间有旅游专线", "共享单车短距离方便"],
    "budget": {
        "economy": {"hotel": "150-300", "meal": "30-60", "transport": "20-40", "total_daily": "200-400"},
        "mid": {"hotel": "400-800", "meal": "80-150", "transport": "40-80", "total_daily": "600-1000"},
        "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"}
    },
    "itinerary_suggestion": ["Day1：市区主要景点", "Day2：周边一日游", "Day3：深度游+美食探索"],
    "best_photo_spots": ["古城老街", "城市地标", "自然风光", "夜景灯光", "人文建筑"],
}

CITY_TAGS = {
    "北京": ["历史名城", "世界遗产", "皇家园林", "胡同文化", "都市"],
    "上海": ["国际都市", "外滩夜景", "主题乐园", "购物天堂", "海派文化"],
    "广州": ["美食之都", "千年商都", "岭南文化", "主题乐园"],
    "深圳": ["创新城市", "主题乐园", "海滨", "现代都市"],
    "杭州": ["西湖美景", "江南水乡", "茶文化", "世界遗产"],
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
    "丽江": ["古城", "雪山", "民族风情", "茶马古道"],
}

EXTENDED_CITY_TAGS = {
    "无锡": ["太湖", "灵山大佛", "影视基地", "江南"],
    "扬州": ["烟花三月", "瘦西湖", "淮扬菜", "古城"],
    "绍兴": ["鲁迅故里", "书法", "水乡", "师爷"],
    "嘉兴": ["乌镇", "西塘", "南湖", "古镇"],
    "湖州": ["莫干山", "南浔", "竹海", "民宿"],
    "金华": ["义乌", "横店", "双龙洞", "诸葛八卦村"],
    "温州": ["雁荡山", "楠溪江", "江心屿", "商帮"],
    "泉州": ["世遗", "海丝起点", "宗教博物馆", "美食"],
    "漳州": ["土楼", "火山岛", "滨海", "水果"],
    "洛阳": ["古都", "龙门石窟", "牡丹", "少林寺"],
    "开封": ["清明上河园", "菊花", "古城", "夜市"],
    "张家界": ["世界遗产", "阿凡达取景", "玻璃桥", "漂流"],
    "大理": ["苍山洱海", "古城", "蝴蝶泉", "风花雪月"],
    "烟台": ["海滨", "葡萄酒", "苹果", "海鲜"],
    "威海": ["海滨", "刘公岛", "成山头", "天鹅湖"],
    "黄山": ["世界遗产", "奇松怪石", "云海", "温泉"],
    "舟山": ["普陀山", "朱家尖", "东极岛", "海鲜"],
    "秦皇岛": ["北戴河", "山海关", "阿那亚", "鸽子窝"],
    "承德": ["避暑山庄", "外八庙", "坝上草原", "枫叶"],
    "平遥": ["古城", "票号", "陈醋", "摄影"],
    "五台山": ["佛教圣地", "文殊道场", "古寺庙", "登山"],
    "九寨沟": ["世界遗产", "人间仙境", "藏羌文化", "摄影"],
    "香格里拉": ["世外桃源", "普达措", "松赞林寺", "雪山"],
    "呼伦贝尔": ["草原", "牧场", "满洲里", "白桦林"],
    "敦煌": ["莫高窟", "月牙泉", "鸣沙山", "丝绸之路"],
    "吐鲁番": ["火焰山", "葡萄沟", "坎儿井", "古城"],
}

ALL_CITY_TAGS = {**CITY_TAGS, **EXTENDED_CITY_TAGS}

CITY_BASIC_INFO = {
    "北京": {
        "name": "北京", "province": "北京",
        "description": "千年古都，中国政治文化中心，拥有故宫、长城等世界文化遗产。四朝古都，历史底蕴深厚，胡同里藏着老北京的故事。",
        "rating": 4.8, "best_time": "9月-11月（秋季），4月-5月（春季）",
        "weather_tips": "冬季寒冷需保暖（-10度左右），夏季炎热注意防晒（35度以上），春秋最舒适（15-25度），早晚温差大",
        "transport": "地铁网络发达，覆盖所有主要景点，推荐使用亿通行APP或支付宝乘车码",
        "highlights": "故宫、长城、颐和园、天坛、天安门、国家博物馆",
        "image": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800",
        "avg_daily_budget": 500, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 5, "walkability": 4, "nightlife": 4,
    },
    "上海": {
        "name": "上海", "province": "上海",
        "description": "东方明珠，国际金融中心，海派文化与现代都市完美结合。外滩夜景、陆家嘴天际线、弄堂里的老上海风情。",
        "rating": 4.7, "best_time": "3月-5月，9月-11月",
        "weather_tips": "梅雨季节(6-7月)多雨潮湿，夏季炎热(35度以上)，冬季湿冷(5度左右)，春秋最舒适",
        "transport": "地铁密集，推荐Metro大都会APP，过江推荐坐地铁避开大桥堵车",
        "highlights": "外滩、东方明珠、上海中心、迪士尼、豫园、田子坊",
        "image": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=800",
        "avg_daily_budget": 600, "food_cost_level": 3, "transport_cost_level": 1,
        "safety_level": 5, "walkability": 4, "nightlife": 5,
    },
    "广州": {
        "name": "广州", "province": "广东",
        "description": "千年商都，南国明珠，美食之都，岭南文化中心。早茶文化、珠江夜游、广州塔小蛮腰。",
        "rating": 4.6, "best_time": "10月-次年4月",
        "weather_tips": "夏季炎热多雨(35度以上)，台风季注意安全，冬季温暖(15-20度)，无需厚外套",
        "transport": "地铁网络发达，推荐广州地铁APP，APM线直达珠江新城",
        "highlights": "广州塔、长隆、陈家祠、沙面、北京路",
        "image": "https://images.unsplash.com/photo-1559286456-b6976a7f4f64?w=800",
        "avg_daily_budget": 450, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 4, "walkability": 3, "nightlife": 4,
    },
    "杭州": {
        "name": "杭州", "province": "浙江",
        "description": "人间天堂，西湖美景闻名天下，龙井茶产地。断桥残雪、三潭印月，诗情画意的江南水乡。",
        "rating": 4.8, "best_time": "3月-5月，10月-11月",
        "weather_tips": "4月梅雨绵绵，7-8月高温酷暑(38度以上)，10月秋高气爽，西湖最美",
        "transport": "地铁公交覆盖，西湖景区有观光车，推荐杭州地铁APP",
        "highlights": "西湖、灵隐寺、千岛湖、宋城、西溪湿地",
        "image": "https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=800",
        "avg_daily_budget": 550, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 5, "walkability": 4, "nightlife": 3,
    },
    "成都": {
        "name": "成都", "province": "四川",
        "description": "天府之国，熊猫故乡，慢生活之都，美食天堂。茶馆文化、宽窄巷子、锦里古街，休闲惬意。",
        "rating": 4.7, "best_time": "3月-6月，9月-11月",
        "weather_tips": "气候温和湿润，四季分明，年均温15-22度，雾霾天注意防护",
        "transport": "地铁发达，推荐成都地铁APP，市区打车方便便宜",
        "highlights": "熊猫基地、宽窄巷子、都江堰、武侯祠、杜甫草堂",
        "image": "https://images.unsplash.com/photo-1533106418989-88406c7cc8ca?w=800",
        "avg_daily_budget": 400, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 5, "walkability": 3, "nightlife": 4,
    },
    "重庆": {
        "name": "重庆", "province": "重庆",
        "description": "山城雾都，8D魔幻城市，火锅之都，夜景媲美香港。洪崖洞、长江索道、李子坝轻轨穿楼。",
        "rating": 4.7, "best_time": "3月-5月，9月-11月",
        "weather_tips": "夏季炎热(38度以上)，有火炉之称，冬季潮湿多雾，能见度低",
        "transport": "地铁网络发达，推荐重庆地铁APP，过江推荐索道或地铁",
        "highlights": "洪崖洞、解放碑、磁器口、长江索道、武隆天坑",
        "image": "https://images.unsplash.com/photo-1555217851-6141535bd771?w=800",
        "avg_daily_budget": 400, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 4, "walkability": 2, "nightlife": 5,
    },
    "西安": {
        "name": "西安", "province": "陕西",
        "description": "十三朝古都，兵马俑世界第八大奇迹，丝绸之路起点。古城墙骑行、回民街美食、大唐不夜城。",
        "rating": 4.7, "best_time": "3月-5月，9月-11月",
        "weather_tips": "春秋干燥，夏季炎热(35度以上)，冬季寒冷(-5度左右)，注意补水防晒",
        "transport": "地铁覆盖市区，推荐西安地铁APP，去兵马俑坐游5路公交",
        "highlights": "兵马俑、大雁塔、古城墙、华清宫、陕西博物馆",
        "image": "https://images.unsplash.com/photo-1591247947424-42d8e2c63f8e?w=800",
        "avg_daily_budget": 400, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 4, "walkability": 3, "nightlife": 4,
    },
    "厦门": {
        "name": "厦门", "province": "福建",
        "description": "海上花园，浪漫海岛，文艺清新。鼓浪屿万国建筑、环岛路骑行、曾厝垵文艺小店。",
        "rating": 4.6, "best_time": "10月-次年4月",
        "weather_tips": "5-9月多雨多台风，夏季炎热(33度以上)，冬季温暖(15-20度)",
        "transport": "地铁覆盖主要区域，推荐厦门地铁APP，鼓浪屿船票要预约",
        "highlights": "鼓浪屿、环岛路、厦门大学、曾厝垵、南普陀",
        "image": "https://images.unsplash.com/photo-1528127269322-539801943592?w=800",
        "avg_daily_budget": 500, "food_cost_level": 2, "transport_cost_level": 2,
        "safety_level": 5, "walkability": 4, "nightlife": 3,
    },
    "青岛": {
        "name": "青岛", "province": "山东",
        "description": "海滨城市，啤酒之都，德式建筑，红瓦绿树。栈桥、八大关、崂山、五四广场。",
        "rating": 4.6, "best_time": "5月-10月",
        "weather_tips": "夏季凉爽多海雾，是避暑胜地，冬季寒冷(-5度左右)，春秋短暂",
        "transport": "地铁覆盖主要景点，推荐青岛地铁APP，去崂山坐旅游专线",
        "highlights": "栈桥、八大关、崂山、啤酒博物馆、五四广场",
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
        "avg_daily_budget": 450, "food_cost_level": 2, "transport_cost_level": 1,
        "safety_level": 5, "walkability": 3, "nightlife": 3,
    },
    "三亚": {
        "name": "三亚", "province": "海南",
        "description": "海岛度假天堂，热带风光，潜水胜地。亚龙湾、蜈支洲岛、天涯海角、南山寺。",
        "rating": 4.6, "best_time": "10月-次年4月",
        "weather_tips": "5-9月炎热多雨(35度以上)，台风季注意安全，冬季温暖(25度左右)，最佳",
        "transport": "市区打车方便，景点之间距离远建议包车，机场有大巴",
        "highlights": "亚龙湾、蜈支洲岛、天涯海角、南山寺、大东海",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
        "avg_daily_budget": 800, "food_cost_level": 3, "transport_cost_level": 2,
        "safety_level": 4, "walkability": 2, "nightlife": 3,
    },
    "桂林": {
        "name": "桂林", "province": "广西",
        "description": "山水甲天下，漓江风光，少数民族风情。20元人民币背景、龙脊梯田、遇龙河。",
        "rating": 4.7, "best_time": "4月-10月",
        "weather_tips": "4-6月雨季，7-8月炎热(35度以上)，10月秋高气爽，山水最美",
        "transport": "桂林到阳朔坐大巴约1.5小时，漓江游船选正规码头",
        "highlights": "漓江、阳朔西街、龙脊梯田、遇龙河、银子岩",
        "image": "https://images.unsplash.com/photo-1513415277900-a62401e19be4?w=800",
        "avg_daily_budget": 500, "food_cost_level": 2, "transport_cost_level": 2,
        "safety_level": 4, "walkability": 3, "nightlife": 3,
    },
    "丽江": {
        "name": "丽江", "province": "云南",
        "description": "古城雪山，民族风情，茶马古道。四方街古城、玉龙雪山、蓝月谷、束河古镇。",
        "rating": 4.6, "best_time": "10月-次年4月",
        "weather_tips": "高原气候，早晚温差大，紫外线强需防晒，冬季寒冷(0度左右)",
        "transport": "丽江到大理坐火车约2小时，玉龙雪山坐大巴约1小时",
        "highlights": "丽江古城、玉龙雪山、蓝月谷、束河古镇、大理洱海",
        "image": "https://images.unsplash.com/photo-1535962224032-6b9e04b2f65d?w=800",
        "avg_daily_budget": 600, "food_cost_level": 2, "transport_cost_level": 2,
        "safety_level": 4, "walkability": 3, "nightlife": 4,
    },
}

DEFAULT_CITY_INFO = {
    "name": "", "province": "",
    "description": "历史文化名城，有独特的地方风情和美食文化。",
    "rating": 4.5, "best_time": "3月-5月，9月-11月",
    "weather_tips": "四季分明，春秋最舒适，夏热冬冷",
    "transport": "地铁公交覆盖主要景点，打车方便",
    "highlights": "当地著名景点、博物馆、公园",
    "image": "",
    "avg_daily_budget": 400, "food_cost_level": 2, "transport_cost_level": 1,
    "safety_level": 4, "walkability": 3, "nightlife": 3,
}


def get_all_start_cities():
    cities = list(ALL_CITY_COORDS.keys())
    cities.sort()
    return cities


def get_destinations_count():
    beijing_count = len(BEIJING_3HR_DESTINATIONS)
    regular_count = len(ALL_CITY_COORDS)
    total = regular_count + beijing_count
    return total


def get_city_info(city):
    basic = CITY_BASIC_INFO.get(city, {})
    
    if city in EXTENDED_CITY_BASIC_INFO:
        ext = EXTENDED_CITY_BASIC_INFO[city]
        basic = {**basic, **{
            "highlights": ext.get("highlights", basic.get("highlights", "")),
            "description": ext.get("description", basic.get("description", "")),
            "rating": ext.get("rating", basic.get("rating", 4.5)),
            "best_time": ext.get("best_time", basic.get("best_time", "")),
            "weather_tips": ext.get("weather_tips", basic.get("weather_tips", "")),
            "transport": ext.get("transport", basic.get("transport", "")),
            "price": ext.get("price", basic.get("price", "")),
            "avg_daily_budget": ext.get("avg_daily_budget", basic.get("avg_daily_budget", 400)),
        }}
    elif city in MASS_CITY_INFO:
        mass = MASS_CITY_INFO[city]
        basic = {**basic, **{
            "highlights": mass.get("highlights", basic.get("highlights", "")),
            "description": mass.get("description", basic.get("description", "")),
            "rating": mass.get("rating", basic.get("rating", 4.5)),
            "best_time": mass.get("best_time", basic.get("best_time", "")),
            "weather_tips": mass.get("weather_tips", basic.get("weather_tips", "")),
            "transport": mass.get("transport", basic.get("transport", "")),
            "price": mass.get("price", basic.get("price", "")),
            "avg_daily_budget": mass.get("avg_daily_budget", basic.get("avg_daily_budget", 400)),
        }}
    elif city in MEGA_CITY_INFO:
        mega = MEGA_CITY_INFO[city]
        basic = {**basic, **{
            "highlights": mega.get("highlights", basic.get("highlights", "")),
            "description": mega.get("description", basic.get("description", "")),
            "rating": mega.get("rating", basic.get("rating", 4.5)),
            "best_time": mega.get("best_time", basic.get("best_time", "")),
            "weather_tips": mega.get("weather_tips", basic.get("weather_tips", "")),
            "transport": mega.get("transport", basic.get("transport", "")),
            "price": mega.get("price", basic.get("price", "")),
            "avg_daily_budget": mega.get("avg_daily_budget", basic.get("avg_daily_budget", 400)),
        }}
    
    if city in EXTENDED_CITY_TIPS:
        ext_tips = EXTENDED_CITY_TIPS[city]
        basic["tips"] = ext_tips
    elif city in MASS_CITY_TIPS:
        basic["tips"] = MASS_CITY_TIPS[city]
    elif city in MEGA_CITY_TIPS:
        basic["tips"] = MEGA_CITY_TIPS[city]
    else:
        extended = get_beijing_3hr_info(city)
        if extended:
            basic = {**basic, **{
                "highlights": extended.get("highlights", basic.get("highlights", "")),
                "description": extended.get("description", basic.get("description", "")),
                "rating": extended.get("rating", basic.get("rating", 4.5)),
                "best_time": extended.get("best_time", basic.get("best_time", "")),
            }}
            basic["tips"] = {
                "food": extended.get("food", []),
                "food_spots": extended.get("food_spots", []),
                "hotels": extended.get("hotels", []),
                "attractions": extended.get("attractions", []),
                "attraction_tips": extended.get("attraction_tips", []),
                "avoid_traps": extended.get("avoid_traps", []),
                "transport_tips": extended.get("transport_tips", []),
                "budget": extended.get("budget", {}),
                "itinerary_suggestion": extended.get("itinerary_suggestion", []),
                "best_photo_spots": extended.get("best_photo_spots", []),
                "clothing_advice": extended.get("clothing_advice", ""),
                "souvenirs": extended.get("souvenirs", []),
                "emergency_contacts": extended.get("emergency_contacts", {}),
                "accessibility": extended.get("accessibility", ""),
                "family_friendly": extended.get("family_friendly", 4),
                "couple_friendly": extended.get("couple_friendly", 4),
                "solo_friendly": extended.get("solo_friendly", 4),
                "nightlife": extended.get("nightlife", 2),
            }
        else:
            basic = {**DEFAULT_CITY_INFO, **basic}
            basic["tips"] = ALL_CITY_TIPS.get(city, DEFAULT_CITY_TIPS)
    
    basic["name"] = basic.get("name") or city
    if city in EXTENDED_CITY_COORDS:
        basic["coords"] = EXTENDED_CITY_COORDS[city]
    elif city in MASS_CITY_COORDS:
        basic["coords"] = MASS_CITY_COORDS[city]
    elif city in MEGA_CITY_COORDS:
        basic["coords"] = MEGA_CITY_COORDS[city]
    elif city in BEIJING_3HR_COORDS:
        basic["coords"] = BEIJING_3HR_COORDS[city]
    else:
        basic["coords"] = ALL_CITY_COORDS.get(city)
    
    if city in EXTENDED_CITY_TAGS:
        basic["tags"] = EXTENDED_CITY_TAGS[city]
    elif city in MASS_CITY_TAGS:
        basic["tags"] = MASS_CITY_TAGS[city]
    elif city in MEGA_CITY_TAGS:
        basic["tags"] = MEGA_CITY_TAGS[city]
    elif city in ALL_CITY_TAGS:
        basic["tags"] = ALL_CITY_TAGS[city]
    elif city in BEIJING_3HR_COORDS:
        basic["tags"] = ["北京周边", "高铁直达"]
    else:
        basic["tags"] = []
    
    return basic


def get_high_speed_routes(city):
    routes = list(CITY_HIGH_SPEED_DATA.get(city, []))
    extended = EXTENDED_HIGH_SPEED.get(city, [])
    if city == "北京":
        for name, dest_time in DESTINATION_TRAVEL_TIMES.items():
            if name not in {r["to"] for r in routes}:
                routes.append({
                    "to": name,
                    "duration": format_travel_time(dest_time),
                    "price": "参考价",
                })
    else:
        for dest in extended[:8]:
            if dest not in {r["to"] for r in routes}:
                routes.append({"to": dest, "duration": "约2-4小时", "price": "以实际为准"})
    return routes[:30]


def get_recommendations(from_city, max_duration_hours=3, preferences=None):
    recommendations = []
    seen = set()
    
    if from_city == "北京":
        if max_duration_hours >= 7:
            time_filter = 999
        else:
            time_filter = max_duration_hours
        
        beijing_dests = get_beijing_3hr_destinations(time_filter)
        
        for dest_data in beijing_dests:
            dest = dest_data["name"]
            info = dest_data["info"]
            coords = dest_data["coords"]
            travel_time = dest_data["travel_time_hours"]
            
            if not info:
                city_tips = ALL_CITY_TIPS.get(dest, {})
                if city_tips:
                    info = {
                        "highlights": city_tips.get("attractions", [])[:3],
                        "description": f"{dest}是中国著名城市",
                        "rating": 4.5,
                        "best_time": "3月-5月，9月-11月",
                        "food": city_tips.get("food", []),
                        "food_spots": city_tips.get("food_spots", []),
                        "hotels": city_tips.get("hotels", []),
                        "attractions": city_tips.get("attractions", []),
                        "attraction_tips": city_tips.get("attraction_tips", []),
                        "avoid_traps": city_tips.get("avoid_traps", []),
                        "transport_tips": city_tips.get("transport_tips", []),
                        "budget": city_tips.get("budget", {}),
                        "itinerary_suggestion": city_tips.get("itinerary_suggestion", []),
                        "best_photo_spots": city_tips.get("best_photo_spots", []),
                        "clothing_advice": "",
                        "souvenirs": [],
                        "emergency_contacts": {},
                        "accessibility": "",
                        "family_friendly": 4,
                        "couple_friendly": 4,
                        "solo_friendly": 4,
                        "nightlife": 2,
                    }
                else:
                    info = {**DEFAULT_EXTENDED_INFO, "highlights": dest, "description": f"{dest}是热门旅游目的地"}
            
            if dest in seen:
                continue
            seen.add(dest)
            
            basic_info = get_city_info(dest)
            
            recommendations.append({
                "city": dest,
                "duration": format_travel_time(travel_time),
                "price": "参考价",
                "tags": basic_info.get("tags", []),
                "image": basic_info.get("image", ""),
                "rating": info.get("rating", 4.5),
                "tips": {
                    "food": info.get("food", []),
                    "food_spots": info.get("food_spots", []),
                    "hotels": info.get("hotels", []),
                    "attractions": info.get("attractions", []),
                    "attraction_tips": info.get("attraction_tips", []),
                    "avoid_traps": info.get("avoid_traps", []),
                    "transport_tips": info.get("transport_tips", []),
                    "budget": info.get("budget", {}),
                    "itinerary_suggestion": info.get("itinerary_suggestion", []),
                    "best_photo_spots": info.get("best_photo_spots", []),
                    "clothing_advice": info.get("clothing_advice", ""),
                    "souvenirs": info.get("souvenirs", []),
                    "emergency_contacts": info.get("emergency_contacts", {}),
                    "accessibility": info.get("accessibility", ""),
                    "family_friendly": info.get("family_friendly", 4),
                    "couple_friendly": info.get("couple_friendly", 4),
                    "solo_friendly": info.get("solo_friendly", 4),
                    "nightlife": info.get("nightlife", 2),
                },
                "highlights": info.get("highlights", ""),
                "description": info.get("description", basic_info.get("description", "")),
                "best_time": info.get("best_time", basic_info.get("best_time", "")),
                "avg_daily_budget": basic_info.get("avg_daily_budget", 400),
                "travel_time_hours": travel_time,
            })
        
        if len(recommendations) < 30:
            others = [c for c in ALL_CITY_COORDS if c != from_city and c not in seen]
            random.shuffle(others)
            for dest in others[:30 - len(recommendations)]:
                basic_info = get_city_info(dest)
                seen.add(dest)
                recommendations.append({
                    "city": dest,
                    "duration": "约3-6小时",
                    "price": "以实际为准",
                    "tags": basic_info.get("tags", []),
                    "image": basic_info.get("image", ""),
                    "rating": basic_info.get("rating", 4.5),
                    "tips": basic_info.get("tips", {}),
                    "highlights": basic_info.get("highlights", ""),
                    "description": basic_info.get("description", ""),
                    "best_time": basic_info.get("best_time", ""),
                    "avg_daily_budget": basic_info.get("avg_daily_budget", 400),
                    "travel_time_hours": 4,
                })
    else:
        direct_routes = CITY_HIGH_SPEED_DATA.get(from_city, [])
        for route in direct_routes:
            dest = route["to"]
            if dest not in seen:
                basic_info = get_city_info(dest)
                seen.add(dest)
                recommendations.append({
                    "city": dest,
                    "duration": route["duration"],
                    "price": route["price"],
                    "tags": basic_info.get("tags", []),
                    "image": basic_info.get("image", ""),
                    "rating": basic_info.get("rating", 4.5),
                    "tips": basic_info.get("tips", {}),
                    "highlights": basic_info.get("highlights", ""),
                    "description": basic_info.get("description", ""),
                    "best_time": basic_info.get("best_time", ""),
                    "avg_daily_budget": basic_info.get("avg_daily_budget", 400),
                    "travel_time_hours": 3,
                })
        
        extended_routes = EXTENDED_HIGH_SPEED.get(from_city, [])
        for dest in extended_routes:
            if dest not in seen:
                basic_info = get_city_info(dest)
                seen.add(dest)
                recommendations.append({
                    "city": dest,
                    "duration": "约2-4小时",
                    "price": "以实际为准",
                    "tags": basic_info.get("tags", []),
                    "image": basic_info.get("image", ""),
                    "rating": basic_info.get("rating", 4.5),
                    "tips": basic_info.get("tips", {}),
                    "highlights": basic_info.get("highlights", ""),
                    "description": basic_info.get("description", ""),
                    "best_time": basic_info.get("best_time", ""),
                    "avg_daily_budget": basic_info.get("avg_daily_budget", 400),
                    "travel_time_hours": 3,
                })
        
        if len(recommendations) < 30:
            others = [c for c in ALL_CITY_COORDS if c != from_city and c not in seen]
            random.shuffle(others)
            for dest in others[:30 - len(recommendations)]:
                basic_info = get_city_info(dest)
                seen.add(dest)
                recommendations.append({
                    "city": dest,
                    "duration": "约3-6小时",
                    "price": "以实际为准",
                    "tags": basic_info.get("tags", []),
                    "image": basic_info.get("image", ""),
                    "rating": basic_info.get("rating", 4.5),
                    "tips": basic_info.get("tips", {}),
                    "highlights": basic_info.get("highlights", ""),
                    "description": basic_info.get("description", ""),
                    "best_time": basic_info.get("best_time", ""),
                    "avg_daily_budget": basic_info.get("avg_daily_budget", 400),
                    "travel_time_hours": 4,
                })
    
    if max_duration_hours >= 7:
        recommendations.sort(key=lambda x: (-x.get("rating", 0), x.get("travel_time_hours", 99)))
    else:
        recommendations.sort(key=lambda x: (x.get("travel_time_hours", 99), -x.get("rating", 0)))
    return recommendations[:200]


def compare_cities(cities):
    results = []
    for city in cities:
        info = get_city_info(city)
        results.append({
            "city": city,
            "province": info["province"],
            "description": info["description"],
            "rating": info["rating"],
            "avg_daily_budget": info["avg_daily_budget"],
            "food_cost_level": info["food_cost_level"],
            "transport_cost_level": info["transport_cost_level"],
            "safety_level": info["safety_level"],
            "walkability": info["walkability"],
            "nightlife": info["nightlife"],
            "best_time": info["best_time"],
            "highlights": info["highlights"],
            "tags": info["tags"],
            "image": info["image"],
            "tips_summary": {
                "food": info["tips"].get("food", [])[:3],
                "attractions": info["tips"].get("attractions", [])[:3],
                "budget": info["tips"].get("budget", {}),
            }
        })
    return results
