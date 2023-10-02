from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Iterable

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        async with db as session:
            stmt = select(self.model).filter(self.model.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, page: int, per_page: int, order_by: str, order: str
    ) -> Iterable[ModelType]:
        async with db as session:
            if not getattr(self.model, order_by, None):
                order_by = "id"
            stmt = (
                select(self.model)
                .order_by(text(f"{order_by} {order}"))
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        async with db as session:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        async with db as session:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def bulk_update(
        self, db: AsyncSession, *, db_objs: List[ModelType]
    ) -> List[ModelType]:
        async with db as session:
            for db_obj in db_objs:
                session.add(db_obj)
            await session.commit()
            return db_objs

    async def bulk_create(
        self, db: AsyncSession, *, objs_in: CreateSchemaType
    ) -> List[ModelType]:
        async with db as session:
            db_objs = []
            for obj_in in objs_in:
                obj_in_data = jsonable_encoder(obj_in)
                db_obj = self.model(**obj_in_data)  # type: ignore
                db_objs.append(db_obj)
                session.add(db_obj)
            await session.commit()
            return db_objs

    async def remove(self, db: AsyncSession, *, id: int):
        async with db as session:
            stmt = delete(self.model).filter(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
