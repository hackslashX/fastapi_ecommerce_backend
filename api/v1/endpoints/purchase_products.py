from fastapi import status
from starlette_context import context

import crud
from models.product import Product
from api.base_resource import PostResource
from crud.schemas import SaleCreate, SaleItemCreate
from ..schemas.purchase_products import (
    Item,
    PurchaseProductsRequest,
    PurchaseProductsResponse,
)


class PurchaseProducts(PostResource):
    request_schema = PurchaseProductsRequest
    response_schema = PurchaseProductsResponse
    authentication_required = True

    # Endpoint details
    api_name = "purchase_products"
    api_url = "purchase_products"

    async def initialize(self):
        self.failed_purchases = []
        self.successful_purchases = []

    async def purchase_product(self, item: Item):
        # Important
        # This should ideally happen in a queue orchestrated by a task manager like Celery
        # to ensure that the inventory is updated only after the payment is successful
        # but for the sake of simplicity, we are doing it here

        # Get Product Information
        product = await crud.product.get_active(self.db, id=item.product_id)
        if not product:
            self.failed_purchases.append(item)
            return

        # Get Product Inventory Information
        inventories = await crud.inventory.get_by_product_id(
            self.db, product_id=item.product_id
        )
        if not inventories:
            self.failed_purchases.append(item)
            return

        # Ensure sum of inventory quantity is greater than or equal to requested quantity
        total_quantity = sum([x.quantity for x in inventories])
        if total_quantity < item.quantity:
            self.failed_purchases.append(item)
            return

        # Sort it by oldest inventories first
        inventories = sorted(inventories, key=lambda x: x.created_at)

        modified_inventories = []

        # Deplete Inventory
        left_quantity = item.quantity
        for inventory in inventories:
            if inventory.quantity >= left_quantity:
                inventory.quantity -= left_quantity
                left_quantity = 0
                modified_inventories.append(inventory)
                break
            else:
                left_quantity -= inventory.quantity
                inventory.quantity = 0
                modified_inventories.append(inventory)

        if modified_inventories:
            await crud.inventory.bulk_update(self.db, db_objs=modified_inventories)
            # Update Product
            await crud.product.update(
                self.db,
                db_obj=product,
                obj_in={"quantity": product.quantity - item.quantity},
            )

        # Create Sale Item object
        sale_item = SaleItemCreate(
            sale_id=0,  # to be populated later
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=product.price,
        )

        self.successful_purchases.append(sale_item)

    async def purchase_products(self):
        for item in self.request_data.items:
            await self.purchase_product(item)

    async def create_sales_data(self):
        self.sale = SaleCreate(
            user_id=context.data["user"]["id"],
            total_amount=sum(
                [x.quantity * x.price_per_unit for x in self.successful_purchases]
            ),
        )
        self.sale = await crud.sale.create(self.db, obj_in=self.sale)

        # Update Sale Item with sale_id
        for sale_item in self.successful_purchases:
            sale_item.sale_id = self.sale.id

        self.successful_purchases = await crud.sale_item.bulk_create(
            self.db, objs_in=self.successful_purchases
        )

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "Products purchased successfully"
        self.response_data = {
            **self.sale.to_dict(),
            "purchased_items": [x.to_dict() for x in self.successful_purchases],
            "failed_items": self.failed_purchases,
        }

    async def process_flow(self):
        await self.initialize()
        await self.purchase_products()
        await self.create_sales_data()
        await self.generate_response()
