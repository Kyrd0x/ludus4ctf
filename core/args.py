from dotenv import load_dotenv
import argparse
import sys
import os

try:
    import argcomplete
    from argcomplete.completers import FilesCompleter
except Exception:
    argcomplete = None
    FilesCompleter = None


def parse_args():
    load_dotenv()  # Load environment variables from .env file
    LUDUS_API_URL = os.getenv("LUDUS_API_URL", "http://localhost:8080/api")
    LUDUS_API_KEY = os.getenv("LUDUS_API_KEY", "")

    parser = argparse.ArgumentParser(
        description="Ludus Groups/Users/WireGuard Config Manager"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available commands",
    )

    masked_token = (
        "****" + LUDUS_API_KEY[-4:]
        if isinstance(LUDUS_API_KEY, str) and len(LUDUS_API_KEY) >= 4
        else "Not set"
    )

    def add_common_args(subparser):
        subparser.add_argument(
            "--ludus-url",
            default=LUDUS_API_URL,
            help=f"URL of the Ludus API. Default: {LUDUS_API_URL or 'Not set'}",
        )
        subparser.add_argument(
            "--ludus-token",
            default=LUDUS_API_KEY,
            help=f"API token for Ludus access. Default from ludus.conf: {masked_token}",
        )
        subparser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable verbose output",
        )
        subparser.add_argument(
            "--insecure",
            action="store_true",
            help="Disable SSL certificate verification",
        )

    # subcommand: list
    list_parser = subparsers.add_parser(
        "list",
        help="List all users and their WireGuard configs",
    )
    add_common_args(list_parser)
    list_parser.add_argument(
        "--groups",
        "-g",
        action="store_true",
        help="Filter users by group name (matches description in Ludus)",
    )
    list_parser.add_argument(
        "--users",
        "-u",
        action="store_true",
        help="Filter users by username (matches description in Ludus)",
    )

    # subcommand: add
    add_parser = subparsers.add_parser(
        "add",
        help="add accounts and generate WireGuard configs",
    )
    add_common_args(add_parser)
    add_parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input CSV file containing account details",
    )
    add_parser.add_argument(
        "--output",
        "-o",
        default="./output",
        help="Directory to save the generated WireGuard config files",
    )
    add_parser.add_argument(
        "--public-ip",
        "-p",
        type=str,
        help="Overwrite config peer IP",
    )
    add_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force creation of groups and users even if they already exist in Ludus (use with caution)",
    )

    if argcomplete is not None:
        argcomplete.autocomplete(parser, always_complete_options=True)

    # If no arguments are provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()
