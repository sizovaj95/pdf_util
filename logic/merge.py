from pikepdf import Pdf
from glob import glob
import re
from pathlib import Path


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
            save_path = check_and_return_unique_name(source_folder / merged_pdf_name)
        merged_pdf.save(save_path)
    else:
        pass


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
