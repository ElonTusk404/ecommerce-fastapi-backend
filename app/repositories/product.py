from app.models.models import ProductModel
from app.utils.repository import SqlAlchemyRepository
from sqlalchemy.orm import joinedload
from sqlalchemy import Result, select
from typing import Type

class ProductRepository(SqlAlchemyRepository):
    model = ProductModel