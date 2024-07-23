from sqlalchemy import Enum, Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database.db import Base
from enum import Enum as PyEnum

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
    cart_items = relationship("CartModel", back_populates="product", lazy='select')
    order_items = relationship("OrderItemModel", back_populates="product", lazy='joined')
# Image Model
class ImageModel(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    
    product = relationship("ProductModel", back_populates="images")

class InventoryModel(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product = relationship("ProductModel", back_populates="inventory")

class AttributeModel(Base):
    __tablename__ = 'attribute'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    product = relationship("ProductModel", back_populates="attributes")

class CartModel(Base):
    __tablename__ = 'cart'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable = False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    product = relationship("ProductModel", back_populates="cart_items", lazy='joined')
    user = relationship("UserModel", back_populates="cart_items", lazy='select')
    

class OrderStatus(PyEnum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)  
    country: Mapped[str] = mapped_column(String(50), nullable=False)       
    city: Mapped[str] = mapped_column(String(50), nullable=False)          
    address: Mapped[str] = mapped_column(String(100), nullable=False)      

    user = relationship("UserModel", back_populates="orders")
    order_items = relationship("OrderItemModel", back_populates="order", lazy='joined')

class OrderItemModel(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Integer, nullable=False)

    order = relationship("OrderModel", back_populates="order_items")
    product = relationship("ProductModel", back_populates="order_items", lazy='joined')
