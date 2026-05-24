from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
from app.database import Base, engine
from app.config import SECRET_KEY, APP_NAME
from app.routers import admin, api, miniapp
Base.metadata.create_all(bind=engine)
app = FastAPI(title=APP_NAME)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site='lax', https_only=False)
app.mount('/static', StaticFiles(directory='backend/app/static'), name='static')
app.state.templates = Jinja2Templates(directory='backend/app/templates')
app.include_router(admin.router); app.include_router(api.router); app.include_router(miniapp.router)
@app.get('/')
def root(): return {'app': APP_NAME, 'status': 'online', 'admin': '/admin', 'mini_app': '/app', 'docs': '/docs'}
