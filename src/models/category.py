from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_model import Base


class CategoryGroup(Base):
    name: Mapped[str]

    categories: Mapped[list["Category"]] = relationship(back_populates="category_group")


class Category(Base):
    category_group_id: Mapped[int] = mapped_column(ForeignKey("category_group.id"))
    name: Mapped[str]

    category_group: Mapped["CategoryGroup"] = relationship(back_populates="categories")
