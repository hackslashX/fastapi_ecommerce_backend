from datetime import datetime
from pydantic import BaseModel, Field

from common.types import TzDateTime


class CategoryBase(BaseModel):
    category_name: str = Field(..., max_length=50, min_length=3)
    category_slug: str = Field(..., max_length=50, min_length=3)


class CategoryCreate(CategoryBase):
    ...


class CategoryUpdate(CategoryBase):
    ...


class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Category(CategoryInDB):
    ...
