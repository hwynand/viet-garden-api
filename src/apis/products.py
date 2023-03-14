import os
import secrets

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from PIL import Image
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_admin, get_db
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
