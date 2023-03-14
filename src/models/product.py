from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base

if TYPE_CHECKING:
    from models.category import Category


class Product(Base):
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    name: Mapped[str]
    price: Mapped[int]
    inventory: Mapped[int]
    summary: Mapped[str]
    detail: Mapped[str]

    category: Mapped["Category"] = relationship(back_populates="products")
    product_images: Mapped[list["ProductImage"]] = relationship(
        back_populates="product"
    )


class ProductImage(Base):
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    image_path: Mapped[str]

    product: Mapped["Product"] = relationship(back_populates="product_images")
