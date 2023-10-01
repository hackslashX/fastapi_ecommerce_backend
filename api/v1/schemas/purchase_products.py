from pydantic import BaseModel, Field
from crud.schemas import Sale, SaleItem


class Item(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class PurchaseProductsRequest(BaseModel):
    items: list[Item]


class PurchaseProductsResponse(Sale):
    purchased_items: list[SaleItem]
    failed_items: list[Item]
