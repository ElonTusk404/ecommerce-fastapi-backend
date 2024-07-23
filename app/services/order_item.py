from app.utils.service import BaseService


class OrderItemService(BaseService):
    base_repository: str = 'order_item'