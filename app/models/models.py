from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database.db import Base

# Category Model
class CategoryModel(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    parent = relationship("CategoryModel", remote_side=[id], back_populates="children")
    products = relationship("ProductModel", back_populates="category")
    children = relationship("CategoryModel", back_populates="parent", remote_side=[parent_id])

# Product Model
class ProductModel(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'))
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    images = relationship("ImageModel", back_populates="product", lazy='subquery')
    inventory = relationship("InventoryModel", uselist=False, back_populates="product", lazy='subquery')
    attributes = relationship("AttributeModel", back_populates="product", lazy='subquery')
    category = relationship("CategoryModel", back_populates="products", lazy='subquery')

# Image Model
class ImageModel(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    
    product = relationship("ProductModel", back_populates="images")

# Inventory Model
class InventoryModel(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product = relationship("ProductModel", back_populates="inventory")

# Attribute Model
class AttributeModel(Base):
    __tablename__ = 'attribute'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    product = relationship("ProductModel", back_populates="attributes")
