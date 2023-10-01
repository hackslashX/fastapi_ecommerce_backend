import datetime
from starlette_context import context

from pydantic.v1.json import ENCODERS_BY_TYPE, isoformat


def tz_aware_conversion(o: datetime.datetime) -> str:
    try:
        user = context.data["user"]
        timezone = user["timezone"]
        return o.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return isoformat(o)


ENCODERS_BY_TYPE[datetime.datetime] = tz_aware_conversion
