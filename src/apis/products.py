import os
import secrets

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from PIL import Image
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_admin, get_db
from core.pagination import PageParams, paginate
from utils.constants import IMAGE_TYPES_ALLOWED

router = APIRouter(
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(get_current_admin)],
)


@router.post(
    "/uploadfile/",
    summary="Upload ảnh sản phẩm",
    dependencies=[Depends(get_current_admin)],
)
async def upload_file(*, file: UploadFile = File(...), request: Request):
    if not file.content_type in IMAGE_TYPES_ALLOWED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ cho phép upload định dạng jpeg/png",
        )
    img = Image.open(file.file)
    img_out_size = (512, 512)
    img.thumbnail(img_out_size)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)  # type: ignore
    image_fn = random_hex + f_ext  # type: ignore
    to_save_path = os.path.join("media/product_images", image_fn)
    img.save(to_save_path)
    img.close()

    return request.url._url.rstrip(request.url.path) + "/files/" + image_fn


@router.get("/")
async def read_products(
    *,
    db: Session = Depends(get_db),
    category_id: int | None = None,
    keyword: str | None = None,
    page_params: PageParams = Depends()
):
    query = crud.product.get_multi_filter(category_id=category_id, keyword=keyword)
    return paginate(db, query, page_params, schemas.Product)


@router.post(
    "/",
    summary="Tạo sản phẩm",
    dependencies=[Depends(get_current_admin)],
)
async def create_product(
    *, db: Session = Depends(get_db), product_in: schemas.ProductCreate
):
    product = crud.product.create(db=db, product_in=product_in)
    return product


@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
    *, db: Session = Depends(get_db), product_id: int, product_in: schemas.ProductUpdate
):
    db_product = crud.product.get(db=db, id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product = crud.product.update(db=db, db_product=db_product, product_in=product_in)
    return product


@router.delete("/product_id", response_model=schemas.Product)
async def delete_product(*, db: Session = Depends(get_db), product_id: int):
    db_product = crud.product.get(db=db, id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found"
        )
    product = crud.product.remove(db=db, db_obj=db_product)
    return product
