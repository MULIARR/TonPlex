import logging

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


class User(BaseModel):
    user_id: int


@app.post("/save_user_id")
async def save_user_id(user: User):
    logger.info(f"Received user_id: {user.user_id}")

    return {
        "status": "success",
        "user_id": user.user_id
    }
