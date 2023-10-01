from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from api.v1.routing import RoutingV1
from middlewares import RequestPreProcessor

# Global app variable
app = FastAPI()


# Middlewares
"""
Order of precedence is important here.
1. Request Middleware
2. Decyrption Middleware
3. Context Plugin Middleware
"""
app.add_middleware(BaseHTTPMiddleware, dispatch=RequestPreProcessor())
# app.add_middleware(
#     RawContextMiddleware,
#     plugins=(
#         SecretsContext(),
#         ConfigContext(),
#         plugins.RequestIdPlugin(),
#         plugins.CorrelationIdPlugin(),
#     ),
# )


# Routing Information
"""
Add versioned routing information here
"""
RoutingV1(app).map_urls()
