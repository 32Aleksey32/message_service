from fastapi import APIRouter, FastAPI, requests, responses, staticfiles

from app import templates
from app.message.handlers import message_router
from app.user.forms import user_forms_router
from app.user.handlers import user_router
from app.websoсket.handlers import websocket_router

app = FastAPI(title='Message Service')


@app.get("/", response_class=responses.HTMLResponse)
async def read_root(request: requests.Request):
    return templates.TemplateResponse("index.html", {"request": request})


api_router = APIRouter()

api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(user_forms_router, prefix='/users', tags=['user_forms'])

api_router.include_router(message_router, prefix='/messages', tags=['messages'])
api_router.include_router(websocket_router, prefix='', tags=['websocket'])

app.include_router(api_router)

app.mount("/static", staticfiles.StaticFiles(directory="app/static"), name="static")
