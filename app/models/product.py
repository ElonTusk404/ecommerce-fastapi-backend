from app.database.db import Base
from sqlalchemy import Integer, String, Column, BigInteger, DateTime, func, ForeignKey, JSON, Date, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database.db import Base
from sqlalchemy import Integer, String, Column, DateTime
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

    images = relationship("ImageModel", back_populates="product")
    inventory = relationship("InventoryModel", uselist=False, back_populates="product")
    values = relationship("ValueModel", back_populates="product")

    category = relationship("CategoryModel", backref="products")