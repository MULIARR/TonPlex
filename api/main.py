from fastapi import FastAPI, HTTPException
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


class User(BaseModel):
    user_id: int


@app.post("/save_user_id")
async def save_user_id(user: User):
    try:
        return {"status": "success", "user_id": user.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/hello")
async def read_hello():
    try:
        return {"message": "Hello, World!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    return {"message": "Hello from the root endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
