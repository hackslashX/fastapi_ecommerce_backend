from fastapi import status

import crud
from models.category import Category
from api.base_resource import PutResource
from ..schemas.create_category import CreateCategoryRequest, CreateCategoryResponse


class CreateCategory(PutResource):
    request_schema = CreateCategoryRequest
    response_schema = CreateCategoryResponse
    authentication_required = True

    # Endpoint details
    api_name = "create_category"
    api_url = "create_category"

    async def check_if_category_exists(self):
        category = await crud.category.get_by_slug(
            self.db, slug=self.request_data.category_slug
        )
        if category:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "Category with this slug already exists"
            self.response_data = {}

    async def create_category(self):
        self.category: Category = await crud.category.create(
            self.db, obj_in=self.request_data
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Category created successfully"
        self.response_data = self.category.to_dict()

    async def process_flow(self):
        await self.check_if_category_exists()
        if self.early_response:
            return

        await self.create_category()
        await self.generate_response()
