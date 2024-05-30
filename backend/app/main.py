from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.app.config import app_config
from backend.app.routers.welcome import welcome_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=app_config.STATIC_DIR), name="static")

templates = Jinja2Templates(directory=app_config.TEMPLATES_DIR)

app.include_router(welcome_router)
# app.include_router(wallet_setup_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8002)
