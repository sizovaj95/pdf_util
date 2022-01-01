source_path = "source_path"
overwrite = "overwrite"
merged_pdf_name = "merged_pdf_name"
pages = "required_pages"
owner_pass = "owner_password"
user_pass = "user_password"
destination = "destination_folder"

incorrect_body_message = "The body to the request is entered incorrectly: missing {} key."


class IncorrectInputFormat(Exception):
    pass


class FolderNotFound(Exception):
    pass
