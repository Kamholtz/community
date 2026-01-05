# LibreOffice Writer - Keyboard Shortcuts to Assign

This document lists LibreOffice Writer commands that currently **do NOT have keyboard shortcuts** but would be useful for Talon voice commands. You need to assign keyboard shortcuts to these functions in LibreOffice (Tools → Customize → Keyboard) before they can be used in Talon.

## Priority 1: Essential Selection Commands

These are the most useful for voice control and should be assigned first:

| Function | Suggested Shortcut | Talon Command | Notes |
|----------|-------------------|---------------|-------|
| Select Word | `Ctrl+Shift+W` | `select word` | Currently uses double-click workaround |
| Select Sentence | `Ctrl+Shift+S` | `select sentence` | Currently uses find dialog workaround |
| Select Paragraph | `Ctrl+Shift+P` | `select paragraph` | Currently uses triple-click workaround |
| Select to Begin of Word | `Ctrl+Shift+Alt+Left` | `select to word start` | Select from cursor to word beginning |
| Select to End of Word | `Ctrl+Shift+Alt+Right` | `select to word end` | Select from cursor to word end |
| Select to Paragraph Begin | `Ctrl+Shift+Alt+Up` | `select to paragraph start` | Better paragraph selection control |
| Select to Paragraph End | `Ctrl+Shift+Alt+Down` | `select to paragraph end` | Better paragraph selection control |
| Select to Next Sentence | `Alt+Shift+Right` | `select to next sentence` | Sentence-level selection |
| Select to Previous Sentence | `Alt+Shift+Left` | `select to previous sentence` | Sentence-level selection |

## Priority 2: Page-Level Selection

Useful for document navigation and editing:

| Function | Suggested Shortcut | Talon Command |
|----------|-------------------|---------------|
| Select to Page Begin | `Ctrl+Shift+PgUp` | `select to page start` |
| Select to Page End | `Ctrl+Shift+PgDn` | `select to page end` |
| Select to Next Page | `Alt+Shift+PgDn` | `select to next page` |
| Select to Previous Page | `Alt+Shift+PgUp` | `select to previous page` |

## Priority 3: Table Selection

Essential if working with tables:

| Function | Suggested Shortcut | Talon Command |
|----------|-------------------|---------------|
| Select Table | `Ctrl+Shift+T` | `select table` |
| Select Row | `Ctrl+Shift+R` | `select row` |
| Select Column | `Ctrl+Shift+K` | `select column` |
| Select Cell | `Ctrl+Shift+C` | `select cell` |

## Priority 4: Additional Selection

Nice to have but less critical:

| Function | Suggested Shortcut | Talon Command |
|----------|-------------------|---------------|
| Select to Top Line | `Ctrl+Shift+Alt+Home` | `select to top line` |
| Select Text | `F8` (already assigned to cycle) | N/A |
| Select Character Left | Already works: `Shift+Left` | N/A |
| Select Character Right | Already works: `Shift+Right` | N/A |
| Select Down | Already works: `Shift+Down` | N/A |

## How to Assign Keyboard Shortcuts in LibreOffice

1. Open LibreOffice Writer
2. Go to **Tools → Customize**
3. Click the **Keyboard** tab
4. In the **Category** list (bottom left), select **All commands**
5. In the **Function** list (bottom center), find the function you want to assign
6. In the **Shortcut Keys** list (top), select your desired key combination
7. Click **Modify** to assign the shortcut
8. Click **OK** to save

## Notes

- Avoid conflicts with existing shortcuts
- The suggested shortcuts above try to avoid conflicts with common LibreOffice shortcuts
- Test each shortcut after assignment to ensure it works
- Some shortcuts may vary by operating system (these are Linux-focused)

## After Assigning Shortcuts

Once you've assigned keyboard shortcuts to the functions above, update the Talon file at:
`apps/libreoffice/libreoffice.talon`

Add commands like:
```
select word: key(ctrl-shift-w)
select sentence: key(ctrl-shift-s)
select to word start: key(ctrl-shift-alt-left)
```
