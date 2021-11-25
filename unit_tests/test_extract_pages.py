from unittest import TestCase
from pathlib import Path
import os

import logic.extract_pages as ex


class TestExtractPages(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_extract_pages(self):
        test_file = self.data_dir / "test_doc_7_pages.pdf"
        expected_file_name = "Extracted_from_test_doc_7_pages.pdf"
        if Path(self.data_dir / expected_file_name).exists():
            os.remove(Path(self.data_dir / expected_file_name))

        pages_to_extract = "1, 2, 5-7"
        ex.extract_and_save_pages(test_file, pages_to_extract)
        self.assertTrue(Path(self.data_dir / expected_file_name).exists())

    def test_extract_pages_file_not_existing(self):
        test_file = self.data_dir / "non_existing_file.pdf"

        pages_to_extract = "1, 2, 5-7"
        self.assertRaises(FileNotFoundError, ex.extract_and_save_pages, test_file, pages_to_extract)
