from unittest import TestCase
from pathlib import Path
import logic.constants as co

import logic.util as util


class TestUtil(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data_dir = Path(__file__).parent.parent.resolve() / 'data'

    def test_convert_page_str_into_list_1(self):
        pages = "1, 2, 3"
        expected = [1, 2, 3]
        result = util.convert_page_str_into_list(pages)
        self.assertEqual(expected, result)

    def test_convert_page_str_into_list_2(self):
        pages = "1, 3-5, 8"
        expected = [1, 3, 4, 5, 8]
        result = util.convert_page_str_into_list(pages)
        self.assertEqual(expected, result)

    def test_convert_page_str_into_list_3(self):
        pages = "3-6"
        expected = [3, 4, 5, 6]
        result = util.convert_page_str_into_list(pages)
        self.assertEqual(expected, result)

    def test_convert_page_str_into_list_4(self):
        pages = "1 2 3 4"
        self.assertRaises(co.IncorrectInputFormat, util.convert_page_str_into_list, pages)

    def test_convert_page_str_into_list_5(self):
        pages = "3-6, 6, 7"
        expected = [3, 4, 5, 6, 7]
        result = util.convert_page_str_into_list(pages)
        self.assertEqual(expected, result)

    def test_check_that_pages_are_allowed_1(self):
        pages = [1, 2, 3, 4]
        doc_len = 10
        expected = [1, 2, 3, 4]
        result = util.check_that_pages_are_allowed(pages, doc_len)
        self.assertEqual(expected, result)

    def test_check_that_pages_are_allowed_2(self):
        pages = [0, 2, 3, 4]
        doc_len = 10
        expected = [1, 2, 3, 4]
        result = util.check_that_pages_are_allowed(pages, doc_len)
        self.assertEqual(expected, result)

    def test_check_that_pages_are_allowed_3(self):
        pages = [2, 3, 4, 11, 14, 54]
        doc_len = 10
        expected = [2, 3, 4, doc_len]
        result = util.check_that_pages_are_allowed(pages, doc_len)
        self.assertEqual(expected, result)

    def test_check_that_pages_are_allowed_4(self):
        pages = [11, 14, 54]
        doc_len = 10
        expected = [doc_len]
        result = util.check_that_pages_are_allowed(pages, doc_len)
        self.assertEqual(expected, result)

    def test_check_and_return_unique_name_file_not_exist(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "capybara.txt"
        expected_path = test_folder / desired_file_name
        result_path = util.check_and_return_unique_name(expected_path)
        self.assertEqual(expected_path, result_path)

    def test_check_and_return_unique_name_one_file_exists(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "test_file.txt"
        expected_path = test_folder / "test_file_1.txt"
        result_path = util.check_and_return_unique_name(test_folder / desired_file_name)
        self.assertEqual(expected_path, result_path)

    def test_check_and_return_unique_name_two_files_exists(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "another_test_file.txt"
        expected_path = test_folder / "another_test_file_2.txt"
        result_path = util.check_and_return_unique_name(test_folder / desired_file_name)
        self.assertEqual(expected_path, result_path)
