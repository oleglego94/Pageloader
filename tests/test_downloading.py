import os
import stat
from tempfile import TemporaryDirectory

import pytest
import requests.exceptions
import requests_mock

from page_loader import download, downloading, errors

URL = "http://test.com"


def test_download_with_local_resources(
    open_with_local_resources,
    open_with_changed_paths,
    open_test_css,
    open_test_html,
    open_test_js,
    open_test_png,
):
    mocks = {
        URL: open_with_local_resources,
        "http://test.com/assets/application.css": open_test_css,
        "http://test.com/courses": open_test_html,
        "http://test.com/assets/professions/nodejs.png": open_test_png,
        "http://test.com/packs/js/runtime.js": open_test_js,
    }

    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            for url, content in mocks.items():
                if isinstance(content, bytes):
                    mock.get(url, content=content)
                else:
                    mock.get(url, text=content)
            received_html_path = download("http://test.com", tempdir)
            dir_path = os.path.join(tempdir, "test-com_files")
            received_resource_list = sorted(os.listdir(dir_path))
        assert received_html_path == f"{tempdir}/test-com.html"
        assert received_resource_list == [
            "test-com-assets-application.css",
            "test-com-assets-professions-nodejs.png",
            "test-com-courses.html",
            "test-com-packs-js-runtime.js",
        ]

        with open(received_html_path, "r") as received:
            assert received.read() == open_with_changed_paths

        with open(
            f"{dir_path}/test-com-assets-application.css", "r"
        ) as received:  # noqa: E501
            assert received.read() == open_test_css

        with open(
            f"{dir_path}/test-com-assets-professions-nodejs.png", "rb"
        ) as received:
            assert received.read() == open_test_png

        with open(f"{dir_path}/test-com-courses.html", "r") as received:
            assert received.read() == open_test_html

        with open(f"{dir_path}/test-com-packs-js-runtime.js", "r") as received:
            assert received.read() == open_test_js


def test_download_not_full_list_of_resources(open_test_css, open_test_js):
    with TemporaryDirectory() as tempdir:
        resources = {
            "http://test.com/assets/application.css": "",
            "https://httpbin.org/status/404": f"{tempdir}/test-com-courses.html",  # noqa: E501
            "http://test.com/packs/js/runtime.js": f"{tempdir}/test-com-packs-js-runtime.js",  # noqa: E501
        }
        with requests_mock.Mocker() as mock:
            mock.get(
                "http://test.com/assets/application.css",
                text=open_test_css,
            )
            mock.get("https://httpbin.org/status/404", status_code=404)
            mock.get("http://test.com/packs/js/runtime.js", text=open_test_js)

            downloading.download_resources(resources)

        received_resource_list = sorted(os.listdir(tempdir))
        assert received_resource_list == ["test-com-packs-js-runtime.js"]


def test_download_in_unfound_directory():
    with requests_mock.Mocker() as mock:
        mock.get(URL, text="test")
        with pytest.raises(errors.SavingError):
            download(URL, "some/path")


def test_download_with_code_not_ok():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, status_code=404)
            with pytest.raises(errors.DownloadingError):
                download(URL, tempdir)


def test_download_page_with_no_connection():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, exc=requests.exceptions.ConnectionError)
            with pytest.raises(errors.DownloadingError):
                download(URL, tempdir)


def test_download_with_existing_name():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text="text")
            download(URL, tempdir)
            with pytest.raises(errors.SavingError):
                download(URL, tempdir)


def test_download_permission_denied():
    with TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text="text")
            os.chmod(tempdir, stat.S_IRUSR)
            with pytest.raises(errors.SavingError):
                download(URL, tempdir)
