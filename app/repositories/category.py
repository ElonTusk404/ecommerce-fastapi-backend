from typing import Dict, List
from sqlalchemy.orm import aliased

from sqlalchemy import select
from app.models.models import CategoryModel
from app.utils.repository import SqlAlchemyRepository


class CategoryRepository(SqlAlchemyRepository):
    model = CategoryModel

    async def get_all_descendants(self, category_id: int):
        async def build_tree(categories, parent_id=None):
            tree = []
            for category in categories:
                if category.parent_id == parent_id:
                    children = await build_tree(categories, category.id)
                    tree.append({
                        "id": category.id,
                        "name": category.name,
                        "children": children
                    })
            return tree

        query = select(CategoryModel)
        result = await self.session.execute(query)
        categories = result.scalars().all()

        return await build_tree(categories, category_id)

    async def get_all_ancestors(self, category_id: int):
        ancestors = []
        current_id = category_id

        while current_id is not None:
            query = select(CategoryModel).filter_by(id=current_id)
            result = await self.session.execute(query)
            category = result.scalar_one_or_none()
            if category:
                ancestors.append({"id": category.id, "name": category.name})
                current_id = category.parent_id
            else:
                break

        return ancestors[::-1]
    
    async def get_all_categories(self):
        async def build_tree(categories, parent_id=None):
            tree = []
            for category in categories:
                if category.parent_id == parent_id:
                    children = await build_tree(categories, category.id)
                    tree.append({
                        "id": category.id,
                        "name": category.name,
                        "children": children
                    })
            return tree

        query = select(CategoryModel)
        result = await self.session.execute(query)
        categories = result.scalars().all()

        return await build_tree(categories)