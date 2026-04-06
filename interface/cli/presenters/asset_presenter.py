from typing import Iterable
from collections import Counter
from domain.asset import Asset

class AssetPresenter:
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
            files = [asset.path.name.lower() for asset in group]
            print(f"Group {n}:\n  {'\n'.join(files)}\n")




