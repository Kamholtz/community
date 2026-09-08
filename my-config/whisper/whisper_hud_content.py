"""Pure formatting helpers for the Whisper HUD panel, choices, and logs.

No Talon imports so the module stays unit-testable outside Talon, matching
whisper_service_state.py. Output strings use Talon HUD rich-text markers:
<* bold, <+ green, <! orange, <!! red, <@ blue, /> close.
"""

from typing import Any, Optional

# Display names for whisper UI states; keep in sync with
# _WHISPER_STATUS_TEXT in whisper_mode.py.
STATE_TEXT = {
    "connecting": "Connecting",
    "connected": "Connected",
    "listening": "Listening",
    "voice_detected": "Voice",
    "realtime": "Live",
    "transcribing": "Transcribing",
    "final": "Final",
    "polishing": "Polishing",
    "polished": "Polished",
    "session_finishing": "Finishing",
    "context_pending": "Context",
    "context_ready": "Context Ready",
    "context_error": "Context Error",
    "connection_failed": "Failed",
    "disconnected": "Disconnected",
}

# Marker groups mirror _WHISPER_SUBTITLE_COLORS: green for settled/good,
# blue for live speech, orange for transitional, red for failures.
_STATE_MARKERS = {
    "connected": "<+",
    "polished": "<+",
    "context_ready": "<+",
    "voice_detected": "<@",
    "realtime": "<@",
    "transcribing": "<!",
    "final": "<!",
    "polishing": "<!",
    "session_finishing": "<!",
    "context_pending": "<!",
    "disconnected": "<!",
    "context_error": "<!!",
    "connection_failed": "<!!",
}

_DRAFT_MARKERS = {
    "realtime": "<@",
    "final": "<!",
    "polished": "<+",
}

_LOG_LEVELS = {
    "client_connected": "event",
    "client_disconnected": "warning",
    "client_connection_failed": "error",
    "context_updated": "event",
    "context_cleared": "event",
    "context_error": "error",
    "session_polished": "success",
    "session_error": "error",
    "control_error": "error",
}


def escape_rich_text(text: str) -> str:
    """Neutralise HUD marker syntax in user speech so it renders literally."""
    return text.replace("<", "‹").replace("/>", "/ >")


def _wrap(marker: str, text: str) -> str:
    return f"{marker}{text}/>" if marker else text


def state_marker(state: Optional[str]) -> str:
    return _STATE_MARKERS.get(state or "", "")


def service_marker(label: str) -> str:
    if label.startswith(("passed", "ready")):
        return "<+"
    if label.startswith(("failed", "unavailable", "disabled")):
        return "<!!"
    return "<!"


def format_state_line(state: Optional[str]) -> str:
    text = STATE_TEXT.get(state or "", (state or "off").replace("_", " ").title())
    return f"<*State:/> {_wrap(state_marker(state), text)}"


def format_services_line(services: Any) -> str:
    polish = services.polishing_label()
    context = services.context_extractor.label()
    return (
        f"<*Polish:/> {_wrap(service_marker(polish), polish)}\n"
        f"<*Context:/> {_wrap(service_marker(context), context)}"
    )


def format_shutdown_line(remaining_s: float) -> str:
    remaining = max(0, int(round(remaining_s)))
    return f"<!Finishing session... forcing stop in {remaining}s/>"


def format_preview(text: str, max_length: int = 60) -> str:
    preview = " ".join(text.split())
    if len(preview) > max_length:
        return preview[: max_length - 3] + "..."
    return preview


def format_whisper_panel(
    state: Optional[str],
    services: Any,
    session_lines: list[str],
    draft_text: Optional[str],
    draft_phase: Optional[str],
    shutdown_remaining_s: Optional[float] = None,
    session_tail: int = 8,
    input_device: Optional[str] = None,
) -> str:
    """Body for the combined Whisper HUD panel.

    Header: state + optional service health; then the rolling session
    transcript tail with the in-progress draft utterance colour-coded by
    phase (realtime blue, final orange, polished green).
    """
    lines = [format_state_line(state), format_services_line(services)]
    if input_device:
        lines.append(f"<*Mic → WSL:/> {escape_rich_text(input_device)}")
    if shutdown_remaining_s is not None:
        lines.append(format_shutdown_line(shutdown_remaining_s))

    transcript: list[str] = []
    for entry in session_lines[-session_tail:]:
        cleaned = " ".join(entry.split())
        if cleaned:
            transcript.append(escape_rich_text(cleaned))
    if draft_text and draft_text.strip():
        marker = _DRAFT_MARKERS.get(draft_phase or "", "<@")
        transcript.append(_wrap(marker, escape_rich_text(" ".join(draft_text.split()))))

    if transcript:
        lines.append("")
        lines.extend(transcript)
    return "\n".join(lines)


def build_history_choices(
    history: list[str], preview_len: int = 60
) -> list[dict]:
    """Choice payloads for hud_create_choices, newest-first and 1-based to
    match the `whisper pick <n>` numbering in whisper_mode.py."""
    return [
        {"text": f"{index}: {format_preview(text, preview_len)}", "index": index}
        for index, text in enumerate(reversed(history), 1)
    ]


def format_service_status_panel(services: Any) -> str:
    """Full service breakdown shown when the user asks for whisper status."""
    lines = [
        "<*Whisper service status/>",
        f"<*Dictation:/> {escape_rich_text(services.dictation_label())}",
        format_services_line(services),
    ]
    for name, service in (
        ("Polisher", services.polisher),
        ("Context extractor", services.context_extractor),
    ):
        if service.tested_at:
            lines.append(f"<*{name} tested:/> {escape_rich_text(service.tested_at)}")
        if service.detail:
            lines.append(f"<*{name} result:/> {escape_rich_text(service.detail)}")
    return "\n".join(lines)


def format_context_panel(status: Any) -> str:
    """Body for showing the current screen-context status on the HUD panel."""
    lines = ["<*Whisper screen context/>"]
    if not status:
        lines.append("No context status received")
    elif isinstance(status, dict):
        for key in ("status", "source", "updated_at", "text"):
            value = status.get(key)
            if value is not None:
                label = key.replace("_", " ").title()
                lines.append(f"<*{label}:/> {escape_rich_text(str(value))}")
    else:
        lines.append(escape_rich_text(str(status)))
    return "\n".join(lines)


def log_level_for_event(event_type: str) -> Optional[str]:
    return _LOG_LEVELS.get(event_type)


def log_level_for_service_change(old_label: str, new_label: str) -> Optional[str]:
    """Level for a service label transition; None when not worth logging."""
    if old_label == new_label:
        return None
    degraded = new_label.startswith(("failed", "unavailable", "disabled"))
    was_degraded = old_label.startswith(("failed", "unavailable", "disabled"))
    if degraded and not was_degraded:
        return "warning"
    if was_degraded and not degraded:
        return "success"
    return "event"
