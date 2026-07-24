"""State primitives for associating Whisper ``full`` and ``polished`` events."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PendingTranscript:
    """A final transcript waiting for either polishing or fallback insertion."""

    identity: int
    original: str
    polished: Optional[str] = None
    inserted: bool = False
    fallback_job: Any = None

    @property
    def insertion_text(self) -> str:
        return self.polished or self.original


class TranscriptState:
    """Track the one ordered transcript that a ``polished`` event can replace."""

    def __init__(self) -> None:
        self._next_identity = 1
        self.pending: Optional[PendingTranscript] = None

    def reset(self) -> None:
        self._next_identity = 1
        self.pending = None

    def begin_full(self, text: str) -> tuple[Optional[PendingTranscript], PendingTranscript]:
        """Start tracking a full transcript and return any displaced pending one."""
        displaced = self.pending
        pending = PendingTranscript(self._next_identity, text)
        self._next_identity += 1
        self.pending = pending
        return displaced, pending

    def apply_polished(self, text: str) -> Optional[PendingTranscript]:
        """Associate polished text with the latest unresolved full transcript."""
        pending = self.pending
        if pending is None or pending.inserted:
            return None
        pending.polished = text
        return pending

    def resolve(self, identity: int) -> Optional[PendingTranscript]:
        """Mark and return a pending transcript if its identity is still current."""
        pending = self.pending
        if pending is None or pending.identity != identity or pending.inserted:
            return None
        pending.inserted = True
        self.pending = None
        return pending
