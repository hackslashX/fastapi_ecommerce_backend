from typing import Union

import jwt
import crud
from datetime import datetime
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import HTTPConnection
from starlette_context.plugins import Plugin

from instance.config import config
from db.dependency import get_db


class AuthenticationContext(Plugin):
    """
    This plugin perform authentication and add necessary data inside the context
    """

    key = "user"

    async def process_request(self, request: Union[Request, HTTPConnection]):
        """
        This method will be called before processing the request
        """

        # Get bearer token from request header
        bearer_token = request.headers.get("Authorization", None)

        # If bearer token is not present, return
        if not bearer_token:
            return

        # Split the bearer token
        bearer_token = bearer_token.split(" ")[1]

        # Verify jwt token
        try:
            jwt_data = jwt.decode(
                bearer_token,
                key=config.JWT_CONFIG.JWT_SECRET_KEY,
                algorithms=[config.JWT_CONFIG.JWT_ALGORITHM],
            )
        except:
            return

        # Verify expiry
        if datetime.utcfromtimestamp(jwt_data["exp"]) < datetime.utcnow():
            return

        # Get user data
        _db = get_db()
        db: AsyncSession = await anext(_db)
        user = await crud.user.get(db, id=jwt_data["user_id"])
        await db.close()
        if not user:
            return

        return user.to_dict()
