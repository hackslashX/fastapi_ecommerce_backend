from pydantic import BaseModel
from crud.schemas import Product


class LowStockProductsRequest(BaseModel):
    quantity_threshold: int = 10


class LowStockProductsResponse(BaseModel):
    products: list[Product]
