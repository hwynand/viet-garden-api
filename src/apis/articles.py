from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from apis.deps import get_current_admin, get_db
from core.pagination import PagedResponseSchema, PageParams, paginate
import crud

router = APIRouter(prefix="/article", tags=["articles"])


@router.get("/", response_model=PagedResponseSchema[schemas.Article])
async def read_articles(
    *,
    db: Session = Depends(get_db),
    page_params: PageParams = Depends(),
):
    query = crud.article.get_multi(db=db)
    return paginate(db, query, page_params, schemas.Article)


@router.post(
    "/", dependencies=[Depends(get_current_admin)], response_model=schemas.Article
)
async def create_article(
    *, db: Session = Depends(get_db), article_in: schemas.ArticleCreate
):
    article = crud.article.create(db=db, obj_in=article_in)
    return article


@router.put(
    "/{article_id}",
    dependencies=[Depends(get_current_admin)],
    response_model=schemas.Article,
)
async def update_artilce(
    *, db: Session = Depends(get_db), article_id: int, article_in: schemas.ArticleUpdate
):
    db_article = crud.article.get(db=db, id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    article = crud.article.update(db=db, db_obj=db_article, obj_in=article_in)
    return article


@router.delete(
    "/{article_id}",
    dependencies=[Depends(get_current_admin)],
    response_model=schemas.Article,
)
async def delete_artilce(*, db: Session = Depends(get_db), article_id: int):
    db_article = crud.article.get(db=db, id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
    article = crud.article.remove(db=db, db_obj=db_article)
    return article
