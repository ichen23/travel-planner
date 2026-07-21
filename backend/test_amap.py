"""
测试高德地图API集成
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_amap_integration():
    print("=" * 60)
    print("测试高德地图API集成")
    print("=" * 60)
    
    # 测试1: 检查AMAP_KEY
    print("\n1. 检查AMAP_KEY配置...")
    from dotenv import load_dotenv
    load_dotenv()
    amap_key = os.environ.get('AMAP_KEY', '')
    if amap_key:
        print(f"   ✓ AMAP_KEY已配置 (长度: {len(amap_key)})")
    else:
        print("   ✗ AMAP_KEY未配置")
        return
    
    # 测试2: 测试获取单个城市的真实数据
    print("\n2. 测试获取真实POI数据...")
    from app.services.multi_city_service import fetch_city_real_data
    
    test_cities = ["北京", "开封", "洛阳", "焦作"]
    
    for city in test_cities:
        print(f"\n   测试 {city}...")
        try:
            data = await fetch_city_real_data(city)
            if data:
                attractions = data.get('attractions', [])
                foods = data.get('food', [])
                print(f"   ✓ {city}: {len(attractions)}个景点, {len(foods)}个美食")
                if attractions:
                    print(f"     第一个景点: {attractions[0].get('name', '未知')}")
            else:
                print(f"   ✗ {city}: 未获取到数据")
        except Exception as e:
            print(f"   ✗ {city}: 出错 - {str(e)}")
    
    # 测试3: 测试生成行程
    print("\n3. 测试生成多城市行程...")
    from app.services.multi_city_service import generate_multi_city_itinerary
    
    try:
        result = await generate_multi_city_itinerary(
            cities=["开封", "洛阳", "焦作"],
            day_allocation=[2, 2, 1],
            total_days=5,
            budget=5000
        )
        
        if result.get('success'):
            days = result.get('days', [])
            print(f"   ✓ 行程生成成功! 共{len(days)}天")
            for day in days[:2]:
                print(f"     第{day['day']}天 ({day['city']}): {len(day['schedule'])}个活动")
        else:
            print(f"   ✗ 行程生成失败: {result.get('message')}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"   ✗ 行程生成出错: {str(e)}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_amap_integration())
