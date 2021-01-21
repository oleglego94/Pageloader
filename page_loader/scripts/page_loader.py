from page_loader.cli import get_parser
from page_loader import download

MSG = "Page was successfully downloaded into "


def main():
    args = get_parser()
    path = download(args.url, args.output)
    print(MSG + "'{}'".format(path))


if __name__ == "__main__":
    main()
