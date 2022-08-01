from collections import OrderedDict
from fastapi import Depends

from config import settings
from db.models.group_name import FolderGroupNameModel
from depends.base_crud import CRUD
from schemas.names import InNameSchema, OutNameWithFolderSchema, NameWithFolderSchema
from utils.grouping import grouping_list


def get_grouped_words(payload: InNameSchema = Depends()) -> OrderedDict:
    """
        Grouping words
        :param payload: List of words
        :return: grouped words
    """
    return grouping_list(payload.names, settings.PREFIX_DELIMITER)


class NamesRepository(CRUD):
    model = FolderGroupNameModel
    schema = NameWithFolderSchema
    list_schema = OutNameWithFolderSchema
