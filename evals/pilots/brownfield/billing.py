"""Brownfield pilot with one intentionally planted defect."""


def format_cents(cents: int) -> str:
    # Planted defect for the independent-review gate: cents are discarded.
    return f"${cents / 100:.0f}"
