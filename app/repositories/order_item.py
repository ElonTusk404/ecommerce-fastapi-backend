from app.models.models import OrderItemModel
from app.utils.repository import SqlAlchemyRepository


class OrderItemRepository(SqlAlchemyRepository):
    model = OrderItemModel