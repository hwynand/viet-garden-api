from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_user, get_db
from models.cart import CartProduct, ShoppingSession
from models.user import User

router = APIRouter(prefix="/cart-products", tags=["cart products"])


@router.get(
    path="/me",
    response_model=list[schemas.CartProduct],
    summary="Lấy tất cả sản phẩm trong giỏ hàng",
)
async def read_cart_products(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    shopping_session = current_user.shopping_session
    if not shopping_session:
        return []
    cart_products = shopping_session.cart_products
    return cart_products


@router.post(
    path="/me",
    response_model=schemas.CartProduct,
    summary="Thêm sản phẩm mới vào giỏ hàng",
)
async def create_cart_product(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_product_in: schemas.CartProductCreate,
):
    shopping_session = current_user.shopping_session
    if not shopping_session:
        shopping_session = ShoppingSession(user_id=current_user.id)
    new_product = CartProduct(
        product_id=cart_product_in.product_id, qty=cart_product_in.qty
    )
    shopping_session.cart_products.append(new_product)
    db.add(shopping_session)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put(
    path="/me/{cart_product_id}",
    response_model=schemas.CartProduct,
    summary="Sửa sản phẩm trong giỏ hàng (ví dụ thay đổi số lượng sản phẩm)",
)
async def update_item(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_product_id: int,
    cart_product_in: schemas.CartProductUpdate,
):
    cart_product = crud.cart_product.get(db=db, id=cart_product_id)
    if not cart_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    cart_product = crud.cart_product.update(
        db=db, db_obj=cart_product, obj_in=cart_product_in
    )
    return cart_product


@router.delete(
    path="/me/{cart_product_id}",
    response_model=schemas.CartProduct,
    summary="Xóa sản phẩm trong giỏ hàng",
)
async def delete_item(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_product_id: int,
):
    cart_product = crud.cart_product.get(db=db, id=cart_product_id)
    if not cart_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    cart_product = crud.cart_product.remove(db=db, db_obj=cart_product)
    return cart_product
