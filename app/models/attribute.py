from app.database.db import Base
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

class AttributeModel(Base):
    __tablename__ = 'attribute'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class ValueModel(Base):
    __tablename__ = 'value'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey('attribute.id'), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @property
    def product(self):
        from app.models.product import ProductModel
        return relationship("ProductModel", back_populates="values")

    @property
    def attribute(self):
        from app.models.attribute import AttributeModel
        return relationship("AttributeModel")
