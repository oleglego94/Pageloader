import os
import requests_mock
from tempfile import TemporaryDirectory
from page_loader import io
from page_loader.downloading import download_page, download_resources

URL = "http://test.com"
URL_content = io.read_file("tests/fixtures/test_page.html")
css_url = "http://test.com/assets/application.css"
css_content = io.read_file("tests/fixtures/files/test.css")
html_url = "http://test.com/courses"
html_content = io.read_file("tests/fixtures/files/test.html")
png_url = "http://test.com/assets/professions/nodejs.png"
png_content = io.read_file("tests/fixtures/files/test.png")
js_url = "http://test.com/packs/js/runtime.js"
js_content = io.read_file("tests/fixtures/files/test.js")

RESOURCES = {
    URL: URL_content,
    css_url: css_content,
    html_url: html_content,
    png_url: png_content,
    js_url: js_content,
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
            for url, content in RESOURCES.items():
                if isinstance(content, bytes):
                    mock.get(url, content=content)
                else:
                    mock.get(url, text=content)
            page_path = download_page(URL, tempdir)
            resources_path = download_resources(page_path, URL, tempdir)

        assert os.path.exists(resources_path) is True
        assert resources_path.endswith("_files") is True

        with open(page_path, "r") as modified_html, open(
            "tests/fixtures/modified_test_page.html", "r"
        ) as sample:
            assert modified_html.read() == sample.read()
