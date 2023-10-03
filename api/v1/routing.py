from api.base_routing import BaseRouting

from .endpoints.register_user import RegisterUser
from .endpoints.login_user import LoginUser
from .endpoints.create_product import CreateProduct
from .endpoints.add_inventory import AddInventory
from .endpoints.get_product import GetProduct
from .endpoints.get_low_stock_products import GetLowStockProducts
from .endpoints.purchase_products import PurchaseProducts
from .endpoints.create_category import CreateCategory
from .endpoints.get_categories import GetCategories
from .endpoints.get_products import GetProducts
from .endpoints.get_sales_data import GetSalesData


class RoutingV1(BaseRouting):
    api_version: str = "v1"

    def set_routing_collection(self):
        self.routing_collection[RegisterUser.api_name] = (
            RegisterUser(),
            RegisterUser.api_url,
        )
        self.routing_collection[LoginUser.api_name] = (LoginUser(), LoginUser.api_url)
        self.routing_collection[CreateProduct.api_name] = (
            CreateProduct(),
            CreateProduct.api_url,
        )
        self.routing_collection[AddInventory.api_name] = (
            AddInventory(),
            AddInventory.api_url,
        )
        self.routing_collection[GetProduct.api_name] = (
            GetProduct(),
            GetProduct.api_url,
        )
        self.routing_collection[GetLowStockProducts.api_name] = (
            GetLowStockProducts(),
            GetLowStockProducts.api_url,
        )
        self.routing_collection[PurchaseProducts.api_name] = (
            PurchaseProducts(),
            PurchaseProducts.api_url,
        )
        self.routing_collection[CreateCategory.api_name] = (
            CreateCategory(),
            CreateCategory.api_url,
        )
        self.routing_collection[GetCategories.api_name] = (
            GetCategories(),
            GetCategories.api_url,
        )
        self.routing_collection[GetProducts.api_name] = (
            GetProducts(),
            GetProducts.api_url,
        )
        self.routing_collection[GetSalesData.api_name] = (
            GetSalesData(),
            GetSalesData.api_url,
        )
