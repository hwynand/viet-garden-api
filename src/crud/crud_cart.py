from crud.base import CRUDBase
from models.cart import CartProduct
from schemas import CartProductCreate, CartProductUpdate


class CRUDCartProduct(CRUDBase[CartProduct, CartProductCreate, CartProductUpdate]):
    pass


cart_product = CRUDCartProduct(CartProduct)
