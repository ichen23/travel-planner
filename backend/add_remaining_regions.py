import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REMAINING_DATA = {
    "拉萨市": {"name": "拉萨市", "province": "西藏自治区", "lng": 91.1322, "lat": 29.6500, "type": "地级市", "parent": "西藏自治区"},
    "城关区": {"name": "城关区", "province": "西藏自治区", "lng": 91.1170, "lat": 29.6500, "type": "市辖区", "parent": "拉萨市"},
    "堆龙德庆区": {"name": "堆龙德庆区", "province": "西藏自治区", "lng": 90.9500, "lat": 29.6500, "type": "市辖区", "parent": "拉萨市"},
    "达孜区": {"name": "达孜区", "province": "西藏自治区", "lng": 91.3830, "lat": 29.6500, "type": "市辖区", "parent": "拉萨市"},
    "林周县": {"name": "林周县", "province": "西藏自治区", "lng": 91.2330, "lat": 29.9500, "type": "县", "parent": "拉萨市"},
    "当雄县": {"name": "当雄县", "province": "西藏自治区", "lng": 90.8000, "lat": 30.5000, "type": "县", "parent": "拉萨市"},
    "尼木县": {"name": "尼木县", "province": "西藏自治区", "lng": 90.1670, "lat": 29.5000, "type": "县", "parent": "拉萨市"},
    "曲水县": {"name": "曲水县", "province": "西藏自治区", "lng": 90.7670, "lat": 29.3830, "type": "县", "parent": "拉萨市"},
    "墨竹工卡县": {"name": "墨竹工卡县", "province": "西藏自治区", "lng": 91.6500, "lat": 29.7670, "type": "县", "parent": "拉萨市"},
    "日喀则市": {"name": "日喀则市", "province": "西藏自治区", "lng": 88.8809, "lat": 29.2671, "type": "地级市", "parent": "西藏自治区"},
    "桑珠孜区": {"name": "桑珠孜区", "province": "西藏自治区", "lng": 88.8830, "lat": 29.2670, "type": "市辖区", "parent": "日喀则市"},
    "南木林县": {"name": "南木林县", "province": "西藏自治区", "lng": 89.0500, "lat": 29.1670, "type": "县", "parent": "日喀则市"},
    "江孜县": {"name": "江孜县", "province": "西藏自治区", "lng": 89.6330, "lat": 28.9170, "type": "县", "parent": "日喀则市"},
    "定日县": {"name": "定日县", "province": "西藏自治区", "lng": 87.4500, "lat": 28.6170, "type": "县", "parent": "日喀则市"},
    "萨迦县": {"name": "萨迦县", "province": "西藏自治区", "lng": 88.0500, "lat": 28.9170, "type": "县", "parent": "日喀则市"},
    "拉孜县": {"name": "拉孜县", "province": "西藏自治区", "lng": 88.0500, "lat": 29.1670, "type": "县", "parent": "日喀则市"},
    "昂仁县": {"name": "昂仁县", "province": "西藏自治区", "lng": 87.2500, "lat": 29.5000, "type": "县", "parent": "日喀则市"},
    "谢通门县": {"name": "谢通门县", "province": "西藏自治区", "lng": 88.2500, "lat": 29.5000, "type": "县", "parent": "日喀则市"},
    "白朗县": {"name": "白朗县", "province": "西藏自治区", "lng": 89.2500, "lat": 29.1670, "type": "县", "parent": "日喀则市"},
    "仁布县": {"name": "仁布县", "province": "西藏自治区", "lng": 89.8330, "lat": 29.1670, "type": "县", "parent": "日喀则市"},
    "康马县": {"name": "康马县", "province": "西藏自治区", "lng": 89.6670, "lat": 28.5000, "type": "县", "parent": "日喀则市"},
    "定结县": {"name": "定结县", "province": "西藏自治区", "lng": 88.1670, "lat": 28.3330, "type": "县", "parent": "日喀则市"},
    "仲巴县": {"name": "仲巴县", "province": "西藏自治区", "lng": 84.1670, "lat": 29.6670, "type": "县", "parent": "日喀则市"},
    "吉隆县": {"name": "吉隆县", "province": "西藏自治区", "lng": 85.3000, "lat": 28.8500, "type": "县", "parent": "日喀则市"},
    "聂拉木县": {"name": "聂拉木县", "province": "西藏自治区", "lng": 85.9000, "lat": 28.1670, "type": "县", "parent": "日喀则市"},
    "萨嘎县": {"name": "萨嘎县", "province": "西藏自治区", "lng": 84.0500, "lat": 29.3330, "type": "县", "parent": "日喀则市"},
    "岗巴县": {"name": "岗巴县", "province": "西藏自治区", "lng": 88.5000, "lat": 28.3000, "type": "县", "parent": "日喀则市"},
    "昌都市": {"name": "昌都市", "province": "西藏自治区", "lng": 97.1787, "lat": 31.1369, "type": "地级市", "parent": "西藏自治区"},
    "卡若区": {"name": "卡若区", "province": "西藏自治区", "lng": 97.1830, "lat": 31.1500, "type": "市辖区", "parent": "昌都市"},
    "江达县": {"name": "江达县", "province": "西藏自治区", "lng": 98.2000, "lat": 31.5000, "type": "县", "parent": "昌都市"},
    "贡觉县": {"name": "贡觉县", "province": "西藏自治区", "lng": 98.2500, "lat": 30.8670, "type": "县", "parent": "昌都市"},
    "类乌齐县": {"name": "类乌齐县", "province": "西藏自治区", "lng": 96.7000, "lat": 31.2500, "type": "县", "parent": "昌都市"},
    "丁青县": {"name": "丁青县", "province": "西藏自治区", "lng": 95.5830, "lat": 31.4170, "type": "县", "parent": "昌都市"},
    "察雅县": {"name": "察雅县", "province": "西藏自治区", "lng": 97.5830, "lat": 30.6500, "type": "县", "parent": "昌都市"},
    "八宿县": {"name": "八宿县", "province": "西藏自治区", "lng": 97.1670, "lat": 30.0330, "type": "县", "parent": "昌都市"},
    "左贡县": {"name": "左贡县", "province": "西藏自治区", "lng": 97.9000, "lat": 29.6500, "type": "县", "parent": "昌都市"},
    "芒康县": {"name": "芒康县", "province": "西藏自治区", "lng": 98.6830, "lat": 29.6330, "type": "县", "parent": "昌都市"},
    "洛隆县": {"name": "洛隆县", "province": "西藏自治区", "lng": 95.8330, "lat": 30.7500, "type": "县", "parent": "昌都市"},
    "边坝县": {"name": "边坝县", "province": "西藏自治区", "lng": 94.6830, "lat": 31.0170, "type": "县", "parent": "昌都市"},
    "林芝市": {"name": "林芝市", "province": "西藏自治区", "lng": 94.3624, "lat": 29.6486, "type": "地级市", "parent": "西藏自治区"},
    "巴宜区": {"name": "巴宜区", "province": "西藏自治区", "lng": 94.3670, "lat": 29.6500, "type": "市辖区", "parent": "林芝市"},
    "工布江达县": {"name": "工布江达县", "province": "西藏自治区", "lng": 93.8500, "lat": 29.9000, "type": "县", "parent": "林芝市"},
    "米林县": {"name": "米林县", "province": "西藏自治区", "lng": 94.2170, "lat": 29.2000, "type": "县", "parent": "林芝市"},
    "墨脱县": {"name": "墨脱县", "province": "西藏自治区", "lng": 95.3330, "lat": 29.3330, "type": "县", "parent": "林芝市"},
    "波密县": {"name": "波密县", "province": "西藏自治区", "lng": 95.7670, "lat": 29.8670, "type": "县", "parent": "林芝市"},
    "察隅县": {"name": "察隅县", "province": "西藏自治区", "lng": 97.4830, "lat": 28.6500, "type": "县", "parent": "林芝市"},
    "朗县": {"name": "朗县", "province": "西藏自治区", "lng": 93.0670, "lat": 29.0500, "type": "县", "parent": "林芝市"},
    "山南市": {"name": "山南市", "province": "西藏自治区", "lng": 91.7730, "lat": 29.2360, "type": "地级市", "parent": "西藏自治区"},
    "乃东区": {"name": "乃东区", "province": "西藏自治区", "lng": 91.7670, "lat": 29.2500, "type": "市辖区", "parent": "山南市"},
    "扎囊县": {"name": "扎囊县", "province": "西藏自治区", "lng": 91.6170, "lat": 29.2330, "type": "县", "parent": "山南市"},
    "贡嘎县": {"name": "贡嘎县", "province": "西藏自治区", "lng": 91.0170, "lat": 29.2670, "type": "县", "parent": "山南市"},
    "桑日县": {"name": "桑日县", "province": "西藏自治区", "lng": 91.8500, "lat": 29.2670, "type": "县", "parent": "山南市"},
    "琼结县": {"name": "琼结县", "province": "西藏自治区", "lng": 91.6830, "lat": 29.0330, "type": "县", "parent": "山南市"},
    "曲松县": {"name": "曲松县", "province": "西藏自治区", "lng": 92.0000, "lat": 29.0500, "type": "县", "parent": "山南市"},
    "措美县": {"name": "措美县", "province": "西藏自治区", "lng": 91.4170, "lat": 28.5000, "type": "县", "parent": "山南市"},
    "洛扎县": {"name": "洛扎县", "province": "西藏自治区", "lng": 90.8500, "lat": 28.4170, "type": "县", "parent": "山南市"},
    "加查县": {"name": "加查县", "province": "西藏自治区", "lng": 92.6170, "lat": 29.1500, "type": "县", "parent": "山南市"},
    "隆子县": {"name": "隆子县", "province": "西藏自治区", "lng": 92.3170, "lat": 28.4500, "type": "县", "parent": "山南市"},
    "错那县": {"name": "错那县", "province": "西藏自治区", "lng": 91.9500, "lat": 27.9830, "type": "县", "parent": "山南市"},
    "浪卡子县": {"name": "浪卡子县", "province": "西藏自治区", "lng": 90.4170, "lat": 29.0170, "type": "县", "parent": "山南市"},
    "那曲市": {"name": "那曲市", "province": "西藏自治区", "lng": 92.0580, "lat": 31.4760, "type": "地级市", "parent": "西藏自治区"},
    "色尼区": {"name": "色尼区", "province": "西藏自治区", "lng": 92.0500, "lat": 31.4670, "type": "市辖区", "parent": "那曲市"},
    "嘉黎县": {"name": "嘉黎县", "province": "西藏自治区", "lng": 93.2830, "lat": 30.6500, "type": "县", "parent": "那曲市"},
    "比如县": {"name": "比如县", "province": "西藏自治区", "lng": 93.2830, "lat": 31.4670, "type": "县", "parent": "那曲市"},
    "聂荣县": {"name": "聂荣县", "province": "西藏自治区", "lng": 92.3000, "lat": 32.1170, "type": "县", "parent": "那曲市"},
    "安多县": {"name": "安多县", "province": "西藏自治区", "lng": 91.6170, "lat": 32.2830, "type": "县", "parent": "那曲市"},
    "申扎县": {"name": "申扎县", "province": "西藏自治区", "lng": 88.7500, "lat": 30.9500, "type": "县", "parent": "那曲市"},
    "索县": {"name": "索县", "province": "西藏自治区", "lng": 93.7670, "lat": 31.9000, "type": "县", "parent": "那曲市"},
    "班戈县": {"name": "班戈县", "province": "西藏自治区", "lng": 90.0500, "lat": 31.3500, "type": "县", "parent": "那曲市"},
    "巴青县": {"name": "巴青县", "province": "西藏自治区", "lng": 94.0000, "lat": 31.9170, "type": "县", "parent": "那曲市"},
    "尼玛县": {"name": "尼玛县", "province": "西藏自治区", "lng": 87.6170, "lat": 31.0170, "type": "县", "parent": "那曲市"},
    "双湖县": {"name": "双湖县", "province": "西藏自治区", "lng": 88.7500, "lat": 33.3500, "type": "县", "parent": "那曲市"},
    "狮泉河镇": {"name": "狮泉河镇", "province": "西藏自治区", "lng": 80.1050, "lat": 32.5010, "type": "地级市", "parent": "西藏自治区"},
    "普兰县": {"name": "普兰县", "province": "西藏自治区", "lng": 81.2500, "lat": 30.2830, "type": "县", "parent": "阿里地区"},
    "札达县": {"name": "札达县", "province": "西藏自治区", "lng": 79.7170, "lat": 31.5170, "type": "县", "parent": "阿里地区"},
    "噶尔县": {"name": "噶尔县", "province": "西藏自治区", "lng": 80.1170, "lat": 32.5000, "type": "县", "parent": "阿里地区"},
    "日土县": {"name": "日土县", "province": "西藏自治区", "lng": 79.6670, "lat": 32.3330, "type": "县", "parent": "阿里地区"},
    "革吉县": {"name": "革吉县", "province": "西藏自治区", "lng": 81.9170, "lat": 32.9170, "type": "县", "parent": "阿里地区"},
    "改则县": {"name": "改则县", "province": "西藏自治区", "lng": 84.2670, "lat": 32.0830, "type": "县", "parent": "阿里地区"},
    "措勤县": {"name": "措勤县", "province": "西藏自治区", "lng": 85.1670, "lat": 31.6500, "type": "县", "parent": "阿里地区"},
    
    # 新疆主要城市
    "乌鲁木齐市": {"name": "乌鲁木齐市", "province": "新疆维吾尔自治区", "lng": 87.6168, "lat": 43.8256, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "克拉玛依市": {"name": "克拉玛依市", "province": "新疆维吾尔自治区", "lng": 84.8745, "lat": 45.5950, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "吐鲁番市": {"name": "吐鲁番市", "province": "新疆维吾尔自治区", "lng": 89.1895, "lat": 42.9513, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "哈密市": {"name": "哈密市", "province": "新疆维吾尔自治区", "lng": 93.5149, "lat": 42.8332, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "昌吉市": {"name": "昌吉市", "province": "新疆维吾尔自治区", "lng": 87.3064, "lat": 44.0110, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "博乐市": {"name": "博乐市", "province": "新疆维吾尔自治区", "lng": 82.0720, "lat": 44.9030, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "库尔勒市": {"name": "库尔勒市", "province": "新疆维吾尔自治区", "lng": 86.1470, "lat": 41.7600, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "阿克苏市": {"name": "阿克苏市", "province": "新疆维吾尔自治区", "lng": 80.2610, "lat": 41.1670, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "喀什市": {"name": "喀什市", "province": "新疆维吾尔自治区", "lng": 75.9891, "lat": 39.4670, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "和田市": {"name": "和田市", "province": "新疆维吾尔自治区", "lng": 79.9264, "lat": 37.1104, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "伊宁市": {"name": "伊宁市", "province": "新疆维吾尔自治区", "lng": 81.3330, "lat": 43.9170, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "阿勒泰市": {"name": "阿勒泰市", "province": "新疆维吾尔自治区", "lng": 88.1330, "lat": 47.8500, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "塔城市": {"name": "塔城市", "province": "新疆维吾尔自治区", "lng": 82.9830, "lat": 46.7500, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "阿图什市": {"name": "阿图什市", "province": "新疆维吾尔自治区", "lng": 76.9670, "lat": 39.7170, "type": "地级市", "parent": "新疆维吾尔自治区"},
    "阜康市": {"name": "阜康市", "province": "新疆维吾尔自治区", "lng": 87.9670, "lat": 44.1670, "type": "县级市", "parent": "昌吉回族自治州"},
    "米泉市": {"name": "米泉市", "province": "新疆维吾尔自治区", "lng": 87.6500, "lat": 43.9500, "type": "县级市", "parent": "昌吉回族自治州"},
    "奎屯市": {"name": "奎屯市", "province": "新疆维吾尔自治区", "lng": 84.8830, "lat": 44.4170, "type": "县级市", "parent": "伊犁哈萨克自治州"},
    "乌苏市": {"name": "乌苏市", "province": "新疆维吾尔自治区", "lng": 84.6830, "lat": 44.4170, "type": "县级市", "parent": "塔城地区"},
    "石河子市": {"name": "石河子市", "province": "新疆维吾尔自治区", "lng": 86.0170, "lat": 44.3170, "type": "县级市", "parent": "昌吉回族自治州"},
    "阿拉尔市": {"name": "阿拉尔市", "province": "新疆维吾尔自治区", "lng": 81.2670, "lat": 40.7170, "type": "县级市", "parent": "阿克苏地区"},
    "图木舒克市": {"name": "图木舒克市", "province": "新疆维吾尔自治区", "lng": 79.0670, "lat": 39.8170, "type": "县级市", "parent": "喀什地区"},
    "五家渠市": {"name": "五家渠市", "province": "新疆维吾尔自治区", "lng": 87.5170, "lat": 44.3170, "type": "县级市", "parent": "昌吉回族自治州"},
    "北屯市": {"name": "北屯市", "province": "新疆维吾尔自治区", "lng": 87.8170, "lat": 47.3170, "type": "县级市", "parent": "阿勒泰地区"},
    "铁门关市": {"name": "铁门关市", "province": "新疆维吾尔自治区", "lng": 86.3170, "lat": 41.7170, "type": "县级市", "parent": "巴音郭楞蒙古自治州"},
    "双河市": {"name": "双河市", "province": "新疆维吾尔自治区", "lng": 82.3170, "lat": 44.8170, "type": "县级市", "parent": "博尔塔拉蒙古自治州"},
    "可克达拉市": {"name": "可克达拉市", "province": "新疆维吾尔自治区", "lng": 81.0170, "lat": 43.9170, "type": "县级市", "parent": "伊犁哈萨克自治州"},
    "昆玉市": {"name": "昆玉市", "province": "新疆维吾尔自治区", "lng": 79.2670, "lat": 37.2170, "type": "县级市", "parent": "和田地区"},
    "胡杨河市": {"name": "胡杨河市", "province": "新疆维吾尔自治区", "lng": 84.7170, "lat": 44.7170, "type": "县级市", "parent": "塔城地区"},
    "新星市": {"name": "新星市", "province": "新疆维吾尔自治区", "lng": 93.5170, "lat": 42.8170, "type": "县级市", "parent": "哈密市"},
    "库尔勒市": {"name": "库尔勒市", "province": "新疆维吾尔自治区", "lng": 86.1470, "lat": 41.7600, "type": "县级市", "parent": "巴音郭楞蒙古自治州"},
    "伊宁市": {"name": "伊宁市", "province": "新疆维吾尔自治区", "lng": 81.3330, "lat": 43.9170, "type": "县级市", "parent": "伊犁哈萨克自治州"},
    "喀什市": {"name": "喀什市", "province": "新疆维吾尔自治区", "lng": 75.9891, "lat": 39.4670, "type": "县级市", "parent": "喀什地区"},
    "阿克苏市": {"name": "阿克苏市", "province": "新疆维吾尔自治区", "lng": 80.2610, "lat": 41.1670, "type": "县级市", "parent": "阿克苏地区"},
    "和田市": {"name": "和田市", "province": "新疆维吾尔自治区", "lng": 79.9264, "lat": 37.1104, "type": "县级市", "parent": "和田地区"},
    "吐鲁番市": {"name": "吐鲁番市", "province": "新疆维吾尔自治区", "lng": 89.1895, "lat": 42.9513, "type": "县级市", "parent": "吐鲁番地区"},
    "哈密市": {"name": "哈密市", "province": "新疆维吾尔自治区", "lng": 93.5149, "lat": 42.8332, "type": "县级市", "parent": "哈密地区"},
    "克拉玛依市": {"name": "克拉玛依市", "province": "新疆维吾尔自治区", "lng": 84.8745, "lat": 45.5950, "type": "县级市", "parent": "克拉玛依地区"},
    "乌鲁木齐市": {"name": "乌鲁木齐市", "province": "新疆维吾尔自治区", "lng": 87.6168, "lat": 43.8256, "type": "县级市", "parent": "乌鲁木齐地区"},
}

from app.services.real_city_data import REAL_CITY_DATA

existing_keys = set(REAL_CITY_DATA.keys())
new_keys = set(REMAINING_DATA.keys())

duplicates = existing_keys & new_keys
if duplicates:
    print(f"发现 {len(duplicates)} 个重复键，正在跳过...")
    for key in duplicates:
        del REMAINING_DATA[key]

REAL_CITY_DATA.update(REMAINING_DATA)

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
