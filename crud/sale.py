from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.sale import Sale
from crud.schemas import SaleCreate, SaleUpdate


class CRUDSale(CRUDBase[Sale, SaleCreate, SaleUpdate]):
    ...


sale = CRUDSale(Sale)
