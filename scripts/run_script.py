from pathlib import Path
import os

from logic import split as sp


def main():
    data_folder = Path(__file__).parent.parent.resolve()/'data'
    data_folder_content = os.scandir(data_folder)
    for file in list(data_folder_content):
        if file.name.endswith(".pdf"):
            sp.split_and_save_pdf(Path(file.path))


if __name__ == "__main__":
    main()
