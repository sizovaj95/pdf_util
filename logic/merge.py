from pikepdf import Pdf
from glob import glob
from pathlib import Path
from typing import Optional
import logging

import logic.util as util
import logic.constants as co


def merge_and_save_pdf(source_path: Path, merged_pdf_name: str = "merged.pdf", overwrite: bool = False,
                       destination_folder: Optional[Path] = None) -> Path:
    """Merge all pdfs from provided folder into single pdf and save in the same folder."""
    if source_path.exists():
        if not destination_folder:
            destination_folder = source_path
        merged_pdf = Pdf.new()
        for file in glob(str(source_path / "*.pdf")):
            page = Pdf.open(file)
            merged_pdf.pages.extend(page.pages)
        if not merged_pdf_name.endswith(".pdf"):
            merged_pdf_name = merged_pdf_name + '.pdf'
        save_path = destination_folder / merged_pdf_name
        if not overwrite:
            save_path = util.check_and_return_unique_name(save_path)
        logging.info(f"Merged file path: {save_path}")
        merged_pdf.save(save_path)
        return save_path
    else:
        message = f"The requested file {source_path.name} does not exist."
        logging.error(message)
        raise co.FolderNotFound(message)
