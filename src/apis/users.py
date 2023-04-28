from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_admin, get_current_user, get_db
from core.pagination import PagedResponseSchema, PageParams, paginate
from models.user import User
from utils.validate import password_strong

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    tags=["users"],
    summary="Lấy thông tin user đang đăng nhập",
    response_model=schemas.User,
)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", tags=["users"], response_model=schemas.User)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    fullname: str = Body(None),
    email: EmailStr = Body(None),
    phone_number: str = Body(None),
    address: str = Body(None),
    password: str = Body(None),
):
    if current_user.is_admin:
        raise HTTPException(
            status_code=400, detail="Không thể thay đổi thông tin admin"
        )
    user = crud.user.get_by_email(db, email=email)
    if user and user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    if password and not password_strong(password):
        raise HTTPException(
            status_code=400,
            detail="Mật khẩu phải có ít nhất 8 kí tự, bao gồm 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 kí tự đặc biệt",
        )
    user_in = schemas.UserUpdate(
        fullname=fullname,
        email=email,
        phone_number=phone_number,
        address=address,
        password=password,
    )
    user = crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user



@router.get(
    "/",
    tags=["users"],
    response_model=PagedResponseSchema[schemas.User],
    dependencies=[Depends(get_current_admin)],
    summary="Lấy danh sách user (admin)",
)
async def read_users(
    *,
    db: Session = Depends(get_db),
    keyword: str | None = None,
    page_params: PageParams = Depends(),
):
    query = crud.user.get_multi_filter(keyword=keyword)
    return paginate(db, query, page_params, schemas.User)


@router.get(
    "/{user_id}",
    tags=["users"],
    response_model=schemas.User,
    dependencies=[Depends(get_current_admin)],
    summary="Xem chi tiết user (admin)",
)
async def read_user(*, db: Session = Depends(get_db), user_id: int):
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Khong ton tai user nay"
        )
    return user
