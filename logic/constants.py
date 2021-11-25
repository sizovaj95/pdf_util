from typing import List


class IncorrectInputFormat(Exception):
    pass


class FolderNotFound(Exception):
    pass


class PageOutsidePageLimit(Exception):
    def __init__(self, page_limit: int, pages_out_of_limit: List[int]):
        self.page_limit = page_limit
        self.pages_out_of_limit = pages_out_of_limit
        self.message = f"Pages are not in allowed (1, {self.page_limit}) range."

    def __str__(self):
        return f"{self.pages_out_of_limit}: {self.message}"
