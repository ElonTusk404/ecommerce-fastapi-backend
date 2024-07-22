from app.models.models import ProductModel
from app.utils.repository import SqlAlchemyRepository
from sqlalchemy.orm import joinedload
from sqlalchemy import Result, select
from typing import Type

class ProductRepository(SqlAlchemyRepository):
    model = ProductModel

    async def get_full_product_info(self, **kwargs) -> ProductModel:
        query = select(self.model).options(
            joinedload(ProductModel.images),
            joinedload(ProductModel.inventory),
            joinedload(ProductModel.attributes),
            joinedload(ProductModel.category)
        ).filter_by(**kwargs)

        
        result = await self.session.execute(query)
        product = result.scalars().first()
        if product:
            return product
        return None