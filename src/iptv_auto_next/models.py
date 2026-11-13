"""Initial runtime data models.

The RunReport model is intentionally minimal at this foundation stage. Its fields
will be extended alongside the corresponding schema and workflow requirements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current UTC time as an aware datetime."""

    return datetime.now(UTC)


@dataclass(slots=True)
class RunReport:
    """Minimal report envelope for a single program invocation."""

    run_id: str
    mode: str
    started_at: datetime = field(default_factory=utc_now)
    finished_at: datetime | None = None
    status: str = "running"
    errors: list[dict[str, str]] = field(default_factory=list)

    def finish(self, status: str) -> None:
        """Mark the report as finished."""

        self.status = status
        self.finished_at = utc_now()
