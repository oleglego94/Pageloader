import pytest


@pytest.fixture
def open_with_local_resources():
    with open("tests/fixtures/with_local_resources.html", "r") as f:
        return f.read()


@pytest.fixture
def open_with_changed_paths():
    with open("tests/fixtures/with_changed_paths.html", "r") as f:
        return f.read()


@pytest.fixture
def open_without_local_resources():
    with open("tests/fixtures/without_local_resources.html", "r") as f:
        return f.read()


@pytest.fixture
def open_test_css():
    with open("tests/fixtures/files/test.css", "r") as f:
        return f.read()


@pytest.fixture
def open_test_html():
    with open("tests/fixtures/files/test.html", "r") as f:
        return f.read()


@pytest.fixture
def open_test_js():
    with open("tests/fixtures/files/test.js", "r") as f:
        return f.read()


@pytest.fixture
def open_test_png():
    with open("tests/fixtures/files/test.png", "rb") as f:
        return f.read()
