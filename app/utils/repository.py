from abc import ABC, abstractmethod
from typing import Dict, Sequence, Union, Type, Any
from uuid import uuid4
from sqlalchemy.orm import joinedload

from sqlalchemy import insert, select, update, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args, **kwargs):
        raise NotImplementedError

    async def add_one_and_get_obj(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_query_one_or_none(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_query(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """
    A basic repository that implements basic CRUD functions with a base table using the SqlAlchemy library

    params:
        - model: SQLAlchemy DeclarativeBase child class
    """

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def add_one_and_get_id(self, **kwargs) -> Union[int, str, uuid4]:
        query = insert(self.model).values(**kwargs).returning(self.model.id)
        _id: Result = await self.session.execute(query)
        return _id.scalar_one()

    async def add_one_and_get_obj(self, **kwargs) -> Type[model]: # type: ignore
        query = insert(self.model).values(**kwargs).returning(self.model)
        _obj: Result = await self.session.execute(query)
        return _obj.unique().scalar_one()

    async def get_by_query_one_or_none(self, **kwargs) -> Type[model]: # type: ignore
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalar_one_or_none()

    async def get_by_query_all(self, **kwargs) -> Sequence[Type[model]]: # type: ignore
        query = select(self.model).filter_by(**kwargs)
        res: Result = await self.session.execute(query)
        return res.unique().scalars().all()
    
    async def get_by_query_with_limit(self, limit: int, offset: int = 0, **kwargs) -> Sequence[Type[model]]: # type: ignore
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .limit(limit)
            .offset(offset)
        )
        res: Result = await self.session.execute(query)
        return res.unique().scalars().all()

    async def update_one_by_id(self, _id: int, **values) -> Type[model]: # type: ignore
 

        query = update(self.model).filter(self.model.id == _id).values(**values).returning(self.model)
        _obj: Result | None = await self.session.execute(query)
        return _obj.unique().scalar_one_or_none()

    async def delete_by_query(self, **kwargs) -> None:
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_all(self) -> None:
        query = delete(self.model)
        await self.session.execute(query)