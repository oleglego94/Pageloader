import logging
import sys
from page_loader.cli import get_parser
from page_loader import download
from page_loader.logging import setup_logging


def main():
    try:
        setup_logging()
        logging.info("Start downloading")
        args = get_parser()
        path = download(args.url, args.output)
    except Exception as error:
        logging.error(f"{error}")
        sys.exit(1)
    else:
        print(f"Page was successfully downloaded into '{path}'")
        logging.info("Finish downloading")


if __name__ == "__main__":
    main()
