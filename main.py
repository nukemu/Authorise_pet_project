import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orm import select_data, create_tables, check_user
from database import Base, engine
from models import UserRegister, UserLogin, DiaryEntryOrm
import uvicorn
from schemas import DiaryEntryCreate, DiaryEntrySchemas
from crud import create_diary_entry

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register(user_data: UserRegister):
    result = await select_data(user_data.username, user_data.password)
    return {"message": result["message"]}


@app.post("/login")
async def login(user_data: UserLogin):
    result = await check_user(user_data.username, user_data.password)
    return {"message": result["message"]}



@app.post("/entries/", response_model=DiaryEntrySchemas)
async def add_entries(entry: DiaryEntryCreate):
    return await create_diary_entry(entry)


async def main():
    await create_tables(engine)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())