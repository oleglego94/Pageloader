import os
from tempfile import TemporaryDirectory

from page_loader import dom

PAGE_URL = "http://test.com"


def test_prepare_html_with_local_resources(
    open_with_local_resources, open_with_changed_paths
):
    with TemporaryDirectory() as tempdir:
        html = open_with_local_resources
        dir_path = os.path.join(tempdir, "test-com_files")

        expected_html = open_with_changed_paths
        received_html, received_resources = dom.prepare_html(
            html, PAGE_URL, dir_path
        )
        assert received_html == expected_html
        assert received_resources == {
            "http://test.com/assets/application.css": f"{dir_path}/test-com-assets-application.css",  # noqa: E501
            "http://test.com/courses": f"{dir_path}/test-com-courses.html",
            "http://test.com/assets/professions/nodejs.png": f"{dir_path}/test-com-assets-professions-nodejs.png",  # noqa: E501
            "http://test.com/packs/js/runtime.js": f"{dir_path}/test-com-packs-js-runtime.js",  # noqa: E501
        }


def test_prepare_html_without_local_resources(open_without_local_resources):
    with TemporaryDirectory() as tempdir:
        html = open_without_local_resources
        dir_path = os.path.join(tempdir, "test-com_files")
        received_html, received_resources = dom.prepare_html(
            html, PAGE_URL, dir_path
        )
        assert received_html == html
        assert received_resources == {}
