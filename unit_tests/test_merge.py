from unittest import TestCase
from pathlib import Path
import os
import shutil

import logic.merge as mr


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

    def test_check_and_return_unique_name_file_not_exist(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "capybara.txt"
        expected_path = test_folder / desired_file_name
        result_path = mr.check_and_return_unique_name(expected_path)
        self.assertEqual(expected_path, result_path)

    def test_check_and_return_unique_name_one_file_exists(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "test_file.txt"
        expected_path = test_folder / "test_file_1.txt"
        result_path = mr.check_and_return_unique_name(test_folder / desired_file_name)
        self.assertEqual(expected_path, result_path)

    def test_check_and_return_unique_name_two_files_exists(self):
        test_folder = self.data_dir / "test_file_names"
        desired_file_name = "another_test_file.txt"
        expected_path = test_folder / "another_test_file_2.txt"
        result_path = mr.check_and_return_unique_name(test_folder / desired_file_name)
        self.assertEqual(expected_path, result_path)
