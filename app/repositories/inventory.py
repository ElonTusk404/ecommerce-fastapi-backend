from app.models.models import InventoryModel
from app.utils.repository import SqlAlchemyRepository


class InventoryRepository(SqlAlchemyRepository):
    model = InventoryModel