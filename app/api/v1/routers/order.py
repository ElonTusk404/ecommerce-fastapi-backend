from http.cookiejar import Cookie
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Query, WebSocketException, status, Depends, WebSocket, WebSocketDisconnect
import websockets
from app.services.security import get_current_admin_user, get_current_user, verify_ws_token
from app.services.order import OrderService
from app.services.order_item import OrderItemService
from app.schemas.order import OrderSchemaCreate, OrderSchemaResponse
from app.services.cart import CartService
from app.utils.unit_of_work import UnitOfWork
from app.models.user import UserModel
from app.services.inventory import InventoryService
from app.models.models import OrderStatus
order_router = APIRouter(prefix='/api/v1/order', tags = ['Orders'])

admins: List[WebSocket] = []



@order_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_order(
    delivery_details: OrderSchemaCreate,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    cart_info = await CartService.get_by_query_all(uow=uow, user_id=user.id)
    if not cart_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    total_amount_sum=0
    new_order_id = await OrderService.add_one_and_get_id(uow=uow, status=OrderStatus.pending, user_id=user.id, total_amount=0, **delivery_details.model_dump(exclude_unset=True))
    for inventory in cart_info:
        if inventory.product.inventory.quantity-inventory.quantity<0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Товара с Айди {inventory.product.id} в количестве {inventory.quantity} нет на складе')
    for cart_item in cart_info:
        await OrderItemService.add_one(
            uow=uow,
            order_id = new_order_id,
            product_id=cart_item.product_id,
            quantity = cart_item.quantity,
            price = cart_item.product.price
        )
        total_amount_sum+=cart_item.quantity*cart_item.product.price
        await InventoryService.update_one_by_id(uow=uow, _id=cart_item.product.inventory.id, quantity=cart_item.product.inventory.quantity-cart_item.quantity)
    await CartService.delete_by_query(uow=uow, user_id=user.id)
    for admin in admins:
        try:
            await admin.send_text(f'New Order with id {new_order_id}')
        except WebSocketDisconnect:
            admins.remove(admin)
    return await OrderService.update_one_by_id(uow=uow, _id=new_order_id, total_amount = total_amount_sum)

@order_router.get('/{order_id}', status_code=status.HTTP_200_OK, response_model=OrderSchemaResponse)
async def get_order_info(
    order_id: int,
    user: Annotated[UserModel, Depends(get_current_user)],
    uow: UnitOfWork = Depends(UnitOfWork)
):
    order_info = await OrderService.get_by_query_one_or_none(
        uow=uow,
        id=order_id
    )
    
    if order_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if user.role != 'admin' and order_info.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this order")
    
    return order_info



@order_router.websocket('/ws')
async def websocket_orders(
    websocket: WebSocket,
    uow: UnitOfWork = Depends(UnitOfWork)
): 
    token = websocket.headers.get('Authorization')
    user = await verify_ws_token(token, uow=uow)
    await websocket.accept()
    admins.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
    except WebSocketDisconnect:
        admins.remove(websocket)



