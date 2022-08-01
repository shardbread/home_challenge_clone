from fastapi import APIRouter, Depends

from config import settings
from depends.group_names import get_grouped_words, NamesRepository
from schemas.names import OutNamesSchema, NameWithFolderSchema, OutNameWithFolderSchema

router = APIRouter()


@router.post(
    "/names/grouping",
    summary="Make grouping",
    response_model=OutNamesSchema
)
async def grouping(
    grouped_names=Depends(get_grouped_words)
):
    return grouped_names


@router.post(
    "/names",
    summary="Save name to folder",
    response_model=NameWithFolderSchema
)
async def save_to_folder(
    payload: NameWithFolderSchema,
    name_crud: NamesRepository = Depends()
):
    return await name_crud.create(payload)


@router.get(
    "/names",
    summary="Gat names in folders",
    response_model=OutNameWithFolderSchema
)
async def get_with_folders(
    limit: int = settings.DEFAULT_LIMIT,
    offset: int = None,
    name_crud: NamesRepository = Depends()
):
    return await name_crud.get_all(limit, offset)
