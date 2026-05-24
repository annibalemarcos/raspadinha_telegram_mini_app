from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config import APP_NAME
router = APIRouter(tags=['miniapp'])
@router.get('/app', response_class=HTMLResponse)
def miniapp(request: Request):
    return request.app.state.templates.TemplateResponse('miniapp/index.html', {'request': request, 'app_name': APP_NAME})
