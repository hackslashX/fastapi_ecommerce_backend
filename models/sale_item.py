from sqlalchemy import ForeignKey, Column, Integer, DECIMAL

from db.base_class import Base


class SaleItem(Base):
    """
    Sale Item Table
    """

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sale.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(DECIMAL(10, 2), nullable=False)
