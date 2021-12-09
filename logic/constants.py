from typing import List

source_path = "source_path"
source_folder = "source_folder"
overwrite = "overwrite"
merged_pdf_name = "merged_pdf_name"
pages = "required_pages"
owner_pass = "owner_password"
user_pass = "user_password"

provide_path_message = "Please provide path to the pdf file."
incorrect_body_message = "The body to the request is entered incorrectly: missing {} key."


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
