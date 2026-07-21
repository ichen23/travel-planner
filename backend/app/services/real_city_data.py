"""
真实的城市景点数据 - 覆盖中国主要城市
所有景点名称均为真实存在的著名景点
"""

REAL_CITY_ATTRACTIONS = {
    "北京": {
        "attractions": [
            {"name": "故宫博物院", "start_time": "08:30", "duration_hours": 5, "best_period": "morning", "ticket": "60元", "rating": 5, "tags": ["历史", "必去"], "tips": "紫禁城，建议提前3天预约门票"},
            {"name": "八达岭长城", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "40元", "rating": 5, "tags": ["历史", "必去"], "tips": "万里长城最具代表性的一段"},
            {"name": "颐和园", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "30元", "rating": 5, "tags": ["园林", "历史"], "tips": "中国清朝皇家园林"},
            {"name": "天坛", "start_time": "07:30", "duration_hours": 3, "best_period": "morning", "ticket": "15元", "rating": 5, "tags": ["宗教", "历史"], "tips": "明清皇帝祭天场所"},
            {"name": "天安门广场", "start_time": "06:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["地标", "必去"], "tips": "看升旗仪式需早到"},
            {"name": "圆明园", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "25元", "rating": 4, "tags": ["历史", "教育"], "tips": "遗址公园，勿忘国耻"},
            {"name": "南锣鼓巷", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["胡同", "文艺"], "tips": "老北京胡同文化"},
            {"name": "什刹海", "start_time": "15:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["夜景", "酒吧"], "tips": "后海酒吧街，夜晚热闹"}
        ],
        "food": [
            {"name": "全聚德烤鸭", "location": "前门", "price_range": "200-400元", "recommend": "挂炉烤鸭", "type": "京菜"},
            {"name": "东来顺涮羊肉", "location": "王府井", "price_range": "150-300元", "recommend": "铜锅涮肉", "type": "火锅"},
            {"name": "北京炸酱面", "location": "老北京面馆", "price_range": "20-40元", "recommend": "北京炸酱面", "type": "面食"},
            {"name": "豆汁焦圈", "location": "老北京小吃", "price_range": "10-20元", "recommend": "豆汁、焦圈、咸菜", "type": "小吃"}
        ],
        "transport": "地铁1-16号线覆盖全市",
        "tips": "故宫、长城需提前预约；天安门需安检；颐和园圆明园可一起游览"
    },
    "上海": {
        "attractions": [
            {"name": "外滩", "start_time": "17:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "地标"], "tips": "上海地标，晚上灯光最美"},
            {"name": "东方明珠", "start_time": "10:00", "duration_hours": 3, "best_period": "morning", "ticket": "160元", "rating": 5, "tags": ["地标", "必去"], "tips": "上海标志建筑"},
            {"name": "豫园", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["园林", "古街"], "tips": "江南古典园林"},
            {"name": "上海博物馆", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "中国四大博物馆之一"},
            {"name": "南京路步行街", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "地标"], "tips": "中华商业第一街"},
            {"name": "上海迪士尼乐园", "start_time": "09:00", "duration_hours": 8, "best_period": "day", "ticket": "475元", "rating": 5, "tags": ["主题乐园", "必去"], "tips": "中国首座迪士尼"},
            {"name": "田子坊", "start_time": "13:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "打卡"], "tips": "老弄堂改造的艺术区"},
            {"name": "朱家角古镇", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "60元", "rating": 4, "tags": ["古镇", "江南"], "tips": "上海水乡古镇"}
        ],
        "food": [
            {"name": "南翔小笼包", "location": "豫园", "price_range": "50-100元", "recommend": "小笼包、蟹粉小笼", "type": "本帮菜"},
            {"name": "小杨生煎", "location": "多家分店", "price_range": "30-60元", "recommend": "鲜肉生煎", "type": "小吃"},
            {"name": "本帮红烧肉", "location": "上海老饭店", "price_range": "80-150元", "recommend": "红烧肉、响油鳝糊", "type": "本帮菜"},
            {"name": "上海青团", "location": "杏花楼", "price_range": "10-20元", "recommend": "豆沙青团、肉松青团", "type": "糕点"}
        ],
        "transport": "地铁1-18号线覆盖全市",
        "tips": "外滩晚上最美；博物馆周一闭馆；迪士尼需一整天"
    },
    "广州": {
        "attractions": [
            {"name": "广州塔", "start_time": "18:00", "duration_hours": 2, "best_period": "evening", "ticket": "150元", "rating": 5, "tags": ["夜景", "地标"], "tips": "小蛮腰，广州地标"},
            {"name": "沙面岛", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["欧陆风情", "拍照"], "tips": "欧陆风情建筑群"},
            {"name": "陈家祠", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "10元", "rating": 4, "tags": ["岭南建筑", "文化"], "tips": "岭南建筑艺术明珠"},
            {"name": "长隆旅游度假区", "start_time": "09:30", "duration_hours": 8, "best_period": "day", "ticket": "300元", "rating": 5, "tags": ["主题乐园", "必去"], "tips": "中国最大的主题乐园集群"},
            {"name": "北京路步行街", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "美食"], "tips": "千年古道遗址"},
            {"name": "广州博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 4, "tags": ["文化", "历史"], "tips": "广州历史文化"},
            {"name": "珠江夜游", "start_time": "19:30", "duration_hours": 2, "best_period": "evening", "ticket": "80元", "rating": 4, "tags": ["夜游", "江景"], "tips": "看广州夜景"},
            {"name": "白云山", "start_time": "07:00", "duration_hours": 4, "best_period": "morning", "ticket": "5元", "rating": 4, "tags": ["登山", "自然"], "tips": "羊城第一秀"}
        ],
        "food": [
            {"name": "广式早茶", "location": "莲香楼", "price_range": "80-150元", "recommend": "虾饺、烧卖、凤爪", "type": "早茶"},
            {"name": "广州肠粉", "location": "银记肠粉", "price_range": "15-25元", "recommend": "牛肉肠粉、鲜虾肠粉", "type": "小吃"},
            {"name": "广州煲汤", "location": "广州酒家", "price_range": "100-200元", "recommend": "老火靓汤、白切鸡", "type": "粤菜"},
            {"name": "双皮奶", "location": "义统双皮奶", "price_range": "10-20元", "recommend": "红豆双皮奶、芒果双皮奶", "type": "甜品"}
        ],
        "transport": "地铁1-9号线覆盖全市",
        "tips": "早茶是广州特色；长隆建议玩2天；珠江夜游值得"
    },
    "深圳": {
        "attractions": [
            {"name": "世界之窗", "start_time": "09:30", "duration_hours": 6, "best_period": "day", "ticket": "220元", "rating": 4, "tags": ["主题乐园", "拍照"], "tips": "微缩世界名胜"},
            {"name": "欢乐谷", "start_time": "09:30", "duration_hours": 8, "best_period": "day", "ticket": "230元", "rating": 4, "tags": ["主题乐园", "刺激"], "tips": "大型游乐场"},
            {"name": "东部华侨城", "start_time": "09:00", "duration_hours": 6, "best_period": "day", "ticket": "200元", "rating": 4, "tags": ["度假", "自然"], "tips": "山海度假胜地"},
            {"name": "莲花山公园", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 3, "tags": ["公园", "休闲"], "tips": "俯瞰深圳中心区"},
            {"name": "大梅沙海滨公园", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "免费", "rating": 4, "tags": ["海滩", "游泳"], "tips": "深圳最大的免费海滨浴场"},
            {"name": "深圳博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 4, "tags": ["文化", "历史"], "tips": "深圳改革开放历史"},
            {"name": "大鹏所城", "start_time": "08:00", "duration_hours": 4, "best_period": "day", "ticket": "免费", "rating": 4, "tags": ["古城", "历史"], "tips": "明清海防军事要塞"},
            {"name": "梧桐山", "start_time": "06:00", "duration_hours": 6, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["登山", "自然"], "tips": "深圳最高峰"}
        ],
        "food": [
            {"name": "潮汕牛肉火锅", "location": "海记牛肉", "price_range": "80-150元", "recommend": "吊龙、匙仁、牛丸", "type": "火锅"},
            {"name": "客家盆菜", "location": "客家菜馆", "price_range": "150-300元", "recommend": "海鲜盆菜、素盆菜", "type": "粤菜"},
            {"name": "深圳沙井蚝", "location": "沙井镇", "price_range": "80-150元", "recommend": "清蒸生蚝、蒜蓉生蚝", "type": "海鲜"},
            {"name": "云吞面", "location": "麦奀记", "price_range": "30-50元", "recommend": "虾籽云吞面", "type": "面食"}
        ],
        "transport": "地铁1-8号线覆盖全市",
        "tips": "主题乐园需一整天；大鹏所城在郊区可顺路去海边；周末人多"
    },
    "杭州": {
        "attractions": [
            {"name": "西湖", "start_time": "07:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费", "rating": 5, "tags": ["必去", "自然"], "tips": "杭州灵魂，绕湖步行或骑车"},
            {"name": "灵隐寺", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "75元", "rating": 5, "tags": ["宗教", "历史"], "tips": "千年古刹，飞来峰石刻"},
            {"name": "千岛湖", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "150元", "rating": 5, "tags": ["自然", "必去"], "tips": "天下第一秀水"},
            {"name": "宋城", "start_time": "14:00", "duration_hours": 5, "best_period": "afternoon", "ticket": "310元", "rating": 5, "tags": ["主题", "演出"], "tips": "宋城千古情必看"},
            {"name": "西溪湿地", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "80元", "rating": 4, "tags": ["自然", "生态"], "tips": "城市湿地"},
            {"name": "雷峰塔", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["地标", "夜景"], "tips": "登塔看西湖全景"},
            {"name": "河坊街", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "南宋御街"},
            {"name": "龙井村", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["茶园", "乡村"], "tips": "龙井茶叶产地"}
        ],
        "food": [
            {"name": "楼外楼", "location": "孤山", "price_range": "150-300元", "recommend": "西湖醋鱼、龙井虾仁、东坡肉", "type": "浙菜"},
            {"name": "知味观", "location": "湖滨", "price_range": "60-120元", "recommend": "片儿川、小笼包", "type": "特色"},
            {"name": "外婆家", "location": "多家分店", "price_range": "50-100元", "recommend": "茶香鸡、麻婆豆腐", "type": "杭帮菜"},
            {"name": "葱包桧", "location": "河坊街", "price_range": "10-20元", "recommend": "葱包桧、定胜糕", "type": "小吃"}
        ],
        "transport": "地铁1-5号线覆盖全市",
        "tips": "西湖早晚最美；千岛湖建议跟团或包车；灵隐寺人多"
    },
    "成都": {
        "attractions": [
            {"name": "大熊猫繁育研究基地", "start_time": "07:30", "duration_hours": 4, "best_period": "morning", "ticket": "55元", "rating": 5, "tags": ["必去", "亲子"], "tips": "看大熊猫，早上最活跃"},
            {"name": "宽窄巷子", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "文化"], "tips": "成都慢生活"},
            {"name": "锦里古街", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古街", "美食"], "tips": "三国文化主题"},
            {"name": "都江堰", "start_time": "07:00", "duration_hours": 6, "best_period": "morning", "ticket": "80元", "rating": 5, "tags": ["历史", "必去"], "tips": "世界遗产，古代水利工程"},
            {"name": "武侯祠", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["历史", "文化"], "tips": "三国文化圣地"},
            {"name": "杜甫草堂", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "50元", "rating": 4, "tags": ["文化", "园林"], "tips": "诗圣故居"},
            {"name": "春熙路", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "夜景"], "tips": "成都最繁华商业街"},
            {"name": "青城山", "start_time": "07:00", "duration_hours": 6, "best_period": "day", "ticket": "80元", "rating": 4, "tags": ["名山", "道教"], "tips": "道教名山，可一日游"}
        ],
        "food": [
            {"name": "小龙坎火锅", "location": "春熙路", "price_range": "80-150元", "recommend": "毛肚、鹅肠、酥肉", "type": "火锅"},
            {"name": "陈麻婆豆腐", "location": "青华路", "price_range": "40-80元", "recommend": "麻婆豆腐、回锅肉", "type": "川菜"},
            {"name": "龙抄手", "location": "春熙路", "price_range": "20-40元", "recommend": "红油抄手、钟水饺", "type": "小吃"},
            {"name": "担担面", "location": "街边店", "price_range": "10-20元", "recommend": "麻辣担担面", "type": "面食"}
        ],
        "transport": "地铁1-7号线覆盖全市",
        "tips": "熊猫基地早去；都江堰可一日游；火锅配凉茶"
    },
    "重庆": {
        "attractions": [
            {"name": "洪崖洞", "start_time": "18:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "打卡"], "tips": "千与千寻原型，夜景必看"},
            {"name": "解放碑", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "购物"], "tips": "重庆地标，周边商圈繁华"},
            {"name": "磁器口古镇", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["古镇", "美食"], "tips": "千年古镇"},
            {"name": "长江索道", "start_time": "09:00", "duration_hours": 1, "best_period": "morning", "ticket": "20元", "rating": 4, "tags": ["体验", "打卡"], "tips": "空中看重庆"},
            {"name": "武隆天坑", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "175元", "rating": 5, "tags": ["自然", "必去"], "tips": "世界自然遗产"},
            {"name": "鹅岭二厂", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "拍照"], "tips": "网红打卡地"},
            {"name": "李子坝轻轨", "start_time": "08:00", "duration_hours": 1, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["打卡", "交通"], "tips": "轻轨穿楼，网红景点"},
            {"name": "三峡博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 4, "tags": ["文化", "历史"], "tips": "三峡历史文化"}
        ],
        "food": [
            {"name": "重庆火锅", "location": "洞子老火锅", "price_range": "80-150元", "recommend": "毛肚、鸭肠、黄喉", "type": "火锅"},
            {"name": "重庆小面", "location": "街边摊", "price_range": "10-20元", "recommend": "麻辣小面、豌杂面", "type": "面食"},
            {"name": "酸辣粉", "location": "解放碑", "price_range": "15-25元", "recommend": "手工酸辣粉", "type": "小吃"},
            {"name": "重庆烤鱼", "location": "万州烤鱼", "price_range": "100-200元", "recommend": "麻辣烤鱼、泡椒烤鱼", "type": "川菜"}
        ],
        "transport": "地铁1-10号线覆盖全市",
        "tips": "洪崖洞晚上最美；武隆建议包车；山路多穿舒适鞋"
    },
    "西安": {
        "attractions": [
            {"name": "秦始皇兵马俑", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "120元", "rating": 5, "tags": ["历史", "必去"], "tips": "世界第八大奇迹"},
            {"name": "大雁塔", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["宗教", "地标"], "tips": "唐代佛教建筑"},
            {"name": "西安城墙", "start_time": "08:00", "duration_hours": 3, "best_period": "morning", "ticket": "54元", "rating": 5, "tags": ["历史", "必去"], "tips": "中国最完整古城墙，可骑自行车"},
            {"name": "华清宫", "start_time": "10:00", "duration_hours": 3, "best_period": "morning", "ticket": "120元", "rating": 4, "tags": ["历史", "温泉"], "tips": "唐明皇与杨贵妃的行宫"},
            {"name": "陕西历史博物馆", "start_time": "09:00", "duration_hours": 4, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["文化", "必去"], "tips": "国家级博物馆"},
            {"name": "回民街", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["美食", "夜景"], "tips": "西安美食聚集地"},
            {"name": "大唐不夜城", "start_time": "18:00", "duration_hours": 3, "best_period": "evening", "ticket": "免费", "rating": 5, "tags": ["夜景", "打卡"], "tips": "盛唐主题街区"},
            {"name": "华山", "start_time": "06:00", "duration_hours": 10, "best_period": "day", "ticket": "160元", "rating": 5, "tags": ["名山", "必去"], "tips": "五岳之西岳"}
        ],
        "food": [
            {"name": "老孙家泡馍", "location": "东大街", "price_range": "30-60元", "recommend": "羊肉泡馍、牛肉泡馍", "type": "西北菜"},
            {"name": "回民街小吃", "location": "北院门", "price_range": "20-50元", "recommend": "肉夹馍、凉皮、甑糕", "type": "小吃"},
            {"name": "魏家凉皮", "location": "多家分店", "price_range": "15-30元", "recommend": "秘制凉皮", "type": "小吃"},
            {"name": "西安饭庄", "location": "东大街", "price_range": "80-150元", "recommend": "葫芦鸡、水晶饼", "type": "陕菜"}
        ],
        "transport": "地铁1-4号线覆盖全市",
        "tips": "兵马俑早去；陕博周一闭馆；华山可一日游或两日"
    },
    "厦门": {
        "attractions": [
            {"name": "鼓浪屿", "start_time": "08:00", "duration_hours": 5, "best_period": "day", "ticket": "35元（船票）", "rating": 5, "tags": ["必去", "岛屿"], "tips": "厦门必去，需提前买船票"},
            {"name": "厦门大学", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费（需预约）", "rating": 5, "tags": ["名校", "必去"], "tips": "中国最美大学之一"},
            {"name": "环岛路", "start_time": "15:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 5, "tags": ["海滨", "骑行"], "tips": "最美海滨骑行道"},
            {"name": "曾厝垵", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["文艺", "小吃"], "tips": "海边文艺村"},
            {"name": "南普陀寺", "start_time": "08:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["宗教", "历史"], "tips": "闽南佛教胜地"},
            {"name": "中山路步行街", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["购物", "美食"], "tips": "厦门老街"},
            {"name": "万石植物园", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["自然", "拍照"], "tips": "多肉植物区拍照好看"},
            {"name": "火山岛", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "60元", "rating": 4, "tags": ["海岛", "地质"], "tips": "可一日游"}
        ],
        "food": [
            {"name": "沙茶面", "location": "乌糖沙茶面", "price_range": "25-40元", "recommend": "招牌沙茶面", "type": "面食"},
            {"name": "海蛎煎", "location": "莲欢海蛎煎", "price_range": "30-50元", "recommend": "海蛎煎蛋", "type": "小吃"},
            {"name": "土笋冻", "location": "西门土笋冻", "price_range": "20-30元", "recommend": "原味土笋冻", "type": "小吃"},
            {"name": "花生汤", "location": "黄则和", "price_range": "10-20元", "recommend": "花生汤、馅饼", "type": "甜品"}
        ],
        "transport": "地铁1-2号线，公交、BRT方便",
        "tips": "鼓浪屿船票提前买；厦大需预约；环岛路骑行"
    },
    "青岛": {
        "attractions": [
            {"name": "栈桥", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "海边"], "tips": "青岛标志性建筑"},
            {"name": "八大关", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["建筑", "拍照"], "tips": "万国建筑博览会"},
            {"name": "五四广场", "start_time": "10:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "免费", "rating": 4, "tags": ["地标", "夜景"], "tips": "青岛新地标"},
            {"name": "崂山", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "130元", "rating": 5, "tags": ["名山", "必去"], "tips": "海上名山第一"},
            {"name": "金沙滩", "start_time": "14:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["海滩", "游泳"], "tips": "亚洲第一滩"},
            {"name": "啤酒博物馆", "start_time": "14:00", "duration_hours": 2, "best_period": "afternoon", "ticket": "50元", "rating": 4, "tags": ["文化", "打卡"], "tips": "了解青岛啤酒"},
            {"name": "信号山公园", "start_time": "09:00", "duration_hours": 1.5, "best_period": "morning", "ticket": "15元", "rating": 4, "tags": ["公园", "观景"], "tips": "俯瞰青岛红屋顶"},
            {"name": "海军博物馆", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "免费（需预约）", "rating": 4, "tags": ["军事", "历史"], "tips": "中国唯一海军博物馆"}
        ],
        "food": [
            {"name": "海鲜", "location": "营口路市场", "price_range": "150-300元", "recommend": "辣炒蛤蜊、清蒸皮皮虾", "type": "海鲜"},
            {"name": "青岛啤酒", "location": "登州路", "price_range": "30-80元", "recommend": "原浆啤酒、扎啤", "type": "饮品"},
            {"name": "船歌鱼水饺", "location": "多家分店", "price_range": "50-100元", "recommend": "鲅鱼水饺", "type": "面食"},
            {"name": "流亭猪蹄", "location": "流亭", "price_range": "30-50元", "recommend": "酱猪蹄", "type": "小吃"}
        ],
        "transport": "地铁1-4号线，公交方便",
        "tips": "崂山建议包车；海鲜在市场买了加工；夏天注意防晒"
    },
    "三亚": {
        "attractions": [
            {"name": "亚龙湾", "start_time": "09:00", "duration_hours": 6, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["海滩", "必去"], "tips": "天下第一湾"},
            {"name": "天涯海角", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "68元", "rating": 5, "tags": ["地标", "必去"], "tips": "海南著名景点"},
            {"name": "蜈支洲岛", "start_time": "08:00", "duration_hours": 8, "best_period": "day", "ticket": "144元", "rating": 5, "tags": ["海岛", "必去"], "tips": "中国马尔代夫"},
            {"name": "南山文化旅游区", "start_time": "08:00", "duration_hours": 6, "best_period": "day", "ticket": "129元", "rating": 5, "tags": ["文化", "宗教"], "tips": "海上观音"},
            {"name": "大东海", "start_time": "14:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["海滩", "潜水"], "tips": "市区附近的海滩"},
            {"name": "西岛", "start_time": "08:30", "duration_hours": 6, "best_period": "day", "ticket": "95元", "rating": 4, "tags": ["海岛", "潜水"], "tips": "原生态海岛"},
            {"name": "三亚湾", "start_time": "16:00", "duration_hours": 2, "best_period": "evening", "ticket": "免费", "rating": 4, "tags": ["日落", "海滩"], "tips": "看日落最佳地点"},
            {"name": "槟榔谷", "start_time": "09:00", "duration_hours": 4, "best_period": "day", "ticket": "80元", "rating": 4, "tags": ["民族", "文化"], "tips": "黎苗族文化"}
        ],
        "food": [
            {"name": "第一市场海鲜", "location": "第一市场", "price_range": "150-300元", "recommend": "和乐蟹、基围虾", "type": "海鲜"},
            {"name": "海南鸡饭", "location": "海南餐厅", "price_range": "50-80元", "recommend": "文昌鸡饭", "type": "海南菜"},
            {"name": "清补凉", "location": "街边摊", "price_range": "15-20元", "recommend": "椰子水清补凉", "type": "甜品"},
            {"name": "椰子鸡", "location": "椰客", "price_range": "150-250元", "recommend": "椰子鸡火锅", "type": "火锅"}
        ],
        "transport": "公交、出租车、网约车方便，可包车",
        "tips": "蜈支洲岛提前买票；海鲜在市场买了加工；夏天防晒"
    },
    "桂林": {
        "attractions": [
            {"name": "漓江", "start_time": "07:00", "duration_hours": 5, "best_period": "morning", "ticket": "215元", "rating": 5, "tags": ["必去", "山水"], "tips": "桂林山水甲天下"},
            {"name": "阳朔西街", "start_time": "15:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古街", "酒吧"], "tips": "中西合璧的小镇"},
            {"name": "龙脊梯田", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "100元", "rating": 5, "tags": ["梯田", "必去"], "tips": "世界梯田之冠"},
            {"name": "遇龙河", "start_time": "08:00", "duration_hours": 4, "best_period": "morning", "ticket": "120元", "rating": 5, "tags": ["漂流", "山水"], "tips": "比漓江更幽静"},
            {"name": "银子岩", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "65元", "rating": 4, "tags": ["溶洞", "自然"], "tips": "溶洞奇观"},
            {"name": "象鼻山", "start_time": "08:00", "duration_hours": 2, "best_period": "morning", "ticket": "55元", "rating": 4, "tags": ["地标", "公园"], "tips": "桂林城徽"},
            {"name": "十里画廊", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "10元", "rating": 4, "tags": ["骑行", "山水"], "tips": "骑行欣赏田园风光"},
            {"name": "印象刘三姐", "start_time": "20:00", "duration_hours": 1.5, "best_period": "evening", "ticket": "238元", "rating": 5, "tags": ["演出", "必看"], "tips": "张艺谋导演"}
        ],
        "food": [
            {"name": "桂林米粉", "location": "石记米粉", "price_range": "10-20元", "recommend": "卤菜粉、汤粉", "type": "面食"},
            {"name": "啤酒鱼", "location": "阳朔大师傅", "price_range": "100-200元", "recommend": "阳朔啤酒鱼", "type": "粤菜"},
            {"name": "田螺酿", "location": "阳朔", "price_range": "40-60元", "recommend": "阳朔田螺酿", "type": "特色菜"},
            {"name": "荔浦芋扣肉", "location": "桂林餐厅", "price_range": "60-100元", "recommend": "荔浦芋扣肉", "type": "桂菜"}
        ],
        "transport": "高铁到桂林，景点间包车或跟团",
        "tips": "漓江游选大船；龙脊梯田建议住一晚；遇龙河漂流"
    },
    "丽江": {
        "attractions": [
            {"name": "丽江古城", "start_time": "14:00", "duration_hours": 4, "best_period": "afternoon", "ticket": "50元（维护费）", "rating": 5, "tags": ["古镇", "必去"], "tips": "世界文化遗产"},
            {"name": "玉龙雪山", "start_time": "07:00", "duration_hours": 8, "best_period": "day", "ticket": "100元+索道", "rating": 5, "tags": ["雪山", "必去"], "tips": "纳西族神山"},
            {"name": "蓝月谷", "start_time": "09:00", "duration_hours": 2, "best_period": "morning", "ticket": "包含在雪山票内", "rating": 5, "tags": ["自然", "必去"], "tips": "云南九寨沟"},
            {"name": "束河古镇", "start_time": "10:00", "duration_hours": 2, "best_period": "morning", "ticket": "40元", "rating": 4, "tags": ["古镇", "安静"], "tips": "比丽江古城清静"},
            {"name": "大理洱海", "start_time": "08:00", "duration_hours": 8, "best_period": "day", "ticket": "免费", "rating": 5, "tags": ["湖泊", "必去"], "tips": "苍山洱海，风花雪月"},
            {"name": "大理古城", "start_time": "14:00", "duration_hours": 3, "best_period": "afternoon", "ticket": "免费", "rating": 4, "tags": ["古城", "文艺"], "tips": "白族文化古城"},
            {"name": "泸沽湖", "start_time": "07:00", "duration_hours": 10, "best_period": "day", "ticket": "70元", "rating": 5, "tags": ["湖泊", "必去"], "tips": "摩梭族女儿国"},
            {"name": "拉市海", "start_time": "09:00", "duration_hours": 3, "best_period": "morning", "ticket": "30元", "rating": 4, "tags": ["湿地", "骑马"], "tips": "冬季观鸟"}
        ],
        "food": [
            {"name": "过桥米线", "location": "桥香园", "price_range": "30-50元", "recommend": "特级过桥米线", "type": "面食"},
            {"name": "腊排骨火锅", "location": "钰洁腊排骨", "price_range": "80-150元", "recommend": "腊排骨、纳西烤鱼", "type": "火锅"},
            {"name": "纳西烤鱼", "location": "古城餐厅", "price_range": "60-100元", "recommend": "纳西烤鱼、鸡豆凉粉", "type": "滇菜"},
            {"name": "鲜花饼", "location": "嘉华鲜花饼", "price_range": "30-60元", "recommend": "玫瑰鲜花饼", "type": "糕点"}
        ],
        "transport": "飞机或高铁到丽江，景点包车或跟团",
        "tips": "雪山提前买票；泸沽湖需一天；高原反应注意休息"
    }
}
