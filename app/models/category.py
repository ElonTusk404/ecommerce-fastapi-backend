from app.database.db import Base
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

class CategoryModel(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @property
    def parent(self):
        return relationship("CategoryModel", remote_side=[self.id], backref="children")
