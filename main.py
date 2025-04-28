import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orm import select_data, create_tables
from database import engine
from models import UserRegister, UserLogin
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/register")
async def register(user_data: UserRegister):
    result = await select_data(user_data.username, user_data.password)
    return {"message": result["message"]}


@app.post("/login")
async def login(user_data: UserLogin):

    return {"message": "Добро пожаловать!"}



if __name__ == "__main__":
    asyncio.run(create_tables(engine))
    uvicorn.run(app, host="0.0.0.0", port=8000)