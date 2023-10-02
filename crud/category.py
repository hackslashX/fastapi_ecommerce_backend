from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.category import Category
from crud.schemas import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[Category]:
        async with db as session:
            stmt = select(self.model).filter(self.model.category_slug == slug)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


category = CRUDCategory(Category)
