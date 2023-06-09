from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_common_queries, get_current_admin, get_current_user, get_db
from core.pagination import PageParams, paginate, PagedResponseSchema

router = APIRouter(prefix="/category-groups", tags=["category"])


@router.get(
    "/",
    response_model=PagedResponseSchema[schemas.CategoryGroup],
    summary="Lấy danh sách các nhóm ngành hàng, VD: nhóm cây cảnh, chậu cảnh, ...",
)
async def read_category_groups(
    *,
    db: Session = Depends(get_db),
    keyword: str | None = None,
    page_params: PageParams = Depends()
):
    query = crud.category_group.get_multi(db=db)
    return paginate(db, query, page_params, schemas.CategoryGroup)


@router.post(
    "/",
    response_model=schemas.CategoryGroup,
    dependencies=[Depends(get_current_admin)],
    summary="Tạo nhóm ngành hàng mới",
)
async def create_category_group(
    *, db: Session = Depends(get_db), group_in: schemas.CategoryGroupCreate
):
    group = crud.category_group.create(db=db, obj_in=group_in)
    return group


@router.put(
    "/{group_id}",
    response_model=schemas.CategoryGroup,
    dependencies=[Depends(get_current_admin)],
    summary="Sửa nhóm ngành hàng",
)
async def update_category_group(
    *,
    db: Session = Depends(get_db),
    group_id: int,
    group_in: schemas.CategoryGroupUpdate
):
    db_group = crud.category_group.get(db=db, id=group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy group với id này",
        )
    group = crud.category_group.update(db=db, db_obj=db_group, obj_in=group_in)
    return group


@router.delete(
    "/{group_id}",
    response_model=schemas.CategoryGroup,
    dependencies=[Depends(get_current_admin)],
    summary="Xóa nhóm ngành hàng",
)
async def delete_category_group(*, db: Session = Depends(get_db), group_id: int):
    db_group = crud.category_group.get(db=db, id=group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy group với id này",
        )
    group = crud.category_group.remove(db=db, db_obj=db_group)
    return group


@router.get('/categories', response_model=PagedResponseSchema[schemas.Category], summary='danh sach category')
async def read_categories(*, db: Session = Depends(get_db), page_params: PageParams = Depends()):
    query = crud.category.get_multi(db=db)
    return paginate(db, query, page_params, schemas.Category)

@router.post(
    "/categories",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
    summary="Thêm ngành hàng",
)
async def create_category(
    *, db: Session = Depends(get_db), category_in: schemas.CategoryCreate
):
    category = crud.category.create(db=db, obj_in=category_in)
    return category


@router.put(
    "/categories/{category_id}",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
    summary="Sửa ngành hàng",
)
async def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate
):
    db_category = crud.category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy category với id này",
        )
    category = crud.category.update(db=db, db_obj=db_category, obj_in=category_in)
    return category


@router.delete(
    "/categories/{category_id}",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_admin)],
    summary="Xóa ngành hàng",
)
async def delete_category(*, db: Session = Depends(get_db), category_id: int):
    db_category = crud.category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy category với id này",
        )
    category = crud.category.remove(db=db, db_obj=db_category)
    return category
