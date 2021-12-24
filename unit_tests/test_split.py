from unittest import TestCase
from pathlib import Path
import os
import tempfile

import logic.split as sp


class TestSplitPDF(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_split_1(self):
        file_path = self.data_dir / 'hobbit.pdf'
        with tempfile.TemporaryDirectory() as temp_dir:
            expected_folder = Path(temp_dir) / "hobbit_split"
            sp.split_and_save_pdf(file_path, destination_folder=Path(temp_dir))
            self.assertTrue(expected_folder.exists())
            self.assertEqual(3, len(list(os.scandir(expected_folder))))

    def test_split_file_not_exist(self):
        file_path = self.data_dir / 'non_existing_file.pdf'
        self.assertRaises(FileNotFoundError, sp.split_and_save_pdf, file_path)

