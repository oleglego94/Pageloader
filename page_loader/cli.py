import argparse
import os

import pkg_resources

VERSION = pkg_resources.get_distribution("hexlet-code").version
DEFAULT_OUTPUT = os.getcwd()


def set_parser():
    parser = argparse.ArgumentParser(
        description="""
        PageLoader is a CLI-utility that downloads pages from the Internet
        and stores them on computer""",
        usage="%(prog)s [options] <url>",
        add_help=False,
    )

    arguments_group = parser.add_argument_group(title="Arguments")
    arguments_group.add_argument("url", type=str, help="download page address")

    options_group = parser.add_argument_group(title="Options")
    options_group.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="[dir]",
        default=DEFAULT_OUTPUT,
        help='output dir (default: current directory)',
    )
    options_group.add_argument(
        "-v",
        "--verbose",
        choices={"info", "debug"},
        help="display verbose log",
    )
    options_group.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(VERSION),
        help="output the version number",
    )
    options_group.add_argument(
        "-h", "--help", action="help", help="display help for command"
    )
    return parser.parse_args()
