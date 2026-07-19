import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
print("Main app OK")

from app.routers.train import router
print("Train router OK")

from app.routers.destination import router
print("Destination router OK")

from app.routers.weather import router
print("Weather router OK")

from app.routers.favorites import router
print("Favorites router OK")

from app.routers.planner import router
print("Planner router OK")

print("\nAll modules loaded successfully!")
print(f"API routes: {len(app.routes)} routes registered")
