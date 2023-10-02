from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP

from db.base_class import Base


class Category(Base):
    """
    Category Table
    """

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, index=True)
    category_slug = Column(String(50), nullable=False, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
