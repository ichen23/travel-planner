from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import os

router = APIRouter(prefix="/favorites", tags=["收藏"])

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_FILE = os.path.join(DB_DIR, "favorites.json")

def ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"trains": [], "planners": []}, f, ensure_ascii=False, indent=2)

def read_db():
    ensure_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class TrainFavorite(BaseModel):
    data: Dict[str, Any]

class PlannerFavorite(BaseModel):
    data: Dict[str, Any]

@router.get("", summary="获取收藏列表")
async def get_favorites():
    data = read_db()
    return {"success": True, "favorites": data}

@router.post("/train", summary="收藏车票")
async def add_train_favorite(fav: TrainFavorite):
    data = read_db()
    data["trains"].append(fav.data)
    write_db(data)
    return {"success": True, "message": "收藏成功"}

@router.delete("/train/{index}", summary="删除车票收藏")
async def remove_train_favorite(index: int):
    data = read_db()
    if 0 <= index < len(data["trains"]):
        data["trains"].pop(index)
        write_db(data)
        return {"success": True, "message": "删除成功"}
    raise HTTPException(status_code=404, detail="收藏不存在")

@router.post("/planner", summary="保存行程")
async def add_planner_favorite(fav: PlannerFavorite):
    data = read_db()
    data["planners"].append(fav.data)
    write_db(data)
    return {"success": True, "message": "保存成功"}

@router.delete("/planner/{index}", summary="删除行程")
async def remove_planner_favorite(index: int):
    data = read_db()
    if 0 <= index < len(data["planners"]):
        data["planners"].pop(index)
        write_db(data)
        return {"success": True, "message": "删除成功"}
    raise HTTPException(status_code=404, detail="行程不存在")
