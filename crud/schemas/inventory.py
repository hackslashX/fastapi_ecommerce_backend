from pydantic import BaseModel

from common.types import TzDateTime


class InventoryBase(BaseModel):
    quantity: int


class InventoryCreate(InventoryBase):
    product_id: int


class InventoryUpdate(InventoryBase):
    ...


class InventoryInDBBase(InventoryCreate):
    id: int
    created_at: TzDateTime
    updated_at: TzDateTime

    class Config:
        from_attributes = True


class Inventory(InventoryInDBBase):
    ...
