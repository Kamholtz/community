from talon import Module, Context, app, ui, actions, resource
from pathlib import Path
import csv
import re

from ..formatters.formatters import de_camel


mod = Module()
ctx = Context()

mod.list("running_application", "All running applications")
ctx.lists["user.running_application"] = {}

# Mapping of current overrides
overrides = {}
# List of running applications
running_applications = {}


def read_app_name_overrides(file) -> dict[str, str]:
    result = {}
    rows = csv.reader(file, skipinitialspace=True)
    for row in rows:
        row = [cell.rstrip() for cell in row]
        if not row or (len(row) == 1 and not row[0]) or row[0].startswith("#"):
            continue
        if len(row) == 1 and row[0] == "-":
            continue
        if row[0] == "Application name":
            continue
        if len(row) == 1:
            result[row[0]] = row[0]
        elif len(row) == 2:
            result[row[0]] = row[1]
        else:
            raise ValueError(f"Can't create dict from csv with row length {len(row)}")
    return result


def parse_name(name):
    if name.lower() in overrides:
        return overrides[name.lower()]
    # Remove executable file ending
    if name.endswith(".exe"):
        name = name.rsplit(".", 1)[0]
    # Remove the last `-` and everything after it
    if " - " in name:
        name = name.rsplit(" - ", 1)[0]
    # Remove numbers
    name = re.sub(r"\d", "", name)
    # Split on camel case
    name = re.sub(r"[^a-zA-Z]", " ", name)
    name = de_camel(name)
    return name


def update_running():
    global running_applications
    running = {}
    for a in ui.apps(background=False):
        name = parse_name(a.name)
        if name:
            running[name] = a.name
    running_applications = running
    ctx.lists["user.running_application"] = running


@mod.action_class
class Actions:
    def get_running_applications() -> dict[str, str]:
        """Fetch a dict of running applications"""
        return running_applications


@resource.watch(Path(__file__).parent / "app_name_overrides.csv")
def update_overrides(f):
    """Updates the overrides list"""
    global overrides
    csv_dict = read_app_name_overrides(f)
    overrides = {k.lower(): v for k, v in csv_dict.items()}
    update_running()


def on_ready():
    ui.register("app_launch", lambda _: update_running())
    ui.register("app_close", lambda _: update_running())
    update_running()


app.register("ready", on_ready)
