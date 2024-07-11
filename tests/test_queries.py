import json
import os
from typing import Any

import pytest

from pdl_api import PDLPersonAPI, Response, PDLSettings

## Get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
example_dir = os.path.join(dir_path, "examples")
person_json_file = os.path.join(example_dir, "person_example.json")
error_json_file = os.path.join(example_dir, "error_example.json")


@pytest.fixture
def success_json():
    with open(person_json_file, "r") as f:
        return json.load(f)


@pytest.fixture
def error_json():
    with open(error_json_file, "r") as f:
        return json.load(f)

class CountingAPI(PDLPersonAPI):
    def __init__(self, *args, **kwargs):
        self.count = 0
        super().__init__(*args, **kwargs)

    def _get_response(self, params: dict[str, Any]) -> dict[str, Any]:
        self.count += 1
        return {}

@pytest.fixture
def success_api(success_json):
    js = {"status": 200, "likelihood": 1, "dataset_version": "1", "data": success_json}

    class SuccessPDLPersonAPI(CountingAPI):
        def _get_response(self, params: dict[str, Any]) -> dict[str, Any]:
            self.count += 1
            return js

    settings = PDLSettings(api_key="test")
    return SuccessPDLPersonAPI(settings=settings)


@pytest.fixture
def error_api(error_json):

    class ErrorPDLPersonAPI(CountingAPI):
        def _get_response(self, params: dict[str, Any]) -> dict[str, Any]:
            self.count += 1
            return error_json

    settings = PDLSettings(api_key="test")
    return ErrorPDLPersonAPI(settings=settings)


def test_success(success_api: CountingAPI, success_json):
    pr = success_api.get_person_via_email("myemail")
    assert pr is not None
    assert pr.is_person
    assert pr.person is not None
    assert pr.person.full_name == success_json["full_name"]


def test_success_json_dump_load(success_api: CountingAPI):
    pr = success_api.get_person_via_email("myemail")
    assert pr is not None
    assert pr.is_person
    assert pr.person and pr.person.full_name
    pr_json = pr.model_dump(mode="json")
    with open("t.json", "w") as f:
        json.dump(pr_json, f)
    pr2 = Response(**pr_json)
    assert pr2.person
    assert pr.person.full_name == pr2.person.full_name


def test_error_json_dump_load(error_api: CountingAPI) :
    pr = error_api.get_person_via_email("myemail")
    assert pr is not None
    assert pr.is_error
    assert pr.error and pr.error.message
    pr_json = pr.model_dump(mode="json")
    pr2 = Response(**pr_json)
    assert pr.error == pr2.error


def test_no_repeated_calls(success_api: CountingAPI):
    pr1 = success_api.get_person_via_email("myemail")
    pr2 = success_api.get_person_via_email("myemail")
    assert pr1 is not None
    assert pr1 == pr2
    assert success_api.count == 1


def test_error(error_api: CountingAPI, error_json):
    pr = error_api.get_person_via_email("myemail")
    assert pr is not None
    assert pr.is_error and pr.error
    assert pr.error.type == error_json["error"]["type"]


def test_error_no_repeated_calls(error_api: CountingAPI):
    pr1 = error_api.get_person_via_email("myemail")
    pr2 = error_api.get_person_via_email("myemail")
    assert pr1 is not None
    assert pr1 == pr2
    assert error_api.count == 1


if __name__ == "__main__":
    pytest.main([__file__])
