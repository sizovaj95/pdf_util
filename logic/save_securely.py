import pikepdf
import re
from pathlib import Path
from typing import Optional
import logging

import logic.util as util


def save_pdf_securely(source_path: Path, owner_password: str = '', user_password: str = '', overwrite: bool = False,
                      destination_folder: Optional[Path] = None) \
        -> Optional[Path]:
    if source_path.exists():
        if not destination_folder:
            destination_folder = source_path.parent.resolve()
        file_name = re.search(r"(.*?)\.pdf", source_path.name)[1]
        save_file_name = f"{file_name}_secured.pdf"
        save_path = destination_folder / save_file_name
        if not overwrite:
            save_path = util.check_and_return_unique_name(save_path)
        logging.info(f"Result file path: {save_path}")
        pdf = pikepdf.Pdf.open(source_path)
        pdf.save(save_path, encryption=pikepdf.Encryption(owner=owner_password, user=user_password,
                                                          allow=pikepdf.Permissions(extract=False)))
        return save_path
    else:
        message = f"The requested file {source_path.name} does not exist."
        logging.error(message)
        raise FileNotFoundError(message)
