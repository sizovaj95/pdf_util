from unittest import TestCase
from pathlib import Path
import os
import shutil

import logic.split as sp


class TestSplitPDF(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_split_1(self):
        file_path = self.data_dir / 'hobbit.pdf'
        expected_folder = Path(self.data_dir / "hobbit_split")
        if expected_folder.exists():
            shutil.rmtree(expected_folder)
        sp.split_and_save_pdf(file_path)
        self.assertTrue(expected_folder.exists())
        self.assertEqual(3, len(list(os.scandir(expected_folder))))

    def test_split_file_not_exist(self):
        file_path = self.data_dir / 'non_existing_file.pdf'
        self.assertRaises(FileNotFoundError, sp.split_and_save_pdf, file_path)

