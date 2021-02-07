import logging
import sys


def set_logging(log_level):
    logging.basicConfig(
        level=log_level,
        stream=sys.stderr,
        format="%(asctime)s %(levelname)s: (%(filename)s:%(lineno)d) %(message)s",  # noqa: E501
        datefmt="%Y-%m-%d %H:%M:%S",
    )
