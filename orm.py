from sqlalchemy import select, insert
from database import session_factory, Base
from models import UsersOrm
from passlib.context import CryptContext
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_tables(engine):
    engine.echo = False
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    engine.echo = True
    

async def insert_data(username: str, password: str):
    async with session_factory() as session:
        hashed_password = pwd_context.hash(password)
        workers = UsersOrm(username=username, password=hashed_password)
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
        
        
async def check_user(username: str, password: str):
    async with session_factory() as session:
        query = select(UsersOrm).where(UsersOrm.username==username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Uncorrect nickname or password", 
            )
            
        if not pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Uncorrect nickname or password",
            )
            
        return {"message": "Welcome!"}