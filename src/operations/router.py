import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_cache.decorator import cache

from src.database import get_async_session
from sqlalchemy import select, insert

from .models import operation
from .shemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['operation']
)

@router.get('/long_operation')
@cache(expire=30)
def get_long_operation():
    time.sleep(2)
    return "Много данных, которые вычислялись 100 лет"

@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return {
        "status": "succes",
        "data": result.mappings().all()
    }

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
