from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.sale_item import SaleItem
from crud.schemas import SaleItemCreate, SaleItemUpdate


class CRUDSaleItem(CRUDBase[SaleItem, SaleItemCreate, SaleItemUpdate]):
    ...


sale_item = CRUDSaleItem(SaleItem)
