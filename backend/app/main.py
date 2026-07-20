import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routers.train import router as train_router
from app.routers.destination import router as destination_router
from app.routers.weather import router as weather_router
from app.routers.planner import router as planner_router
from app.routers.favorites import router as favorites_router
from app.routers.ai import router as ai_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("travel-planner")

logger.info(f"Starting Travel Planner API")
logger.info(f"AMAP_KEY in env: {bool(os.environ.get('AMAP_KEY'))}")
logger.info(f"JUHE_API_KEY in env: {bool(os.environ.get('JUHE_API_KEY'))}")

app = FastAPI(
    title="高铁旅行规划",
    description="基于高铁出行的智能旅行规划系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(train_router, prefix="/api")
app.include_router(destination_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(planner_router, prefix="/api")
app.include_router(favorites_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "dist"

if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok", 
        "version": "1.0.0", 
        "service": "travel-planner-api",
        "amap_key_in_env": bool(os.environ.get('AMAP_KEY')),
        "amap_key_length": len(os.environ.get('AMAP_KEY', ''))
    }

@app.get("/api/config-status")
async def config_status():
    amap_key = os.environ.get('AMAP_KEY', '')
    juhe_key = os.environ.get('JUHE_API_KEY', '')
    return {
        "amap_key_present": bool(amap_key),
        "amap_key_preview": amap_key[:8] + "..." if amap_key else "NOT SET",
        "amap_key_length": len(amap_key),
        "juhe_key_present": bool(juhe_key),
        "all_env_keys": [k for k in os.environ.keys() if 'KEY' in k.upper() or 'AMAP' in k.upper() or 'JUHE' in k.upper()],
        "environment": "production"
    }

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    if full_path.startswith("api/") or full_path == "api":
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")
    
    if FRONTEND_DIR.exists():
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")
    return {"message": "前端文件不存在，请先构建"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
