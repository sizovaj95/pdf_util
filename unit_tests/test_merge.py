from unittest import TestCase
from pathlib import Path
import tempfile

import logic.merge as mr
import logic.constants as co


class TestMergePDF(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="unit_test_")
        cls.destination_dir = Path(cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_merge_1(self):
        test_folder = self.data_dir / "test_to_merge"
        expected_file_name = "hobbit_merged.pdf"
        mr.merge_and_save_pdf(test_folder, expected_file_name, destination_folder=self.destination_dir)
        self.assertTrue((self.destination_dir / expected_file_name).exists())

    def test_merge_directory_not_found(self):
        test_folder = self.data_dir / "non_existing_folder"
        expected_file_name = "non_existing_merged.pdf"
        self.assertRaises(co.FolderNotFound, mr.merge_and_save_pdf, test_folder, expected_file_name)
