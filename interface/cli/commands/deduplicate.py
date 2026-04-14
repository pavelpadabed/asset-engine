from application.services.duplicate_service import DuplicateService
from application.services.duplicate_resolver import DecisionLayer
from application.services.delete_service import DeleteService
from interface.cli.presenters.asset_presenter import AssetPresenter

def confirm(message) -> bool:
    response = input(message)
    if response.strip().lower() in ("y", "yes"):
        return True
    return False

class DeduplicateCommand:
    def __init__(
            self, duplicate_service: DuplicateService,
            duplicate_resolver: DecisionLayer,
            delete_service: DeleteService,
            presenter: AssetPresenter
    ) -> None:
        self.duplicate_service = duplicate_service
        self.duplicate_resolver = duplicate_resolver
        self.delete_service = delete_service
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

        confirmed = confirm(message)

        if not confirmed:
            self.presenter.show_no_confirmation()
            return

        self.delete_service.delete_assets(assets_to_delete)

        self.presenter.show_deleted(decision_result)

        # TODO: Refactor DeduplicateCommand
        # - (Future) Consider extracting user interaction (confirm input)
        #   into a separate component (e.g., InputHandler / PromptService).
       







