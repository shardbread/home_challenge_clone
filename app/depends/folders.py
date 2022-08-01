from db.models.folder import FolderModel
from depends.base_crud import CRUD
from schemas.folders import OutFoldersSchema, FolderSchema


class FolderRepository(CRUD):
    model = FolderModel
    schema = FolderSchema
    list_schema = OutFoldersSchema
