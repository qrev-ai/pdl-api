import json

import pytest
import os

from pdl_api.models.person import Certification, Education, Email, Experience, Person

## Get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))
example_dir = os.path.join(dir_path, "examples")
person_json = os.path.join(example_dir, "person_example.json")


@pytest.fixture
def example_data():
    with open(person_json, "r") as f:
        return json.load(f)


def test_person_model(example_data):
    person = Person(**example_data)
    assert person


def test_certification_model(example_data):
    certification_data = example_data["certifications"]
    for certification in certification_data:
        certification = Certification(**certification_data)
        assert certification


def test_education_model(example_data):
    education_data = example_data["education"][0]
    education = Education(**education_data)

    assert education


def test_email_model(example_data):
    email_data = example_data["emails"][0]
    email = Email(**email_data)

    for key, value in email_data.items():
        found_value = value
        expected_value = getattr(email, key)
        if isinstance(value, dict):
            expected_value = json.loads(expected_value)
            found_value = json.loads(found_value)

        assert (
            found_value == expected_value
        ), f"Mismatch for field '{key}' in Email. Expected {expected_value}, got {found_value}"


def test_experience_model(example_data):
    experience_data = example_data["experience"][0]
    experience = Experience(**experience_data)
    assert experience


if __name__ == "__main__":
    pytest.main(["-v", __file__])
    # pytest.main(["-v", __file__, "-k", "test_experience_model"])
