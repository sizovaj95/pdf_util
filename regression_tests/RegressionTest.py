import requests
from pathlib import Path
import os
import shutil
import tempfile
from pikepdf import Pdf

import logic.constants as co


BASE_URL = "http://127.0.0.1:5000/"
REQUEST_DIR = Path(__file__).parent.resolve() / "requests"
RESPONSE_DIR = Path(__file__).parent.resolve() / "responses"

endpoints = ["split",
             "merge",
             "extract"]


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
        print("\n")
        print(f"RUNNING TESTS FOR {endpoint_name.upper()}.")
        for file in list(os.scandir(request_folder)):
            print(f"=====Test for {file.name}=====")
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Creating temporary dir {temp_dir}")
                payload = get_payload(endpoint_name)
                payload[co.source_path] = file.path
                payload[co.destination] = temp_dir
                make_post_request(url, payload)
                self.compare_results(response_folder, Path(temp_dir))

    def compare_results(self, expected_dir: Path, result_dir: Path):
        for result_file in list(os.scandir(result_dir)):
            expected_path = expected_dir / result_file.name
            try:
                assert expected_path.exists()
            except AssertionError:
                print(f"{expected_path} does not exists!")
                self.failed_tests += 1
                return

            if result_file.is_dir():
                try:
                    assert len(list(os.scandir(result_file.path))) == len(list(os.scandir(expected_path)))
                except AssertionError:
                    print(f"{expected_path} : Number of files in expected vs result is not equal!")
                    self.failed_tests += 1
            else:
                result_pdf = Pdf.open(result_file.path)
                expected_pdf = Pdf.open(expected_dir / result_file.name)
                try:
                    assert len(result_pdf.pages) == len(expected_pdf.pages)
                except AssertionError:
                    print(f"{expected_path} : Number of pages in expected pdf and result pdf are not equal!")
                    self.failed_tests += 1

    def analyse_results(self):
        if not self.failed_tests:
            print("\nAll tests passed!")
        else:
            print(f"\n{self.failed_tests} test(s) failed!")


def make_post_request(url: str, payload: dict):
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
    return response


def get_payload(endpoint_name: str) -> dict:
    kwargs = {co.destination: str(Path(RESPONSE_DIR / endpoint_name))}
    if endpoint_name == "merge":
        kwargs[co.overwrite] = False
    elif endpoint_name == "extract":
        kwargs[co.overwrite] = False
        kwargs[co.pages] = "1,2, 4-6"
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
            print(f"Creating response for {file.name}")
            payload = get_payload(endpoint)
            payload[co.source_path] = file.path
            payload[co.destination] = response_folder
            make_post_request(url, payload)


if __name__ == "__main__":
    create_new_response_files = False
    if create_new_response_files:
        _remove_old_and_create_new_response_files()
    else:
        reg_tests = RegressionTests()
        reg_tests.run_regression_tests()
