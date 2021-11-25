import re
from pathlib import Path
from typing import List

import logic.constants as co


def check_and_return_unique_name(file_path: Path) -> Path:
    """Check that file_path does not already exist. If it does, add index to the end of file name."""
    if file_path.exists():
        file_name = file_path.name
        if not (match := re.search(r"_(\d{1,2})\.", file_name)):
            file_name = re.sub(r"(?=\..{3,4}$)", "_1", file_name)
        else:
            num = int(match[1])
            file_name = re.sub(r"_%s\." % str(num), "_%s." % str(num+1), file_name)
        new_path = check_and_return_unique_name(file_path.parent.resolve() / file_name)
        return new_path
    else:
        return file_path


def convert_page_str_into_list(page_nums: str) -> List[int]:
    """Convert input for pages to be extracted to actual list of numbers."""
    range_re = r"(\d{1,4})-(\d{1,4})"
    pages_list = []
    for page in re.split(r',', page_nums):
        numbers = re.findall(r"\d{1,4}", page)
        if len(numbers) == 1:
            pages_list.append(int(numbers[0]))
        elif match := re.search(range_re, page):
            start = int(match[1])
            end = int(match[2])
            page_range = list(range(start, end+1))
            pages_list.extend(page_range)
        else:
            raise co.IncorrectInputFormat(
                "Incorrect input for pages to be extracted! Allowed are e.g. '1, 2, 3' or '3-5' or combination.")

    return sorted(set(pages_list))


def check_that_pages_are_allowed(pages_list: List[int], last_page: int) -> List[int]:
    """Check that pages are within limits of the document. Replace out of limit pages with last page num (or 1)."""
    if 0 in pages_list:
        print("Page 0 is not allowed.")
        pages_list.remove(0)
        pages_list.append(1)
    if out_limit_pages := [p for p in pages_list if p > last_page]:
        print(f"Pages {out_limit_pages} are not in the document (last page is {last_page}).")
        for page in out_limit_pages:
            pages_list.remove(page)
        pages_list.append(last_page)

    pages_list = sorted(set(pages_list))
    return pages_list
