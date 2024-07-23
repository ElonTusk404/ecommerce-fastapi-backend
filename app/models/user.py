from app.database.db import Base
from sqlalchemy import Integer, String, Column, BigInteger, DateTime, func, ForeignKey, JSON, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

class UserModel(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable = False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default='user')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    cart_items = relationship("CartModel", back_populates="user")
    orders = relationship("OrderModel", back_populates="user")
    