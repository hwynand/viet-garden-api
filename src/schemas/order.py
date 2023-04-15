from pydantic import BaseModel

from schemas.user import User
from schemas.product import Product


class OrderProductBase(BaseModel):
    product_id: int | None
    qty: int | None


class OrderProductCreate(OrderProductBase):
    product_id: int
    price: int
    qty: int


class OrderProductUpdate(OrderProductBase):
    pass


class OrderProduct(BaseModel):
    id: int
    product: Product
    qty: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    code: str | None
    status: int | None
    total: int | None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: int | None


class Order(OrderBase):
    id: int
    order_products: list["OrderProduct"]

    class Config:
        orm_mode = True


class OrderAdmin(Order):
    user: User
