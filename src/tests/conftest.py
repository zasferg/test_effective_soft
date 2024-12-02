import pytest
from settings import TEST_DATA_FILE
from service.service import Library
import os


@pytest.fixture
def test_library():
    test_library = Library(data_file=TEST_DATA_FILE)
    try:
        yield test_library
    finally:
        if os.path.exists(TEST_DATA_FILE):
            os.remove(TEST_DATA_FILE)
            print(f"Файл {TEST_DATA_FILE} был успешно удален.")
        else:
            print(f"Файл {TEST_DATA_FILE} не найден.")


@pytest.fixture
def get_check_data():
    check_data = {
        "title": "title for check",
        "author": "author for check",
        "year": "1113",
    }
    return check_data
