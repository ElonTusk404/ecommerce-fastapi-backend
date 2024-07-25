from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.product import ProductSchemaInDB, ProductSchemaResponse
from app.services.product import ProductService
from typing import List
from fastapi_cache.decorator import cache

from app.utils.unit_of_work import UnitOfWork

catalog_router = APIRouter(prefix='/api/v1/catalog', tags=['Catalog'])


@catalog_router.get('/{limit}/{offset}', status_code=status.HTTP_200_OK, response_model=List[ProductSchemaInDB])
@cache(expire=30)
async def get_products_with_limit(
    limit: int, 
    offset: int, 
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.get_by_query_with_limit(uow=uow, limit=limit, offset=offset)
@cache(expire=30)
@catalog_router.get('/category/{category_id}/{limit}/{offset}', status_code=status.HTTP_200_OK, response_model=List[ProductSchemaInDB])
async def get_products_with_limit_via_category(
    category_id: int,
    limit: int,
    offset: int,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await ProductService.get_by_query_with_limit(uow=uow, limit=limit, offset=offset, category_id=category_id)


@catalog_router.get('/{product_id}', response_model=ProductSchemaResponse)
@cache(expire=30)
async def get_product_info(
    product_id: int,
    uow: UnitOfWork = Depends(UnitOfWork)
):
    product = await ProductService.get_by_query_one_or_none(uow=uow, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product