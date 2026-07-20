import json
import os
import random

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "mass_city_data.py")

GENERIC_TEMPLATES = {
    "历史文化": {
        "adjectives": ["历史悠久的", "文化底蕴深厚的", "千年古都", "古城风韵", "书香气息"],
        "attractions_patterns": [
            "{}博物馆（国家一级）", "{}古城墙（保存完整）", "{}老街（明清风格）", 
            "{}文庙（文化圣地）", "{}名人故居", "{}历史街区", "{}古镇", "{}遗址公园"
        ],
        "food_patterns": [
            "{}特色小吃", "{}老字号餐厅", "{}传统糕点", "{}名菜", "{}面食", "{}茶馆"
        ],
        "tags": ["历史文化", "古迹", "博物馆", "古镇"],
    },
    "自然风光": {
        "adjectives": ["山清水秀的", "风景如画的", "自然风光优美", "天然氧吧", "避暑胜地"],
        "attractions_patterns": [
            "{}风景区（4A/5A级）", "{}森林公园", "{}湿地公园", "{}大峡谷", 
            "{}瀑布群", "{}溶洞", "{}温泉度假区", "{}漂流基地"
        ],
        "food_patterns": [
            "{}农家菜", "{}山野菜", "{}特色野味", "{}水库鱼", "{}有机食品"
        ],
        "tags": ["自然风光", "景区", "森林公园", "避暑"],
    },
    "海滨度假": {
        "adjectives": ["阳光明媚的", "海风习习的", "浪漫的海边", "度假天堂", "水清沙白"],
        "attractions_patterns": [
            "{}海滨浴场", "{}沙滩", "{}海岛度假村", "{}海洋公园", 
            "{}灯塔", "{}渔港", "{}滨海大道", "{}海上乐园"
        ],
        "food_patterns": [
            "{}海鲜大排档", "{}特色鱼排", "{}贝类美食", "{}海鲜市场", "{}椰子鸡"
        ],
        "tags": ["海滨", "度假", "海鲜", "阳光"],
    },
    "美食之都": {
        "adjectives": ["味蕾天堂", "吃货圣地", "美食聚集地", "舌尖上的城市", "小吃王国"],
        "attractions_patterns": [
            "{}美食街", "{}小吃城", "{}老字号一条街", "{}夜市", "{}餐饮博物馆"
        ],
        "food_patterns": [
            "{}招牌菜", "{}地道小吃", "{}老字号美味", "{}街头美食", "{}网红餐厅", "{}隐藏美食"
        ],
        "tags": ["美食", "小吃", "老字号", "网红"],
    },
    "现代都市": {
        "adjectives": ["繁华的", "现代化的", "时尚的", "充满活力的", "国际化的"],
        "attractions_patterns": [
            "{}CBD中心", "{}摩天大楼", "{}主题乐园", "{}购物中心", 
            "{}艺术中心", "{}科技馆", "{}音乐厅", "{}展览馆"
        ],
        "food_patterns": [
            "{}国际美食", "{}高级餐厅", "{}咖啡厅", "{}酒吧街", "{}日料店"
        ],
        "tags": ["现代", "时尚", "购物", "主题乐园"],
    },
    "古镇水乡": {
        "adjectives": ["古色古香的", "小桥流水的", "江南水乡风格", "保留完好的古镇", "如诗如画"],
        "attractions_patterns": [
            "{}古镇（AAAA级）", "{}老街", "{}水乡", "{}园林", 
            "{}桥", "{}庙", "{}戏台", "{}名人故居"
        ],
        "food_patterns": [
            "{}特色糕点", "{}农家饭", "{}腌制品", "{}米酒", "{}茶叶"
        ],
        "tags": ["古镇", "水乡", "江南", "历史"],
    },
}

CITY_POOL = [
    {"city": "北京", "province": "北京", "type": "历史文化", "coords": (116.4074, 39.9042)},
    {"city": "上海", "province": "上海", "type": "现代都市", "coords": (121.4737, 31.2304)},
    {"city": "广州", "province": "广东", "type": "美食之都", "coords": (113.2644, 23.1291)},
    {"city": "深圳", "province": "广东", "type": "现代都市", "coords": (114.0579, 22.5431)},
    {"city": "重庆", "province": "重庆", "type": "美食之都", "coords": (106.5516, 29.5630)},
    {"city": "天津", "province": "天津", "type": "历史文化", "coords": (117.2009, 39.1256)},
    {"city": "南京", "province": "江苏", "type": "历史文化", "coords": (118.7674, 32.0415)},
    {"city": "苏州", "province": "江苏", "type": "古镇水乡", "coords": (120.5853, 31.2989)},
    {"city": "无锡", "province": "江苏", "type": "古镇水乡", "coords": (120.3119, 31.4912)},
    {"city": "常州", "province": "江苏", "type": "历史文化", "coords": (119.9741, 31.8106)},
    {"city": "南通", "province": "江苏", "type": "历史文化", "coords": (120.8667, 32.0170)},
    {"city": "扬州", "province": "江苏", "type": "历史文化", "coords": (119.4129, 32.3936)},
    {"city": "徐州", "province": "江苏", "type": "历史文化", "coords": (117.2847, 34.2616)},
    {"city": "杭州", "province": "浙江", "type": "自然风光", "coords": (120.1551, 30.2741)},
    {"city": "宁波", "province": "浙江", "type": "海滨度假", "coords": (121.5498, 29.8684)},
    {"city": "温州", "province": "浙江", "type": "自然风光", "coords": (120.6908, 28.0006)},
    {"city": "绍兴", "province": "浙江", "type": "历史文化", "coords": (120.5833, 30.0000)},
    {"city": "嘉兴", "province": "浙江", "type": "古镇水乡", "coords": (120.7555, 30.7469)},
    {"city": "湖州", "province": "浙江", "type": "古镇水乡", "coords": (120.0938, 30.8946)},
    {"city": "金华", "province": "浙江", "type": "古镇水乡", "coords": (119.6494, 29.0795)},
    {"city": "台州", "province": "浙江", "type": "历史文化", "coords": (121.4400, 28.6563)},
    {"city": "合肥", "province": "安徽", "type": "现代都市", "coords": (117.2272, 31.8206)},
    {"city": "芜湖", "province": "安徽", "type": "自然风光", "coords": (118.3740, 31.3340)},
    {"city": "黄山", "province": "安徽", "type": "自然风光", "coords": (118.3376, 29.7147)},
    {"city": "福州", "province": "福建", "type": "历史文化", "coords": (119.2965, 26.0745)},
    {"city": "厦门", "province": "福建", "type": "海滨度假", "coords": (118.0894, 24.4798)},
    {"city": "泉州", "province": "福建", "type": "历史文化", "coords": (118.6758, 24.8741)},
    {"city": "漳州", "province": "福建", "type": "自然风光", "coords": (117.6471, 24.5127)},
    {"city": "南昌", "province": "江西", "type": "历史文化", "coords": (115.8579, 28.6820)},
    {"city": "九江", "province": "江西", "type": "自然风光", "coords": (116.0019, 29.7050)},
    {"city": "赣州", "province": "江西", "type": "历史文化", "coords": (114.9333, 25.8310)},
    {"city": "景德镇", "province": "江西", "type": "历史文化", "coords": (117.1784, 29.2687)},
    {"city": "上饶", "province": "江西", "type": "自然风光", "coords": (117.9423, 28.4535)},
    {"city": "济南", "province": "山东", "type": "历史文化", "coords": (117.0009, 36.6758)},
    {"city": "青岛", "province": "山东", "type": "海滨度假", "coords": (120.3826, 36.0671)},
    {"city": "烟台", "province": "山东", "type": "海滨度假", "coords": (121.3910, 37.5273)},
    {"city": "潍坊", "province": "山东", "type": "历史文化", "coords": (119.1071, 36.7069)},
    {"city": "淄博", "province": "山东", "type": "历史文化", "coords": (118.0548, 36.8131)},
    {"city": "泰安", "province": "山东", "type": "自然风光", "coords": (117.0883, 36.1943)},
    {"city": "威海", "province": "山东", "type": "海滨度假", "coords": (122.1200, 37.5131)},
    {"city": "日照", "province": "山东", "type": "海滨度假", "coords": (119.5269, 35.4166)},
    {"city": "临沂", "province": "山东", "type": "自然风光", "coords": (118.3489, 35.1041)},
    {"city": "郑州", "province": "河南", "type": "现代都市", "coords": (113.6254, 34.7466)},
    {"city": "洛阳", "province": "河南", "type": "历史文化", "coords": (112.4540, 34.6197)},
    {"city": "开封", "province": "河南", "type": "历史文化", "coords": (114.3416, 34.7972)},
    {"city": "安阳", "province": "河南", "type": "历史文化", "coords": (114.3931, 36.0998)},
    {"city": "新乡", "province": "河南", "type": "历史文化", "coords": (113.8835, 35.3029)},
    {"city": "南阳", "province": "河南", "type": "历史文化", "coords": (112.5328, 33.0042)},
    {"city": "信阳", "province": "河南", "type": "自然风光", "coords": (114.0724, 32.1310)},
    {"city": "武汉", "province": "湖北", "type": "美食之都", "coords": (114.3055, 30.5931)},
    {"city": "宜昌", "province": "湖北", "type": "自然风光", "coords": (111.2864, 30.6919)},
    {"city": "襄阳", "province": "湖北", "type": "历史文化", "coords": (112.1400, 32.0420)},
    {"city": "荆州", "province": "湖北", "type": "历史文化", "coords": (112.2390, 30.3260)},
    {"city": "黄冈", "province": "湖北", "type": "自然风光", "coords": (114.8721, 30.4541)},
    {"city": "咸宁", "province": "湖北", "type": "自然风光", "coords": (114.3224, 29.8378)},
    {"city": "长沙", "province": "湖南", "type": "美食之都", "coords": (112.9388, 28.2282)},
    {"city": "株洲", "province": "湖南", "type": "现代都市", "coords": (113.1340, 27.8274)},
    {"city": "湘潭", "province": "湖南", "type": "历史文化", "coords": (112.9449, 27.8291)},
    {"city": "衡阳", "province": "湖南", "type": "自然风光", "coords": (112.5719, 26.8936)},
    {"city": "岳阳", "province": "湖南", "type": "自然风光", "coords": (113.1289, 29.3562)},
    {"city": "常德", "province": "湖南", "type": "自然风光", "coords": (111.6856, 29.0318)},
    {"city": "张家界", "province": "湖南", "type": "自然风光", "coords": (110.4792, 29.3249)},
    {"city": "深圳", "province": "广东", "type": "现代都市", "coords": (114.0579, 22.5431)},
    {"city": "珠海", "province": "广东", "type": "海滨度假", "coords": (113.5767, 22.2710)},
    {"city": "汕头", "province": "广东", "type": "美食之都", "coords": (116.6829, 23.3535)},
    {"city": "佛山", "province": "广东", "type": "美食之都", "coords": (113.1219, 23.0218)},
    {"city": "东莞", "province": "广东", "type": "现代都市", "coords": (113.7518, 23.0496)},
    {"city": "中山", "province": "广东", "type": "历史文化", "coords": (113.3926, 22.5171)},
    {"city": "惠州", "province": "广东", "type": "海滨度假", "coords": (114.4157, 23.1152)},
    {"city": "湛江", "province": "广东", "type": "海滨度假", "coords": (110.3594, 21.2707)},
    {"city": "肇庆", "province": "广东", "type": "自然风光", "coords": (112.4725, 23.0517)},
    {"city": "江门", "province": "广东", "type": "历史文化", "coords": (113.0819, 22.5789)},
    {"city": "南宁", "province": "广西", "type": "自然风光", "coords": (108.3665, 22.8170)},
    {"city": "桂林", "province": "广西", "type": "自然风光", "coords": (110.2992, 25.2742)},
    {"city": "柳州", "province": "广西", "type": "自然风光", "coords": (109.4116, 24.3264)},
    {"city": "北海", "province": "广西", "type": "海滨度假", "coords": (109.1197, 21.4812)},
    {"city": "海口", "province": "海南", "type": "海滨度假", "coords": (110.3494, 20.0174)},
    {"city": "三亚", "province": "海南", "type": "海滨度假", "coords": (109.5082, 18.2479)},
    {"city": "成都", "province": "四川", "type": "美食之都", "coords": (104.0665, 30.5728)},
    {"city": "自贡", "province": "四川", "type": "美食之都", "coords": (104.7784, 29.3397)},
    {"city": "攀枝花", "province": "四川", "type": "自然风光", "coords": (101.7173, 26.5823)},
    {"city": "泸州", "province": "四川", "type": "历史文化", "coords": (105.4326, 28.8718)},
    {"city": "德阳", "province": "四川", "type": "历史文化", "coords": (104.4058, 31.1279)},
    {"city": "绵阳", "province": "四川", "type": "历史文化", "coords": (104.7344, 31.4676)},
    {"city": "广元", "province": "四川", "type": "历史文化", "coords": (105.8297, 32.4336)},
    {"city": "乐山", "province": "四川", "type": "自然风光", "coords": (103.7619, 29.5521)},
    {"city": "南充", "province": "四川", "type": "历史文化", "coords": (106.0690, 30.8373)},
    {"city": "宜宾", "province": "四川", "type": "历史文化", "coords": (104.5656, 28.7734)},
    {"city": "达州", "province": "四川", "type": "历史文化", "coords": (107.4682, 31.2090)},
    {"city": "雅安", "province": "四川", "type": "自然风光", "coords": (103.0010, 29.9880)},
    {"city": "毕节", "province": "贵州", "type": "自然风光", "coords": (105.2847, 27.3010)},
    {"city": "遵义", "province": "贵州", "type": "历史文化", "coords": (106.9073, 27.7257)},
    {"city": "六盘水", "province": "贵州", "type": "自然风光", "coords": (104.8333, 26.5944)},
    {"city": "安顺", "province": "贵州", "type": "自然风光", "coords": (105.9307, 26.2453)},
    {"city": "贵阳", "province": "贵州", "type": "自然风光", "coords": (106.7135, 26.5783)},
    {"city": "曲靖", "province": "云南", "type": "自然风光", "coords": (103.7961, 25.4890)},
    {"city": "昆明", "province": "云南", "type": "自然风光", "coords": (102.8329, 24.8801)},
    {"city": "玉溪", "province": "云南", "type": "自然风光", "coords": (102.5457, 24.3518)},
    {"city": "大理", "province": "云南", "type": "自然风光", "coords": (100.2676, 25.6065)},
    {"city": "丽江", "province": "云南", "type": "古镇水乡", "coords": (100.2299, 26.8721)},
    {"city": "红河", "province": "云南", "type": "自然风光", "coords": (103.3899, 23.3640)},
    {"city": "西双版纳", "province": "云南", "type": "自然风光", "coords": (100.7973, 22.0074)},
    {"city": "楚雄", "province": "云南", "type": "自然风光", "coords": (101.5280, 25.0417)},
    {"city": "香格里拉", "province": "云南", "type": "自然风光", "coords": (99.7061, 27.8675)},
    {"city": "拉萨", "province": "西藏", "type": "历史文化", "coords": (91.1322, 29.6500)},
    {"city": "日喀则", "province": "西藏", "type": "历史文化", "coords": (88.8809, 29.2734)},
    {"city": "林芝", "province": "西藏", "type": "自然风光", "coords": (94.3624, 29.6486)},
    {"city": "西安", "province": "陕西", "type": "历史文化", "coords": (108.9402, 34.3416)},
    {"city": "铜川", "province": "陕西", "type": "历史文化", "coords": (108.9451, 34.8967)},
    {"city": "宝鸡", "province": "陕西", "type": "历史文化", "coords": (107.2370, 34.3550)},
    {"city": "咸阳", "province": "陕西", "type": "历史文化", "coords": (108.7089, 34.3296)},
    {"city": "渭南", "province": "陕西", "type": "历史文化", "coords": (109.5098, 34.4998)},
    {"city": "延安", "province": "陕西", "type": "历史文化", "coords": (109.4898, 36.5853)},
    {"city": "汉中", "province": "陕西", "type": "历史文化", "coords": (107.0237, 33.0700)},
    {"city": "榆林", "province": "陕西", "type": "历史文化", "coords": (109.7348, 38.2883)},
    {"city": "安康", "province": "陕西", "type": "自然风光", "coords": (109.0293, 32.6890)},
    {"city": "商洛", "province": "陕西", "type": "自然风光", "coords": (109.9387, 33.8700)},
    {"city": "兰州", "province": "甘肃", "type": "自然风光", "coords": (103.8343, 36.0611)},
    {"city": "嘉峪关", "province": "甘肃", "type": "历史文化", "coords": (98.2894, 39.7726)},
    {"city": "天水", "province": "甘肃", "type": "历史文化", "coords": (105.7249, 34.5809)},
    {"city": "武威", "province": "甘肃", "type": "历史文化", "coords": (102.6482, 37.9284)},
    {"city": "张掖", "province": "甘肃", "type": "历史文化", "coords": (100.4453, 38.9302)},
    {"city": "平凉", "province": "甘肃", "type": "自然风光", "coords": (106.6753, 35.5426)},
    {"city": "酒泉", "province": "甘肃", "type": "历史文化", "coords": (98.4941, 39.7321)},
    {"city": "敦煌", "province": "甘肃", "type": "历史文化", "coords": (94.6607, 40.1422)},
    {"city": "银川", "province": "宁夏", "type": "历史文化", "coords": (106.2309, 38.4872)},
    {"city": "石嘴山", "province": "宁夏", "type": "自然风光", "coords": (106.3877, 39.2332)},
    {"city": "吴忠", "province": "宁夏", "type": "自然风光", "coords": (106.1817, 37.9862)},
    {"city": "固原", "province": "宁夏", "type": "自然风光", "coords": (106.2325, 36.0152)},
    {"city": "中卫", "province": "宁夏", "type": "自然风光", "coords": (105.1966, 37.5149)},
    {"city": "西宁", "province": "青海", "type": "自然风光", "coords": (101.7782, 36.6232)},
    {"city": "海东", "province": "青海", "type": "自然风光", "coords": (102.1052, 36.5013)},
    {"city": "乌鲁木齐", "province": "新疆", "type": "现代都市", "coords": (87.6168, 43.8256)},
    {"city": "克拉玛依", "province": "新疆", "type": "自然风光", "coords": (84.8747, 45.5961)},
    {"city": "吐鲁番", "province": "新疆", "type": "历史文化", "coords": (89.1895, 42.9513)},
    {"city": "哈密", "province": "新疆", "type": "历史文化", "coords": (93.5149, 42.8332)},
    {"city": "昌吉", "province": "新疆", "type": "自然风光", "coords": (87.3077, 44.0153)},
    {"city": "博尔塔拉", "province": "新疆", "type": "自然风光", "coords": (82.0750, 44.9030)},
    {"city": "巴音郭楞", "province": "新疆", "type": "自然风光", "coords": (86.1558, 41.7673)},
    {"city": "阿克苏", "province": "新疆", "type": "历史文化", "coords": (80.2610, 41.1672)},
    {"city": "克孜勒苏", "province": "新疆", "type": "自然风光", "coords": (76.1681, 39.4603)},
    {"city": "喀什", "province": "新疆", "type": "历史文化", "coords": (75.9891, 39.4753)},
    {"city": "和田", "province": "新疆", "type": "历史文化", "coords": (79.9264, 37.1104)},
    {"city": "伊犁", "province": "新疆", "type": "自然风光", "coords": (81.3348, 43.9178)},
    {"city": "塔城", "province": "新疆", "type": "自然风光", "coords": (82.9848, 46.7432)},
    {"city": "阿勒泰", "province": "新疆", "type": "自然风光", "coords": (88.1407, 47.8783)},
    {"city": "沈阳", "province": "辽宁", "type": "历史文化", "coords": (123.4315, 41.8057)},
    {"city": "大连", "province": "辽宁", "type": "海滨度假", "coords": (121.6147, 38.9140)},
    {"city": "鞍山", "province": "辽宁", "type": "自然风光", "coords": (122.9956, 41.1087)},
    {"city": "抚顺", "province": "辽宁", "type": "自然风光", "coords": (123.9736, 41.8819)},
    {"city": "本溪", "province": "辽宁", "type": "自然风光", "coords": (123.7714, 41.2979)},
    {"city": "丹东", "province": "辽宁", "type": "自然风光", "coords": (124.3538, 40.0061)},
    {"city": "锦州", "province": "辽宁", "type": "海滨度假", "coords": (121.1561, 41.1330)},
    {"city": "营口", "province": "辽宁", "type": "海滨度假", "coords": (122.2357, 40.6682)},
    {"city": "阜新", "province": "辽宁", "type": "自然风光", "coords": (121.6561, 42.0150)},
    {"city": "辽阳", "province": "辽宁", "type": "历史文化", "coords": (123.1707, 41.2704)},
    {"city": "盘锦", "province": "辽宁", "type": "自然风光", "coords": (122.0707, 41.1177)},
    {"city": "铁岭", "province": "辽宁", "type": "自然风光", "coords": (123.8417, 42.2833)},
    {"city": "朝阳", "province": "辽宁", "type": "自然风光", "coords": (120.4586, 41.5718)},
    {"city": "葫芦岛", "province": "辽宁", "type": "海滨度假", "coords": (120.8489, 40.7175)},
    {"city": "长春", "province": "吉林", "type": "现代都市", "coords": (125.3245, 43.8171)},
    {"city": "吉林", "province": "吉林", "type": "自然风光", "coords": (126.5549, 43.8380)},
    {"city": "四平", "province": "吉林", "type": "历史文化", "coords": (124.3506, 43.1666)},
    {"city": "辽源", "province": "吉林", "type": "自然风光", "coords": (125.1446, 42.8880)},
    {"city": "通化", "province": "吉林", "type": "自然风光", "coords": (125.9397, 41.7278)},
    {"city": "白山", "province": "吉林", "type": "自然风光", "coords": (126.4274, 41.9427)},
    {"city": "松原", "province": "吉林", "type": "自然风光", "coords": (124.8167, 45.1258)},
    {"city": "白城", "province": "吉林", "type": "自然风光", "coords": (122.8446, 45.6197)},
    {"city": "延边", "province": "吉林", "type": "自然风光", "coords": (129.5129, 42.8918)},
    {"city": "哈尔滨", "province": "黑龙江", "type": "历史文化", "coords": (126.6424, 45.7567)},
    {"city": "齐齐哈尔", "province": "黑龙江", "type": "自然风光", "coords": (123.9741, 47.3542)},
    {"city": "鸡西", "province": "黑龙江", "type": "自然风光", "coords": (130.9697, 45.3000)},
    {"city": "鹤岗", "province": "黑龙江", "type": "自然风光", "coords": (130.2771, 47.3508)},
    {"city": "双鸭山", "province": "黑龙江", "type": "自然风光", "coords": (131.1571, 46.6420)},
    {"city": "大庆", "province": "黑龙江", "type": "现代都市", "coords": (125.1297, 46.5908)},
    {"city": "伊春", "province": "黑龙江", "type": "自然风光", "coords": (128.8499, 47.7270)},
    {"city": "佳木斯", "province": "黑龙江", "type": "自然风光", "coords": (130.3198, 46.7971)},
    {"city": "七台河", "province": "黑龙江", "type": "自然风光", "coords": (131.0014, 45.7710)},
    {"city": "牡丹江", "province": "黑龙江", "type": "自然风光", "coords": (129.5968, 44.5527)},
    {"city": "黑河", "province": "黑龙江", "type": "自然风光", "coords": (127.5284, 50.2455)},
    {"city": "绥化", "province": "黑龙江", "type": "自然风光", "coords": (126.9689, 46.6372)},
    {"city": "大兴安岭", "province": "黑龙江", "type": "自然风光", "coords": (124.7112, 52.3357)},
    {"city": "呼和浩特", "province": "内蒙古", "type": "历史文化", "coords": (111.6756, 40.8428)},
    {"city": "包头", "province": "内蒙古", "type": "现代都市", "coords": (109.8403, 40.6571)},
    {"city": "乌海", "province": "内蒙古", "type": "自然风光", "coords": (106.7821, 39.6531)},
    {"city": "赤峰", "province": "内蒙古", "type": "历史文化", "coords": (118.8870, 42.2579)},
    {"city": "通辽", "province": "内蒙古", "type": "自然风光", "coords": (122.2485, 43.6527)},
    {"city": "鄂尔多斯", "province": "内蒙古", "type": "现代都市", "coords": (109.7814, 39.6086)},
    {"city": "呼伦贝尔", "province": "内蒙古", "type": "自然风光", "coords": (119.7727, 49.2149)},
    {"city": "巴彦淖尔", "province": "内蒙古", "type": "自然风光", "coords": (107.3880, 40.7495)},
    {"city": "乌兰察布", "province": "内蒙古", "type": "自然风光", "coords": (113.1330, 41.0340)},
    {"city": "兴安盟", "province": "内蒙古", "type": "自然风光", "coords": (122.0720, 46.0770)},
    {"city": "锡林郭勒", "province": "内蒙古", "type": "自然风光", "coords": (116.0470, 43.9333)},
    {"city": "阿拉善", "province": "内蒙古", "type": "自然风光", "coords": (105.7340, 38.8431)},
    {"city": "石家庄", "province": "河北", "type": "历史文化", "coords": (114.5149, 38.0428)},
    {"city": "唐山", "province": "河北", "type": "现代都市", "coords": (118.1802, 39.6309)},
    {"city": "秦皇岛", "province": "河北", "type": "海滨度假", "coords": (119.6006, 39.9354)},
    {"city": "邯郸", "province": "河北", "type": "历史文化", "coords": (114.4717, 36.6242)},
    {"city": "邢台", "province": "河北", "type": "历史文化", "coords": (114.5048, 37.0682)},
    {"city": "保定", "province": "河北", "type": "历史文化", "coords": (115.4646, 38.8727)},
    {"city": "张家口", "province": "河北", "type": "自然风光", "coords": (114.8860, 40.8210)},
    {"city": "承德", "province": "河北", "type": "历史文化", "coords": (117.9310, 40.9707)},
    {"city": "沧州", "province": "河北", "type": "历史文化", "coords": (116.8386, 38.3037)},
    {"city": "廊坊", "province": "河北", "type": "现代都市", "coords": (116.6839, 39.5246)},
    {"city": "衡水", "province": "河北", "type": "自然风光", "coords": (115.6741, 37.7408)},
]

WEATHER_SEASONS = {
    "春": "3月-5月（春暖花开，适合踏青）",
    "夏": "6月-8月（盛夏时节，注意防暑）",
    "秋": "9月-11月（秋高气爽，最佳旅行季节）",
    "冬": "12月-2月（冬季寒冷，适合看雪景或避寒）",
}

def generate_attractions(city_name, city_type, count=8):
    template = GENERIC_TEMPLATES.get(city_type, GENERIC_TEMPLATES["历史文化"])
    patterns = template["attractions_patterns"]
    
    attractions = []
    for i in range(min(count, len(patterns))):
        attraction = patterns[i].format(city_name)
        attractions.append(attraction)
    
    return attractions

def generate_foods(city_name, city_type, count=8):
    template = GENERIC_TEMPLATES.get(city_type, GENERIC_TEMPLATES["美食之都"])
    patterns = template["food_patterns"]
    
    foods = []
    for i in range(min(count, len(patterns))):
        food = patterns[i].format(city_name)
        foods.append(food)
    
    return foods

def generate_description(city_name, city_type):
    template = GENERIC_TEMPLATES.get(city_type, GENERIC_TEMPLATES["历史文化"])
    adjective = random.choice(template["adjectives"])
    
    descriptions = {
        "历史文化": f"{adjective}{city_name}是{random.choice(['历史名城', '文化古都', '旅游胜地'])}，见证了数千年的文明发展。这里古迹众多，文化底蕴深厚，是了解中国历史的重要窗口。",
        "自然风光": f"{adjective}{city_name}拥有得天独厚的自然条件，山清水秀，风景如画。这里气候宜人，四季分明，是休闲度假的理想去处。",
        "海滨度假": f"{adjective}{city_name}是一座美丽的海滨城市，阳光、沙滩、海浪构成了迷人的画卷。这里空气清新，气候温暖，是度假休闲的天堂。",
        "美食之都": f"{adjective}{city_name}以美食闻名天下，独特的饮食文化吸引了无数吃货慕名而来。这里小吃遍地，老字号云集，是味蕾的天堂。",
        "现代都市": f"{adjective}{city_name}是一座充满活力的现代化都市，繁华的CBD、林立的高楼、丰富的娱乐设施，展现着时代的脉搏。",
        "古镇水乡": f"{adjective}{city_name}保留着完整的古镇风貌，小桥流水人家的景致如诗如画。这里古色古香，民风淳朴，是感受传统江南的好去处。",
    }
    
    return descriptions.get(city_type, descriptions["历史文化"])

def generate_itinerary(city_name, count=4):
    activities = [
        f"游览{city_name}核心景区，感受当地文化",
        f"品尝{city_name}特色美食，大饱口福",
        f"参观{city_name}博物馆，了解历史",
        f"漫步{city_name}老街，体验市井生活",
        f"前往{city_name}周边景点，探索自然",
        f"购买{city_name}特色纪念品",
        f"体验{city_name}民俗活动",
    ]
    
    itinerary = []
    for day in range(1, count + 1):
        activity = activities[(day - 1) % len(activities)]
        itinerary.append(f"Day{day}: {activity}")
    
    return itinerary

def generate_tips(city_name, city_type):
    attractions = generate_attractions(city_name, city_type, 10)
    foods = generate_foods(city_name, city_type, 10)
    hotels = [
        f"{city_name}国际大酒店（五星级）",
        f"{city_name}假日酒店（商务型）",
        f"{city_name}精品民宿（当地特色）",
        f"{city_name}快捷连锁酒店（性价比高）",
        f"{city_name}温泉度假村（度假型）",
    ]
    itinerary = generate_itinerary(city_name, 5)
    transport_tips = [
        f"{city_name}公共交通便利，推荐地铁出行",
        f"机场到市区有直达大巴，票价约20元",
        f"出租车起步价约10元，网约车更便宜",
        f"景区之间可乘坐旅游专线车",
        f"共享单车是短途出行的好选择",
    ]
    photo_spots = [
        f"{city_name}标志性建筑",
        f"{city_name}最佳观景点",
        f"{city_name}老街巷弄",
        f"{city_name}夜景灯光",
        f"{city_name}自然风光",
    ]
    avoid_traps = [
        f"{city_name}景区周边可能有黑导游，注意识别",
        f"购买特产建议去正规商场或老字号",
        f"旅游旺季酒店价格翻倍，建议提前预订",
        f"热门景点可能需要排队，请合理安排时间",
    ]
    budget = {
        "economy": {"hotel": "150-300", "meal": "30-60", "transport": "10-20", "total_daily": "200-400"},
        "mid": {"hotel": "400-700", "meal": "60-120", "transport": "20-40", "total_daily": "500-800"},
        "luxury": {"hotel": "1000+", "meal": "200+", "transport": "打车为主", "total_daily": "1500+"},
    }
    
    return {
        "attractions": attractions,
        "food": foods,
        "food_spots": [f"{city_name}美食街", f"{city_name}老字号一条街", f"{city_name}夜市"],
        "hotels": hotels,
        "itinerary_suggestion": itinerary,
        "transport_tips": transport_tips,
        "best_photo_spots": photo_spots,
        "avoid_traps": avoid_traps,
        "clothing_advice": f"{city_name}四季分明，建议根据季节选择合适衣物。夏季穿轻薄透气的衣服，冬季需要保暖外套。",
        "souvenirs": [f"{city_name}特色小吃", f"{city_name}手工艺品", f"{city_name}茶叶"],
        "budget": budget,
        "family_friendly": random.choice([3, 4, 5]),
        "couple_friendly": random.choice([3, 4, 5]),
        "solo_friendly": random.choice([3, 4, 5]),
        "nightlife": random.choice([2, 3, 4]),
        "accessibility": "交通便利，景区设施完善",
    }

def generate_city_data():
    city_coords = {}
    city_tags = {}
    city_info = {}
    city_tips = {}
    
    for city_data in CITY_POOL:
        city_name = city_data["city"]
        city_type = city_data["type"]
        province = city_data["province"]
        coords = city_data["coords"]
        
        city_coords[city_name] = list(coords)
        
        template = GENERIC_TEMPLATES[city_type]
        extra_tags = [province, f"{province}省会" if city_name in ["石家庄", "太原", "沈阳", "长春", "哈尔滨", "南京", "杭州", "合肥", "福州", "南昌", "济南", "郑州", "武汉", "长沙", "广州", "海口", "成都", "贵阳", "昆明", "西安", "兰州", "西宁", "拉萨", "乌鲁木齐", "呼和浩特", "南宁", "银川", "台北"] else ""]
        extra_tags = [t for t in extra_tags if t]
        city_tags[city_name] = template["tags"] + extra_tags
        
        city_info[city_name] = {
            "name": city_name,
            "province": province,
            "description": generate_description(city_name, city_type),
            "rating": round(random.uniform(4.0, 4.9), 1),
            "best_time": WEATHER_SEASONS.get(random.choice(list(WEATHER_SEASONS.keys())), WEATHER_SEASONS["秋"]),
            "weather_tips": f"{city_name}属于{random.choice(['温带季风', '亚热带季风', '热带季风', '高原山地', '温带大陆性'])}气候，四季分明。建议出行前查看天气预报。",
            "transport": f"{city_name}交通便利，有国际机场、火车站和完善的城市交通网络。",
            "highlights": f"{generate_attractions(city_name, city_type, 3)}",
            "price": random.choice(["经济型，人均300-500元/天", "中等消费，人均500-800元/天", "较高消费，人均800-1200元/天"]),
            "avg_daily_budget": random.choice([300, 400, 500, 600, 700]),
        }
        
        city_tips[city_name] = generate_tips(city_name, city_type)
    
    # 输出Python代码
    output = f'''# 批量生成的城市数据 - {len(CITY_POOL)}个城市
# 自动生成，包含丰富的旅游信息

MASS_CITY_COORDS = {json.dumps(city_coords, ensure_ascii=False, indent=4)}

MASS_CITY_TAGS = {json.dumps(city_tags, ensure_ascii=False, indent=4)}

MASS_CITY_INFO = {json.dumps(city_info, ensure_ascii=False, indent=4)}

MASS_CITY_TIPS = {json.dumps(city_tips, ensure_ascii=False, indent=4)}
'''
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"✅ 成功生成 {len(CITY_POOL)} 个城市的数据！")
    print(f"   输出文件: {OUTPUT_FILE}")
    print(f"   文件大小: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")
    
    # 统计各类型数量
    type_count = {}
    for city in CITY_POOL:
        t = city["type"]
        type_count[t] = type_count.get(t, 0) + 1
    
    print("\n📊 城市类型分布:")
    for t, count in type_count.items():
        print(f"   {t}: {count} 个")
    
    print(f"\n📍 总共有 {len(CITY_POOL)} 个城市")

if __name__ == "__main__":
    generate_city_data()
