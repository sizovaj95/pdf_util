import pikepdf
import os
import re
from pathlib import Path


def split_and_save_pdf(source_path: Path) -> None:
    """Split pdf, create folder (in source_path) and save individual pages into that folder."""
    if source_path.exists():
        file_name = re.search(r"(.*)\.pdf", source_path.name, re.I)[1]
        dest_folder = source_path.parent.resolve() / f"{file_name}_split"
        if not dest_folder.exists():
            os.mkdir(dest_folder)
        pdf = pikepdf.Pdf.open(source_path)
        for i, page in enumerate(pdf.pages):
            dst = pikepdf.Pdf.new()
            dst.pages.append(page)
            dst.save(dest_folder / f"{file_name}_page_{i+1}.pdf")
    else:
        raise FileNotFoundError(f"The requested file {source_path.name} does not exist")
