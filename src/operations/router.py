from fastapi import APIRouter

router = APIRouter(
    prefix='/operations',
    tags=['operation']
)

@router.get('/')
async def get_operations():
    return


