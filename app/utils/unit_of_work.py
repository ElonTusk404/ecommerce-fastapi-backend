from abc import ABC, abstractmethod

from app.database.db import async_session_maker
from app.repositories.category import CategoryRepository
from app.repositories.inventory import InventoryRepository
from app.repositories.user import UserRepository
from app.repositories.product import ProductRepository
from app.repositories.image import ImageRepository
from app.repositories.attribute import AttributeRepository
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.repositories.order_item import OrderItemRepository


class AbstractUnitOfWork(ABC):
    user: UserRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions"""

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.product = ProductRepository(self.session)
        self.image = ImageRepository(self.session)
        self.inventory = InventoryRepository(self.session)
        self.attribute = AttributeRepository(self.session)
        self.cart = CartRepository(self.session)
        self.order = OrderRepository(self.session)
        self.order_item = OrderItemRepository(self.session)

    async def __aexit__(self, exc_type, *args):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()