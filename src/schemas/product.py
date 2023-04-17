from pydantic import BaseModel, AnyHttpUrl

from schemas.category import Category


class ProductImageBase(BaseModel):
    image_path: AnyHttpUrl


class ProductImageUpdate(ProductImageBase):
    id: int | None = None

class ProductImage(ProductImageBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    category_id: int | None
    name: str | None
    price: int | None
    inventory: int | None
    summary: str | None
    detail: str | None
    product_images: list["ProductImageBase"] = []


class ProductCreate(ProductBase):
    category_id: int
    name: str
    price: int
    inventory: int
    summary: str
    detail: str
    product_images: list["ProductImageBase"]


class ProductUpdate(ProductBase):
    pass


class Product(BaseModel):
    id: int
    category: Category
    name: str
    price: int
    inventory: int
    summary: str
    detail: str
    product_images: list["ProductImage"]

    class Config:
        orm_mode = True
