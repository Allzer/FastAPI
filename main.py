from redis import asyncio as aioredis

from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.staticfiles import StaticFiles

from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks

from src.pages.router import router as router_pages

#Создаём приложение
app = FastAPI(
    title="Trading App"
)

#Роутеры регистрации и авторизации
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


#Роутер операций
app.include_router(router_operation)

#Роутер tasks
app.include_router(router_tasks)

#Роутер pages
app.include_router(router_pages)
#Подключение статичных файлов
app.mount("/static", StaticFiles(directory="src/static"), name='static')

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

@app.on_event("startup") #Функция startup выполняется при запуске приложения
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

#Cors
#Адреса фронтов, которые имеют доступ к бекенду
origins = [
    "http://localhost:8080",
]

app.add_middleware( #middleware нужен для обработки запроса перед тем, как он придёт на бэкэнд
    CORSMiddleware, #Эта шняга отвечает за то, чтобы всё это дело работало
    allow_origins=origins,
    allow_credentials=True, #отвечает за куки
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'], #разрешение всех методов. Важно прописать вручную все методы дял избежания проблем
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)

