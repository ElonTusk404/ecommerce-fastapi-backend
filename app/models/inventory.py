from app.database.db import Base
from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class InventoryModel(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    @property
    def product(self):
        from app.models.product import ProductModel
        return relationship("ProductModel", back_populates="inventory")

    __table_args__ = (
        UniqueConstraint('product_id', name='uq_product_id'),
    )
