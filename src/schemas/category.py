from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str | None


class CategoryCreate(CategoryBase):
    category_group_id: int
    name: str


class CategoryUpdate(CategoryBase):
    name: str


class Category(CategoryBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryGroupBase(BaseModel):
    name: str | None


class CategoryGroupCreate(CategoryGroupBase):
    name: str


class CategoryGroupUpdate(CategoryGroupBase):
    name: str


class CategoryGroup(CategoryGroupBase):
    id: int
    name: str
    categories: list["Category"]

    class Config:
        orm_mode = True
