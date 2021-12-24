from unittest import TestCase
from pathlib import Path
import tempfile

import logic.extract_pages as ex


class TestExtractPages(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_extract_pages(self):
        test_file = self.data_dir / "test_doc_7_pages.pdf"
        expected_file_name = "Extracted_from_test_doc_7_pages.pdf"

        pages_to_extract = "1, 2, 5-7"
        with tempfile.TemporaryDirectory() as temp_dir:
            ex.extract_and_save_pages(test_file, pages_to_extract, destination_folder=Path(temp_dir))
            self.assertTrue((Path(temp_dir) / expected_file_name).exists())

    def test_extract_pages_file_not_existing(self):
        test_file = self.data_dir / "non_existing_file.pdf"

        pages_to_extract = "1, 2, 5-7"
        self.assertRaises(FileNotFoundError, ex.extract_and_save_pages, test_file, pages_to_extract)
