from typing import Iterable
from collections import Counter

from domain.asset import Asset
from utils.time_utils import format_datetime
from application.dto.deduplicate_result import DecisionResult

class AssetPresenter:
    def _pluralize(self, count: int, word: str) -> str:
        return word if count == 1 else word + "s"

    def show_scan_result(self, count: int) -> None:
        print("No assets found" if not count else f"Found {count} assets")

    def show_search_result(self, assets: Iterable[Asset]) -> None:
        count = 0
        ext_counter = Counter()

        print("\nResults: \n")

        for asset in assets:
            count += 1

            ext = asset.path.suffix.lower().lstrip(".") or "no_ext"
            ext_counter[ext] += 1

            print(f"– {asset.path}")

        if not count:
            print("No assets found")
            return

        print(f"\nFound {count} assets")

        print("\nBy extension:")
        for ext, c in ext_counter.most_common():
            print(f"{ext}: {c}")

    def show_duplicates(self, duplicates: list[list[Asset]]) -> None:
        for n, group in enumerate(duplicates, start=1):
            files = ["  " + asset.path.name.lower() for asset in group]
            print(f"Group {n}:\n  {'\n'.join(files)}\n")

    def show_no_duplicates(self) -> None:
        print("No duplicates found in the scanned data.")

    def show_decisions(self, decision_result: DecisionResult) -> None:
        groups = decision_result.total_groups
        files = decision_result.total_files
        files_to_delete = decision_result.total_files_to_delete

        print(
            f"Found {files} {self._pluralize(files, 'file')} "
            f"in {groups} {self._pluralize(groups, 'group')}\n"
            f"{files_to_delete} {self._pluralize(files_to_delete, 'file')} "
            f"will be deleted\n"
        )

        for i, group in enumerate(decision_result.groups, start=1):
            asset = group.to_keep
            time = format_datetime(asset.metadata.modified_time)
            filename = asset.path.name.strip().lower()
            delete_count = len(group.to_delete)
            print(
                f"Group {i}:\n"
                f"  Keep: {filename} ({time})\n"
                f"  Delete: {delete_count} {self._pluralize(delete_count, 'file')}\n"
            )

    def show_no_confirmation(self) -> None:
        print("Deletion cancelled. No files were removed.")

    def show_deleted(self, decision_result: DecisionResult) -> None:
        count_files = decision_result.total_files_to_delete
        count_groups = decision_result.total_groups

        print(
            f"Deleted {count_files} {self._pluralize(count_files, 'file')} "
            f"from {count_groups} {self._pluralize(count_groups, 'group')}"
        )







