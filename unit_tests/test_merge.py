from unittest import TestCase
from pathlib import Path
import os

import logic.merge as mr
import logic.constants as co


class TestMergePDF(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_merge_1(self):
        test_folder = self.data_dir / "test_to_merge"
        expected_file_name = "hobbit_merged.pdf"
        if Path(test_folder / expected_file_name).exists():
            os.remove(Path(test_folder / expected_file_name))
        mr.merge_and_save_pdf(test_folder, expected_file_name)
        self.assertTrue(Path(test_folder / expected_file_name).exists())

    def test_merge_directory_not_found(self):
        test_folder = self.data_dir / "non_existing_folder"
        expected_file_name = "non_existing_merged.pdf"
        self.assertRaises(co.FolderNotFound, mr.merge_and_save_pdf, test_folder, expected_file_name)
