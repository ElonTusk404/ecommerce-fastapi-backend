from app.utils.service import BaseService


class InventoryService(BaseService):
    base_repository: str = 'inventory'