import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base

if typing.TYPE_CHECKING:
    from models.user import User
    from models.product import Product


class ShoppingSession(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="shopping_session")
    cart_products: Mapped[list["CartProduct"]] = relationship(
        back_populates="shopping_session", cascade="all, delete-orphan"
    )


class CartProduct(Base):
    shopping_session_id: Mapped[int] = mapped_column(ForeignKey("shopping_session.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    qty: Mapped[int]

    shopping_session: Mapped["ShoppingSession"] = relationship(
        back_populates="cart_products"
    )
    product: Mapped["Product"] = relationship(back_populates="cart_products")
