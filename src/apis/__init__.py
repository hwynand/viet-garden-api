from fastapi import APIRouter

from apis import articles, carts, categories, login, products, users, orders

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(carts.router)
api_router.include_router(orders.router)
api_router.include_router(articles.router)
