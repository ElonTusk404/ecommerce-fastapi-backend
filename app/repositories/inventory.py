from app.models.inventory import InventoryModel
from app.utils.repository import SqlAlchemyRepository


class InventoryRepository(SqlAlchemyRepository):
    model = InventoryModel