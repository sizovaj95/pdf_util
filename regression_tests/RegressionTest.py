import requests
from pathlib import Path
import os
import shutil
import tempfile
import pikepdf
import time
import logging

import logic.constants as co


BASE_URL = "http://127.0.0.1:5000/"
REQUEST_DIR = Path(__file__).parent.resolve() / "requests"
RESPONSE_DIR = Path(__file__).parent.resolve() / "responses"

user_password = "strong_password"
owner_password = "very_strong_password"

endpoints = ["split",
             "merge",
             "extract",
             "save-securely"]


class RegressionTests:
    def __init__(self, url: str = BASE_URL):
        self.failed_tests = 0
        self.url = url

    def run_regression_tests(self):
        for endpoint in endpoints:
            self.run_tests_for_one_endpoint(endpoint)

        self.analyse_results()

    def run_tests_for_one_endpoint(self, endpoint_name: str):
        url = self.url + endpoint_name
        request_folder = Path(REQUEST_DIR / endpoint_name)
        response_folder = Path(RESPONSE_DIR / endpoint_name)
        logging.info(f"RUNNING TESTS FOR {endpoint_name.upper()}.")
        for file in list(os.scandir(request_folder)):
            logging.info(f"=====Test for {file.name}=====")
            with tempfile.TemporaryDirectory(prefix="reg_test_") as temp_dir:
                logging.debug(f"Creating temporary folder: {temp_dir}")
                payload = get_payload(endpoint_name)
                payload[co.source_path] = file.path
                payload[co.destination] = temp_dir
                make_post_request(url, payload)
                self.compare_results(response_folder, Path(temp_dir))
                logging.debug(f"Removing temporary folder: {temp_dir}")
                print('\n')
                time.sleep(1)

    def compare_results(self, expected_dir: Path, result_dir: Path):
        result_files = list(os.scandir(result_dir))
        if not result_files:
            self.failed_tests += 1
            logging.warning("The result is None!")
            return
        for result_file in list(os.scandir(result_dir)):
            expected_path = expected_dir / result_file.name
            try:
                assert expected_path.exists()
            except AssertionError:
                logging.warning(f"{expected_path} does not exists!")
                self.failed_tests += 1
                return

            if result_file.is_dir():
                try:
                    assert len(list(os.scandir(result_file.path))) == len(list(os.scandir(expected_path)))
                except AssertionError:
                    logging.warning(f"{expected_path} : Number of files in expected vs result is not equal!")
                    self.failed_tests += 1
            else:
                self.compare_files(expected_dir, result_file)

    def compare_files(self, expected_dir: Path, result_file: os.DirEntry):
        expected_path = expected_dir / result_file.name
        try:
            result_pdf = pikepdf.Pdf.open(result_file.path)
            expected_pdf = pikepdf.Pdf.open(expected_dir / result_file.name)
        except pikepdf._qpdf.PasswordError:
            if "save-securely" in expected_dir.name:
                result_pdf = pikepdf.Pdf.open(result_file.path, password=owner_password)
                logging.info(f"Opening secured result PDF {result_file.name} with password '{owner_password}'")
                expected_pdf = pikepdf.Pdf.open(expected_dir / result_file.name, password=owner_password)
                logging.info(f"Opening secured expected PDF {result_file.name} with password '{owner_password}'")
            else:
                self.failed_tests += 1
                logging.warning(f"{result_file.name} is password-protected, but shouldn't be!")
                return
        try:
            assert len(result_pdf.pages) == len(expected_pdf.pages)
        except AssertionError:
            logging.warning(f"{expected_path} : Number of pages in expected pdf and result pdf are not equal!")
            self.failed_tests += 1

    def analyse_results(self):
        if not self.failed_tests:
            logging.warning("\nAll tests passed!")
        else:
            logging.warning(f"\n{self.failed_tests} test(s) failed!")


def make_post_request(url: str, payload: dict):
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        logging.error(f"Status code: {response.status_code}. Message: {response.text}")
    return response


def get_payload(endpoint_name: str) -> dict:
    kwargs = {co.destination: str(Path(RESPONSE_DIR / endpoint_name))}
    if endpoint_name == "merge":
        kwargs[co.overwrite] = False
    elif endpoint_name == "extract":
        kwargs[co.overwrite] = False
        kwargs[co.pages] = "1,2, 4-6"
    elif endpoint_name == "save-securely":
        kwargs[co.user_pass] = user_password
        kwargs[co.owner_pass] = owner_password
    return kwargs


def clean_response_directory(directory: Path):
    for file in list(os.scandir(directory)):
        try:
            shutil.rmtree(file.path)
        except OSError:
            os.remove(file.path)


def _remove_old_and_create_new_response_files():
    for endpoint in endpoints:
        url = BASE_URL + endpoint
        request_folder = Path(REQUEST_DIR / endpoint)
        response_folder = Path(RESPONSE_DIR / endpoint)
        clean_response_directory(response_folder)
        for file in list(os.scandir(request_folder)):
            logging.info(f"Creating response for {file.name}")
            payload = get_payload(endpoint)
            payload[co.source_path] = file.path
            payload[co.destination] = response_folder
            make_post_request(url, payload)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    create_new_response_files = False
    if create_new_response_files:
        _remove_old_and_create_new_response_files()
    else:
        reg_tests = RegressionTests()
        reg_tests.run_regression_tests()
