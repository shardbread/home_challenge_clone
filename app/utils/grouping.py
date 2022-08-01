import json
from typing import List
from itertools import groupby
from collections import OrderedDict

from config import settings

FILENAME = 'example.csv'


def from_file(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        content = []
        for line in f:
            words = line.split('\n')
            content.append(words[0])
        return content


def grouping_list(inp_list: List[str], delimiter: str = settings.PREFIX_DELIMITER) -> OrderedDict:
    inp_list.sort(key=lambda s: s.rsplit(delimiter, 1)[0])
    grouped_list = []
    for key, value in groupby(inp_list, key=lambda s: s.rsplit('_', 1)[0]):
        grouped_list.append((key, list(value)))
    return OrderedDict(grouped_list)


def to_json(ordered_dict: OrderedDict) -> str:
    return json.dumps(ordered_dict, indent=4)
