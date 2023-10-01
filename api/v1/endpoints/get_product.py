from fastapi import status

import crud
from models.product import Product
from api.base_resource import GetResource
from ..schemas.get_product import GetProductRequest, GetProductResponse


class GetProduct(GetResource):
    request_schema = GetProductRequest
    response_schema = GetProductResponse
    authentication_required = True

    # Endpoint details
    api_name = "get_product"
    api_url = "get_product"

    async def check_if_product_exists(self):
        self.product: Product = await crud.product.get(
            self.db, id=self.request_data.product_id
        )
        if not self.product:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "Product does not exist"
            self.response_data = {}

    async def get_inventory(self):
        self.inventories = await crud.inventory.get_by_product_id(
            self.db, product_id=self.request_data.product_id
        )
        self.inventories = list(map(lambda x: x.to_dict(), self.inventories))

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Product retrieved successfully"
        self.response_data = {
            **self.product.to_dict(),
            "inventory": self.inventories,
        }

    async def process_flow(self):
        await self.check_if_product_exists()
        if self.early_response:
            return
        await self.get_inventory()
        await self.generate_response()
