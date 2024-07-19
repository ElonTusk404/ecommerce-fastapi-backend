from app.utils.service import BaseService
from typing import Optional, Union, Any, Sequence, Dict
from uuid import uuid4


from app.utils.unit_of_work import UnitOfWork

class CategoryService(BaseService):
    base_repository: str = 'category'


    @classmethod
    async def get_all_descendants(cls, uow: UnitOfWork, category_id: int) -> Dict:
        async with uow:
            category_repo = uow.__dict__[cls.base_repository]
            descendants_tree = await category_repo.get_all_descendants(category_id)
            return descendants_tree

    @classmethod
    async def get_all_ancestors(cls, uow: UnitOfWork, category_id: int) -> Dict:
        async with uow:
            category_repo = uow.__dict__[cls.base_repository]
            ancestors_tree = await category_repo.get_all_ancestors(category_id)
            return ancestors_tree
        
    @classmethod
    async def get_all_categories(cls, uow: UnitOfWork):
        async with uow:
            category_repo = uow.__dict__[cls.base_repository]
            all_categories_tree = await category_repo.get_all_categories()
            return all_categories_tree