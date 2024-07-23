from app.utils.service import BaseService


class OrderService(BaseService):
    base_repository: str = 'order'