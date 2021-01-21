import os
from tempfile import TemporaryDirectory
from page_loader import io


def test_write_and_read_file():
    with TemporaryDirectory() as tempdir:
        content = io.read_file("tests/fixtures/test_page.html")
        new_file = io.write_file(
            content,
            os.path.join(tempdir, "test.txt"),
            "w",
        )
        assert io.read_file(new_file) == content
