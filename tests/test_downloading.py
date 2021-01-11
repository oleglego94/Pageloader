import os
import requests_mock
from tempfile import TemporaryDirectory
from page_loader import download_page


def test_download_page():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            with open("tests/fixtures/test_page.html", "r") as t:
                response = t.read()
            mock_url = mock.get("http://test.com", text=response)
            page_path = download_page("http://test.com", tempdir)
            assert page_path.endswith(".html") is True
            with open(page_path, "r") as page:
                assert page.readline() == "<!DOCTYPE html>\n"
