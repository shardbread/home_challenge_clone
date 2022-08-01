import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB,
)


from db.base_model import BaseModel


class FolderGroupNameModel(BaseModel):
    __tablename__ = "folder_group_name"
    name = Column(JSONB, nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("folder.id"), nullable=False)
