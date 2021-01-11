from page_loader.cli import get_parser
from page_loader import download_page

MSG = "Page was successfully downloaded into "


def main():
    args = get_parser()
    print(MSG + download_page(args.url, args.output))


if __name__ == "__main__":
    main()
