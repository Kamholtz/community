"""Expose private contact student numbers to Talon prose.

The first JSON contact that provides a particular spoken name wins.  This
matches the order in ``contacts.json`` and makes duplicate aliases predictable.
"""

import json
import logging
from pathlib import Path

from talon import Context, Module, resource

mod = Module()
ctx = Context()

mod.list(
    "contact_student_numbers",
    desc="Maps contact names to the corresponding private student number.",
)

CONTACTS_PATH = Path(__file__).parents[2] / "private" / "contacts.json"
CONTACTS_PATH.parent.mkdir(exist_ok=True)
if not CONTACTS_PATH.exists():
    CONTACTS_PATH.write_text("[]", encoding="utf-8")


def spoken_names(contact: dict) -> dict[str, str]:
    """Return spoken aliases for a contact using the core contacts convention."""
    names = {}

    full_name_raw = contact.get("full_name", "")
    if isinstance(full_name_raw, str):
        pronunciation, separator, full_name = full_name_raw.partition(":")
        full_name = full_name.strip() if separator else full_name_raw.strip()
        pronunciation = pronunciation.strip() if separator else full_name
        if full_name and pronunciation:
            names[pronunciation] = full_name

            pronunciation_parts = pronunciation.split()
            full_name_parts = full_name.split()
            if len(pronunciation_parts) == len(full_name_parts):
                names[pronunciation_parts[0]] = full_name_parts[0]
            else:
                names[full_name_parts[0]] = full_name_parts[0]

    nicknames = contact.get("nicknames", [])
    if not isinstance(nicknames, list):
        return names

    for nickname_raw in nicknames:
        if not isinstance(nickname_raw, str):
            continue
        pronunciation, separator, nickname = nickname_raw.partition(":")
        nickname = nickname.strip() if separator else nickname_raw.strip()
        pronunciation = pronunciation.strip() if separator else nickname
        if nickname and pronunciation:
            names[pronunciation] = nickname

    return names


@resource.watch(str(CONTACTS_PATH))
def on_contacts_json(f):
    try:
        contacts = json.load(f)
    except Exception:
        logging.exception("Unable to parse contacts.json for contact student numbers")
        return

    if not isinstance(contacts, list):
        logging.error("contacts.json must contain a list for contact student numbers")
        return

    student_numbers = {}
    prose_snippets = {}
    for contact in contacts:
        if not isinstance(contact, dict):
            continue
        student_number = contact.get("student_number")
        if not isinstance(student_number, str) or not student_number.strip():
            continue

        for spoken_name in spoken_names(contact):
            if spoken_name in student_numbers:
                logging.warning(
                    "Ignoring duplicate contact student-number alias: %s", spoken_name
                )
                continue
            student_numbers[spoken_name] = student_number
            prose_snippets[f"{spoken_name} student number"] = student_number

    ctx.lists["user.contact_student_numbers"] = student_numbers
    ctx.lists["user.prose_snippets"] = prose_snippets


@mod.capture(rule="{user.contact_student_numbers} student number")
def prose_contact_student_number(m) -> str:
    return m.contact_student_numbers
