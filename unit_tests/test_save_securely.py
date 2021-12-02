import os
from unittest import TestCase
from pathlib import Path

import logic.save_securely as secure


class TestSaveSecurely(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = Path(__file__).parent.parent.resolve() / "data"

    def test_save_pdf_securely(self):
        file = self.data / "hobbit.pdf"
        expected_dest = Path(self.data / "hobbit_secured.pdf")
        if expected_dest.exists():
            os.remove(expected_dest)
        secure.save_pdf_securely(file, "owner_password", "user_password")
        self.assertTrue(expected_dest.exists())

    def test_split_file_not_exist(self):
        file_path = self.data / 'non_existing_file.pdf'
        self.assertRaises(FileNotFoundError, secure.save_pdf_securely, file_path)
