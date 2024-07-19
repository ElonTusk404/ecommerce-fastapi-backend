from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.category import CategoryModel
from app.models.user import UserModel
from app.schemas.product import ProductCreate, ProductInDB, ProductUpdate
from app.services.product import ProductService
from app.utils.unit_of_work import UnitOfWork
from app.services.security import get_current_user, get_current_admin_user

product_router = APIRouter(prefix='/api/v1/product', tags=['Product\'s Admin'])

@product_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductInDB)
async def add_product(
    new_product_data: ProductCreate,
    admin_user: Annotated[UserModel, Depends(get_current_admin_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.add_one_and_get_obj(uow=uow, **new_product_data.model_dump(exclude_unset=True))