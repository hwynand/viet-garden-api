from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base

if TYPE_CHECKING:
    from models.product import Product


class CategoryGroup(Base):
    name: Mapped[str]

    categories: Mapped[list["Category"]] = relationship(back_populates="category_group")


class Category(Base):
    category_group_id: Mapped[int] = mapped_column(ForeignKey("category_group.id"))
    name: Mapped[str]

    category_group: Mapped["CategoryGroup"] = relationship(back_populates="categories")
    products: Mapped[list["Product"]] = relationship(back_populates="category")
