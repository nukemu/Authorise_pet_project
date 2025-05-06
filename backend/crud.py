from schemas import DiaryEntryCreate
from models import DiaryEntryOrm
from database import session_factory



async def create_diary_entry(entry: DiaryEntryCreate):
    async with session_factory() as session:
        new_entry = DiaryEntryOrm(text=entry.text)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry