import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from src.database import metadata, get_async_session

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False) #Переписываем зависимость AsyncSession, чтобы мы подключались к тестовой базе
metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session
client = TestClient(app)

#SETUP
@pytest.fixture(scope='session') #session = прогон всех тестов
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True,scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:      #создаём БД и подключаемся к ней
        await conn.run_sync(metadata.create_all)
    yield #отдаём доступ pytest
    async with engine_test.begin() as conn:      #удаляем БД
        await conn.run_sync(metadata.drop_all)

@pytest.fixture(scope='session') #Это для асинхронного клиента, для асинхронных эндпоинтов
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac








