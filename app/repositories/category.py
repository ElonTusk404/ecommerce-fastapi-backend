from typing import Dict, List
from sqlalchemy.orm import aliased

from sqlalchemy import select
from app.models.models import CategoryModel
from app.utils.repository import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository):
    model = CategoryModel