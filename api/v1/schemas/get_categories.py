from pydantic import BaseModel

from common.schemas import PaginatedRequest
from crud.schemas import Category


class GetCategoriesRequest(PaginatedRequest):
    ...


class GetCategoriesResponse(BaseModel):
    categories: list[Category]
