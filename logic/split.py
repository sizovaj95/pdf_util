import pikepdf
import os
import re
from pathlib import Path
from typing import Optional


def split_and_save_pdf(source_path: Path, destination_folder: Optional[Path] = None) -> Optional[Path]:
    """Split pdf, create folder (in source_path) and save individual pages into that folder."""
    if source_path.exists():
        if not destination_folder:
            destination_folder = source_path.parent.resolve()
        file_name = re.search(r"(.*)\.pdf", source_path.name, re.I)[1]
        dest_folder = destination_folder / f"{file_name}_split"
        if not dest_folder.exists():
            os.mkdir(dest_folder)
        pdf = pikepdf.Pdf.open(source_path)
        for i, page in enumerate(pdf.pages):
            dst = pikepdf.Pdf.new()
            dst.pages.append(page)
            dst.save(dest_folder / f"{file_name}_page_{i+1}.pdf")
        return dest_folder
    else:
        raise FileNotFoundError(f"The requested file {source_path.name} does not exist.")
