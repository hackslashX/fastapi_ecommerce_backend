from fastapi import status

import crud
from models.category import Category
from api.base_resource import GetResource
from ..schemas.get_categories import GetCategoriesRequest, GetCategoriesResponse


class GetCategories(GetResource):
    request_schema = GetCategoriesRequest
    response_schema = GetCategoriesResponse
    authentication_required = True

    # Endpoint details
    api_name = "get_categories"
    api_url = "get_categories"

    async def get_categories(self):
        self.categories: list[Category] = await crud.category.get_multi(
            self.db,
            page=self.request_data.page,
            per_page=self.request_data.per_page,
            order_by=self.request_data.order_by,
            order=self.request_data.order,
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Categories fetched successfully"
        self.response_data = {"categories": [c.to_dict() for c in self.categories]}

    async def process_flow(self):
        await self.get_categories()
        await self.generate_response()
