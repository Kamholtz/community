"""State and readiness rules for optional Whisper server services."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ServiceState:
    enabled: Optional[bool] = None
    available: Optional[bool] = None
    test_state: str = "unknown"
    detail: str = ""
    tested_at: Optional[str] = None
    attempts: int = 0

    def apply_availability(self, content: Any) -> None:
        if not isinstance(content, dict):
            return
        enabled = content.get("enabled")
        available = content.get("available")
        if isinstance(enabled, bool):
            self.enabled = enabled
        if isinstance(available, bool):
            self.available = available
        if self.enabled is False:
            self.test_state = "disabled"
        elif self.available is False and self.test_state != "passed":
            self.test_state = "unavailable"

    def apply_test(self, passed: bool, detail: str, attempts: int = 1) -> None:
        self.test_state = "passed" if passed else "failed"
        self.detail = detail
        self.attempts = attempts
        self.tested_at = datetime.now().astimezone().isoformat(timespec="seconds")

    def verify_live(self, detail: str = "verified by live use") -> bool:
        """Record proof from a real event (e.g. a polished transcript), which
        is stronger evidence than a probe. Returns True when this changed the
        state; an existing pass (and its probe detail) is left untouched."""
        if self.test_state == "passed":
            return False
        self.apply_test(True, detail)
        return True

    def label(self) -> str:
        if self.enabled is False:
            return "disabled"
        if self.available is False:
            return "unavailable"
        if self.test_state == "passed":
            suffix = " after retry" if self.attempts > 1 else ""
            return f"passed{suffix}"
        if self.test_state == "failed":
            return "failed"
        if self.available is True:
            return "available, not tested"
        return self.test_state.replace("_", " ")


@dataclass
class WhisperServiceState:
    connected: bool = False
    polisher: ServiceState = field(default_factory=ServiceState)
    context_extractor: ServiceState = field(default_factory=ServiceState)
    whisper: ServiceState = field(default_factory=ServiceState)

    def apply_service_status(self, content: Any) -> None:
        if not isinstance(content, dict):
            return
        self.polisher.apply_availability(content.get("polisher"))
        self.context_extractor.apply_availability(content.get("context_extractor"))

    def dictation_label(self) -> str:
        if not self.connected:
            return "disconnected"
        if self.whisper.test_state == "failed":
            return "connected, Whisper test failed"
        if self.whisper.test_state == "passed":
            return "ready"
        return "connected, Whisper not tested"

    def polishing_label(self) -> str:
        if self.polisher.enabled is False:
            return "disabled; plain transcription available"
        if self.polisher.available is False:
            return "unavailable; plain transcription available"
        if self.polisher.test_state == "passed":
            return "ready"
        if self.polisher.test_state == "failed":
            return "failed; plain transcription available"
        if self.polisher.available is True:
            return "available, not tested"
        return "unavailable; plain transcription available"
