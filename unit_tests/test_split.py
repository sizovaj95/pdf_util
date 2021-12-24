from unittest import TestCase
from pathlib import Path
import os
import tempfile

import logic.split as sp


class TestSplitPDF(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="unit_test_")
        cls.destination_dir = Path(cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_split_1(self):
        file_path = self.data_dir / 'hobbit.pdf'
        expected_folder = Path(self.destination_dir) / "hobbit_split"
        sp.split_and_save_pdf(file_path, destination_folder=self.destination_dir)
        self.assertTrue(expected_folder.exists())
        self.assertEqual(3, len(list(os.scandir(expected_folder))))

    def test_split_file_not_exist(self):
        file_path = self.data_dir / 'non_existing_file.pdf'
        self.assertRaises(FileNotFoundError, sp.split_and_save_pdf, file_path)

