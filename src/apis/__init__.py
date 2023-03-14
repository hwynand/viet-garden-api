from fastapi import APIRouter

from apis import login, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
