from application.services.duplicate_service import DuplicateService
from application.services.duplicate_resolver import DecisionLayer
from application.services.delete_service import DeleteService
from interface.cli.presenters.asset_presenter import AssetPresenter
from interface.cli.promt.input_handler import InputHandler

class DeduplicateCommand:
    def __init__(
            self, duplicate_service: DuplicateService,
            duplicate_resolver: DecisionLayer,
            input_handler: InputHandler,
            delete_service: DeleteService,
            presenter: AssetPresenter
    ) -> None:
        self.duplicate_service = duplicate_service
        self.duplicate_resolver = duplicate_resolver
        self.delete_service = delete_service
        self.input_handler = input_handler
        self.presenter = presenter

    def execute(self) -> None:
        groups = self.duplicate_service.detect_duplicates()

        if not groups:
            self.presenter.show_no_duplicates()
            return

        decision_result = self.duplicate_resolver.build_decisions(groups)
        self.presenter.show_decisions(decision_result)

        assets_to_delete = decision_result.get_assets_to_delete()

        count_files = decision_result.total_files
        count_groups = decision_result.total_groups

        message = f"Delete {count_files} duplicates from {count_groups} groups? (y/n)"

        confirmed = self.input_handler.confirm(message)

        if not confirmed:
            self.presenter.show_no_confirmation()
            return

        self.delete_service.delete_assets(assets_to_delete)

        self.presenter.show_deleted(decision_result)

# TODO: Improve CLI confirmation message UX
# - use pluralization for "file/files" and "group/groups"
# - align wording with presenter output
# - consider moving message formatting to a separate helper








