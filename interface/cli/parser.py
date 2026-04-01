import argparse
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="asset-engine",
        description="Asset Engine CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a folder")
    scan_parser.add_argument(
        "path",
        type=Path,
        help="Path to folder"
    )

    search_parser = subparsers.add_parser("search", help="Search assets")
    search_parser.add_argument("--name", type=str, help="Filter by name")
    search_parser.add_argument("--ext", type=str,
                               help="Filter by extension"
    )
    search_parser.add_argument("--after", type=str, help="Modified after date")
    search_parser.add_argument("--before", type=str, help="Modified before date")

    return parser