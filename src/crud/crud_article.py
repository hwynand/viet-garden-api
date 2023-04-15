from crud.base import CRUDBase
from models.article import Article
from schemas import ArticleCreate, ArticleUpdate


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    pass


article = CRUDArticle(Article)
