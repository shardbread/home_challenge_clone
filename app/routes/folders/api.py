from fastapi import APIRouter, Depends

from config import settings
from depends.folders import FolderRepository
from schemas.folders import FolderSchema, OutFoldersSchema, InFolderSchema

router = APIRouter()


@router.get(
    "/folder",
    summary="Get folders",
    response_model=OutFoldersSchema
)
async def get_folders(
        limit: int = settings.DEFAULT_LIMIT,
        offset: int = None,
        folder_crud: FolderRepository = Depends()
):
    return await folder_crud.get_all(limit, offset)


@router.post(
    "/folder",
    summary="Create folder",
    response_model=FolderSchema
)
async def create_folder(
    payload: InFolderSchema,
    folder_crud: FolderRepository = Depends()
):
    return await folder_crud.create(payload)
