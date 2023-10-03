from pydantic import BaseModel, Field
from decimal import Decimal

from common.types import TzDateTime


class ProductBase(BaseModel):
    product_name: str = Field(..., max_length=50, min_length=3)
    description: str = Field(None, max_length=255, min_length=3)
    category_id: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    is_active: bool = True


class ProductCreate(ProductBase):
    ...


class ProductUpdate(ProductBase):
    ...


class ProductInDB(ProductBase):
    id: int
    quantity: int | None
    created_at: TzDateTime
    updated_at: TzDateTime

    class Config:
        from_attributes = True


class Product(ProductInDB):
    ...
