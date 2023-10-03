from pydantic import BaseModel, Field
from decimal import Decimal

from common.types import TzDateTime


class SaleBase(BaseModel):
    user_id: int
    total_amount: Decimal = Field(..., decimal_places=2)


class SaleCreate(SaleBase):
    ...


class SaleUpdate(SaleBase):
    ...


class SaleInDB(SaleBase):
    id: int
    created_at: TzDateTime

    class Config:
        from_attributes = True


class Sale(SaleInDB):
    ...
