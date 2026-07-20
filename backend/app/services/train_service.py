import httpx
from app.config import get_settings

settings = get_settings()

JUHE_TRAIN_URL = "https://apis.juhe.cn/fapigw/train/query"

async def search_trains(from_station: str, to_station: str, date: str, is_high: bool = True):
    params = {
        "key": settings.JUHE_API_KEY,
        "search_type": "1",
        "departure_station": from_station,
        "arrival_station": to_station,
        "date": date,
        "filter": "G,D,C" if is_high else "",
    }
    
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(JUHE_TRAIN_URL, params=params)
        data = resp.json()
        
        if data.get("error_code") != 0:
            return {"success": False, "message": data.get("reason", "查询失败")}
        
        trains = []
        for item in data.get("result", []):
            train_no = item.get("train_no", "")
            is_high_train = train_no.startswith("G") or train_no.startswith("D") or train_no.startswith("C")
            
            prices_raw = item.get("prices", [])
            prices = {}
            availability = {}
            for p in prices_raw:
                seat_type = p.get("seat_type_code", "")
                seat_name = p.get("seat_name", "")
                price = p.get("price")
                num = p.get("num", "无")
                prices[seat_type] = price
                availability[seat_type] = num
            
            trains.append({
                "train_no": train_no,
                "type": "高铁" if train_no.startswith("G") else "动车" if train_no.startswith("D") else "城际" if train_no.startswith("C") else "普通",
                "from": item.get("departure_station", ""),
                "to": item.get("arrival_station", ""),
                "departure_time": item.get("departure_time", ""),
                "arrival_time": item.get("arrival_time", ""),
                "duration": item.get("duration", ""),
                "is_high": is_high_train,
                "enable_booking": item.get("enable_booking", ""),
                "flags": item.get("train_flags", []),
                "prices": {
                    "business_seat": prices.get("9"),
                    "first_seat": prices.get("M") or prices.get("3"),
                    "second_seat": prices.get("O") or prices.get("4"),
                    "no_seat": prices.get("1"),
                    "soft_sleeper": prices.get("2"),
                    "hard_sleeper": prices.get("5"),
                    "hard_seat": prices.get("6"),
                },
                "availability": {
                    "business_seat": availability.get("9", "无"),
                    "first_seat": availability.get("M") or availability.get("3", "无"),
                    "second_seat": availability.get("O") or availability.get("4", "无"),
                    "no_seat": availability.get("1", "无"),
                    "soft_sleeper": availability.get("2", "无"),
                    "hard_sleeper": availability.get("5", "无"),
                    "hard_seat": availability.get("6", "无"),
                },
            })
        
        return {"success": True, "trains": trains, "total": len(trains)}
