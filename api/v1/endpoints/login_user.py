from fastapi import status

import crud
from models.user import User
from api.base_resource import PostResource
from core.security import verify_password, create_jwt_token
from ..schemas.login_user import UserLoginRequest, UserLoginResponse


class LoginUser(PostResource):
    request_schema = UserLoginRequest
    response_schema = UserLoginResponse
    authentication_required = False

    # Endpoint details
    api_name = "login_user"
    api_url = "login_user"

    async def check_user_exists(self):
        self.user: User = await crud.user.get_by_email(
            self.db, email=self.request_data.email
        )
        if not self.user:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "User with specified credentials does not exists."
            self.response_data = {}

    async def verify_password(self):
        password_check = verify_password(
            self.request_data.password, self.user.hashed_password
        )
        if not password_check:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "User with specified credentials does not exists."
            self.response_data = {}

    async def generate_access_token(self):
        payload = {
            "user_id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        self.access_token = create_jwt_token(payload=payload, typ="access")

    async def touch_last_login(self):
        await crud.user.touch_last_login(self.db, db_obj=self.user)

    async def generate_response(self):
        self.status_code = status.HTTP_200_OK
        self.response_message = "User logged in successfully"
        self.response_data = {"access_token": self.access_token}

    async def process_flow(self):
        # First check if the user already exists
        await self.check_user_exists()
        if self.early_response:
            return

        # Verify Password
        await self.verify_password()
        if self.early_response:
            return

        # Process login flow
        await self.generate_access_token()
        await self.touch_last_login()
        await self.generate_response()
