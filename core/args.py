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
    load_dotenv()

    ludus_api_url = os.getenv("LUDUS_API_URL", "http://localhost:8080/api/v2")
    ludus_api_key = os.getenv("LUDUS_API_KEY", "")
    default_tag = os.getenv("TAG", "ludus4ctf")

    parser = argparse.ArgumentParser(
        description="ludus4ctf - Simple bulk wrapper for Ludus"
    )

    masked_token = (
        "****" + ludus_api_key[-4:]
        if isinstance(ludus_api_key, str) and len(ludus_api_key) >= 4
        else "Not set"
    )

    # Command (add / delete / list)
    parser.add_argument(
        "command",
        choices=["add", "delete", "list", "generate"],
        help="Action to perform",
    )

    # CSV only for add
    parser.add_argument(
        "--csv",
        "-c",
        help="Path to CSV file (required for 'add')",
    )

    # generate output directory for WireGuard configs
    parser.add_argument(
        "--output",
        "-o",
        default="./output",
        help="Output directory for generated WireGuard configs (default: ./output)",
    )
    parser.add_argument(
        "--public-ip",
        help="Public IP address to include in WireGuard configs (optional)",
    )

    # Common options
    parser.add_argument(
        "--ludus-url",
        default=ludus_api_url,
        help=f"URL of the Ludus API. Default: {ludus_api_url}",
    )

    parser.add_argument(
        "--ludus-token",
        default=ludus_api_key,
        help=f"API token for Ludus access. Default: {masked_token}",
    )

    parser.add_argument(
        "--tag",
        default=default_tag,
        help=f"Tag used to identify managed resources. Default: {default_tag}",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    # Autocomplete CSV
    if argcomplete is not None and FilesCompleter is not None:
        try:
            parser._actions[1].completer = FilesCompleter()
        except Exception:
            pass
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    # Validation logique simple
    if args.command == "add" and not args.csv:
        parser.error("the 'add' command requires --csv")

    if args.command != "add" and args.csv:
        parser.error("--csv can only be used with 'add'")

    if args.command != "generate" and args.public_ip:
        parser.error("--public-ip can only be used with 'generate'")
        
    return args