"""Persistent visibility and context-menu options for Whisper status icons."""

import json
from pathlib import Path


class WhisperHudButtons:
    def __init__(self, path: Path, actions, labels: dict[str, str], refresh, images=None):
        self.path = path
        self.actions = actions
        self.labels = labels
        self.refresh = refresh
        self.images = images or (lambda: {})
        self.hidden = set()
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
                    raise ValueError("expected a list of hidden button topics")
                self.hidden = set(data) & labels.keys()
            except (OSError, ValueError) as error:
                print(f"whisper_hud: could not load button preferences: {error}")

    def set_visible(self, topic: str, visible: bool) -> None:
        if topic not in self.labels:
            raise ValueError(f"Unknown Whisper HUD button: {topic}")
        hidden = self.hidden - {topic} if visible else self.hidden | {topic}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(sorted(hidden)), encoding="utf-8")
        temporary.replace(self.path)
        self.hidden = hidden
        if not visible:
            self.actions.hud_remove_status_icon(topic)
        self.refresh()

    def publish_icon(self, topic, icon) -> None:
        if topic not in self.hidden:
            self.actions.hud_publish_status_icon(topic, icon)
        else:
            self.actions.hud_remove_status_icon(topic)

    def publish_options(self) -> None:
        images = self.images()
        for topic, label in self.labels.items():
            visible = topic not in self.hidden
            button = self.actions.hud_create_button(
                f"{'Remove' if visible else 'Add'} {label}",
                lambda *_args, topic=topic, visible=visible: self.set_visible(topic, not visible),
                images.get(topic, ""),
            )
            # Conditional icons can be absent while enabled. Both branches must
            # describe the saved preference, rather than current availability.
            option = self.actions.hud_create_status_option(topic, button, button)
            self.actions.hud_publish_status_option(f"{topic}_option", option)
