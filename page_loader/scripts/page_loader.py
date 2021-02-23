import logging as log
import sys

from page_loader import cli, download, errors
from page_loader.logging import set_logging

EXIT_OK = 0
EXIT_ERROR = 1


def main():
    args = cli.set_parser()

    if args.verbose == "debug":
        set_logging(log.DEBUG)
    elif args.verbose == "info":
        set_logging(log.INFO)
    else:
        set_logging(log.WARNING)

    try:
        path = download(args.url, args.output)
    except errors.KnownError as error:
        log.error(f"{error}")
        sys.exit(EXIT_ERROR)
    else:
        print(f"\u2714 Page was successfully downloaded into '{path}'")
        log.info("Page with resources were successfully downloaded")
        sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
