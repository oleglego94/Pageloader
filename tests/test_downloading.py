import os
import requests_mock
from tempfile import TemporaryDirectory
from page_loader import io
from page_loader.downloading import download_page, download_resources

URL = "http://test.com"
RESOURCES = {
    URL: "tests/fixtures/test_page.html",
    "http://test.com/assets/application.css": "tests/fixtures/files/test.css",
    "http://test.com/courses": "tests/fixtures/files/test.html",
    "http://test.com/assets/professions/nodejs.png": "tests/fixtures/files/test.png",  # noqa: E501
    "http://test.com/packs/js/runtime.js": "tests/fixtures/files/test.js",
}


def test_download_page_():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text="test")
            page_path = download_page(URL, tempdir)
        assert os.path.exists(page_path) is True
        assert page_path.endswith(".html") is True


def test_download_resources():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:

            for url, content_path in RESOURCES.items():
                response = io.read_file(content_path)
                if isinstance(response, bytes):
                    mock.get(url, content=response)
                else:
                    mock.get(url, text=response)

            page_path = download_page(URL, tempdir)
            resources_path = download_resources(page_path, URL, tempdir)

        assert os.path.exists(resources_path) is True
        assert resources_path.endswith("_files") is True

        with open(page_path, "r") as modified_html, open(
            "tests/fixtures/modified_test_page.html", "r"
        ) as sample:
            assert modified_html.read() == sample.read()
