from app.utils.service import BaseService
from app.utils.unit_of_work import UnitOfWork
from typing import Optional, Any


class ProductService(BaseService):
    base_repository: str = 'product'

    @classmethod
    async def get_full_product_info(
            cls,
            uow: UnitOfWork,
            **kwargs
    ) -> Optional[Any]:
        async with uow:
            _result = await uow.__dict__[cls.base_repository].get_full_product_info(**kwargs)
            return _result