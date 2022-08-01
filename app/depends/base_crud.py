import uuid
from typing import Optional, Type

from abc import ABC

from pydantic import BaseModel
from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError

from db.session import DbSessionProvider
from db.base_model import BaseModel as BaseDBModel
from errors import UnexpectedError


class BaseCRUD:
    def __init__(self):
        """ Create session for each instance """
        self.master_session = self.get_session

    def get_session(self):
        return DbSessionProvider.get_session()


class CRUD(BaseCRUD, ABC):
    """ Class implement basic CRUD.
       Attributes:
           model - orm model (required)
           schema - pydantic schema for object (required)
           list_schema - pydantic schema for collection of object (required)
           query - preliminary query (optional)
    """
    model: BaseDBModel
    input_schema: Type[BaseModel]
    schema: Type[BaseModel]
    list_schema: Type[BaseModel]
    id_name: str
    query: Optional[str] = None

    async def get_all(self, limit: int = None, offset: int = None) -> BaseModel:
        query = self.query

        if not query:
            query = select(self.model)

        if limit:
            query = query.limit(limit).offset(offset)

        if offset:
            query = query.offset(offset)

        async with self.get_session() as session:
            result = await session.execute(query)
            objs = result.scalars().all()
            print(objs)
            return self.list_schema.from_orm(objs)

    async def get_one(self, key: uuid.UUID) -> Optional[BaseModel]:
        self.query = select(self.model).where(self.model.id == key)

        async with self.get_session() as session:
            result = await session.execute(self.query)
            obj = result.scalars().first()
            return self.schema.from_orm(obj) if obj else None

    async def is_exist(self, key: uuid.UUID) -> bool:
        self.query = select(exists(self.model.id)).where(self.model.id == key)
        async with self.get_session() as session:
            result = await session.execute(self.query)
            return result.scalars().first()

    async def create(self, data: BaseModel) -> Optional[BaseModel]:
        instance = self.model(**data.dict(exclude_defaults=True))

        async with self.get_session() as session:
            session.add(instance)
            try:
                await session.flush()
                return self.schema.from_orm(instance)
            except IntegrityError as e:
                error_message = ""
                if "duplicate key value" in str(e):
                    error_message = "Already exists"
                raise UnexpectedError(e,
                                      message=f"{error_message} " + str(e),
                                      code=400
                                      )
