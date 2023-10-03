import pandas as pd
from fastapi import status
from collections import defaultdict

import crud
from api.base_resource import GetResource
from ..schemas.get_sales_data import GetSalesDataRequest, GetSalesDataResponse


class GetSalesData(GetResource):
    request_schema = GetSalesDataRequest
    authentication_required = True

    # Endpoint details
    api_name = "get_sales_data"
    api_url = "get_sales_data"

    async def get_sales_data(self):
        self.sales = await crud.sale.get_sales_data(
            self.db,
            start_date=self.request_data.start_date,
            end_date=self.request_data.end_date,
            product_ids=self.request_data.product_ids,
            category_ids=self.request_data.category_ids,
        )
        self.sales = [s._asdict() for s in self.sales]
        for sale in self.sales:
            sale["revenue"] = sale["quantity"] * sale["price_per_unit"]

    async def create_buckets(self):
        # Buckets can be daily, weekly, monthly and yearly
        # Given start and end date construct possible buckets
        self.buckets = {}

        match (self.request_data.buckets):
            case "weekly":
                buckets = pd.DataFrame(
                    pd.period_range(
                        start=self.request_data.start_date,
                        end=self.request_data.end_date,
                        freq="W",
                    )
                )
            case "monthly":
                buckets = pd.DataFrame(
                    pd.period_range(
                        start=self.request_data.start_date,
                        end=self.request_data.end_date,
                        freq="M",
                    )
                )
            case "yearly":
                buckets = pd.DataFrame(
                    pd.period_range(
                        start=self.request_data.start_date,
                        end=self.request_data.end_date,
                        freq="Y",
                    )
                )
            case _:
                buckets = pd.DataFrame(
                    pd.period_range(
                        start=self.request_data.start_date,
                        end=self.request_data.end_date,
                        freq="D",
                    )
                )

        for bucket in buckets[0]:
            self.buckets[
                (
                    bucket.start_time,
                    bucket.end_time,
                )
            ] = {
                "sales": list(),
                "total_revenue": 0,
                "revenue_by_categories": defaultdict(lambda: 0),
                "revenue_by_products": defaultdict(lambda: 0),
                "quantity_by_categories": defaultdict(lambda: 0),
                "quantity_by_products": defaultdict(lambda: 0),
            }

    async def populate_buckets(self):
        for sale in self.sales:
            for bucket in self.buckets:
                if sale["created_at"] >= bucket[0] and sale["created_at"] <= bucket[1]:
                    if self.request_data.include_sales_items:
                        self.buckets[bucket]["sales"].append(sale)
                    self.buckets[bucket]["total_revenue"] += sale["revenue"]
                    self.buckets[bucket]["revenue_by_categories"][
                        (sale["category_id"], sale["category_name"])
                    ] += sale["revenue"]
                    self.buckets[bucket]["revenue_by_products"][
                        (sale["product_id"], sale["product_name"])
                    ] += sale["revenue"]
                    self.buckets[bucket]["quantity_by_categories"][
                        (sale["category_id"], sale["category_name"])
                    ] += sale["quantity"]
                    self.buckets[bucket]["quantity_by_products"][
                        (sale["product_id"], sale["product_name"])
                    ] += sale["quantity"]
                    break

    async def populate_metrics(self):
        # Metrics without the buckets headache
        self.buckets = {
            "sales": list(),
            "total_revenue": 0,
            "revenue_by_categories": defaultdict(lambda: 0),
            "revenue_by_products": defaultdict(lambda: 0),
            "quantity_by_categories": defaultdict(lambda: 0),
            "quantity_by_products": defaultdict(lambda: 0),
        }
        if self.request_data.include_sales_items:
            self.buckets["sales"] = self.sales
        for sale in self.sales:
            self.buckets["total_revenue"] += sale["revenue"]
            self.buckets["revenue_by_categories"][
                (sale["category_id"], sale["category_name"])
            ] += sale["revenue"]
            self.buckets["revenue_by_products"][
                (sale["product_id"], sale["product_name"])
            ] += sale["revenue"]
            self.buckets["quantity_by_categories"][
                (sale["category_id"], sale["category_name"])
            ] += sale["quantity"]
            self.buckets["quantity_by_products"][
                (sale["product_id"], sale["product_name"])
            ] += sale["quantity"]

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Sales and Revenue data retrieved successfully"
        self.response_data = self.buckets

    async def process_flow(self):
        await self.get_sales_data()

        if self.request_data.buckets:
            await self.create_buckets()
            await self.populate_buckets()
        else:
            await self.populate_metrics()

        await self.generate_response()
