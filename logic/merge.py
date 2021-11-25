from pikepdf import Pdf
from glob import glob
from pathlib import Path

import logic.util as util
import logic.constants as co


def merge_and_save_pdf(source_folder: Path, merged_pdf_name: str = "merged.pdf", overwrite: bool = False):
    """Merge all pdfs from provided folder into single pdf and save in the same folder."""
    if source_folder.exists():
        merged_pdf = Pdf.new()
        for file in glob(str(source_folder / "*.pdf")):
            page = Pdf.open(file)
            merged_pdf.pages.extend(page.pages)
        if not merged_pdf_name.endswith(".pdf"):
            merged_pdf_name = merged_pdf_name + '.pdf'
        save_path = source_folder / merged_pdf_name
        if not overwrite:
            save_path = util.check_and_return_unique_name(save_path)
        merged_pdf.save(save_path)
    else:
        raise co.FolderNotFound(f"The requested folder {source_folder.name} is not found.")
