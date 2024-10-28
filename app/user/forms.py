from fastapi import APIRouter, requests, responses

from app import templates

user_forms_router = APIRouter()


@user_forms_router.get("/register", response_class=responses.HTMLResponse, include_in_schema=False)
async def register_form(request: requests.Request):
    return templates.TemplateResponse("register.html", {"request": request})


@user_forms_router.get("/login", response_class=responses.HTMLResponse, include_in_schema=False)
async def login_form(request: requests.Request):
    return templates.TemplateResponse("login.html", {"request": request})
