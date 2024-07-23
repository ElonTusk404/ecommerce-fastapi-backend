from app.models.models import OrderModel
from app.utils.repository import SqlAlchemyRepository


class OrderRepository(SqlAlchemyRepository):
    model = OrderModel