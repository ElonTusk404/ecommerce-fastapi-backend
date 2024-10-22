from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserModel
from app.schemas.category import CategorySchemaCreate, CategorySchemaInDB, CategoryResponse, CategorySchemaUpdate
from app.services.category import CategoryService
from app.utils.unit_of_work import UnitOfWork
from app.services.security import get_current_admin_user

category_router = APIRouter(prefix='/api/v1/categorys', tags=['Category\'s Admin'])

@category_router.post('', status_code=status.HTTP_201_CREATED, response_model=CategorySchemaInDB)
async def create_category(new_category_data: CategorySchemaCreate, admin_user: Annotated[UserModel, Depends(get_current_admin_user)], uow: UnitOfWork = Depends(UnitOfWork)):
    exists_category = await CategoryService.get_by_query_one_or_none(uow=uow, name = new_category_data.name)
    if exists_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Category with name {new_category_data.name} already exists')
    new_category = await CategoryService.add_one_and_get_obj(uow=uow, **new_category_data.model_dump(exclude_unset=True))
    return new_category


@category_router.get('', response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_main_categories(uow: UnitOfWork = Depends(UnitOfWork)):
    return await CategoryService.get_by_query_all(uow=uow, parent_id=None)
