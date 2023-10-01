from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, DECIMAL, TIMESTAMP

from db.base_class import Base


class Sale(Base):
    """
    Sale Table
    """

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, index=True)
