import pytest

from page_loader import storage


@pytest.mark.parametrize(
    "link, dir_path, path, rel_path",
    [
        (
            "https://test.com/assets/menu.css",
            "../app/test-com_files",
            "../app/test-com_files/test-com-assets-menu.css",
            "test-com_files/test-com-assets-menu.css",
        ),
        (
            "https://test.com/packs/js/runtime.js",
            "./app/page-loader/test-com_files",
            "./app/page-loader/test-com_files/test-com-packs-js-runtime.js",
            "test-com_files/test-com-packs-js-runtime.js",
        ),
        (
            "http://test.com/assets/professions/nodejs.png",
            "test-com_files",
            "test-com_files/test-com-assets-professions-nodejs.png",
            "test-com_files/test-com-assets-professions-nodejs.png",
        ),
    ],
)
def test_make_file_path(link, dir_path, path, rel_path):
    assert storage.make_file_path(link, dir_path) == (path, rel_path)
