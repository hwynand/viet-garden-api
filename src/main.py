from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apis import api_router

app = FastAPI(
    title="API Viet-garden",
    contact={
        "name": "Huong Pham",
        "github": "https://github.com/huongpx",
    },
    root_path="/viet-garden",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

app.mount(
    "/files", StaticFiles(directory="media/product_images"), name="product_images"
)
