from application.projections.asset_projection import AssetProjection
from application.dto.duplicate_analysis import DuplicateAnalysis


class DuplicateService:
    """Analyze asset projections and classify duplicate signals."""
    def analyze(self, projection: AssetProjection) -> DuplicateAnalysis:
        """
            Analyze an asset projection and classify it as:
            - re_observed
            - strong_duplicate_candidate
            - possible_moved
        """
        if len(projection.active_paths) == 1:
            return DuplicateAnalysis(
                projection=projection,
                outcome="re_observed"
            )
        if len(projection.active_paths) > 1:
            for i, path in enumerate(projection.active_paths):
                for other_path in projection.active_paths[i + 1:]:
                    if path.related_scan_ids & other_path.related_scan_ids:
                        return DuplicateAnalysis(
                            projection=projection,
                            outcome="strong_duplicate_candidate"
                        )

        return DuplicateAnalysis(
            projection=projection,
            outcome="possible_moved"
        )

    # TODO:
    # Revisit DuplicateOutcome enum after analysis rules stabilize.
    #
    # Current outcomes are simple strings:
    # - re_observed
    # - strong_duplicate_candidate
    # - possible_moved
    #
    # Introduce Enum only if outcome count grows and starts spreading
    # across multiple services.

    # TODO:
    # Revisit latest_observed_at usage.
    #
    # Field is intentionally preserved in AssetProjection but is not
    # currently required for duplicate classification.
    #
    # Potential future use:
    # - confidence scoring
    # - move detection refinement
    # - stale path handling

    # TODO:
    # Revisit Ambiguous category.
    #
    # Current rules fully classify known scenarios:
    # - ReObserved
    # - StrongDuplicateCandidate
    # - PossibleMoved
    #
    # Introduce Ambiguous only when a real-world scenario cannot be
    # confidently classified by existing rules.

    # TODO:
    # Revisit Rule Engine extraction.
    #
    # Current analyze() implementation is simple and readable.
    # Extract independent rule objects only if duplicate analysis
    # grows beyond several rules and starts becoming difficult to maintain.
