import asyncio
import uvicorn

from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import DiaryEntryCreate, DiaryEntrySchemas
from crud import create_diary_entry
from orm import select_data, create_tables, check_user
from database import Base, engine, session_factory
from models import UserRegister, UserLogin, DiaryEntryOrm
from JWT_config import security


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
async def login(user_data: UserLogin, response: Response):
    return await check_user(user_data.username, user_data.password, response)
    # return {"message": result["access_token"]}


@app.post("/entries/", response_model=DiaryEntrySchemas, dependencies=[Depends(security.access_token_required)])
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
