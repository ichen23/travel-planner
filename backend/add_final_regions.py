import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FINAL_DATA = {
    "兰州市": {"name": "兰州市", "province": "甘肃省", "lng": 103.8343, "lat": 36.0611, "type": "地级市", "parent": "甘肃省"},
    "嘉峪关市": {"name": "嘉峪关市", "province": "甘肃省", "lng": 98.2894, "lat": 39.7726, "type": "地级市", "parent": "甘肃省"},
    "金昌市": {"name": "金昌市", "province": "甘肃省", "lng": 102.1830, "lat": 38.5170, "type": "地级市", "parent": "甘肃省"},
    "白银市": {"name": "白银市", "province": "甘肃省", "lng": 104.1389, "lat": 36.5310, "type": "地级市", "parent": "甘肃省"},
    "天水市": {"name": "天水市", "province": "甘肃省", "lng": 105.7249, "lat": 34.5809, "type": "地级市", "parent": "甘肃省"},
    "武威市": {"name": "武威市", "province": "甘肃省", "lng": 102.6330, "lat": 37.9170, "type": "地级市", "parent": "甘肃省"},
    "张掖市": {"name": "张掖市", "province": "甘肃省", "lng": 100.4472, "lat": 38.9381, "type": "地级市", "parent": "甘肃省"},
    "平凉市": {"name": "平凉市", "province": "甘肃省", "lng": 106.6670, "lat": 35.5170, "type": "地级市", "parent": "甘肃省"},
    "酒泉市": {"name": "酒泉市", "province": "甘肃省", "lng": 98.4941, "lat": 39.7432, "type": "地级市", "parent": "甘肃省"},
    "庆阳市": {"name": "庆阳市", "province": "甘肃省", "lng": 107.6330, "lat": 35.7330, "type": "地级市", "parent": "甘肃省"},
    "定西市": {"name": "定西市", "province": "甘肃省", "lng": 104.6170, "lat": 35.5830, "type": "地级市", "parent": "甘肃省"},
    "陇南市": {"name": "陇南市", "province": "甘肃省", "lng": 104.9170, "lat": 33.3830, "type": "地级市", "parent": "甘肃省"},
    "临夏回族自治州": {"name": "临夏市", "province": "甘肃省", "lng": 103.2170, "lat": 35.6170, "type": "地级市", "parent": "甘肃省"},
    "甘南藏族自治州": {"name": "合作市", "province": "甘肃省", "lng": 102.9170, "lat": 34.9830, "type": "地级市", "parent": "甘肃省"},
    "敦煌市": {"name": "敦煌市", "province": "甘肃省", "lng": 94.6650, "lat": 40.1430, "type": "县级市", "parent": "酒泉市"},
    "玉门市": {"name": "玉门市", "province": "甘肃省", "lng": 97.6330, "lat": 40.2830, "type": "县级市", "parent": "酒泉市"},
    "天水市": {"name": "天水市", "province": "甘肃省", "lng": 105.7249, "lat": 34.5809, "type": "县级市", "parent": "天水地区"},
    "兰州市": {"name": "兰州市", "province": "甘肃省", "lng": 103.8343, "lat": 36.0611, "type": "县级市", "parent": "兰州地区"},
    
    "昆明市": {"name": "昆明市", "province": "云南省", "lng": 102.8329, "lat": 24.8801, "type": "地级市", "parent": "云南省"},
    "曲靖市": {"name": "曲靖市", "province": "云南省", "lng": 103.7960, "lat": 25.4890, "type": "地级市", "parent": "云南省"},
    "玉溪市": {"name": "玉溪市", "province": "云南省", "lng": 102.5410, "lat": 24.3520, "type": "地级市", "parent": "云南省"},
    "保山市": {"name": "保山市", "province": "云南省", "lng": 99.1670, "lat": 25.1170, "type": "地级市", "parent": "云南省"},
    "昭通市": {"name": "昭通市", "province": "云南省", "lng": 103.7170, "lat": 27.3330, "type": "地级市", "parent": "云南省"},
    "丽江市": {"name": "丽江市", "province": "云南省", "lng": 100.2330, "lat": 26.8721, "type": "地级市", "parent": "云南省"},
    "普洱市": {"name": "普洱市", "province": "云南省", "lng": 100.9670, "lat": 22.8250, "type": "地级市", "parent": "云南省"},
    "临沧市": {"name": "临沧市", "province": "云南省", "lng": 100.0830, "lat": 23.8830, "type": "地级市", "parent": "云南省"},
    "楚雄彝族自治州": {"name": "楚雄市", "province": "云南省", "lng": 101.5170, "lat": 25.0170, "type": "地级市", "parent": "云南省"},
    "红河哈尼族彝族自治州": {"name": "蒙自市", "province": "云南省", "lng": 103.3670, "lat": 23.3670, "type": "地级市", "parent": "云南省"},
    "文山壮族苗族自治州": {"name": "文山市", "province": "云南省", "lng": 104.2500, "lat": 23.3670, "type": "地级市", "parent": "云南省"},
    "西双版纳傣族自治州": {"name": "景洪市", "province": "云南省", "lng": 100.8170, "lat": 22.0170, "type": "地级市", "parent": "云南省"},
    "大理白族自治州": {"name": "大理市", "province": "云南省", "lng": 100.2676, "lat": 25.6065, "type": "地级市", "parent": "云南省"},
    "德宏傣族景颇族自治州": {"name": "芒市", "province": "云南省", "lng": 98.5830, "lat": 24.4330, "type": "地级市", "parent": "云南省"},
    "怒江傈僳族自治州": {"name": "六库市", "province": "云南省", "lng": 98.8500, "lat": 25.8670, "type": "地级市", "parent": "云南省"},
    "迪庆藏族自治州": {"name": "香格里拉市", "province": "云南省", "lng": 99.7082, "lat": 27.8721, "type": "地级市", "parent": "云南省"},
    "安宁市": {"name": "安宁市", "province": "云南省", "lng": 102.3830, "lat": 24.8830, "type": "县级市", "parent": "昆明市"},
    "曲靖市": {"name": "曲靖市", "province": "云南省", "lng": 103.7960, "lat": 25.4890, "type": "县级市", "parent": "曲靖地区"},
    
    "西安市": {"name": "西安市", "province": "陕西省", "lng": 108.9402, "lat": 34.3416, "type": "地级市", "parent": "陕西省"},
    "铜川市": {"name": "铜川市", "province": "陕西省", "lng": 108.9500, "lat": 34.9000, "type": "地级市", "parent": "陕西省"},
    "宝鸡市": {"name": "宝鸡市", "province": "陕西省", "lng": 107.2369, "lat": 34.3617, "type": "地级市", "parent": "陕西省"},
    "咸阳市": {"name": "咸阳市", "province": "陕西省", "lng": 108.7089, "lat": 34.3296, "type": "地级市", "parent": "陕西省"},
    "渭南市": {"name": "渭南市", "province": "陕西省", "lng": 109.5000, "lat": 34.5170, "type": "地级市", "parent": "陕西省"},
    "延安市": {"name": "延安市", "province": "陕西省", "lng": 109.4898, "lat": 36.5853, "type": "地级市", "parent": "陕西省"},
    "汉中市": {"name": "汉中市", "province": "陕西省", "lng": 107.0230, "lat": 33.0700, "type": "地级市", "parent": "陕西省"},
    "榆林市": {"name": "榆林市", "province": "陕西省", "lng": 109.7330, "lat": 38.2830, "type": "地级市", "parent": "陕西省"},
    "安康市": {"name": "安康市", "province": "陕西省", "lng": 109.0293, "lat": 32.6890, "type": "地级市", "parent": "陕西省"},
    "商洛市": {"name": "商洛市", "province": "陕西省", "lng": 109.9400, "lat": 33.8670, "type": "地级市", "parent": "陕西省"},
    "铜川市": {"name": "铜川市", "province": "陕西省", "lng": 108.9500, "lat": 34.9000, "type": "县级市", "parent": "铜川地区"},
    "宝鸡市": {"name": "宝鸡市", "province": "陕西省", "lng": 107.2369, "lat": 34.3617, "type": "县级市", "parent": "宝鸡地区"},
    
    "台北市": {"name": "台北市", "province": "台湾省", "lng": 121.5654, "lat": 25.0330, "type": "地级市", "parent": "台湾省"},
    "新北市": {"name": "新北市", "province": "台湾省", "lng": 121.4670, "lat": 25.0170, "type": "地级市", "parent": "台湾省"},
    "桃园市": {"name": "桃园市", "province": "台湾省", "lng": 121.3170, "lat": 24.9830, "type": "地级市", "parent": "台湾省"},
    "台中市": {"name": "台中市", "province": "台湾省", "lng": 120.6736, "lat": 24.1477, "type": "地级市", "parent": "台湾省"},
    "台南市": {"name": "台南市", "province": "台湾省", "lng": 120.2270, "lat": 23.0000, "type": "地级市", "parent": "台湾省"},
    "高雄市": {"name": "高雄市", "province": "台湾省", "lng": 120.3130, "lat": 22.6273, "type": "地级市", "parent": "台湾省"},
    "基隆市": {"name": "基隆市", "province": "台湾省", "lng": 121.7680, "lat": 25.1330, "type": "地级市", "parent": "台湾省"},
    "新竹市": {"name": "新竹市", "province": "台湾省", "lng": 120.9670, "lat": 24.8030, "type": "地级市", "parent": "台湾省"},
    "嘉义市": {"name": "嘉义市", "province": "台湾省", "lng": 120.4500, "lat": 23.4670, "type": "地级市", "parent": "台湾省"},
    "宜兰县": {"name": "宜兰县", "province": "台湾省", "lng": 121.7500, "lat": 24.7670, "type": "县", "parent": "台湾省"},
    "新竹县": {"name": "新竹县", "province": "台湾省", "lng": 120.9670, "lat": 24.8330, "type": "县", "parent": "台湾省"},
    "苗栗县": {"name": "苗栗县", "province": "台湾省", "lng": 120.9000, "lat": 24.5670, "type": "县", "parent": "台湾省"},
    "彰化县": {"name": "彰化县", "province": "台湾省", "lng": 120.5670, "lat": 24.0830, "type": "县", "parent": "台湾省"},
    "南投县": {"name": "南投县", "province": "台湾省", "lng": 120.9830, "lat": 23.9170, "type": "县", "parent": "台湾省"},
    "云林县": {"name": "云林县", "province": "台湾省", "lng": 120.4670, "lat": 23.7170, "type": "县", "parent": "台湾省"},
    "嘉义县": {"name": "嘉义县", "province": "台湾省", "lng": 120.4670, "lat": 23.4670, "type": "县", "parent": "台湾省"},
    "屏东县": {"name": "屏东县", "province": "台湾省", "lng": 120.6500, "lat": 22.5670, "type": "县", "parent": "台湾省"},
    "台东县": {"name": "台东县", "province": "台湾省", "lng": 121.1500, "lat": 23.0170, "type": "县", "parent": "台湾省"},
    "花莲县": {"name": "花莲县", "province": "台湾省", "lng": 121.6000, "lat": 23.9830, "type": "县", "parent": "台湾省"},
    "澎湖县": {"name": "澎湖县", "province": "台湾省", "lng": 119.6170, "lat": 23.5670, "type": "县", "parent": "台湾省"},
    "金门县": {"name": "金门县", "province": "台湾省", "lng": 118.3170, "lat": 24.4330, "type": "县", "parent": "台湾省"},
    "连江县": {"name": "连江县", "province": "台湾省", "lng": 119.9500, "lat": 26.1830, "type": "县", "parent": "台湾省"},
    
    "香港岛": {"name": "香港岛", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.2670, "type": "地级市", "parent": "香港特别行政区"},
    "九龙": {"name": "九龙", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.3170, "type": "地级市", "parent": "香港特别行政区"},
    "新界": {"name": "新界", "province": "香港特别行政区", "lng": 114.0830, "lat": 22.4170, "type": "地级市", "parent": "香港特别行政区"},
    "中西区": {"name": "中西区", "province": "香港特别行政区", "lng": 114.1500, "lat": 22.2830, "type": "区", "parent": "香港岛"},
    "湾仔区": {"name": "湾仔区", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.2830, "type": "区", "parent": "香港岛"},
    "东区": {"name": "东区", "province": "香港特别行政区", "lng": 114.2170, "lat": 22.2830, "type": "区", "parent": "香港岛"},
    "南区": {"name": "南区", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.2170, "type": "区", "parent": "香港岛"},
    "油尖旺区": {"name": "油尖旺区", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.3170, "type": "区", "parent": "九龙"},
    "深水埗区": {"name": "深水埗区", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.3330, "type": "区", "parent": "九龙"},
    "九龙城区": {"name": "九龙城区", "province": "香港特别行政区", "lng": 114.1830, "lat": 22.3170, "type": "区", "parent": "九龙"},
    "黄大仙区": {"name": "黄大仙区", "province": "香港特别行政区", "lng": 114.2170, "lat": 22.3330, "type": "区", "parent": "九龙"},
    "观塘区": {"name": "观塘区", "province": "香港特别行政区", "lng": 114.2170, "lat": 22.3170, "type": "区", "parent": "九龙"},
    "荃湾区": {"name": "荃湾区", "province": "香港特别行政区", "lng": 114.1170, "lat": 22.3670, "type": "区", "parent": "新界"},
    "屯门区": {"name": "屯门区", "province": "香港特别行政区", "lng": 113.9670, "lat": 22.4000, "type": "区", "parent": "新界"},
    "元朗区": {"name": "元朗区", "province": "香港特别行政区", "lng": 114.0170, "lat": 22.4330, "type": "区", "parent": "新界"},
    "北区": {"name": "北区", "province": "香港特别行政区", "lng": 114.1170, "lat": 22.5170, "type": "区", "parent": "新界"},
    "大埔区": {"name": "大埔区", "province": "香港特别行政区", "lng": 114.1670, "lat": 22.4670, "type": "区", "parent": "新界"},
    "沙田区": {"name": "沙田区", "province": "香港特别行政区", "lng": 114.1830, "lat": 22.4000, "type": "区", "parent": "新界"},
    "西贡区": {"name": "西贡区", "province": "香港特别行政区", "lng": 114.2670, "lat": 22.3830, "type": "区", "parent": "新界"},
    "葵青区": {"name": "葵青区", "province": "香港特别行政区", "lng": 114.1170, "lat": 22.3670, "type": "区", "parent": "新界"},
    "离岛区": {"name": "离岛区", "province": "香港特别行政区", "lng": 113.9170, "lat": 22.2830, "type": "区", "parent": "新界"},
    
    "澳门半岛": {"name": "澳门半岛", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.1830, "type": "地级市", "parent": "澳门特别行政区"},
    "氹仔岛": {"name": "氹仔岛", "province": "澳门特别行政区", "lng": 113.5670, "lat": 22.1670, "type": "地级市", "parent": "澳门特别行政区"},
    "路环岛": {"name": "路环岛", "province": "澳门特别行政区", "lng": 113.5830, "lat": 22.1170, "type": "地级市", "parent": "澳门特别行政区"},
    "花地玛堂区": {"name": "花地玛堂区", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.2000, "type": "堂区", "parent": "澳门半岛"},
    "圣安多尼堂区": {"name": "圣安多尼堂区", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.2000, "type": "堂区", "parent": "澳门半岛"},
    "大堂区": {"name": "大堂区", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.2000, "type": "堂区", "parent": "澳门半岛"},
    "望德堂区": {"name": "望德堂区", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.2000, "type": "堂区", "parent": "澳门半岛"},
    "风顺堂区": {"name": "风顺堂区", "province": "澳门特别行政区", "lng": 113.5500, "lat": 22.1830, "type": "堂区", "parent": "澳门半岛"},
    "嘉模堂区": {"name": "嘉模堂区", "province": "澳门特别行政区", "lng": 113.5670, "lat": 22.1670, "type": "堂区", "parent": "氹仔岛"},
    "路凼填海区": {"name": "路凼填海区", "province": "澳门特别行政区", "lng": 113.5670, "lat": 22.1500, "type": "堂区", "parent": "氹仔岛"},
    "圣方济各堂区": {"name": "圣方济各堂区", "province": "澳门特别行政区", "lng": 113.5830, "lat": 22.1170, "type": "堂区", "parent": "路环岛"},
    "路凼填海区": {"name": "路凼填海区", "province": "澳门特别行政区", "lng": 113.5670, "lat": 22.1500, "type": "堂区", "parent": "路环岛"},
}

from app.services.real_city_data import REAL_CITY_DATA

existing_keys = set(REAL_CITY_DATA.keys())
new_keys = set(FINAL_DATA.keys())

duplicates = existing_keys & new_keys
if duplicates:
    print(f"发现 {len(duplicates)} 个重复键，正在跳过...")
    for key in duplicates:
        del FINAL_DATA[key]

REAL_CITY_DATA.update(FINAL_DATA)

provinces = {}
for name, data in REAL_CITY_DATA.items():
    province = data.get('province', '未知')
    if province not in provinces:
        provinces[province] = 0
    provinces[province] += 1

print(f"\n最终数据统计：")
print(f"总数据量: {len(REAL_CITY_DATA)}")
print(f"省份数量: {len(provinces)}")
print(f"\n各省份数据分布：")
for prov, count in sorted(provinces.items()):
    print(f"  {prov}: {count}个")
