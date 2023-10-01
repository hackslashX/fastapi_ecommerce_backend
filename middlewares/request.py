"""
Request Middleware
==================
This module contains the request middleware for the API. The request middleware
basically checks form_data, body, query_params and converts them to a dictionary
"""

import json
from fastapi import Request


class RequestPreProcessor(object):
    async def __call__(self, request: Request, call_next) -> dict:
        """
        The order of precedence is:
        1. body (json)
        2. form_data
        3. query_params
        """
        return_dict = {}

        # Process query_params
        if request.query_params:
            try:
                return_dict.update(dict(request.query_params))
            except:
                pass

        # Process body
        body = await request.body()
        if body:
            try:
                return_dict.update(json.loads(body))
            except:
                pass

        # Process form_data
        form = await request.form()
        if form:
            try:
                return_dict.update(dict(form))
            except:
                pass

        request.state.data = return_dict

        response = await call_next(request)
        return response
