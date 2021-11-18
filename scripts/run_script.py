from pathlib import Path
import os

from logic import split as sp
from logic import merge as mr


def main():
    data_folder = Path(__file__).parent.parent.resolve()/'data'
    run_merge(data_folder)


def run_split(data_folder):
    data_folder_content = os.scandir(data_folder)
    for file in list(data_folder_content):
        if file.name.endswith(".pdf"):
            sp.split_and_save_pdf(Path(file.path))


def run_merge(data_folder):
    to_merge_folder = data_folder / 'test_to_merge'
    mr.merge_and_save_pdf(to_merge_folder)


if __name__ == "__main__":
    main()
