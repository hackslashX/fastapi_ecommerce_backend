from fastapi import status

import crud
from models.product import Product
from api.base_resource import PutResource
from ..schemas.create_product import CreateProductRequest, CreateProductResponse


class CreateProduct(PutResource):
    request_schema = CreateProductRequest
    response_schema = CreateProductResponse
    authentication_required = True

    # Endpoint details
    api_name = "create_product"
    api_url = "create_product"

    async def create_product(self):
        self.product: Product = await crud.product.create(
            self.db, obj_in=self.request_data
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Product created successfully"
        self.response_data = self.product.to_dict()

    async def process_flow(self):
        await self.create_product()
        await self.generate_response()
