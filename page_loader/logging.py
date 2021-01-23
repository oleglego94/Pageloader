import sys
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.WARNING,
        stream=sys.stderr,
        format="[%(asctime)s]-[%(levelname)s]-%(filename)s:%(lineno)d => %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S",
    )
