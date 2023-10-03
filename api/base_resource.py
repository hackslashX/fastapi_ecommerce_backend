from abc import abstractmethod
from typing import Any

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_restful import Resource
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_context import context

from core.logger import Logger
from db.dependency import get_db


class FinalResponse(BaseModel):
    status_code: int
    success: bool
    message: str
    data: Any = None


class BaseResource(Resource):
    # add more things here later on...

    request_schema = None
    response_schema = None
    response_data = None
    authentication_required = False

    @abstractmethod
    async def process_flow(self):
        raise NotImplementedError

    async def run_preprocess(self, request: Request):
        if self.request_schema:
            self.request_data = self.request_schema(**request.state.data)

    async def run_postprocess(self):
        # Close DB connection
        await self.db.close()

        if (
            self.response_schema
            and not self.dont_postprocess
            and not self.early_response
        ):
            if isinstance(self.response_data, list):
                self.response_data = [
                    self.response_schema(**data) for data in self.response_data
                ]
            else:
                self.response_data = self.response_schema(**self.response_data)

        self.response_data = FinalResponse(
            status_code=self.status_code,
            success=self.success,
            message=self.response_message,
            data=self.response_data,
        )

        return JSONResponse(
            content=jsonable_encoder(self.response_data),
            status_code=self.status_code,
        )

    async def set_pre_request_vars(self):
        # Initialize Logger
        self.logger = Logger.get_logger(self.api_url, self.api_name)

    async def _base_req_params(self, request: Request, db: AsyncSession):
        self.dont_postprocess = False
        self.db = db
        self.request = request
        self.status_code = status.HTTP_200_OK
        self.success = True
        self.response_message = ""
        self.early_response = False

    async def _process_request(self, request: Request, db: AsyncSession):
        # Set pre request vars
        await self._base_req_params(request, db)
        await self.set_pre_request_vars()
        try:
            # Check authentication data
            if self.authentication_required and not context.data["user"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this resource",
                )
            # Run preprocess
            await self.run_preprocess(request)
            # Run API specific process flow
            await self.process_flow()
        # TODO: Add DB related exceptions too for rollback
        except HTTPException as e:
            await self.db.close()
            raise e
        except Exception as e:
            await self.db.close()
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.success = False
            self.logger.error(e)

            # Get errors from Pydantic if applicable
            errors = getattr(e, "errors", None)
            if errors:
                errors = errors()
                errors = {e["loc"]: e["msg"] for e in errors}
            else:
                errors = {}
            self.response_message = "We're unable to process your request at this time."
            self.response_data = errors
            self.dont_postprocess = True

        # Run postprocess
        return await self.run_postprocess()


class PostResource(BaseResource):
    async def post(self, request: Request, db: AsyncSession = Depends(get_db)):
        return await self._process_request(request=request, db=db)


class GetResource(BaseResource):
    async def get(self, request: Request, db: AsyncSession = Depends(get_db)):
        return await self._process_request(request=request, db=db)


class PutResource(BaseResource):
    async def put(self, request: Request, db: AsyncSession = Depends(get_db)):
        return await self._process_request(request=request, db=db)
