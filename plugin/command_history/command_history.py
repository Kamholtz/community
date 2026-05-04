from dataclasses import dataclass
from time import time
from typing import Optional
from uuid import uuid4

from talon import Module, actions, imgui, settings, speech_system

from ..subtitles.on_phrase import skip_phrase

# We keep command_history_size lines of history, but by default display only
# command_history_display of them.
mod = Module()
mod.setting("command_history_size", type=int, default=50)
mod.setting("command_history_display", type=int, default=10)

hist_more: bool = False
history: list["HistoryEntry"] = []
suppress_next_phrase: bool = False


@dataclass
class HistoryEntry:
    id: str
    text: str
    words: Optional[list[str]]
    app_name: str
    app_executable: str
    timestamp: float


def active_app_name() -> str:
    try:
        return actions.app.name() or ""
    except Exception:
        return ""


def active_app_executable() -> str:
    try:
        return actions.app.executable() or ""
    except Exception:
        return ""


def active_app_key() -> tuple[str, str]:
    return (active_app_name().lower(), active_app_executable().lower())


def phrase_words(j) -> Optional[list[str]]:
    parsed = j.get("parsed")
    unmapped = getattr(parsed, "_unmapped", None)
    if unmapped:
        return [str(word) for word in unmapped]

    words = j.get("phrase")
    return [str(word) for word in words] if words else None


def should_skip_history(text: str) -> bool:
    return text.lower() in {
        "quick pick",
        "code menu",
    }


def on_phrase(j):
    global history, suppress_next_phrase
    if suppress_next_phrase:
        suppress_next_phrase = False
        return

    if skip_phrase(j):
        return

    words = j.get("phrase")
    text = actions.user.history_transform_phrase_text(words)
    if text is not None:
        if should_skip_history(text):
            return

        history.append(
            HistoryEntry(
                str(uuid4()),
                text,
                phrase_words(j),
                active_app_name(),
                active_app_executable(),
                time(),
            )
        )
        history = history[-settings.get("user.command_history_size") :]


@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global history
    gui.text("Command History")
    gui.line()
    text = (
        history[:]
        if hist_more
        else history[-settings.get("user.command_history_display") :]
    )
    for entry in text:
        gui.text(entry.text)

    gui.spacer()
    if gui.button("Command history close"):
        actions.user.history_disable()


speech_system.register("phrase", on_phrase)


@mod.action_class
class Actions:
    def history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def history_enable():
        """Enables the history"""
        gui.show()

    def history_disable():
        """Disables the history"""
        gui.hide()

    def history_clear():
        """Clear the history"""
        global history
        history = []

    def history_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def history_less():
        """Show less history"""
        global hist_more
        hist_more = False

    def history_get(number: int) -> str:
        """returns the history entry at the specified index"""
        num = (0 - number) - 1
        return history[num].text

    def history_get_recent_for_active_app(limit: int) -> list:
        """Return recent replayable history entries for the active app."""
        name, executable = active_app_key()
        results = []

        for entry in reversed(history):
            entry_key = (entry.app_name.lower(), entry.app_executable.lower())
            if entry.words and entry_key == (name, executable):
                results.append(
                    {
                        "id": entry.id,
                        "text": entry.text,
                        "words": entry.words,
                        "app_name": entry.app_name,
                        "app_executable": entry.app_executable,
                        "timestamp": entry.timestamp,
                    }
                )
            if len(results) >= limit:
                break

        return results

    def history_replay_entry(entry_id: str):
        """Replay the history entry with the given id."""
        global suppress_next_phrase
        for entry in history:
            if entry.id == entry_id and entry.words:
                suppress_next_phrase = True
                try:
                    actions.mimic(entry.words)
                except Exception:
                    suppress_next_phrase = False
                return

    def history_transform_phrase_text(words: list[str]) -> Optional[str]:
        """Transforms phrase text for presentation in history. Return `None` to omit from history"""
        return " ".join(words) if words else None
