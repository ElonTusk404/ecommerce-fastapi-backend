from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, List
from app.models.user import UserModel
from app.services.security import get_current_user
from app.utils.unit_of_work import UnitOfWork
from app.services.cart import CartService
from app.schemas.cart import CartSchemaCreate, CartSchemaInDB, CartSchemaUpdate
cart_router = APIRouter(prefix = '/api/v1/cart', tags = ['Cart'])

@cart_router.get('', status_code = status.HTTP_200_OK, response_model=List[CartSchemaInDB])
async def get_user_cart(
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    return await CartService.get_by_query_all(uow=uow, user_id = user.id)

@cart_router.post('/{id}', status_code = status.HTTP_201_CREATED)
async def add_product_to_cart(
    id: int,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    exists_product_in_cart = await CartService.get_by_query_one_or_none(uow=uow, user_id=user.id, product_id=id)
    if exists_product_in_cart:
        return await CartService.update_one_by_id(uow=uow, _id=exists_product_in_cart.id, quantity = exists_product_in_cart.quantity+1)

    return await CartService.add_one_and_get_obj(
        uow=uow,
        user_id = user.id,
        product_id = id,
        quantity = 1
    )

@cart_router.patch('/{id}', status_code=status.HTTP_200_OK)
async def update_cart_item(
    id: int,
    new_data: CartSchemaUpdate,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    cart_item = await CartService.get_by_query_all(uow=uow, id=id, user_id=user.id)

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    result = await CartService.update_one_by_id(uow=uow, _id=id, **new_data.model_dump(exclude_unset=True))

@cart_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    cart_items = await CartService.get_by_query_all(uow=uow, user_id=user.id)
    
    if not cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is already empty")

    await CartService.delete_by_query(uow=uow, user_id=user.id)
    


@cart_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    id: int,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    cart_item = await CartService.get_by_query_one_or_none(uow=uow, id=id)
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if cart_item.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await CartService.delete_by_query(uow=uow, id=id)

