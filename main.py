import sqlite3
from pathlib import Path
from datetime import datetime

from storage.sqlite.sqlite_asset_repository import SqliteAssetRepository
from application.services.save_service import SaveService
from application.services.search_service import SearchService
from application.components.hash.hash_calculator import HashCalculator
from domain.source import Source
from application.services.index_service import IndexService
from application.services.scan_service import ScanService
from interface.cli.parser import create_parser
from interface.cli.commands.duplicate import DuplicateCommand
from interface.cli.commands.deduplicate import DeduplicateCommand
from interface.cli.presenters.asset_presenter import AssetPresenter
from interface.cli.commands.scan import ScanCommand
from interface.cli.commands.search import SearchCommand
from interface.cli.promt.input_handler import InputHandler
from application.criteria.asset_search_criteria import AssetSearchCriteria
from application.services.duplicate_service import DuplicateService
from application.services.duplicate_resolver import DecisionLayer
from application.services.delete_service import DeleteService

def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)

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

def create_duplicate_command(
        duplicate_service: DuplicateService,
        presenter: AssetPresenter
) -> DuplicateCommand:
    return DuplicateCommand(
        duplicate_service,
        presenter
    )

def create_deduplicate_command(
        duplicate_service: DuplicateService,
        duplicate_resolver: DecisionLayer,
        input_handler: InputHandler,
        delete_service: DeleteService,
        presenter: AssetPresenter
) -> DeduplicateCommand:
    return DeduplicateCommand(
        duplicate_service,
        duplicate_resolver,
        input_handler,
        delete_service,
        presenter
    )



def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    with sqlite3.connect("assets.db") as connection:
        repository = SqliteAssetRepository(connection)

        save_service = SaveService(repository)
        search_service = SearchService(repository)
        duplicate_service = DuplicateService(repository)
        delete_service = DeleteService(repository)


        hasher = HashCalculator()
        presenter = AssetPresenter()
        duplicate_resolver = DecisionLayer()
        input_handler = InputHandler()

        try:
            parsed_after = parse_datetime(getattr(args, "after", None))
            parsed_before = parse_datetime(getattr(args, "before", None))
        except ValueError:
            print("Invalid date format. Please use ISO format: YYYY-MM-DD")
            return

        commands = {
            "scan": lambda: create_scan_command(
                args.path,
                hasher,
                save_service,
                presenter
            ).execute(args.path),

            "search": lambda: create_search_command(
                search_service,
                presenter
            ).execute(criteria = AssetSearchCriteria(
            name_contains=args.name,
            extension=args.ext,
            modified_after=parsed_after,
            modified_before=parsed_before,
            min_size=args.min_size,
            max_size=args.max_size
        )),

            "duplicate": lambda: create_duplicate_command(
                duplicate_service,
                presenter
            ).execute(),

            "deduplicate": lambda: create_deduplicate_command(
                duplicate_service,
                duplicate_resolver,
                input_handler,
                delete_service,
                presenter
            ).execute()
        }

        command = commands.get(args.command)
        if not command:
            raise ValueError(f"Unknown command: {args.command}")

        command()


if __name__ == "__main__":
    main()

# TODO: Refactor main() for cleaner command handling and argument safety
# - use getattr(args, "after", None) and getattr(args, "before", None)
#   to avoid AttributeError for non-search commands
# - move AssetSearchCriteria creation inside "search" command lambda
#   to avoid unnecessary object creation for other commands
# - consider isolating command-specific argument parsing per command
#   (each command should only depend on its own args)
# - optionally validate required args (e.g. args.path for scan) before execution
# - consider moving command wiring (commands dict) into a separate factory/helper
#   to simplify main() and reduce clutter
# - keep main() focused on composition root responsibilities only
