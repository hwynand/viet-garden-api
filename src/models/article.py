from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base_model import Base


class Article(Base):
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str]
