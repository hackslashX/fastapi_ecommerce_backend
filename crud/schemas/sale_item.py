from pydantic import BaseModel, Field
from decimal import Decimal


class SaleItemBase(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    price_per_unit: Decimal = Field(..., decimal_places=2)


class SaleItemCreate(SaleItemBase):
    ...


class SaleItemUpdate(SaleItemBase):
    ...


class SaleItemInDB(SaleItemBase):
    id: int

    class Config:
        orm_mode = True


class SaleItem(SaleItemInDB):
    ...
