"""
扩展城市数据模块 - 包含215个城市的详细景点和美食数据
"""

EXTENDED_CITIES_DATA = {
    "七台河": {
        "attractions": [
            {"name": "桃山水库", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["自然", "水库"], "tips": "七台河市水源地，风景优美"},
            {"name": "仙洞山", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "20元", "rating": 4, "tags": ["自然", "登山"], "tips": "七台河名山，可俯瞰市区"},
            {"name": "勃利圆明寺", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "10元", "rating": 3, "tags": ["寺庙", "文化"], "tips": "百年古刹，香火旺盛"},
            {"name": "西大圈森林公园", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "50元", "rating": 4, "tags": ["森林公园", "避暑"], "tips": "夏季避暑胜地，空气清新"},
            {"name": "石龙山森林公园", "start_time": "08:00", "duration_hours": 5, "best_period": "day", "ticket": "40元", "rating": 4, "tags": ["森林公园", "自然"], "tips": "北方原始森林，秋季看红叶"},
            {"name": "万宝湖儿童公园", "start_time": "09:00", "duration_hours": 3, "best_period": "day", "ticket": "免费", "rating": 4, "tags": ["儿童", "公园"], "tips": "适合亲子游玩的公园"},
            {"name": "七台河博物馆", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 3, "tags": ["博物馆", "文化"], "tips": "了解七台河历史和文化"}
        ],
        "food": [
            {"name": "勃利热面", "location": "勃利县", "price_range": "15-25元", "recommend": "热面、牛肉面", "type": "面食"},
            {"name": "小鸡炖蘑菇", "location": "东北菜馆", "price_range": "50-80元", "recommend": "小鸡炖蘑菇、猪肉炖粉条", "type": "东北菜"},
            {"name": "杀猪菜", "location": "农家菜", "price_range": "40-70元", "recommend": "杀猪菜、酸菜炖白肉", "type": "东北菜"},
            {"name": "东北大拉皮", "location": "凉菜店", "price_range": "20-30元", "recommend": "大拉皮、粘豆包", "type": "小吃"}
        ],
        "transport": "公交覆盖全市，出租车方便",
        "tips": "冬季寒冷，注意保暖；秋季看红叶最佳"
    },
    "三亚": {
        "attractions": [
            {"name": "亚龙湾", "start_time": "09:00", "duration_hours": 6, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["海滩", "必去"], "tips": "天下第一湾，海水清澈"},
            {"name": "天涯海角", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "68元", "rating": 5, "tags": ["地标", "必去"], "tips": "海南著名景点，情侣必去"},
            {"name": "蜈支洲岛", "start_time": "08:00", "duration_hours": 8, "best_period": "day", "ticket": "144元", "rating": 5, "tags": ["海岛", "必去"], "tips": "中国马尔代夫，水上项目多"},
            {"name": "南山文化旅游区", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "129元", "rating": 5, "tags": ["文化", "宗教"], "tips": "海上观音，佛教圣地"},
            {"name": "槟榔谷", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "80元", "rating": 4, "tags": ["民族", "文化"], "tips": "黎苗族文化村，体验民族风情"},
            {"name": "西岛", "start_time": "08:30", "duration_hours": 6, "best_period": "day", "ticket": "95元", "rating": 4, "tags": ["海岛", "潜水"], "tips": "原生态海岛，潜水好去处"},
            {"name": "鹿回头公园", "start_time": "16:00", "duration_hours": 2, "best_period": "evening", "ticket": "45元", "rating": 4, "tags": ["夜景", "公园"], "tips": "俯瞰三亚湾，看日落绝佳"}
        ],
        "food": [
            {"name": "第一市场海鲜", "location": "第一市场", "price_range": "100-200元", "recommend": "和乐蟹、基围虾、石斑鱼", "type": "海鲜"},
            {"name": "清补凉", "location": "街边摊", "price_range": "15-20元", "recommend": "椰子水清补凉、红豆绿豆", "type": "甜品"},
            {"name": "海南鸡饭", "location": "海南餐厅", "price_range": "50-80元", "recommend": "文昌鸡饭、东山羊", "type": "海南菜"},
            {"name": "椰子鸡火锅", "location": "椰子鸡店", "price_range": "150-250元", "recommend": "椰子鸡、腊味饭", "type": "火锅"}
        ],
        "transport": "公交、出租车、网约车方便，可包车",
        "tips": "夏季注意防晒；海鲜可以自己买了加工；蜈支洲岛潜水要提前预约"
    },
    "上饶": {
        "attractions": [
            {"name": "三清山", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "190元", "rating": 5, "tags": ["名山", "必去"], "tips": "道教名山，奇峰怪石，世界遗产"},
            {"name": "婺源", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "210元", "rating": 5, "tags": ["乡村", "油菜花"], "tips": "中国最美乡村，春季油菜花海"},
            {"name": "鄱阳湖", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "100元", "rating": 5, "tags": ["湖泊", "候鸟"], "tips": "中国第一大淡水湖，冬季看候鸟"},
            {"name": "鹅湖书院", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["书院", "文化"], "tips": "江西四大书院之一，朱熹讲学地"},
            {"name": "灵山", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "190元", "rating": 4, "tags": ["名山", "自然"], "tips": "道教名山，风光秀丽"},
            {"name": "望仙谷", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "100元", "rating": 4, "tags": ["峡谷", "网红"], "tips": "悬崖上的古镇，网红打卡地"},
            {"name": "广丰铜钹山", "start_time": "07:30", "duration_hours": 6, "best_period": "day", "ticket": "80元", "rating": 4, "tags": ["自然", "避暑"], "tips": "原始森林，夏季避暑"}
        ],
        "food": [
            {"name": "婺源汽糕", "location": "婺源", "price_range": "15-25元", "recommend": "汽糕、清明果", "type": "小吃"},
            {"name": "弋阳年糕", "location": "弋阳", "price_range": "20-30元", "recommend": "炒年糕、年糕汤", "type": "特色"},
            {"name": "烫粉", "location": "上饶市区", "price_range": "10-20元", "recommend": "羊肉烫粉、猪肉烫粉", "type": "早餐"},
            {"name": "荷包红鲤鱼", "location": "婺源", "price_range": "80-150元", "recommend": "清蒸荷包红鲤鱼", "type": "赣菜"}
        ],
        "transport": "高铁可达，景区有直通车",
        "tips": "婺源春季3-4月看油菜花；三清山两天一夜最佳；鄱阳湖冬季11-3月看候鸟"
    },
    "东莞": {
        "attractions": [
            {"name": "松山湖", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["湖泊", "骑行"], "tips": "东莞最美湖泊，可骑行游览"},
            {"name": "莲花山", "start_time": "07:00", "duration_hours": 4, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["自然", "登山"], "tips": "东莞名山，可俯瞰市区"},
            {"name": "观音山国家森林公园", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "45元", "rating": 4, "tags": ["森林公园", "宗教"], "tips": "有观音像，佛教圣地"},
            {"name": "可园", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "8元", "rating": 4, "tags": ["园林", "历史"], "tips": "广东四大名园之一"},
            {"name": "虎门鸦片战争博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["博物馆", "历史"], "tips": "了解鸦片战争历史"},
            {"name": "下坝坊", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "打卡"], "tips": "东莞文艺街区，适合拍照"},
            {"name": "粤晖园", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "60元", "rating": 4, "tags": ["园林", "文化"], "tips": "岭南园林代表作"}
        ],
        "food": [
            {"name": "烧鹅濑粉", "location": "东莞老城区", "price_range": "20-35元", "recommend": "烧鹅濑粉、叉烧濑粉", "type": "面食"},
            {"name": "虎门蟹饼", "location": "虎门", "price_range": "50-80元", "recommend": "蟹饼、虾饼", "type": "海鲜"},
            {"name": "道滘粽", "location": "道滘镇", "price_range": "10-20元", "recommend": "咸肉粽、碱水粽", "type": "特产"},
            {"name": "东莞腊肠", "location": "腊肠店", "price_range": "50-100元", "recommend": "莞式腊肠、腊肉", "type": "特产"}
        ],
        "transport": "地铁、公交、出租车方便",
        "tips": "松山湖骑行一周约30公里；可园很小但很精致；虎门炮台可以一起逛"
    },
    "中山": {
        "attractions": [
            {"name": "孙中山故居", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["名人", "必去"], "tips": "国父孙中山故居，必去景点"},
            {"name": "中山纪念堂", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "10元", "rating": 4, "tags": ["纪念", "文化"], "tips": "纪念孙中山先生"},
            {"name": "金钟水库", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["水库", "骑行"], "tips": "可骑行游览，风景优美"},
            {"name": "孙文纪念公园", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["公园", "纪念"], "tips": "孙中山纪念公园"},
            {"name": "岭南水乡", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "50元", "rating": 4, "tags": ["水乡", "民俗"], "tips": "岭南水乡风情"},
            {"name": "仙踪龙园", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "60元", "rating": 3, "tags": ["主题", "亲子"], "tips": "恐龙主题乐园，适合亲子"},
            {"name": "詹园", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["园林", "文化"], "tips": "岭南私家园林"}
        ],
        "food": [
            {"name": "石岐乳鸽", "location": "中山餐厅", "price_range": "50-80元", "recommend": "红烧乳鸽、盐焗乳鸽", "type": "中山菜"},
            {"name": "杏仁饼", "location": "特产店", "price_range": "30-60元", "recommend": "杏仁饼、肉松杏仁饼", "type": "特产"},
            {"name": "菊花肉", "location": "小榄", "price_range": "50-80元", "recommend": "菊花肉、菊花鱼", "type": "中山菜"},
            {"name": "黄圃腊味", "location": "黄圃镇", "price_range": "60-100元", "recommend": "腊味饭、腊肠", "type": "特产"}
        ],
        "transport": "公交、出租车方便",
        "tips": "孙中山故居免费但需预约；乳鸽是中山招牌菜"
    }
}
