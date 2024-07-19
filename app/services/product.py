from app.utils.service import BaseService
from app.utils.unit_of_work import UnitOfWork
from typing import Optional, Any


class ProductService(BaseService):
    base_repository: str = 'product'