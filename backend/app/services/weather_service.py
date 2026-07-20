import httpx
import logging
from datetime import datetime, timedelta
from app.config import get_settings

logger = logging.getLogger(__name__)

AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"


async def get_city_adcode(city_name: str) -> str:
    settings = get_settings()
    if not settings.AMAP_KEY:
        logger.error("AMAP_KEY is not configured")
        return ""
    
    params = {
        "key": settings.AMAP_KEY,
        "address": city_name,
        "output": "JSON",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(AMAP_GEOCODE_URL, params=params)
            data = resp.json()
            if data.get("status") == "1" and data.get("geocodes"):
                return data["geocodes"][0].get("adcode", "")
            else:
                logger.warning(f"Geocode failed for {city_name}: {data.get('info')}")
    except Exception as e:
        logger.error(f"Geocode request failed: {str(e)}")
    return ""


async def get_weather(city_adcode: str):
    settings = get_settings()
    if not settings.AMAP_KEY:
        logger.error("AMAP_KEY is not configured")
        return None
    
    params = {
        "key": settings.AMAP_KEY,
        "city": city_adcode,
        "extensions": "base",
        "output": "JSON",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(AMAP_WEATHER_URL, params=params)
            data = resp.json()
            if data.get("status") == "1" and data.get("lives"):
                live = data["lives"][0]
                return {
                    "city": live.get("city"),
                    "weather": live.get("weather"),
                    "temperature": live.get("temperature"),
                    "wind_direction": live.get("winddirection"),
                    "wind_power": live.get("windpower"),
                    "humidity": live.get("humidity"),
                    "report_time": live.get("reporttime"),
                }
            else:
                logger.warning(f"Weather request failed: {data.get('info')}")
    except Exception as e:
        logger.error(f"Weather request failed: {str(e)}")
    return None


async def get_weather_forecast(city_name: str):
    settings = get_settings()
    if not settings.AMAP_KEY:
        logger.error("AMAP_KEY is not configured")
        return None
    
    adcode = await get_city_adcode(city_name)
    if not adcode:
        return None
    
    current = await get_weather(adcode)
    
    params = {
        "key": settings.AMAP_KEY,
        "city": adcode,
        "extensions": "all",
        "output": "JSON",
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(AMAP_WEATHER_URL, params=params)
            data = resp.json()
        
        if data.get("status") == "1" and data.get("forecasts"):
            forecast = data["forecasts"][0]
            days = forecast.get("casts", [])
            
            weather_types = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "雷阵雨", "雪"]
            
            result_days = []
            for i, day in enumerate(days[:7]):
                item = {
                    "date": day.get("date"),
                    "weekday": _get_weekday(day.get("date")),
                    "day_weather": day.get("dayweather"),
                    "night_weather": day.get("nightweather"),
                    "day_temp": day.get("daytemp"),
                    "night_temp": day.get("nighttemp"),
                    "day_wind": day.get("daywind"),
                    "night_wind": day.get("nightwind"),
                    "comfort_index": _calculate_comfort(day),
                    "suggestion": _get_day_suggestion(day),
                }
                result_days.append(item)
            
            return {
                "city": forecast.get("city") or city_name,
                "report_time": forecast.get("reporttime"),
                "current": current,
                "forecast": result_days,
                "travel_advice": _generate_travel_advice(result_days),
                "clothing_suggestions": _generate_clothing_suggestions(result_days),
                "sun_protection": _check_sun_protection(result_days),
                "rain_alert": _check_rain_alert(result_days),
                "temperature_trend": _analyze_temperature_trend(result_days),
            }
        else:
            logger.warning(f"Weather forecast failed: {data.get('info')}")
            return None
    except Exception as e:
        logger.error(f"Weather forecast error: {str(e)}")
        return None


def _get_weekday(date_str: str) -> str:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
        return weekdays[date.weekday()]
    except:
        return ""


def _calculate_comfort(day_data: dict) -> dict:
    try:
        day_temp = float(day_data.get("daytemp", 25))
        night_temp = float(day_data.get("nighttemp", 15))
        avg_temp = (day_temp + night_temp) / 2
        
        if avg_temp <= 5:
            level = "very_cold"
            desc = "非常寒冷"
        elif avg_temp <= 10:
            level = "cold"
            desc = "寒冷"
        elif avg_temp <= 18:
            level = "cool"
            desc = "凉爽"
        elif avg_temp <= 25:
            level = "comfortable"
            desc = "舒适"
        elif avg_temp <= 30:
            level = "warm"
            desc = "温暖"
        elif avg_temp <= 35:
            level = "hot"
            desc = "炎热"
        else:
            level = "very_hot"
            desc = "酷热"
        
        return {"level": level, "description": desc, "avg_temp": round(avg_temp, 1)}
    except:
        return {"level": "unknown", "description": "未知", "avg_temp": 0}


def _get_day_suggestion(day_data: dict) -> list:
    suggestions = []
    weather = (day_data.get("dayweather", "") + day_data.get("nightweather", "")).lower()
    try:
        day_temp = float(day_data.get("daytemp", 25))
    except:
        day_temp = 25
    
    if "雨" in weather:
        suggestions.append("携带雨伞或雨衣")
        suggestions.append("穿着防滑鞋")
    if "雷" in weather:
        suggestions.append("避免在空旷地带活动")
        suggestions.append("关闭手机等电子设备")
    if "雪" in weather or day_temp <= 0:
        suggestions.append("穿着保暖羽绒服")
        suggestions.append("注意路面结冰")
    if day_temp >= 32:
        suggestions.append("避免正午户外活动")
        suggestions.append("大量补充水分")
        suggestions.append("注意防晒")
    if day_temp <= 5:
        suggestions.append("穿着厚外套")
        suggestions.append("戴上手套、围巾")
    if "晴" in weather and day_temp >= 25:
        suggestions.append("涂抹防晒霜")
        suggestions.append("佩戴太阳镜和遮阳帽")
    
    return suggestions


def _generate_travel_advice(days: list) -> dict:
    if not days:
        return {"general": [], "best_days": [], "avoid_days": []}
    
    best_days = []
    avoid_days = []
    general = []
    
    for day in days:
        weather = (day.get("dayweather", "") + day.get("nightweather", ""))
        try:
            temp = float(day.get("daytemp", 25))
        except:
            temp = 25
        
        is_good = True
        reasons = []
        
        if "雨" in weather or "雪" in weather:
            is_good = False
            reasons.append("有降水")
        if "雷" in weather:
            is_good = False
            reasons.append("有雷雨")
        if temp > 35:
            reasons.append("过于炎热")
        if temp < 0:
            reasons.append("过于寒冷")
        
        day_info = f"{day.get('date', '')}({day.get('weekday', '')}) {weather} {day.get('daytemp', '')}°"
        
        if is_good and ("晴" in weather or "多云" in weather):
            best_days.append(day_info)
        elif not is_good:
            avoid_days.append(day_info)
    
    if best_days:
        general.append(f"未来7天中有{len(best_days)}天适合户外活动")
    if avoid_days:
        general.append(f"建议避开{avoid_days[0][:10]}等天气不佳的日子")
    
    return {
        "general": general,
        "best_days": best_days[:3],
        "avoid_days": avoid_days[:3],
    }


def _generate_clothing_suggestions(days: list) -> dict:
    if not days:
        return {"daily": [], "essentials": [], "luggage_checklist": []}
    
    daily_suggestions = []
    all_temps = []
    
    for day in days[:7]:
        try:
            day_temp = float(day.get("daytemp", 25))
            night_temp = float(day.get("nighttemp", 15))
            all_temps.extend([day_temp, night_temp])
        except:
            continue
        
        weather = (day.get("dayweather", "") + day.get("nightweather", ""))
        date = day.get("date", "")
        
        if day_temp >= 30:
            clothing = "短袖T恤/衬衫 + 短裤/薄长裤 + 凉鞋"
        elif day_temp >= 22:
            clothing = "短袖 + 薄外套 + 长裤/七分裤"
        elif day_temp >= 15:
            clothing = "长袖 + 薄外套/卫衣 + 长裤"
        elif day_temp >= 8:
            clothing = "毛衣/卫衣 + 厚外套 + 长裤"
        elif day_temp >= 0:
            clothing = "保暖内衣 + 毛衣 + 羽绒服/棉服 + 长裤"
        else:
            clothing = "加厚保暖内衣 + 毛衣 + 厚羽绒服 + 秋裤"
        
        daily_suggestions.append({
            "date": date,
            "weekday": day.get("weekday", ""),
            "weather": weather[:2],
            "temperature": f"{day_temp}°/{night_temp}°",
            "clothing": clothing,
        })
    
    essentials = []
    if any(t >= 30 for t in all_temps):
        essentials.extend(["防晒霜(SPF50+)", "太阳镜", "遮阳帽", "清凉喷雾"])
    if any(t <= 5 for t in all_temps):
        essentials.extend(["保暖内衣", "羽绒服", "围巾", "手套", "暖宝宝"])
    if any("雨" in (d.get("dayweather", "") + d.get("nightweather", "")) for d in days):
        essentials.extend(["雨伞", "雨衣", "防水鞋套"])
    
    essentials.extend(["舒适的运动鞋", "便携充电宝", "常用药品"])
    
    return {
        "daily": daily_suggestions,
        "essentials": list(set(essentials)),
        "temperature_range": f"{min(all_temps) if all_temps else '?'}° ~ {max(all_temps) if all_temps else '?'}°",
    }


def _check_sun_protection(days: list) -> dict:
    sunny_days = []
    high_temp_days = []
    
    for day in days:
        weather = (day.get("dayweather", "") + day.get("nightweather", ""))
        try:
            temp = float(day.get("daytemp", 25))
        except:
            temp = 25
        
        if "晴" in weather and temp >= 25:
            sunny_days.append(f"{day.get('date', '')} 最高{temp}°")
        if temp >= 32:
            high_temp_days.append(f"{day.get('date', '')} {temp}°")
    
    return {
        "need_sun_protection": len(sunny_days) > 0,
        "sunny_days": sunny_days,
        "high_temp_days": high_temp_days,
        "tips": [
            "涂抹高倍数防晒霜(SPF50+, PA+++)",
            "每2-3小时补涂一次",
            "佩戴太阳镜和遮阳帽",
            "避免正午12-14点长时间户外活动",
        ] if sunny_days else [],
    }


def _check_rain_alert(days: list) -> dict:
    rainy_days = []
    storm_days = []
    
    for day in days:
        weather = (day.get("dayweather", "") + day.get("nightweather", ""))
        if "雨" in weather:
            rainy_days.append(f"{day.get('date', '')} {weather[:4]}")
        if "雷" in weather or "暴" in weather:
            storm_days.append(f"{day.get('date', '')} {weather[:4]}")
    
    return {
        "has_rain": len(rainy_days) > 0,
        "rainy_days": rainy_days,
        "storm_days": storm_days,
        "tips": [
            "随身携带折叠伞",
            "穿着防滑防水鞋",
            "雷雨天气避免使用手机",
            "注意行车安全",
        ] if rainy_days else ["未来7天无明显降水，出行条件良好"],
    }


def _analyze_temperature_trend(days: list) -> dict:
    if not days:
        return {"trend": "stable", "description": "数据不足"}
    
    temps = []
    for day in days:
        try:
            temps.append(float(day.get("daytemp", 25)))
        except:
            continue
    
    if len(temps) < 2:
        return {"trend": "stable", "description": "数据不足"}
    
    first_half = sum(temps[:3]) / min(3, len(temps))
    second_half = sum(temps[-3:]) / min(3, len(temps))
    
    diff = second_half - first_half
    
    if diff > 3:
        trend = "rising"
        desc = "气温逐渐升高"
    elif diff < -3:
        trend = "falling"
        desc = "气温逐渐下降"
    else:
        trend = "stable"
        desc = "气温相对稳定"
    
    return {
        "trend": trend,
        "description": desc,
        "max_temp": max(temps),
        "min_temp": min(temps),
        "avg_temp": round(sum(temps) / len(temps), 1),
        "daily_temps": [{"date": days[i].get("date"), "temp": t} for i, t in enumerate(temps)],
    }
