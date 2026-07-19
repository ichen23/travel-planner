from fastapi import APIRouter, Query
from app.services.train_service import search_trains

router = APIRouter(prefix="/train", tags=["火车票查询"])

@router.get("/search", summary="查询火车票")
async def get_trains(
    from_station: str = Query(..., description="出发站名"),
    to_station: str = Query(..., description="到达站名"),
    date: str = Query(..., description="出发日期 YYYY-MM-DD"),
    is_high_speed: bool = Query(True, description="是否只查高铁/动车")
):
    result = await search_trains(from_station, to_station, date, is_high_speed)
    return result
