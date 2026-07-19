from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/planner", tags=["行程规划"])

class BudgetRequest(BaseModel):
    transport: float = 0
    accommodation_nights: int = 2
    hotel_price: float = 300
    meals_per_day: float = 100
    days: int = 3
    tickets: float = 100
    transport_local: float = 150

@router.post("/budget", summary="计算预算")
async def calculate_budget(req: BudgetRequest):
    total_hotel = req.accommodation_nights * req.hotel_price
    total_meals = req.days * req.meals_per_day
    grand_total = req.transport * 2 + total_hotel + total_meals + req.tickets + req.transport_local
    
    return {
        "success": True,
        "breakdown": {
            "transport_round": round(req.transport * 2, 2),
            "hotel": round(total_hotel, 2),
            "meals": round(total_meals, 2),
            "tickets": round(req.tickets, 2),
            "local_transport": round(req.transport_local, 2),
        },
        "total": round(grand_total, 2),
        "per_person_day": round(grand_total / req.days, 2),
    }
