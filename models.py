from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    
    
class UserRegister(BaseModel):
    username: str
    password: str
    

class UserLogin(BaseModel):
    username: str
    password: str
