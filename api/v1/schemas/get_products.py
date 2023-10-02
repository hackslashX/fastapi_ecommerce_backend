from pydantic import BaseModel

from common.schemas import PaginatedRequest
from crud.schemas import Product


class GetProductsRequest(PaginatedRequest):
    category_ids: list[int] = []


class ProductWithCategory(Product):
    category_name: str
    category_slug: str


class GetProductsResponse(BaseModel):
    products: list[ProductWithCategory]
