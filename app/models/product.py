from app.database.db import Base
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

class ProductModel(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'))
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @property
    def images(self):
        from app.models.image import ImageModel
        return relationship("ImageModel", back_populates="product", lazy='subquery')

    @property
    def inventory(self):
        from app.models.inventory import InventoryModel
        return relationship("InventoryModel", uselist=False, back_populates="product", lazy='subquery')

    @property
    def values(self):
        from app.models.attribute import ValueModel
        return relationship("ValueModel", back_populates="product", lazy='subquery')

    @property
    def category(self):
        from app.models.category import CategoryModel
        return relationship("CategoryModel", backref="products", lazy='subquery')
