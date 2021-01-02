from page_loader.cli import get_parser
from page_loader import download


def main():
    args = get_parser()
    print(
        download(
            args.url,
            args.output,
        )
    )


if __name__ == "__main__":
    main()
