from datetime import datetime
from pydantic import BaseModel, validator
from enum import StrEnum


class Buckets(StrEnum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class GetSalesDataRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    include_sales_items: bool = True
    buckets: Buckets | None = None
    product_ids: list[int] = []
    category_ids: list[int] = []

    @validator("end_date")
    def end_date_must_be_greater_than_start_date(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date must be greater than start_date")
        return v

    @validator("category_ids")
    def product_ids_or_category_ids_but_not_both(cls, v, values):
        product_ids = values.get("product_ids")
        if v and product_ids:
            raise ValueError("product_ids or category_ids but not both")
        return v


class GetSalesDataResponse(BaseModel):
    ...
