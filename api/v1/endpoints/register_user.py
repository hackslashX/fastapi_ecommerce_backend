from fastapi import status

import crud
from api.base_resource import PutResource
from crud.schemas import User, UserCreate


class RegisterUser(PutResource):
    request_schema = UserCreate
    response_schema = User
    authentication_required = False

    # Endpoint details
    api_name = "register_user"
    api_url = "register_user"

    async def check_user_exists(self):
        user = await crud.user.get_by_email(self.db, email=self.request_data.email)
        if user:
            self.early_response = True
            self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            self.response_message = "User with specified email already exists."
            self.response_data = {}

    async def create_account(self):
        user = await crud.user.create(self.db, obj_in=self.request_data)
        self.response_data = user.to_dict()
        self.status_code = status.HTTP_200_OK
        self.respone_message = "User created successfully."

    async def process_flow(self):
        # First check if the user already exists
        await self.check_user_exists()
        if self.early_response:
            return

        # Create the account
        await self.create_account()
