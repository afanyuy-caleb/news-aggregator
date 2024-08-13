from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.source import Source
from ..schemas.source import SourceCreate, SourceUpdate

async def get_source(db: AsyncSession, source_id: int):
    result = await db.execute(select(Source).where(Source.id == source_id))
    return result.scalars().first()


# modify to filter by given fields if any
async def get_sources(db: AsyncSession, skip: int=0, limit: int = 10, field : str = None, value: str = None):
    try:
        if field:
            if field == "type":
                stmt = select(Source).where(getattr(Source, field) == value).offset(skip).limit(limit)
            else:
                stmt = select(Source).where(getattr(Source, field).contains(value)).offset(skip).limit(limit)
            result = await db.execute(stmt)
        else:   
            result = await db.execute(select(Source).offset(skip).limit(limit))
            
        return True, result.scalars().all()
    
    except Exception as e:
        return False, e


async def create_source(db: AsyncSession, source: SourceCreate):
    db_source = Source(**source.dict())
    db.add(db_source)
    await db.commit()
    await db.close()
    return db_source


async def update_source(db: AsyncSession, source_id: int, source: SourceUpdate):
    db_source = await get_source(db, source_id)
    if db_source:
        for key, value in source.dict().items():
            setattr(db_source, key, value) 
        await db.commit()
        await db.close()
        return db_source
    else:
        raise Exception(f"source with id {id} not found")


async def delete_source(db: AsyncSession, source_id: int):
    db_source = await get_source(db, source_id)
    if db_source:
        await db.delete(db_source)
        await db.commit()
        await db.close()
        return db_source
    else:
        raise Exception(f"source with id {id} not found")


async def delete_source(db: AsyncSession, source_id: int):
    db_source = await get_source(db, source_id)
    if db_source:
        await db.delete(db_source)
        await db.commit()
        await db.close()
        return db_source
    else:
        raise Exception(f"source with id {id} not found")
