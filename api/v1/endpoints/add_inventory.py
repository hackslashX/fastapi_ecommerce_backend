from fastapi import status

import crud
from models.product import Product
from api.base_resource import PutResource
from ..schemas.add_inventory import AddInventoryRequest, AddInventoryResponse


class AddInventory(PutResource):
    request_schema = AddInventoryRequest
    response_schema = AddInventoryResponse
    authentication_required = True

    # Endpoint details
    api_name = "add_inventory"
    api_url = "add_inventory"

    async def check_if_product_exists(self):
        self.product = await crud.product.get(self.db, id=self.request_data.product_id)
        if not self.product:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "Product does not exist"
            self.response_data = {}

    async def add_inventory(self):
        self.inventory = await crud.inventory.create(self.db, obj_in=self.request_data)
        # Update Product
        self.product = await crud.product.update(
            self.db,
            db_obj=self.product,
            obj_in={"quantity": self.product.quantity + self.request_data.quantity},
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Inventory added successfully"
        self.response_data = self.inventory.to_dict()

    async def process_flow(self):
        await self.check_if_product_exists()
        if self.early_response:
            return
        await self.add_inventory()
        await self.generate_response()
