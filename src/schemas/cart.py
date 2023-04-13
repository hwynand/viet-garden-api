from pydantic import BaseModel

from schemas.product import Product


class CartProductBase(BaseModel):
    product_id: int | None
    qty: int | None


class CartProductCreate(CartProductBase):
    product_id: int
    qty: int


class CartProductUpdate(CartProductBase):
    pass


class CartProduct(BaseModel):
    id: int
    product: Product
    qty: int

    class Config:
        orm_mode = True
