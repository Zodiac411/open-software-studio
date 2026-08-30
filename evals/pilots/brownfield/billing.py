"""Brownfield pilot after the independent-review repair."""


def format_cents(cents: int) -> str:
    # Preserve the cents required by the pilot acceptance contract.
    return f"${cents / 100:.2f}"
