import os
from tempfile import TemporaryDirectory
from page_loader import download


def test_download():
    with TemporaryDirectory() as tempdir:
        url = "https://ru.hexlet.io/courses"
        file_path = os.path.join(tempdir, "ru-hexlet-io-courses.html")
        assert download(url, tempdir) == file_path
        assert os.path.isfile(file_path) is True
