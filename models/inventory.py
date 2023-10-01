from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, TIMESTAMP

from db.base_class import Base


class Inventory(Base):
    """
    Inventory Table
    """

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
