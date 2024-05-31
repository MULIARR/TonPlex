from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.config import app_config
from backend.app.routers.welcome import welcome_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=app_config.STATIC_DIR), name="static")

app.include_router(welcome_router)
# app.include_router(wallet_setup_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8002)
