# Contact student-number insertion

## Goal

Allow a student number held in the private `contacts.json` record to be
inserted through the normal Talon prose/text system. The expected spoken form
is `<contact name> student number`; for example, `Carl student number` inserts
the configured value.

## Scope

- Keep the upstream `core/contacts/contacts.py` unchanged.
- Implement the extension under `my-config/` so it remains a personal override
  and is unlikely to conflict with community updates.
- Continue to use the existing private `contacts.json` file. Add an optional
  `student_number` field to the relevant contact record.
- Do not add student numbers to `contacts.csv`; the CSV importer supports only
  names and email addresses.

## Proposed design

1. Create a personal Python module in `my-config/contacts/` (or the closest
   existing personal contacts location) that watches the private
   `contacts.json` file using the same Talon file-tracking pattern as the core
   contacts module.
2. Parse only records that supply both a usable spoken contact name and a
   non-empty `student_number`. Preserve the number as text so leading zeroes
   are never lost.
3. Populate a dedicated dynamic list, such as
   `user.contact_student_numbers`, mapping each supported spoken name to its
   student number. Reuse the full name, first name, and configured nicknames
   where practical; ensure a duplicate spoken name follows a documented,
   deterministic precedence rule.
4. Define a capture named `user.prose_contact_student_number` with the rule
   `{user.contact_student_numbers} student number`.
5. Make the capture available to the normal prose/text path without replacing
   or copying upstream captures. Prefer an additive personal capture or a
   narrowly scoped extension point; only alter a core capture if Talon offers
   no compatible additive mechanism.

## Example private data

```json
[
  {
    "email": "carl@example.com",
    "full_name": "Carl Example",
    "nicknames": ["Carl"],
    "student_number": "01234567"
  }
]
```

The private contact file must not be committed because it contains personal
identifying information.

## Validation

1. Run `python3 .agents/scripts/check_talon_config.py --skip-tests` after
   adding the Talon/Python files.
2. Check the latest Talon reload result with
   `python3 .agents/scripts/check_talon_config.py --talon-errors`.
3. Use the Talon REPL to confirm the dynamic list contains the intended entry
   and its value remains a string.
4. Use Talon phrase simulation to verify `<name> student number` selects the
   new capture, then mimic it in a safe text field to verify the exact digits
   are inserted.
5. Verify existing commands such as `<name> name`, `<name> full name`, and
   `<name> email` still behave unchanged.

## Rollback

Remove the personal extension module and its corresponding Talon capture file.
The extra `student_number` key in `contacts.json` is safely ignored by the core
contacts module, so it may remain or be removed independently.
