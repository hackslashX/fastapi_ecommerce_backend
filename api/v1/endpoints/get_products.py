from fastapi import status

import crud
from api.base_resource import GetResource
from ..schemas.get_products import GetProductsRequest, GetProductsResponse


class GetProducts(GetResource):
    request_schema = GetProductsRequest
    response_schema = GetProductsResponse
    authentication_required = True

    # Endpoint details
    api_name = "get_products"
    api_url = "get_products"

    async def get_products(self):
        self.products = await crud.product.get_multi_with_category(
            self.db,
            category_ids=self.request_data.category_ids,
            page=self.request_data.page,
            per_page=self.request_data.per_page,
            order_by=self.request_data.order_by,
            order=self.request_data.order,
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Products fetched successfully"
        self.response_data = {"products": [p._asdict() for p in self.products]}

    async def process_flow(self):
        await self.get_products()
        await self.generate_response()
