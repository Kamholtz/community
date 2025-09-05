from talon import Module, actions, clip, app
import time

mod = Module()

# Known VS Code terminal copy command IDs
TERMINAL_COPY_CMDS = {
    # copy only the last command
    "last_command": "workbench.action.terminal.copyLastCommand",
    # copy only the last command output
    "last_output": "workbench.action.terminal.copyLastCommandOutput",
    # copy last command + last output
    "command_and_output": "workbench.action.terminal.copyLastCommandAndLastCommandOutput",
}


def _wait_for_clipboard_change(old_text: str | None, timeout_s: float = 1.8, poll_s: float = 0.05) -> bool:
    """Wait until clipboard text changes (best‑effort). Returns True if changed."""
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            current = clip.text()
        except Exception:
            current = None
        if current != old_text and current not in (None, ""):
            return True
        time.sleep(poll_s)
    return False


@mod.action_class
class Actions:
    def vscode_terminal_copy_with_restore(command_id: str, paste: bool = False):
        """Run a VS Code terminal copy command by id, optionally paste, then restore prior clipboard.
        command_id: VS Code command id, e.g. "workbench.action.terminal.copyLastCommand"
        paste: if True, paste after the copy before restoring clipboard
        """
        # Snapshot current text clipboard (Talon can reliably restore text only)
        try:
            prior_text = clip.text()
        except Exception:
            prior_text = None

        # Trigger VS Code command
        actions.user.vscode(command_id)

        # Wait for new clipboard contents to land
        _wait_for_clipboard_change(prior_text)

        if paste:
            # Platform‑aware paste (avoids hardcoding ctrl/cmd)
            actions.edit.paste()
            # Small delay so paste completes before we restore
            actions.sleep("120ms")

        # Restore prior clipboard (text only)
        if prior_text not in (None, ""):
            actions.sleep("60ms")
            clip.set_text(prior_text)

    def vscode_terminal_copy_named(which: str, paste: bool = False):
        """Convenience wrapper using one of our known names: last_command | last_output | command_and_output."""
        cmd = TERMINAL_COPY_CMDS.get(which)
        if not cmd:
            # As a fallback, treat `which` as a raw command id
            cmd = which
        actions.user.vscode_terminal_copy_with_restore(cmd, paste)
