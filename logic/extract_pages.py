import pikepdf
from pathlib import Path

import logic.util as util


def extract_and_save_pages(source_path: Path, required_pages: str, overwrite: bool = False):
    """Extract required pages from document and save them in the same folder.
    required_pages must be listed either separated by commas (,) or as ranges (2-4)."""
    if source_path.exists():
        file_name = source_path.name
        extracted_file_name = f"Extracted_from_{file_name}"
        extracted_pdf = pikepdf.Pdf.new()
        pdf = pikepdf.Pdf.open(source_path)
        pdf_length = len(pdf.pages)
        page_list = util.convert_page_str_into_list(required_pages)
        page_list = util.check_that_pages_are_allowed(page_list, pdf_length)
        for page_num, page in enumerate(pdf.pages):
            if page_num + 1 in page_list:
                extracted_pdf.pages.append(page)

        save_path = source_path.parent.resolve() / extracted_file_name
        if not overwrite:
            save_path = util.check_and_return_unique_name(save_path)

        extracted_pdf.save(save_path)
    else:
        raise FileNotFoundError(F"The requested file {source_path.name} does not exist.")
