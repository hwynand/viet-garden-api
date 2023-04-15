from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str | None
    content: str | None


class ArticleCreate(ArticleBase):
    title: str
    content: str


class ArticleUpdate(ArticleBase):
    ...


class Article(ArticleCreate):
    id: int

    class Config:
        orm_mode = True
