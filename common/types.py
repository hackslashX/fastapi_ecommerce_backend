import pytz
from datetime import datetime
from typing import Annotated
from pydantic import PlainSerializer
from pydantic.v1.json import isoformat
from starlette_context import context


def tz_aware_conversion(o: datetime) -> str:
    try:
        user = context.data["user"]
        timezone = user["timezone"]
        local_time = o.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
        return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    except:
        return isoformat(o)


TzDateTime = Annotated[datetime, PlainSerializer(tz_aware_conversion)]
