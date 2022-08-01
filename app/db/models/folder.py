from sqlalchemy import (
    Column,
    String,
)

from db.base_model import BaseModel


class FolderModel(BaseModel):
    __tablename__ = "folder"

    name = Column(String, nullable=False, unique=True)
