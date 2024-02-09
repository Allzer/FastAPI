from fastapi import APIRouter, Depends

from src.auth.base_config import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(
    prefix='/report',
    tags=['Report']
)

@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        'status': 200,
        'data': "Письмо отправлено",
        'details': None
    }

#Как сделать фоновую задачу на FastAPI
#@router.get('/dashboard')
#def get_dashboard_report_fastapi(background_tasks: BackgroundTasks, user=Depends(current_user)):
#    background_tasks.add_task(send_email_report_dashboard, user.username) #Передаём функцию, которую нужно вызвать. Не вызываем, но передаём аргументы
#    return {
#        'status': 200,
#        'data': "Письмо отправлено",
#        'details': None
#    }





