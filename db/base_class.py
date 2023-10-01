import re
from typing import Any
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all models."""

    id: Any

    @declared_attr
    def __tablename__(cls):
        """Convert class name to snake case for table name."""
        return "_".join(re.findall(r"[A-Z][^A-Z]*", cls.__name__)).lower()

    def to_dict(self):
        ret = {}
        for key in self.__mapper__.c.keys():
            ret[key] = getattr(self, key)
        return ret
