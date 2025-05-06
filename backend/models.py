from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from pydantic import BaseModel, Field
from datetime import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]
    password: Mapped[str]
    
    
class DiaryEntryOrm(Base):
    __tablename__ = "entries"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    
class UserLogin(BaseModel):
    username: str
    password: str
