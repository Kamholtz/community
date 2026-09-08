"""Persist Whisper insertion preferences and withheld transcripts locally."""

import json
from pathlib import Path
from threading import RLock
from uuid import uuid4


class InsertionPreferences:
    def __init__(self, path: Path):
        self.path = path
        self.lock = RLock()
        self.data = {"polished_only": None, "withheld": {}}
        if path.exists():
            self.data.update(json.loads(path.read_text(encoding="utf-8")))

    def enabled(self, default: bool) -> bool:
        value = self.data["polished_only"]
        return default if value is None else bool(value)

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        temporary.replace(self.path)

    def set_enabled(self, enabled: bool) -> None:
        with self.lock:
            self.data["polished_only"] = enabled
            self._save()

    def retain(self, text: str) -> str:
        with self.lock:
            identity = uuid4().hex
            self.data["withheld"][identity] = text
            self._save()
            return identity

    def release(self, identity: str) -> None:
        with self.lock:
            self.data["withheld"].pop(identity, None)
            self._save()

    def withheld_text(self) -> str:
        with self.lock:
            return "\n\n".join(self.data["withheld"].values())
