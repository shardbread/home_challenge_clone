import uuid
from typing import List

from schemas.base import BaseDBSchema


class InFolderSchema(BaseDBSchema):
    name: str


class FolderSchema(InFolderSchema):
    id: uuid.UUID


class OutFoldersSchema(BaseDBSchema):
    __root__: List[FolderSchema] = []
