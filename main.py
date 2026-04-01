import sqlite3

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

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    with sqlite3.connect("assets.db") as connection:
        repository = SqliteAssetRepository(connection)

        save_service = SaveService(repository)
        search_service = SearchService(repository)

        hasher = HashCalculator()

        presenter = AssetPresenter()

        if args.command == "scan":
            source = Source.filesystem(args.path)
            index_service = IndexService(hasher, source)
            scan_service = ScanService()
            scan_command = ScanCommand(
                scan_service,
                index_service,
                save_service,
                presenter
            )
            scan_command.execute(args.path)

        elif args.command == "search":
            criteria = AssetSearchCriteria(
                name_contains=args.name,
                extension=args.ext,
                modified_after=args.after,
                modified_before=args.before
                #TODO:min and max sizes
            )
            search_command = SearchCommand(
                search_service,
                presenter
            )
            search_command.execute(criteria)

if __name__ == "__main__":
    main()
