from sqlalchemy import select, insert
from database import session_factory, Base
from models import UsersOrm


async def create_tables(engine):
    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    engine.echo = True
    

async def insert_data(username: str, password: str):
    async with session_factory() as session:
        workers = UsersOrm(username=username, password=password)
        session.add(workers)
        await session.flush()
        await session.commit()
        return {"message": "User created!"}
        

async def select_data(username: str, password: str):
    async with session_factory() as session:
        query = select(UsersOrm).where(UsersOrm.username==username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if user:
            return {"message": "User with this nickname have"}
        else:
            await insert_data(username, password)
            return {"message": "User with this nickname havnt"}