from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from core.security import get_password_hash
from crud.base import CRUDBase
from models.user import User
from crud.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            db (AsyncSession): SQLAlchemy session
            email (str): The email

        Returns:
            Optional[User]: The user object or None
        """

        async with db as session:
            stmt = select(self.model).filter(self.model.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """Create a new user.

        Args:
            db (AsyncSession): SQLAlchemy session
            obj_in (UserCreate): The user object

        Returns:
            User: The created user object
        """

        # Create the user, and hash the password
        obj_in = jsonable_encoder(obj_in)
        obj_in["hashed_password"] = get_password_hash(obj_in.pop("password"))
        # Commit the user to the database
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """Update a user.

        Args:
            db (AsyncSession): SQLAlchemy session
            db_obj (User): The user object
            obj_in UserUpdate: The user object with the new values

        Returns:
            User: The updated user object
        """

        # Check user object type
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # If the password is set, hash it
        if update_data.new_password:
            hashed_password = get_password_hash(update_data.new_password)
            update_data.hashed_password = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    async def touch_last_login(self, db: AsyncSession, *, db_obj: User) -> User:
        """Update the last login time of a user.

        Args:
            db (AsyncSession): SQLAlchemy session
            db_obj (User): The user object

        Returns:
            User: The updated user object
        """

        async with db as session:
            db_obj.last_login = datetime.utcnow()
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj


user = CRUDUser(User)
