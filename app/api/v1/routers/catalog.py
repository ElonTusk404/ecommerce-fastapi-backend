from fastapi import APIRouter, status, Depends
from app.schemas.product import ProductInDB
from app.services.product import ProductService
from typing import List

from app.utils.unit_of_work import UnitOfWork

catalog_router = APIRouter(prefix='/api/v1/catalog', tags=['Catalog'])

@catalog_router.get('/{limit}/{offset}', status_code=status.HTTP_200_OK, response_model=List[ProductInDB])
async def get_products_with_limit(
    limit: int, 
    offset: int, 
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.get_by_query_with_limit(uow=uow, limit=limit, offset=offset)

@catalog_router.get('/category/{category_id}/{limit}/{offset}', status_code=status.HTTP_200_OK, response_model=List[ProductInDB])
async def get_products_with_limit_via_category(
    category_id: int,
    limit: int,
    offset: int,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.get_by_query_with_limit(uow=uow, limit=limit, offset=offset, category_id=category_id)