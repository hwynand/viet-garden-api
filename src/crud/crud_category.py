from crud.base import CRUDBase
from models.category import Category, CategoryGroup
from schemas import (
    CategoryCreate,
    CategoryGroupCreate,
    CategoryGroupUpdate,
    CategoryUpdate,
)


class CRUDCategoryGroup(
    CRUDBase[CategoryGroup, CategoryGroupCreate, CategoryGroupUpdate]
):
    pass


category_group = CRUDCategoryGroup(CategoryGroup)


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDCategory(Category)
