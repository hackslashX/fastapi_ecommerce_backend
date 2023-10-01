from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.product import Product
from crud.schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_products_quantity_le(
        self, db: AsyncSession, *, quantity: int
    ) -> Iterable[Product]:
        async with db as session:
            stmt = select(self.model).filter(self.model.quantity <= quantity)
            results = await session.execute(stmt)
            return results.scalars().all()

    async def get_active(self, db: AsyncSession, *, id: int) -> Optional[Product]:
        async with db as session:
            stmt = select(self.model).filter(
                self.model.id == id, self.model.is_active == True
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


product = CRUDProduct(Product)
