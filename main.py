import sqlite3
from pathlib import Path

from interface.cli.parser import create_parser
from storage.sqlite.sqlite_asset_repository import SqliteAssetRepository
from application.services.save_service import SaveService
from application.services.search_service import SearchService
from application.components.hash.hash_calculator import HashCalculator
from domain.source import Source
from application.services.index_service import IndexService
from application.services.scan_service import ScanService
from interface.cli.presenters.asset_presenter import AssetPresenter
from interface.cli.commands.scan import ScanCommand
from interface.cli.commands.search import SearchCommand
from application.criteria.asset_search_criteria import AssetSearchCriteria

def create_scan_command(
        path: Path,
        hasher: HashCalculator,
        save_service: SaveService,
        presenter: AssetPresenter
) -> ScanCommand:
    source = Source.filesystem(path)
    index_service = IndexService(hasher, source)
    scan_service = ScanService()

    return ScanCommand(
        scan_service,
        index_service,
        save_service,
        presenter
    )

def create_search_command(
        search_service: SearchService,
        presenter: AssetPresenter
) -> SearchCommand:
    return SearchCommand(
        search_service,
        presenter
    )

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    with sqlite3.connect("assets.db") as connection:
        repository = SqliteAssetRepository(connection)

        save_service = SaveService(repository)
        search_service = SearchService(repository)

        hasher = HashCalculator()
        presenter = AssetPresenter()

        commands = {
            "scan": lambda: (
                create_scan_command(
                args.path,
                hasher,
                save_service,
                presenter
            ).execute(args.path)
            ),

            "search": lambda: (
                create_search_command(
                search_service,
                presenter
            ).execute(
                AssetSearchCriteria(
                    name_contains=args.name,
                    extension=args.ext,
                    modified_after=args.after,
                    modified_before=args.before,
                    min_size=args.min_size,
                    max_size=args.max_size
                )
            ))
        }

        command = commands.get(args.command)
        if not command:
            raise ValueError(f"Unknown command: {args.command}")

        command()


if __name__ == "__main__":
    main()
