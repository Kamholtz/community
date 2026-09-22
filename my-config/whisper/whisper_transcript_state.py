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
    recovery_id: Optional[str] = None
    insertion_mode: Optional[str] = None

    @property
    def insertion_text(self) -> str:
        return self.original if self.insertion_mode == "raw" else self.polished or self.original


class TranscriptState:
    """Track the one ordered transcript that a ``polished`` event can replace."""

    def __init__(self) -> None:
        self._next_identity = 1
        self.pending: Optional[PendingTranscript] = None

    def reset(self) -> None:
        self._next_identity = 1
        self.pending = None

    def begin_full(self, text: str, insertion_mode: Optional[str] = None) -> tuple[Optional[PendingTranscript], PendingTranscript]:
        """Start tracking a full transcript and return any displaced pending one."""
        displaced = self.pending
        pending = PendingTranscript(self._next_identity, text, insertion_mode=insertion_mode)
        self._next_identity += 1
        self.pending = pending
        return displaced, pending

    def apply_polished(self, text: str) -> Optional[PendingTranscript]:
        """Associate polished text with the latest unresolved full transcript."""
        pending = self.pending
        if pending is None or pending.inserted or pending.insertion_mode == "raw":
            return None
        pending.polished = text
        return pending

    def resolve(self, identity: int, polished_only: bool = False) -> Optional[PendingTranscript]:
        """Mark and return a pending transcript if its identity is still current."""
        pending = self.pending
        if pending is None or pending.identity != identity or pending.inserted:
            return None
        if (pending.insertion_mode == "polished" or (pending.insertion_mode is None and polished_only)) and not pending.polished:
            return None
        pending.inserted = True
        self.pending = None
        return pending
