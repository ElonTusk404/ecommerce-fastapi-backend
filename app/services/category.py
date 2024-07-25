from app.utils.service import BaseService
from typing import Optional, Union, Any, Sequence, Dict
from uuid import uuid4


from app.utils.unit_of_work import UnitOfWork

class CategoryService(BaseService):
    base_repository: str = 'category'
