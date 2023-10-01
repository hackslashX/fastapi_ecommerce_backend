from fastapi import status

import crud
from api.base_resource import GetResource
from ..schemas.get_low_stock_products import (
    LowStockProductsRequest,
    LowStockProductsResponse,
)


class GetLowStockProducts(GetResource):
    request_schema = LowStockProductsRequest
    response_schema = LowStockProductsResponse
    authentication_required = True

    # Endpoint details
    api_name = "get_low_stock_products"
    api_url = "get_low_stock_products"

    async def get_low_stock_products(self):
        self.products = await crud.product.get_products_quantity_le(
            self.db, quantity=self.request_data.quantity_threshold
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Low Stock Products retrieved successfully"
        self.response_data = {"products": [x.to_dict() for x in self.products]}

    async def process_flow(self):
        await self.get_low_stock_products()
        await self.generate_response()
