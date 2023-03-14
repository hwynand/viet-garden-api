from fastapi import APIRouter

from apis import login, users, categories

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(categories.router)
