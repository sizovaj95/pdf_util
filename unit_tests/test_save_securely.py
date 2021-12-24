from unittest import TestCase
from pathlib import Path
import tempfile

import logic.save_securely as secure


class TestSaveSecurely(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = Path(__file__).parent.parent.resolve() / "data"
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="unit_test_")
        cls.destination_dir = Path(cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_save_pdf_securely(self):
        file = self.data / "hobbit.pdf"
        expected_file_name = "hobbit_secured.pdf"
        secure.save_pdf_securely(file, "owner_password", "user_password", destination_folder=self.destination_dir)
        self.assertTrue((self.destination_dir / expected_file_name).exists())

    def test_split_file_not_exist(self):
        file_path = self.data / 'non_existing_file.pdf'
        self.assertRaises(FileNotFoundError, secure.save_pdf_securely, file_path)
