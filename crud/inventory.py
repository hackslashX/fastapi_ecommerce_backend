from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.inventory import Inventory
from crud.schemas import InventoryCreate, InventoryUpdate


class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    async def get_by_product_id(
        self, db: AsyncSession, *, product_id: int
    ) -> Iterable[Inventory]:
        async with db as session:
            stmt = select(self.model).filter(self.model.product_id == product_id)
            results = await session.execute(stmt)
            return results.scalars().all()


inventory = CRUDInventory(Inventory)
