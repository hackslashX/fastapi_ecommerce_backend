from crud.schemas import Inventory, InventoryCreate


class AddInventoryRequest(InventoryCreate):
    ...


class AddInventoryResponse(Inventory):
    ...
