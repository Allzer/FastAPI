from sqlalchemy import insert, select

from src.auth.models import role
from tests.conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name = 'admin', permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        print(query)


#Тест регистрации
def test_register():
    response = client.post('/auth/register', json={
        "email": "XDD@mail.ru",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })
    assert response.status_code == 201, "Что-то пошло не так"






