from app.utils.service import BaseService


class CartService(BaseService):
    base_repository: str = 'cart'