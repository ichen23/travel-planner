import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MISSING_DATA = {
    # ==================== 青海省 ====================
    "西宁市": {"name": "西宁市", "province": "青海省", "lng": 101.7782, "lat": 36.6232, "type": "地级市", "parent": "青海省"},
    "城东区": {"name": "城东区", "province": "青海省", "lng": 101.8170, "lat": 36.6170, "type": "市辖区", "parent": "西宁市"},
    "城中区": {"name": "城中区", "province": "青海省", "lng": 101.7670, "lat": 36.6170, "type": "市辖区", "parent": "西宁市"},
    "城西区": {"name": "城西区", "province": "青海省", "lng": 101.7670, "lat": 36.6330, "type": "市辖区", "parent": "西宁市"},
    "城北区": {"name": "城北区", "province": "青海省", "lng": 101.7670, "lat": 36.6500, "type": "市辖区", "parent": "西宁市"},
    "大通回族土族自治县": {"name": "大通回族土族自治县", "province": "青海省", "lng": 101.6830, "lat": 36.9330, "type": "自治县", "parent": "西宁市"},
    "湟中县": {"name": "湟中县", "province": "青海省", "lng": 101.5670, "lat": 36.5170, "type": "县", "parent": "西宁市"},
    "湟源县": {"name": "湟源县", "province": "青海省", "lng": 101.2670, "lat": 36.6670, "type": "县", "parent": "西宁市"},
    "海东市": {"name": "海东市", "province": "青海省", "lng": 102.1670, "lat": 36.5170, "type": "地级市", "parent": "青海省"},
    "乐都区": {"name": "乐都区", "province": "青海省", "lng": 102.4170, "lat": 36.4830, "type": "市辖区", "parent": "海东市"},
    "平安区": {"name": "平安区", "province": "青海省", "lng": 102.1170, "lat": 36.5170, "type": "市辖区", "parent": "海东市"},
    "民和回族土族自治县": {"name": "民和回族土族自治县", "province": "青海省", "lng": 102.8170, "lat": 36.3330, "type": "自治县", "parent": "海东市"},
    "互助土族自治县": {"name": "互助土族自治县", "province": "青海省", "lng": 102.0500, "lat": 36.8330, "type": "自治县", "parent": "海东市"},
    "化隆回族自治县": {"name": "化隆回族自治县", "province": "青海省", "lng": 102.2500, "lat": 36.1170, "type": "自治县", "parent": "海东市"},
    "循化撒拉族自治县": {"name": "循化撒拉族自治县", "province": "青海省", "lng": 102.4670, "lat": 35.8500, "type": "自治县", "parent": "海东市"},
    "海北藏族自治州": {"name": "海晏县", "province": "青海省", "lng": 100.9830, "lat": 36.9830, "type": "地级市", "parent": "青海省"},
    "海晏县": {"name": "海晏县", "province": "青海省", "lng": 100.9830, "lat": 36.9830, "type": "县", "parent": "海北藏族自治州"},
    "祁连县": {"name": "祁连县", "province": "青海省", "lng": 100.2500, "lat": 38.1830, "type": "县", "parent": "海北藏族自治州"},
    "刚察县": {"name": "刚察县", "province": "青海省", "lng": 100.1670, "lat": 37.3330, "type": "县", "parent": "海北藏族自治州"},
    "门源回族自治县": {"name": "门源回族自治县", "province": "青海省", "lng": 101.6170, "lat": 37.3830, "type": "自治县", "parent": "海北藏族自治州"},
    "黄南藏族自治州": {"name": "同仁市", "province": "青海省", "lng": 102.0170, "lat": 35.5170, "type": "地级市", "parent": "青海省"},
    "同仁市": {"name": "同仁市", "province": "青海省", "lng": 102.0170, "lat": 35.5170, "type": "县级市", "parent": "黄南藏族自治州"},
    "尖扎县": {"name": "尖扎县", "province": "青海省", "lng": 102.0670, "lat": 35.9170, "type": "县", "parent": "黄南藏族自治州"},
    "泽库县": {"name": "泽库县", "province": "青海省", "lng": 101.4670, "lat": 35.0330, "type": "县", "parent": "黄南藏族自治州"},
    "河南蒙古族自治县": {"name": "河南蒙古族自治县", "province": "青海省", "lng": 101.6170, "lat": 34.7330, "type": "自治县", "parent": "黄南藏族自治州"},
    "海南藏族自治州": {"name": "共和县", "province": "青海省", "lng": 100.6170, "lat": 36.2830, "type": "地级市", "parent": "青海省"},
    "共和县": {"name": "共和县", "province": "青海省", "lng": 100.6170, "lat": 36.2830, "type": "县", "parent": "海南藏族自治州"},
    "同德县": {"name": "同德县", "province": "青海省", "lng": 100.6170, "lat": 35.2670, "type": "县", "parent": "海南藏族自治州"},
    "贵德县": {"name": "贵德县", "province": "青海省", "lng": 101.4170, "lat": 36.0330, "type": "县", "parent": "海南藏族自治州"},
    "兴海县": {"name": "兴海县", "province": "青海省", "lng": 99.9170, "lat": 35.5170, "type": "县", "parent": "海南藏族自治州"},
    "贵南县": {"name": "贵南县", "province": "青海省", "lng": 100.7330, "lat": 35.5170, "type": "县", "parent": "海南藏族自治州"},
    "果洛藏族自治州": {"name": "玛沁县", "province": "青海省", "lng": 100.2330, "lat": 34.4830, "type": "地级市", "parent": "青海省"},
    "玛沁县": {"name": "玛沁县", "province": "青海省", "lng": 100.2330, "lat": 34.4830, "type": "县", "parent": "果洛藏族自治州"},
    "班玛县": {"name": "班玛县", "province": "青海省", "lng": 100.7500, "lat": 32.9170, "type": "县", "parent": "果洛藏族自治州"},
    "甘德县": {"name": "甘德县", "province": "青海省", "lng": 99.9170, "lat": 33.9170, "type": "县", "parent": "果洛藏族自治州"},
    "达日县": {"name": "达日县", "province": "青海省", "lng": 99.6500, "lat": 33.7170, "type": "县", "parent": "果洛藏族自治州"},
    "久治县": {"name": "久治县", "province": "青海省", "lng": 101.4170, "lat": 33.4670, "type": "县", "parent": "果洛藏族自治州"},
    "玛多县": {"name": "玛多县", "province": "青海省", "lng": 98.2500, "lat": 34.9170, "type": "县", "parent": "果洛藏族自治州"},
    "玉树藏族自治州": {"name": "玉树市", "province": "青海省", "lng": 96.9830, "lat": 33.0170, "type": "地级市", "parent": "青海省"},
    "玉树市": {"name": "玉树市", "province": "青海省", "lng": 96.9830, "lat": 33.0170, "type": "县级市", "parent": "玉树藏族自治州"},
    "杂多县": {"name": "杂多县", "province": "青海省", "lng": 95.2830, "lat": 32.9170, "type": "县", "parent": "玉树藏族自治州"},
    "称多县": {"name": "称多县", "province": "青海省", "lng": 97.1170, "lat": 33.3830, "type": "县", "parent": "玉树藏族自治州"},
    "治多县": {"name": "治多县", "province": "青海省", "lng": 95.2830, "lat": 34.1500, "type": "县", "parent": "玉树藏族自治州"},
    "囊谦县": {"name": "囊谦县", "province": "青海省", "lng": 96.4830, "lat": 32.2170, "type": "县", "parent": "玉树藏族自治州"},
    "曲麻莱县": {"name": "曲麻莱县", "province": "青海省", "lng": 95.5170, "lat": 34.5170, "type": "县", "parent": "玉树藏族自治州"},
    "海西蒙古族藏族自治州": {"name": "德令哈市", "province": "青海省", "lng": 97.3830, "lat": 37.3830, "type": "地级市", "parent": "青海省"},
    "德令哈市": {"name": "德令哈市", "province": "青海省", "lng": 97.3830, "lat": 37.3830, "type": "县级市", "parent": "海西蒙古族藏族自治州"},
    "格尔木市": {"name": "格尔木市", "province": "青海省", "lng": 94.9000, "lat": 36.4170, "type": "县级市", "parent": "海西蒙古族藏族自治州"},
    "乌兰县": {"name": "乌兰县", "province": "青海省", "lng": 98.4670, "lat": 36.9170, "type": "县", "parent": "海西蒙古族藏族自治州"},
    "都兰县": {"name": "都兰县", "province": "青海省", "lng": 98.1170, "lat": 36.3170, "type": "县", "parent": "海西蒙古族藏族自治州"},
    "天峻县": {"name": "天峻县", "province": "青海省", "lng": 97.8170, "lat": 37.2830, "type": "县", "parent": "海西蒙古族藏族自治州"},
    "茫崖市": {"name": "茫崖市", "province": "青海省", "lng": 91.6170, "lat": 38.3330, "type": "县级市", "parent": "海西蒙古族藏族自治州"},

    # ==================== 宁夏回族自治区 ====================
    "银川市": {"name": "银川市", "province": "宁夏回族自治区", "lng": 106.2309, "lat": 38.4872, "type": "地级市", "parent": "宁夏回族自治区"},
    "兴庆区": {"name": "兴庆区", "province": "宁夏回族自治区", "lng": 106.2830, "lat": 38.4830, "type": "市辖区", "parent": "银川市"},
    "西夏区": {"name": "西夏区", "province": "宁夏回族自治区", "lng": 106.1170, "lat": 38.5170, "type": "市辖区", "parent": "银川市"},
    "金凤区": {"name": "金凤区", "province": "宁夏回族自治区", "lng": 106.2170, "lat": 38.4670, "type": "市辖区", "parent": "银川市"},
    "永宁县": {"name": "永宁县", "province": "宁夏回族自治区", "lng": 106.2500, "lat": 38.2830, "type": "县", "parent": "银川市"},
    "贺兰县": {"name": "贺兰县", "province": "宁夏回族自治区", "lng": 106.3500, "lat": 38.5670, "type": "县", "parent": "银川市"},
    "灵武市": {"name": "灵武市", "province": "宁夏回族自治区", "lng": 106.3400, "lat": 38.1000, "type": "县级市", "parent": "银川市"},
    "石嘴山市": {"name": "石嘴山市", "province": "宁夏回族自治区", "lng": 106.3780, "lat": 39.0130, "type": "地级市", "parent": "宁夏回族自治区"},
    "大武口区": {"name": "大武口区", "province": "宁夏回族自治区", "lng": 106.3830, "lat": 39.0170, "type": "市辖区", "parent": "石嘴山市"},
    "惠农区": {"name": "惠农区", "province": "宁夏回族自治区", "lng": 106.7670, "lat": 39.2500, "type": "市辖区", "parent": "石嘴山市"},
    "平罗县": {"name": "平罗县", "province": "宁夏回族自治区", "lng": 106.5500, "lat": 38.9000, "type": "县", "parent": "石嘴山市"},
    "吴忠市": {"name": "吴忠市", "province": "宁夏回族自治区", "lng": 106.1950, "lat": 37.9860, "type": "地级市", "parent": "宁夏回族自治区"},
    "利通区": {"name": "利通区", "province": "宁夏回族自治区", "lng": 106.2170, "lat": 37.9830, "type": "市辖区", "parent": "吴忠市"},
    "红寺堡区": {"name": "红寺堡区", "province": "宁夏回族自治区", "lng": 106.0670, "lat": 37.4170, "type": "市辖区", "parent": "吴忠市"},
    "盐池县": {"name": "盐池县", "province": "宁夏回族自治区", "lng": 107.4170, "lat": 37.7830, "type": "县", "parent": "吴忠市"},
    "同心县": {"name": "同心县", "province": "宁夏回族自治区", "lng": 105.9170, "lat": 36.9830, "type": "县", "parent": "吴忠市"},
    "青铜峡市": {"name": "青铜峡市", "province": "宁夏回族自治区", "lng": 106.0700, "lat": 38.0200, "type": "县级市", "parent": "吴忠市"},
    "固原市": {"name": "固原市", "province": "宁夏回族自治区", "lng": 106.2420, "lat": 36.0150, "type": "地级市", "parent": "宁夏回族自治区"},
    "原州区": {"name": "原州区", "province": "宁夏回族自治区", "lng": 106.2500, "lat": 36.0170, "type": "市辖区", "parent": "固原市"},
    "西吉县": {"name": "西吉县", "province": "宁夏回族自治区", "lng": 105.7330, "lat": 35.9670, "type": "县", "parent": "固原市"},
    "隆德县": {"name": "隆德县", "province": "宁夏回族自治区", "lng": 106.1170, "lat": 35.6330, "type": "县", "parent": "固原市"},
    "泾源县": {"name": "泾源县", "province": "宁夏回族自治区", "lng": 106.3500, "lat": 35.4830, "type": "县", "parent": "固原市"},
    "彭阳县": {"name": "彭阳县", "province": "宁夏回族自治区", "lng": 106.6500, "lat": 35.8500, "type": "县", "parent": "固原市"},
    "中卫市": {"name": "中卫市", "province": "宁夏回族自治区", "lng": 105.1960, "lat": 37.5150, "type": "地级市", "parent": "宁夏回族自治区"},
    "沙坡头区": {"name": "沙坡头区", "province": "宁夏回族自治区", "lng": 105.2500, "lat": 37.5170, "type": "市辖区", "parent": "中卫市"},
    "中宁县": {"name": "中宁县", "province": "宁夏回族自治区", "lng": 105.6830, "lat": 37.5170, "type": "县", "parent": "中卫市"},
    "海原县": {"name": "海原县", "province": "宁夏回族自治区", "lng": 105.6500, "lat": 36.5170, "type": "县", "parent": "中卫市"},

    # ==================== 贵州省 ====================
    "贵阳市": {"name": "贵阳市", "province": "贵州省", "lng": 106.7135, "lat": 26.5783, "type": "地级市", "parent": "贵州省"},
    "南明区": {"name": "南明区", "province": "贵州省", "lng": 106.7170, "lat": 26.5670, "type": "市辖区", "parent": "贵阳市"},
    "云岩区": {"name": "云岩区", "province": "贵州省", "lng": 106.6670, "lat": 26.5830, "type": "市辖区", "parent": "贵阳市"},
    "花溪区": {"name": "花溪区", "province": "贵州省", "lng": 106.6670, "lat": 26.4170, "type": "市辖区", "parent": "贵阳市"},
    "乌当区": {"name": "乌当区", "province": "贵州省", "lng": 106.8170, "lat": 26.6170, "type": "市辖区", "parent": "贵阳市"},
    "白云区": {"name": "白云区", "province": "贵州省", "lng": 106.7170, "lat": 26.6670, "type": "市辖区", "parent": "贵阳市"},
    "观山湖区": {"name": "观山湖区", "province": "贵州省", "lng": 106.7670, "lat": 26.6170, "type": "市辖区", "parent": "贵阳市"},
    "清镇市": {"name": "清镇市", "province": "贵州省", "lng": 106.4830, "lat": 26.5670, "type": "县级市", "parent": "贵阳市"},
    "修文县": {"name": "修文县", "province": "贵州省", "lng": 106.5670, "lat": 26.8170, "type": "县", "parent": "贵阳市"},
    "息烽县": {"name": "息烽县", "province": "贵州省", "lng": 106.7170, "lat": 27.1170, "type": "县", "parent": "贵阳市"},
    "开阳县": {"name": "开阳县", "province": "贵州省", "lng": 106.9170, "lat": 27.0830, "type": "县", "parent": "贵阳市"},
    "六盘水市": {"name": "六盘水市", "province": "贵州省", "lng": 104.8330, "lat": 26.5830, "type": "地级市", "parent": "贵州省"},
    "钟山区": {"name": "钟山区", "province": "贵州省", "lng": 104.8330, "lat": 26.5830, "type": "市辖区", "parent": "六盘水市"},
    "六枝特区": {"name": "六枝特区", "province": "贵州省", "lng": 105.4670, "lat": 26.2170, "type": "特区", "parent": "六盘水市"},
    "水城区": {"name": "水城区", "province": "贵州省", "lng": 104.8170, "lat": 26.5170, "type": "市辖区", "parent": "六盘水市"},
    "盘州市": {"name": "盘州市", "province": "贵州省", "lng": 104.4670, "lat": 25.7830, "type": "县级市", "parent": "六盘水市"},
    "遵义市": {"name": "遵义市", "province": "贵州省", "lng": 106.9273, "lat": 27.7254, "type": "地级市", "parent": "贵州省"},
    "红花岗区": {"name": "红花岗区", "province": "贵州省", "lng": 106.9170, "lat": 27.7170, "type": "市辖区", "parent": "遵义市"},
    "汇川区": {"name": "汇川区", "province": "贵州省", "lng": 106.9170, "lat": 27.7500, "type": "市辖区", "parent": "遵义市"},
    "播州区": {"name": "播州区", "province": "贵州省", "lng": 106.9170, "lat": 27.6170, "type": "市辖区", "parent": "遵义市"},
    "仁怀市": {"name": "仁怀市", "province": "贵州省", "lng": 106.4170, "lat": 27.8170, "type": "县级市", "parent": "遵义市"},
    "赤水市": {"name": "赤水市", "province": "贵州省", "lng": 105.7170, "lat": 28.5170, "type": "县级市", "parent": "遵义市"},
    "桐梓县": {"name": "桐梓县", "province": "贵州省", "lng": 106.8170, "lat": 28.1170, "type": "县", "parent": "遵义市"},
    "绥阳县": {"name": "绥阳县", "province": "贵州省", "lng": 107.0170, "lat": 27.9170, "type": "县", "parent": "遵义市"},
    "正安县": {"name": "正安县", "province": "贵州省", "lng": 107.4170, "lat": 28.5170, "type": "县", "parent": "遵义市"},
    "道真仡佬族苗族自治县": {"name": "道真仡佬族苗族自治县", "province": "贵州省", "lng": 107.6170, "lat": 28.8170, "type": "自治县", "parent": "遵义市"},
    "务川仡佬族苗族自治县": {"name": "务川仡佬族苗族自治县", "province": "贵州省", "lng": 107.9170, "lat": 27.8830, "type": "自治县", "parent": "遵义市"},
    "凤冈县": {"name": "凤冈县", "province": "贵州省", "lng": 107.7170, "lat": 27.9170, "type": "县", "parent": "遵义市"},
    "湄潭县": {"name": "湄潭县", "province": "贵州省", "lng": 107.4670, "lat": 27.7670, "type": "县", "parent": "遵义市"},
    "余庆县": {"name": "余庆县", "province": "贵州省", "lng": 107.8830, "lat": 27.2170, "type": "县", "parent": "遵义市"},
    "习水县": {"name": "习水县", "province": "贵州省", "lng": 106.2170, "lat": 28.3170, "type": "县", "parent": "遵义市"},
    "西秀区": {"name": "西秀区", "province": "贵州省", "lng": 105.9330, "lat": 26.2500, "type": "市辖区", "parent": "安顺市"},
    "平坝区": {"name": "平坝区", "province": "贵州省", "lng": 106.2500, "lat": 26.4170, "type": "市辖区", "parent": "安顺市"},
    "普定县": {"name": "普定县", "province": "贵州省", "lng": 105.7500, "lat": 26.3170, "type": "县", "parent": "安顺市"},
    "镇宁布依族苗族自治县": {"name": "镇宁布依族苗族自治县", "province": "贵州省", "lng": 105.7500, "lat": 25.9170, "type": "自治县", "parent": "安顺市"},
    "关岭布依族苗族自治县": {"name": "关岭布依族苗族自治县", "province": "贵州省", "lng": 105.6170, "lat": 25.9500, "type": "自治县", "parent": "安顺市"},
    "紫云苗族布依族自治县": {"name": "紫云苗族布依族自治县", "province": "贵州省", "lng": 106.0670, "lat": 25.7670, "type": "自治县", "parent": "安顺市"},
}

from app.services.real_city_data import REAL_CITY_DATA

existing_keys = set(REAL_CITY_DATA.keys())
new_keys = set(MISSING_DATA.keys())

duplicates = existing_keys & new_keys
if duplicates:
    print(f"发现 {len(duplicates)} 个重复键，正在跳过...")
    for key in duplicates:
        del MISSING_DATA[key]

REAL_CITY_DATA.update(MISSING_DATA)

provinces = {}
for name, data in REAL_CITY_DATA.items():
    province = data.get('province', '未知')
    if province not in provinces:
        provinces[province] = 0
    provinces[province] += 1

print(f"\n合并后数据统计：")
print(f"总数据量: {len(REAL_CITY_DATA)}")
print(f"省份数量: {len(provinces)}")
print(f"\n各省份数据分布：")
for prov, count in sorted(provinces.items()):
    print(f"  {prov}: {count}个")
