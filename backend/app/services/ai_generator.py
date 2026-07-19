import re
import random
from datetime import datetime, timedelta


CITY_FOODS = {
    "北京": ["北京烤鸭", "炸酱面", "豆汁焦圈", "卤煮火烧", "涮羊肉", "爆肚"],
    "上海": ["小笼包", "生煎", "蟹粉面", "本帮红烧肉", "葱油饼", "青团"],
    "广州": ["早茶点心", "肠粉", "双皮奶", "艇仔粥", "烧腊", "虾饺"],
    "成都": ["火锅", "串串香", "担担面", "龙抄手", "钟水饺", "蛋烘糕"],
    "西安": ["肉夹馍", "羊肉泡馍", "凉皮", "biangbiang面", "葫芦头", "甑糕"],
    "杭州": ["西湖醋鱼", "东坡肉", "龙井虾仁", "叫花鸡", "片儿川", "定胜糕"],
    "重庆": ["麻辣火锅", "小面", "酸辣粉", "豆花饭", "毛血旺", "桃酥"],
    "南京": ["盐水鸭", "鸭血粉丝汤", "小笼包", "美龄粥", "牛肉锅贴", "赤豆元宵"],
    "天津": ["煎饼果子", "狗不理包子", "麻花", "锅巴菜", "老豆腐", "炸糕"],
    "武汉": ["热干面", "豆皮", "面窝", "鸭脖", "糊汤粉", "油焖大虾"],
    "长沙": ["臭豆腐", "糖油粑粑", "口味虾", "茶颜悦色", "米粉", "剁椒鱼头"],
    "厦门": ["沙茶面", "海蛎煎", "土笋冻", "花生汤", "扁食", "姜母鸭"],
    "青岛": ["啤酒", "蛤蜊", "鲅鱼水饺", "海菜凉粉", "炸虾仁", "烤鱿鱼"],
    "大连": ["海鲜烧烤", "炒蛤", "鲅鱼圈", "焖子", "海胆", "鲍鱼"],
    "苏州": ["松鼠桂鱼", "响油鳝糊", "桂花鸡头米", "生煎", "汤面", "海棠糕"],
}

CITY_ATTRACTIONS = {
    "北京": ["故宫博物院", "长城", "颐和园", "天坛", "圆明园", "王府井", "三里屯", "南锣鼓巷"],
    "上海": ["外滩", "东方明珠", "豫园", "南京路", "田子坊", "迪士尼", "朱家角", "新天地"],
    "广州": ["小蛮腰", "陈家祠", "沙面岛", "白云山", "长隆欢乐世界", "北京路", "上下九", "珠江夜游"],
    "成都": ["宽窄巷子", "锦里", "熊猫基地", "武侯祠", "杜甫草堂", "春熙路", "太古里", "都江堰"],
    "西安": ["兵马俑", "大雁塔", "古城墙", "回民街", "华清宫", "华山", "碑林", "大唐不夜城"],
    "杭州": ["西湖", "灵隐寺", "千岛湖", "宋城", "西溪湿地", "断桥", "雷峰塔", "清河坊"],
    "重庆": ["解放碑", "洪崖洞", "磁器口", "武隆", "长江索道", "天坑地缝", "鹅岭", "观音桥"],
    "南京": ["中山陵", "夫子庙", "明孝陵", "总统府", "玄武湖", "秦淮河", "紫金山", "老门东"],
    "天津": ["五大道", "古文化街", "意式风情区", "瓷房子", "盘山", "独乐寺", "七里海", "天津之眼"],
    "武汉": ["黄鹤楼", "东湖", "户部巷", "汉正街", "湖北省博物馆", "武当山", "归元寺", "江汉路"],
    "长沙": ["橘子洲", "岳麓山", "太平街", "坡子街", "湖南省博物馆", "韶山", "世界之窗", "火宫殿"],
    "厦门": ["鼓浪屿", "厦门大学", "南普陀寺", "曾厝垵", "环岛路", "万石植物园", "沙坡尾", "环岛骑行"],
}

CITY_TIPS = {
    "北京": [
        "故宫门票必须提前7天在官网预约，现场无法购票",
        "长城建议去慕田峪或箭扣，人少景色美",
        "前门大街的老字号可以尝尝，但别买贵的特产",
        "南锣鼓巷适合拍照，但消费偏高",
        "注意保暖，北京冬季寒冷干燥",
    ],
    "上海": [
        "外滩夜景最美，建议18:00后去",
        "南京路人山人海，注意随身物品",
        "田子坊适合小资购物，但价格偏高",
        "迪士尼周末人多，建议工作日前往",
        "地铁发达，基本能到达所有景点",
    ],
    "广州": [
        "早茶建议7点前到，不用排队",
        "沙面岛适合拍照，欧式建筑风格",
        "长隆建议玩2天，买套票更划算",
        "夏季炎热，注意防暑降温",
        "粤语地区，部分老人不会说普通话",
    ],
    "成都": [
        "火锅一定要找本地人多的店",
        "熊猫基地建议8点前到，熊猫最活跃",
        "宽窄巷子和锦里商业化严重，拍照即可",
        "都江堰值得一去，世界文化遗产",
        "成都阴天多，难得见到太阳",
    ],
}

PHOTO_SPOTS = {
    "北京": [
        {"name": "故宫角楼", "time": "日出前/日落时", "tip": "故宫西北角楼，经典机位"},
        {"name": "长城慕田峪", "time": "清晨", "tip": "人少光线好，可用长焦压缩"},
        {"name": "798艺术区", "time": "全天", "tip": "工业风涂鸦，适合街拍"},
        {"name": "颐和园十七孔桥", "time": "日落时", "tip": "金光穿洞，冬季更佳"},
        {"name": "三里屯太古里", "time": "夜晚", "tip": "时尚街拍，霓虹灯背景"},
    ],
    "上海": [
        {"name": "外滩", "time": "夜晚18:30-21:00", "tip": "陆家嘴天际线最佳机位"},
        {"name": "豫园", "time": "黄昏", "tip": "古典园林配现代城市"},
        {"name": "武康大楼", "time": "全天", "tip": "网红建筑，多角度拍摄"},
        {"name": "朱家角古镇", "time": "清晨", "tip": "水乡晨雾，意境优美"},
        {"name": "东方明珠", "time": "夜晚", "tip": "隔江拍摄倒影"},
    ],
}


def generate_content(template_type: str, context: dict) -> str:
    generators = {
        "travel_copy": _generate_travel_copy,
        "punch_card": _generate_punch_card,
        "photo_spots": _generate_photo_spots,
        "pitfall_guide": _generate_pitfall_guide,
        "itinerary_memo": _generate_itinerary_memo,
        "packing_list": _generate_packing_list,
        "city_brief": _generate_city_brief,
        "station_guide": _generate_station_guide,
        "food_guide": _generate_food_guide,
        "shopping_list": _generate_shopping_list,
        "daily_plan": _generate_daily_plan,
        "emergency_contacts": _generate_emergency_contacts,
    }
    
    generator = generators.get(template_type)
    if generator:
        return generator(context)
    return _generate_default(context)


def _generate_travel_copy(context: dict) -> str:
    poi_name = context.get("poi_name", "景点")
    city = context.get("city", "")
    days = context.get("days", 1)
    
    copies = [
        f"📍 {poi_name} | {city}\n\n终于来了！{poi_name}真的值得专程跑一趟～\n\n建议早上早点去，人少光线好，拍照超出片！门票记得提前预约哦～\n\n在这里待了{days}天，最大的感受就是：来之前想了N种可能，走的时候只想再来一次。\n\n#旅行 #{city}#{poi_name}#说走就走",
        f"✨ {poi_name} 打卡成功！\n\n{city}必去的地方，真的名不虚传！\n\n门票：记得提前预约\n最佳时间：上午9点前\n拍照tips：找好角度，随手一拍都是大片\n\n总之一句话：来了绝对不后悔！\n\n#{city}旅行#",
        f"📸 {poi_name} | 此生必去\n\n如果你来{city}，一定要来{poi_name}看看。\n\n这里藏着太多故事，每一步都是风景。\n\n实用tips：\n✅ 提前预约门票\n✅ 穿舒服的鞋子\n✅ 带好充电宝\n✅ 相机内存卡准备充足\n\n出发吧，别等！\n\n#说走就走#",
    ]
    
    return random.choice(copies)


def _generate_punch_card(context: dict) -> str:
    poi_name = context.get("poi_name", "景点")
    city = context.get("city", "")
    
    return f"【{city}·{poi_name} 300字速览】\n\n📌 基本信息\n📍 位置：{city}市中心/近郊\n🎫 门票：¥40-60（以实际为准）\n⏰ 开放时间：8:00-17:30\n\n🌟 必看亮点\n1. 核心景观：标志性建筑/自然奇观\n2. 文化底蕴：历史背景值得了解\n3. 拍照胜地：多角度出片\n\n💡 游玩建议\n• 建议游玩时间：2-3小时\n• 最佳时段：上午9点前/下午4点后\n• 交通：地铁X号线X站\n\n⚠️ 注意事项\n• 人流较大，注意安全\n• 部分区域需要额外购票\n• 夏季注意防晒补水\n\n💰 总花费参考\n门票：¥50\n交通：¥10\n餐饮：¥30\n合计：¥90/人"


def _generate_photo_spots(context: dict) -> str:
    city = context.get("city", "")
    poi_name = context.get("poi_name", "")
    
    spots = PHOTO_SPOTS.get(city, [
        {"name": f"{poi_name}主入口", "time": "清晨/黄昏", "tip": "经典角度，拍全标志性建筑"},
        {"name": "周边小巷", "time": "全天", "tip": "人文气息，适合街拍"},
        {"name": "高处观景台", "time": "日落时", "tip": "俯瞰全景，金光时刻"},
    ])
    
    result = f"📷 {city}{poi_name}拍照攻略\n\n"
    result += "【最佳拍摄时间】\n"
    result += f"🌅 日出：6:00-7:30（人少光柔）\n"
    result += f"☀️ 白天：9:00-11:00/15:00-17:00（侧光好）\n"
    result += f"🌇 日落：17:30-19:00（黄金时刻）\n"
    result += f"🌙 夜景：19:30后（灯光亮起）\n\n"
    result += "【推荐机位】\n"
    
    for i, spot in enumerate(spots[:5], 1):
        result += f"{i}. {spot['name']}\n"
        result += f"   🕐 最佳时间：{spot['time']}\n"
        result += f"   💡 拍摄建议：{spot['tip']}\n\n"
    
    result += "【穿搭建议】\n"
    result += "• 主色：白色、米色、浅蓝（与风景和谐）\n"
    result += "• 风格：休闲、复古、文艺\n"
    result += "• 配件：帽子、墨镜、包包\n\n"
    result += "【避坑指南】\n"
    result += "• 避开正午顶光（12:00-14:00）\n"
    result += "• 热门机位提前占位\n"
    result += "• 人像照用大光圈虚化背景\n"
    
    return result


def _generate_pitfall_guide(context: dict) -> str:
    city = context.get("city", "")
    
    pitfalls = {
        "北京": [
            "⚠️ 前门大街的'北京特产'多为天价，别买",
            "⚠️ 故宫门口的'快速通道'都是骗子，没有内部关系",
            "⚠️ 长城一日游黑车多，去正规枢纽站坐车",
            "⚠️ 王府井的小吃街贵且难吃，本地不去",
            "⚠️ 机场/火车站的出租车拒载很正常，用网约车",
        ],
        "上海": [
            "⚠️ 南京路的金店打折都是套路",
            "⚠️ 外滩'游船票代买'黄牛，原价120卖200",
            "⚠️ 豫园周边的糕点店排队是雇的托",
            "⚠️ 田子坊的手工香皂/饰品成本几块卖几十",
            "⚠️ 新天地的餐厅'网红'是刷出来的",
        ],
        "成都": [
            "⚠️ 宽窄巷子/锦里的火锅店贵且不正宗",
            "⚠️ '10元3斤水果'缺斤少两",
            "⚠️ 熊猫基地黄牛票，官网才55",
            "⚠️ 春熙路的'免费SPA体验'别进",
            "⚠️ 打车说'不去'是正常的，换一辆",
        ],
    }
    
    tips = pitfalls.get(city, [
        f"⚠️ {city}景区门口的'专家讲解'多为野导",
        f"⚠️ {city}特产店'买一送一'实际先涨价",
        f"⚠️ {city}出租车可能绕路，开导航",
        f"⚠️ {city}夜市'网红'摊位性价比低",
        f"⚠️ {city}机场/火车站黑车要价翻倍",
    ])
    
    result = f"🚫 {city}避坑指南\n\n"
    result += "【消费陷阱】\n"
    for tip in tips:
        result += f"{tip}\n"
    
    result += "\n【省钱技巧】\n"
    result += f"💰 {city}本地超市的特产比景区便宜一半\n"
    result += f"💰 景区门票官网购买，别找代购\n"
    result += f"💰 吃饭去本地人多的小店，看排队就知道\n"
    result += f"💰 地铁/公交比打车划算\n"
    
    result += "\n【防骗提醒】\n"
    result += "❌ 不要信'内部关系''快速通道'\n"
    result += "❌ 不要去'免费体验'的SPA/美容\n"
    result += "❌ 不要买路边的'古董''字画'\n"
    result += "❌ 贵重物品随身携带\n"
    
    return result


def _generate_itinerary_memo(context: dict) -> str:
    city = context.get("city", "")
    days = context.get("days", 3)
    from_city = context.get("from_city", "")
    budget = context.get("budget", 3000)
    preferences = context.get("preferences", [])
    
    result = f"📝 {city}{days}日游备忘录\n"
    result += f"出发地：{from_city}\n"
    result += f"总预算：¥{budget}\n"
    result += f"日期：{datetime.now().strftime('%Y-%m-%d')}\n"
    result += "=" * 40 + "\n\n"
    
    attractions = CITY_ATTRACTIONS.get(city, [])
    foods = CITY_FOODS.get(city, [])
    
    for day in range(1, days + 1):
        result += f"【Day {day}】\n"
        result += f"🕐 07:30 起床洗漱\n"
        result += f"🍳 08:00 早餐：{random.choice(foods) if foods else '酒店早餐'}\n"
        result += f"🎯 09:00 景点：{attractions[(day-1) % len(attractions)] if attractions else '核心景区'}\n"
        result += f"🍜 12:00 午餐：附近推荐餐厅\n"
        result += f"🎨 14:00 景点：{attractions[day % len(attractions)] if attractions else '特色街区'}\n"
        result += f"☕ 16:00 下午茶/休息\n"
        result += f"🌃 18:00 晚餐：{random.choice(foods) if foods else '本地特色'}\n"
        result += f"👀 19:30 夜景/散步\n"
        result += f"🛌 22:00 回到酒店\n\n"
    
    result += "=" * 40 + "\n【费用预算】\n"
    result += f"🚄 高铁往返：¥{int(budget * 0.4)}\n"
    result += f"🏨 住宿：¥{int(budget * 0.3)}\n"
    result += f"🍽️ 餐饮：¥{int(budget * 0.15)}\n"
    result += f"🎫 门票：¥{int(budget * 0.08)}\n"
    result += f"🚕 交通：¥{int(budget * 0.05)}\n"
    result += f"🎁 购物：¥{int(budget * 0.02)}\n\n"
    
    result += "【证件提醒】\n"
    result += "✅ 身份证（必带）\n"
    result += "✅ 手机充电器/充电宝\n"
    result += "✅ 耳机\n"
    result += "✅ 雨伞（看天气）\n"
    result += "✅ 常用药品\n"
    
    return result


def _generate_packing_list(context: dict) -> str:
    days = context.get("days", 3)
    season = context.get("season", "spring")
    with_old = context.get("with_old", False)
    with_kids = context.get("with_kids", False)
    has_rain = context.get("has_rain", False)
    
    result = f"🎒 {days}天旅行行李清单\n\n"
    
    clothes = {
        "spring": [f"长袖衬衫x2", "薄外套x1", "长裤x2", "休闲鞋x1", f"内衣裤x{days+1}", f"袜子x{days+1}"],
        "summer": ["短袖T恤x3", "短裤/裙子x2", "防晒衫x1", "凉鞋x1", f"内衣裤x{days+1}", "袜子x2", "帽子x1", "墨镜x1"],
        "autumn": ["长袖T恤x2", "薄毛衣x1", "外套x1", "长裤x2", "休闲鞋x1", f"内衣裤x{days+1}", f"袜子x{days+1}", "围巾x1"],
        "winter": ["保暖内衣x2", "厚毛衣x1", "羽绒服/大衣x1", "厚裤x1", "保暖鞋x1", "袜子x3", "手套x1", "帽子x1", "围巾x1"],
    }
    
    result += "【衣物类】\n"
    for item in clothes.get(season, clothes["spring"]):
        result += f"☐ {item}\n"
    
    if has_rain:
        result += "☐ 折叠伞/雨衣\n"
        result += "☐ 防水鞋套\n"
    
    result += "\n【证件财物】\n"
    result += "☐ 身份证\n"
    result += "☐ 银行卡\n"
    result += "☐ 现金（少量）\n"
    result += "☐ 手机/充电器/充电宝\n"
    result += "☐ 耳机\n"
    
    result += "\n【洗漱用品】\n"
    result += "☐ 牙刷/牙膏/毛巾\n"
    result += "☐ 洗发水/沐浴露（分装）\n"
    result += "☐ 洗面奶/护肤品\n"
    result += "☐ 防晒霜（夏季必带）\n"
    result += "☐ 梳子/镜子\n"
    
    result += "\n【药品类】\n"
    result += "☐ 感冒药\n"
    result += "☐ 肠胃药\n"
    result += "☐ 创可贴\n"
    result += "☐ 晕车药\n"
    result += "☐ 口罩\n"
    
    if with_old:
        result += "\n【老人专用】\n"
        result += "☐ 常用药（降压/降糖等）\n"
        result += "☐ 拐杖（如需）\n"
        result += "☐ 便携座椅\n"
        result += "☐ 保温壶\n"
    
    if with_kids:
        result += "\n【儿童专用】\n"
        result += "☐ 尿不湿\n"
        result += "☐ 奶粉/辅食\n"
        result += "☐ 儿童餐具\n"
        result += "☐ 玩具/绘本\n"
        result += "☐ 驱蚊液\n"
    
    result += "\n【电子设备】\n"
    result += "☐ 相机/镜头\n"
    result += "☐ 三脚架\n"
    result += "☐ 存储卡\n"
    result += "☐ 转换插头\n"
    
    return result


def _generate_city_brief(context: dict) -> str:
    city = context.get("city", "")
    days = context.get("days", 3)
    budget = context.get("budget", 3000)
    
    foods = CITY_FOODS.get(city, [])
    attractions = CITY_ATTRACTIONS.get(city, [])
    tips = CITY_TIPS.get(city, [])
    
    result = f"🏙️ {city}速览卡片\n"
    result += "=" * 30 + "\n\n"
    result += f"📅 建议游玩：{days}天\n"
    result += f"💰 人均消费：¥{int(budget/days*1.2)}/天\n"
    result += f"🚗 交通方式：高铁/飞机直达\n\n"
    
    result += "🍜 必吃3样：\n"
    for food in (foods or ["特色小吃"] * 3)[:3]:
        result += f"  • {food}\n"
    
    result += "\n🎯 必去3景：\n"
    for attr in (attractions or ["标志性景点"] * 3)[:3]:
        result += f"  • {attr}\n"
    
    result += "\n⚠️ 避坑3条：\n"
    if tips:
        for tip in tips[:3]:
            result += f"  • {tip}\n"
    else:
        result += "  • 景区门口黄牛票别买\n  • 特产去超市不要在景区\n  • 开导航防止打车绕路\n"
    
    result += "\n💡 小贴士：\n"
    result += f"  • 最佳季节：{random.choice(['春秋季', '四季皆宜', '3-5月', '9-11月'])}\n"
    result += f"  • 交通：地铁发达，建议办交通卡\n"
    result += f"  • 住宿：推荐住市中心/景区附近\n"
    
    return result


def _generate_station_guide(context: dict) -> str:
    station = context.get("station", "")
    city = context.get("city", "")
    
    result = f"🚉 {station}站内指南\n"
    result += "=" * 30 + "\n\n"
    result += "【出站指引】\n"
    result += "🅰️ A出口：地铁X号线/公交枢纽\n"
    result += "🅱️ B出口：出租车/网约车\n"
    result += "🅲️ C出口：停车场\n\n"
    result += "【站内设施】\n"
    result += "🍱 餐饮：肯德基/麦当劳/地方小吃\n"
    result += "🛒 购物：便利店/特产店\n"
    result += "📦 行李寄存：到达层出口旁\n"
    result += "♿ 无障碍：直梯/坡道/母婴室\n"
    result += "🛌 贵宾厅：候车室2F（凭票/会员卡）\n"
    result += "💳 取票机：1F大厅两侧\n"
    result += "🚕 出租车：到达层门外\n"
    result += "📱 充电宝：便利店/候车区\n\n"
    result += "【交通接驳】\n"
    result += f"🚇 地铁：直达{city}主要区域\n"
    result += "🚌 公交：X路/X路/X路\n"
    result += "🚕 打车：排队区约5-10分钟\n"
    result += "🚲 共享单车：出站右侧\n\n"
    result += "【注意事项】\n"
    result += "⚠️ 高峰期（7-9点/17-19点）人多\n"
    result += "⚠️ 取票至少提前30分钟\n"
    result += "⚠️ 安检需出示身份证\n"
    result += "⚠️ 发车前5分钟停止检票\n"
    
    return result


def _generate_food_guide(context: dict) -> str:
    city = context.get("city", "")
    
    foods = CITY_FOODS.get(city, [])
    if not foods:
        foods = ["特色小吃A", "特色小吃B", "特色小吃C"]
    
    result = f"🍜 {city}美食指南\n"
    result += "=" * 30 + "\n\n"
    
    for i, food in enumerate(foods[:6], 1):
        result += f"{i}. {food}\n"
        result += f"   💰 价格：¥15-50\n"
        result += f"   📍 推荐：本地人多的街边店\n"
        result += f"   ⏰ 营业时间：10:00-22:00\n\n"
    
    result += "【省钱技巧】\n"
    result += "💰 早餐：本地豆浆油条¥5-10\n"
    result += "💰 午餐：工作餐¥15-25\n"
    result += "💰 晚餐：正餐¥50-80/人\n\n"
    result += "【避坑提醒】\n"
    result += "❌ 景区门口的'网红店'贵且难吃\n"
    result += "❌ 不要买'天价'特产\n"
    result += "❌ 看排队就知道哪家好吃\n"
    
    return result


def _generate_shopping_list(context: dict) -> str:
    city = context.get("city", "")
    
    result = f"🛒 {city}购物清单\n"
    result += "=" * 30 + "\n\n"
    result += "【本地特产】\n"
    result += "☐ 特色零食（超市购买更便宜）\n"
    result += "☐ 手工制品/文创产品\n"
    result += "☐ 茶叶/药材（正规渠道）\n\n"
    result += "【必买好物】\n"
    result += "☐ 当地特色小吃（带回家）\n"
    result += "☐ 精美明信片/冰箱贴\n"
    result += "☐ 服饰/手袋（奥莱/折扣店）\n\n"
    result += "【省钱建议】\n"
    result += "💰 去本地大超市，别在景区买\n"
    result += "💰 特产批发市场更划算\n"
    result += "💰 关注商场折扣活动\n\n"
    result += "【避坑提醒】\n"
    result += "❌ 街边'古董'都是假货\n"
    result += "❌ 不要在景区珠宝店消费\n"
    result += "❌ 警惕'强制购物'团\n"
    
    return result


def _generate_daily_plan(context: dict) -> str:
    city = context.get("city", "")
    day = context.get("day", 1)
    weather = context.get("weather", "晴")
    
    attractions = CITY_ATTRACTIONS.get(city, [])
    foods = CITY_FOODS.get(city, [])
    
    result = f"📅 {city} Day {day} 行程\n"
    result += f"天气：{weather}\n"
    result += "=" * 30 + "\n\n"
    
    idx = (day - 1) * 2
    attr1 = attractions[idx % len(attractions)] if attractions else "景点A"
    attr2 = attractions[(idx + 1) % len(attractions)] if attractions else "景点B"
    
    result += "⏰ 时间安排：\n"
    result += f"07:30 ⏰ 起床\n"
    result += f"08:00 🍳 早餐\n"
    result += f"09:00 🚗 出发去{attr1}\n"
    result += f"09:30 🎯 游览{attr1}（约2小时）\n"
    result += f"12:00 🍜 午餐：{random.choice(foods) if foods else '本地特色'}\n"
    result += f"13:30 ☕ 休息/咖啡厅\n"
    result += f"14:30 🎨 前往{attr2}\n"
    result += f"15:00 📸 游览{attr2}（约2小时）\n"
    result += f"17:30 🛍️ 逛街/购物\n"
    result += f"19:00 🍽️ 晚餐\n"
    result += f"20:30 🌃 夜景/散步\n"
    result += f"22:00 🛌 回酒店\n\n"
    
    result += "💡 今日提醒：\n"
    result += "✅ 穿舒服的鞋子\n"
    result += "✅ 带充电宝\n"
    result += "✅ 防晒/雨具\n"
    result += "✅ 多喝水\n"
    
    return result


def _generate_emergency_contacts(context: dict) -> str:
    city = context.get("city", "")
    
    result = f"🆘 {city}紧急联系方式\n"
    result += "=" * 30 + "\n\n"
    result += "【紧急电话】\n"
    result += "📞 报警：110\n"
    result += "🚑 急救：120\n"
    result += "🔥 消防：119\n"
    result += "🚗 交通事故：122\n\n"
    result += "【旅游投诉】\n"
    result += "📞 全国旅游服务热线：12301\n"
    result += "📞 消费者投诉：12315\n\n"
    result += "【交通服务】\n"
    result += "🚄 铁路客服：12306\n"
    result += "✈️ 民航客服：95583\n"
    result += "🚌 公交服务：咨询当地\n\n"
    result += "【实用APP】\n"
    result += "📱 高德地图/百度地图（导航）\n"
    result += "📱 12306（查票）\n"
    result += "📱 美团/大众点评（美食）\n"
    result += "📱 滴滴出行（打车）\n"
    
    return result


def _generate_default(context: dict) -> str:
    return f"【AI生成内容】\n\n{context.get('prompt', '请提供更多信息')}\n\n（此为默认生成内容，更多模板请选择具体类型）"
