from app.models.models import CartModel
from app.utils.repository import SqlAlchemyRepository


class CartRepository(SqlAlchemyRepository):
    model = CartModel