import argparse

from config import settings
from utils.grouping import from_file, grouping_list, to_json

FILENAME = 'example.txt'


def main(filename: str, prefix_delimiter: str) -> str:
    file_content = from_file(filename)
    ordered_dict = grouping_list(file_content, prefix_delimiter)
    return to_json(ordered_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grouping words by their prefix")
    parser.add_argument("-f", "--file", help="path to file with words (optional)", required=False, default=FILENAME)
    parser.add_argument(
        "-wd", "--word_delimiter",
        help="prefix delimiter in word (option)",
        required=False,
        default=settings.PREFIX_DELIMITER
    )
    args = parser.parse_args()
    result = main(args.file, args.word_delimiter)
    print(result)
