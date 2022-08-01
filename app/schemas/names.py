import uuid
from typing import List, Dict

from pydantic import BaseModel, validator

from config import settings
from errors import UnexpectedError
from schemas.base import BaseDBSchema


class InNameSchema(BaseModel):
    names: List[str]

    @validator('names', each_item=True)
    def check_names(cls, v):
        if settings.PREFIX_DELIMITER not in v:
            raise UnexpectedError(
                'names',
                message=f'`{v}` is not contain prefix `{settings.PREFIX_DELIMITER}`',
                code=400
            )
        return v


class NameWithFolderSchema(BaseDBSchema):
    name: Dict[str, List[str]]
    folder_id: uuid.UUID


class OutNamesSchema(BaseDBSchema):
    __root__: Dict[str, List[str]] = []


class OutNameWithFolderSchema(BaseDBSchema):
    __root__: List[NameWithFolderSchema] = []
