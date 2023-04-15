from typing import Any, Sequence

from sqlalchemy import select, Select
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.product import Product, ProductImage, Product
from schemas import ProductCreate, ProductUpdate, ProductImageBase


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi_filter(
        self,
        category_id: int | None = None,
        keyword: str | None = None,
    ) -> Select[tuple[Product]]:
        stmt = select(Product)
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)
        if keyword:
            stmt = stmt.where(Product.name.icontains(keyword))
        return stmt

    def create(self, db: Session, product_in: ProductCreate) -> Product:
        product = Product(
            category_id=product_in.category_id,
            name=product_in.name,
            price=product_in.price,
            inventory=product_in.inventory,
            summary=product_in.summary,
            detail=product_in.detail,
        )
        for image in product_in.product_images:
            product_image = ProductImage(image_path=image.image_path)
            product.product_images.append(product_image)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(
        self,
        db: Session,
        db_product: Product,
        product_in: ProductUpdate | dict[str, Any],
    ):
        product = super().update(db=db, db_obj=db_product, obj_in=product_in)
        if isinstance(product_in, dict):
            images = product_in.get("product_images", [])
            images = [ProductImageBase(**image) for image in images]
        else:
            images = product_in.product_images
        # since we allow to delete images and/or add new image to
        # we need to treat them by checking ids
        current_image_ids = [image.id for image in product.product_images]
        coming_image_ids = [image.id for image in images if image.id]
        unsaved_images = [image for image in images if not image.id]
        deleted_image_ids = [
            id for id in current_image_ids if id not in coming_image_ids
        ]
        for image in unsaved_images:
            new_image = ProductImage(image_path=image.image_path)
            product.product_images.append(new_image)
        for image_id in deleted_image_ids:
            deleted_image = db.scalar(
                select(ProductImage).filter(ProductImage.id == image_id)
            )
            # ignore type here, since the image surely exist
            product.product_images.remove(deleted_image)  # type: ignore
            db.delete(deleted_image)
        db.commit()
        db.refresh(product)
        return product


product = CRUDProduct(Product)
