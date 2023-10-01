from pydantic import BaseModel
from crud.schemas import Product, Inventory


class GetProductRequest(BaseModel):
    product_id: int


class GetProductResponse(Product):
    inventory: list[Inventory]
