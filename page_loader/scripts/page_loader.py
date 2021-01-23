import logging
from page_loader.cli import get_parser
from page_loader import download
from page_loader.logging import setup_logging

MSG = "Page was successfully downloaded into "


def main():
    setup_logging()
    logging.info("Start downloading")
    args = get_parser()
    path = download(args.url, args.output)
    print(MSG + "'{}'".format(path))
    logging.info("Finish downloading")


if __name__ == "__main__":
    main()
