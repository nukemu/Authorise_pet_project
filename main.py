import asyncio
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orm import select_data, create_tables, check_user
from database import Base, engine, session_factory
from models import UserRegister, UserLogin, DiaryEntryOrm
import uvicorn
from schemas import DiaryEntryCreate, DiaryEntrySchemas
from crud import create_diary_entry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db():
    async with session_factory() as session:
        yield session


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


@app.get("/entries/", response_model=list[DiaryEntrySchemas])
async def get_entries(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(DiaryEntryOrm))
    entries = result.scalars().all()
    return entries


async def main():
    await create_tables(engine)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()    


if __name__ == "__main__":
    asyncio.run(main())