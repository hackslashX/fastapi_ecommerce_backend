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

    async def check_if_category_exists(self):
        category = await crud.category.get(self.db, id=self.request_data.category_id)
        if not category:
            self.early_response = True
            self.status_code = status.HTTP_404_NOT_FOUND
            self.response_message = "Category not found"
            self.response_data = {}

    async def create_product(self):
        self.product: Product = await crud.product.create(
            self.db, obj_in=self.request_data
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Product created successfully"
        self.response_data = self.product.to_dict()

    async def process_flow(self):
        await self.check_if_category_exists()
        if self.early_response:
            return

        await self.create_product()
        await self.generate_response()
