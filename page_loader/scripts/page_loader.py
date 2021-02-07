import logging as log
import sys

from requests.exceptions import RequestException

from page_loader import cli, download
from page_loader.logging import set_logging


def main():
    args = cli.set_parser()

    if args.verbose == "info":
        set_logging(log.INFO)
    elif args.verbose == "debug":
        set_logging(log.DEBUG)
    else:
        set_logging(log.WARNING)

    try:
        path = download(args.url, args.output)
    except (OSError, RequestException) as error:
        log.error(f"{error}")
        sys.exit(1)
    else:
        print(f"\u2714 Page was successfully downloaded into '{path}'")
        log.info("Successfully downloaded")


if __name__ == "__main__":
    main()
