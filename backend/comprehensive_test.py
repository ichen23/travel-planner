import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("全功能测试脚本")
print("=" * 60)

errors = []

def test(name, func):
    try:
        func()
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {str(e)}")
        errors.append((name, str(e)))

print("\n1. 测试城市数据加载...")
try:
    from app.services.real_city_data import REAL_CITY_DATA
    print(f"   - 已加载 {len(REAL_CITY_DATA)} 个城市")
    
    provinces = set()
    for data in REAL_CITY_DATA.values():
        provinces.add(data.get('province', ''))
    print(f"   - 覆盖 {len(provinces)} 个省级行政区")
    
    expected_provinces = [
        '北京市', '天津市', '上海市', '重庆市',
        '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省',
        '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
        '河南省', '湖北省', '湖南省', '广东省', '海南省',
        '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省',
        '台湾省', '内蒙古自治区', '广西壮族自治区', '西藏自治区',
        '宁夏回族自治区', '新疆维吾尔自治区',
        '香港特别行政区', '澳门特别行政区'
    ]
    
    missing = [p for p in expected_provinces if p not in provinces]
    if missing:
        print(f"   ⚠ 缺失省份: {missing}")
        errors.append(("省份覆盖", f"缺失: {missing}"))
    else:
        print(f"   ✓ 已覆盖所有34个省级行政区")
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("城市数据加载", str(e)))

print("\n2. 测试城市搜索功能...")
try:
    from app.services.city_database import search_cities
    
    test_cases = [
        ("北京", 5),
        ("上海", 5),
        ("拉萨", 5),
        ("乌鲁木齐", 5),
        ("香港", 5),
        ("台北", 5),
        ("丽江", 5),
        ("九寨沟", 5),
    ]
    
    for keyword, limit in test_cases:
        results = search_cities(keyword, limit)
        if len(results) > 0:
            print(f"   ✓ 搜索'{keyword}': 找到 {len(results)} 个结果")
        else:
            print(f"   ⚠ 搜索'{keyword}': 未找到结果")
            errors.append(("城市搜索", f"'{keyword}'未找到结果"))
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("城市搜索", str(e)))

print("\n3. 测试AI生成功能...")
try:
    import asyncio
    from app.services.ai_generator_service import (
        get_available_templates, 
        generate_content,
        generate_random_blind_box,
        generate_recommendations
    )
    
    templates = get_available_templates()
    print(f"   ✓ 可用模板: {len(templates)} 种")
    for t in templates:
        print(f"     - {t['name']}")
    
    async def test_ai():
        context = {"title": "故宫", "city": "北京", "type": "古建筑", "days": 2}
        result = await generate_content("poetic", context)
        if result.get("success"):
            print(f"   ✓ AI内容生成成功: {result['data']['title']}")
        else:
            print(f"   ⚠ AI内容生成失败: {result.get('error')}")
        
        blind_box = await generate_random_blind_box()
        if blind_box:
            print(f"   ✓ 盲盒推荐: {blind_box.get('city', '未知')}")
        
        recs = await generate_recommendations("北京", 5)
        if recs:
            print(f"   ✓ 推荐生成: {len(recs)} 个推荐")
    
    asyncio.run(test_ai())
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("AI生成", str(e)))

print("\n4. 测试坐标数据...")
try:
    from app.services.city_database import REAL_CITY_COORDS
    
    test_cities = ["北京市", "上海市", "广州市", "深圳市", "拉萨市", "乌鲁木齐市", "香港", "台北市"]
    for city in test_cities:
        coords = REAL_CITY_COORDS.get(city)
        if coords:
            print(f"   ✓ {city}: {coords}")
        else:
            print(f"   ⚠ {city}: 无坐标数据")
            errors.append(("坐标数据", f"{city}无坐标"))
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("坐标数据", str(e)))

print("\n5. 测试POI数据...")
try:
    from app.services.poi_tips import POI_TIPS
    
    test_pois = ["B000A1V61H", "B000A1V61G", "B0FFF0M5Y6"]
    for poi_id in test_pois:
        poi = POI_TIPS.get(poi_id)
        if poi:
            print(f"   ✓ {poi['name']}: {poi['city']}")
        else:
            print(f"   ⚠ {poi_id}: 未找到")
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("POI数据", str(e)))

print("\n6. 测试天气服务...")
try:
    import asyncio
    from app.services.amap_service import get_city_adcode
    
    async def test_weather():
        adcode = await get_city_adcode("北京")
        if adcode:
            print(f"   ✓ 北京adcode: {adcode}")
        else:
            print(f"   ⚠ 北京adcode获取失败")
    
    asyncio.run(test_weather())
except Exception as e:
    print(f"   ⚠ 天气服务测试跳过: {str(e)} (可能未配置API Key)")

print("\n7. 检查数据完整性...")
try:
    from app.services.real_city_data import REAL_CITY_DATA
    
    invalid_entries = []
    for name, data in REAL_CITY_DATA.items():
        if not data.get('province'):
            invalid_entries.append((name, '缺少省份'))
        if not data.get('lng') or not data.get('lat'):
            invalid_entries.append((name, '缺少坐标'))
    
    if invalid_entries:
        print(f"   ⚠ 发现 {len(invalid_entries)} 个无效条目")
        for name, issue in invalid_entries[:5]:
            print(f"     - {name}: {issue}")
    else:
        print(f"   ✓ 所有条目数据完整")
    
    duplicate_names = []
    all_names = list(REAL_CITY_DATA.keys())
    if len(all_names) != len(set(all_names)):
        print(f"   ⚠ 发现重复名称")
    else:
        print(f"   ✓ 无重复名称")
except Exception as e:
    print(f"   ✗ 测试失败: {str(e)}")
    errors.append(("数据完整性", str(e)))

print("\n" + "=" * 60)
print("测试结果汇总")
print("=" * 60)
print(f"\n总测试项: 7")
print(f"错误数: {len(errors)}")

if errors:
    print("\n错误详情:")
    for name, err in errors:
        print(f"  - {name}: {err}")
else:
    print("\n✓ 所有测试通过!")

print("\n数据统计:")
print(f"  - 城市总数: {len(REAL_CITY_DATA)}")
print(f"  - 省级行政区: {len(provinces)}")
print(f"  - POI景点: {len(POI_TIPS)}")
print(f"  - AI模板: {len(templates)}")
