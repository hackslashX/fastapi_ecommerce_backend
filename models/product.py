from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, TEXT, DECIMAL

from db.base_class import Base


class Product(Base):
    """
    Product Table
    """

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(50), nullable=False, index=True)
    description = Column(TEXT, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, default=0)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
