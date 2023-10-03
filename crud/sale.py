from typing import Iterable
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.sale import Sale
from models.product import Product
from models.category import Category
from models.sale_item import SaleItem
from crud.schemas import SaleCreate, SaleUpdate


class CRUDSale(CRUDBase[Sale, SaleCreate, SaleUpdate]):
    async def get_sales_data(
        self,
        db: AsyncSession,
        *,
        start_date: datetime,
        end_date: datetime,
        product_ids: list[int],
        category_ids: list[int]
    ) -> Iterable:
        async with db as session:
            stmt = select(
                self.model.id,
                self.model.user_id,
                self.model.created_at,
                Product.product_name,
                Product.description,
                SaleItem.product_id,
                SaleItem.price_per_unit,
                SaleItem.quantity,
                Product.category_id,
                Category.category_name,
                Category.category_slug,
            )
            stmt = (
                stmt.join(
                    SaleItem,
                    SaleItem.sale_id == self.model.id,
                )
                .join(
                    Product,
                    Product.id == SaleItem.product_id,
                )
                .join(Category, Category.id == Product.category_id)
            )
            stmt = stmt.filter(self.model.created_at.between(start_date, end_date))
            if product_ids:
                stmt = stmt.filter(SaleItem.product_id.in_(product_ids))
            elif category_ids:
                stmt = stmt.filter(Category.id.in_(category_ids))

            results = await session.execute(stmt)
            return results.all()


sale = CRUDSale(Sale)
