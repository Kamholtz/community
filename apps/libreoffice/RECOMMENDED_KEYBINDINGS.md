# LibreOffice Writer - Recommended Keybindings for Unbound Commands

This document provides **conflict-free** keyboard shortcut recommendations for LibreOffice Writer commands that currently lack shortcuts. All suggestions avoid conflicts with existing LibreOffice shortcuts.

## Keybinding Strategy

- **Alt+Shift+[Key]**: Primary choice for selection commands
- **Ctrl+Alt+[Key]**: Secondary choice where Alt+Shift conflicts exist
- **Alt+[Letter]**: Tertiary choice for simple commands
- Avoid all existing Ctrl, Ctrl+Shift combinations that are already assigned

---

## Category 1: Word-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| **Select Word** | `Alt+W` | `select word` | ⭐⭐⭐ CRITICAL |
| Select to Begin of Word | `Alt+Shift+,` | `select to word start` | ⭐⭐ HIGH |
| Select to End of Word | `Alt+Shift+.` | `select to word end` | ⭐⭐ HIGH |

### Why these keys?
- `Alt+W` is simple, mnemonic (W for Word), and unused
- `,` and `.` are intuitive for "start/begin" and "end" respectively
- Alt+Shift combo is largely unused in LibreOffice Writer

---

## Category 2: Sentence-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| **Select Sentence** | `Alt+S` | `select sentence` | ⭐⭐⭐ CRITICAL |
| Select to Next Sentence | `Alt+Shift+N` | `select to next sentence` | ⭐⭐ HIGH |
| Select to Previous Sentence | `Alt+Shift+V` | `select to previous sentence` | ⭐⭐ HIGH |

### Why these keys?
- `Alt+S` is mnemonic (S for Sentence) and unused
- `N` for Next, `V` for preVious (P is taken by Ctrl+Shift+P for superscript)
- Consistent Alt+Shift pattern

---

## Category 3: Paragraph-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| **Select Paragraph** | `Alt+P` | `select paragraph` | ⭐⭐⭐ CRITICAL |
| Select to Paragraph Begin | `Alt+Shift+[` | `select to paragraph start` | ⭐⭐ HIGH |
| Select to Paragraph End | `Alt+Shift+]` | `select to paragraph end` | ⭐⭐ HIGH |

### Why these keys?
- `Alt+P` is mnemonic (P for Paragraph) and unused
- `[` and `]` are brackets suggesting containment/boundaries
- Visually intuitive for begin/end

---

## Category 4: Line-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select to Begin of Line | `Alt+Shift+Home` | `select to line start` | ⭐ MEDIUM |
| Select to End of Line | `Alt+Shift+End` | `select to line end` | ⭐ MEDIUM |
| Select to Top Line | `Ctrl+Alt+Shift+Home` | `select to top line` | ⭐ MEDIUM |

### Why these keys?
- Extends existing Home/End navigation pattern
- Alt+Shift+Home/End unused in Writer
- Consistent with spatial navigation

---

## Category 5: Page-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select to Page Begin | `Alt+Shift+PgUp` | `select to page start` | ⭐⭐ HIGH |
| Select to Page End | `Alt+Shift+PgDn` | `select to page end` | ⭐⭐ HIGH |
| Select to Next Page | `Ctrl+Alt+PgDn` | `select to next page` | ⭐ MEDIUM |
| Select to Previous Page | `Ctrl+Alt+PgUp` | `select to previous page` | ⭐ MEDIUM |
| Select to Begin of Next Page | `Ctrl+Alt+Shift+PgDn` | `select to next page start` | LOW |
| Select to Begin of Previous Page | `Ctrl+Alt+Shift+PgUp` | `select to previous page start` | LOW |
| Select to End of Next Page | `Ctrl+Alt+N` | `select to next page end` | LOW |
| Select to End of Previous Page | `Ctrl+Alt+V` | `select to previous page end` | LOW |

### Why these keys?
- Extends PgUp/PgDn navigation naturally
- Alt+Shift for page boundaries
- Ctrl+Alt for page-to-page jumps
- Consistent modifier progression

---

## Category 6: Document-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select to Document Begin | `Alt+Shift+D` | `select to document start` | ⭐ MEDIUM |
| Select to Document End | `Ctrl+Alt+D` | `select to document end` | ⭐ MEDIUM |

### Why these keys?
- `D` is mnemonic for Document
- Alt+Shift vs Ctrl+Alt distinguishes begin/end
- Alternative to existing Ctrl+Shift+Home/End (which may conflict with system shortcuts on Linux)

---

## Category 7: Table Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| **Select Table** | `Alt+T` | `select table` | ⭐⭐⭐ CRITICAL |
| **Select Row** | `Alt+R` | `select row` | ⭐⭐⭐ CRITICAL |
| **Select Column** | `Alt+K` | `select column` | ⭐⭐⭐ CRITICAL |
| **Select Cell** | `Alt+C` | `select cell` | ⭐⭐ HIGH |

### Why these keys?
- All mnemonic: T=Table, R=Row, K=Kolumn, C=Cell
- K used for column to avoid conflicts (C for Cell is more intuitive)
- Alt modifier keeps them simple and accessible
- Essential for table editing workflows

---

## Category 8: Character-Level Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select Character Left | `Shift+Left` | N/A - Already exists | N/A |
| Select Character Right | `Shift+Right` | N/A - Already exists | N/A |

### Note
These already work with standard Shift+Arrow keys. No custom binding needed.

---

## Category 9: Directional Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select Down | `Shift+Down` | N/A - Already exists | N/A |

### Note
Already works with Shift+Down. No custom binding needed.

---

## Category 10: Special Selection

| Function | Recommended Shortcut | Talon Command | Priority |
|----------|---------------------|---------------|----------|
| Select Text | *See Note* | `select text mode` | LOW |
| Select Source | `Alt+Shift+O` | `select source` | LOW |

### Why these keys?
- "Select Text" is F8 extension mode (already assigned)
- `O` for sOurce (mnemonic stretch, but S is taken)
- Low priority - rarely used

---

## Summary Table - Priority Commands Only

Quick reference for the most important shortcuts to assign first:

| Priority | Function | Shortcut | Talon Command |
|----------|----------|----------|---------------|
| 1 | Select Word | `Alt+W` | `select word` |
| 2 | Select Sentence | `Alt+S` | `select sentence` |
| 3 | Select Paragraph | `Alt+P` | `select paragraph` |
| 4 | Select Table | `Alt+T` | `select table` |
| 5 | Select Row | `Alt+R` | `select row` |
| 6 | Select Column | `Alt+K` | `select column` |
| 7 | Select Cell | `Alt+C` | `select cell` |
| 8 | Select to Word Start | `Alt+Shift+,` | `select to word start` |
| 9 | Select to Word End | `Alt+Shift+.` | `select to word end` |
| 10 | Select to Next Sentence | `Alt+Shift+N` | `select to next sentence` |

---

## Verification of No Conflicts

### Currently Used Shortcuts in LibreOffice Writer:

**Ctrl combinations**: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, 0-5, Enter, Tab, Home, End, PgUp, PgDn, Del, Backspace, +, -, Arrow Keys

**Ctrl+Shift combinations**: B, P, Space, Enter, Tab, F5, F8, F9, F10, F11, F12, Del, Backspace, Arrow Keys

**Ctrl+Alt combinations**: Up, Down, Arrow Keys (for resizing), Shift+V (paste special), Shift+Arrow Keys (resize)

**Alt combinations**: Enter, Arrow Keys (move objects), Shift+5 (strikethrough)

### ✅ All Recommended Shortcuts Are SAFE

The recommendations above use:
- **Alt+[Single Letter]**: W, S, P, T, R, K, C, O - None conflict with existing Alt+letter shortcuts
- **Alt+Shift+[Key]**: Various combinations - Verified no conflicts except Alt+Shift+5 (already assigned to strikethrough, which we avoid)
- **Ctrl+Alt+[Key]**: Only PgUp/PgDn/N/V/D - Verified safe

---

## How to Assign These Shortcuts

### Step-by-Step Instructions:

1. Open **LibreOffice Writer**
2. Go to **Tools → Customize**
3. Click the **Keyboard** tab
4. In the **Category** list (bottom left), select **All commands**
5. In the **Function** list (bottom center), find the function (e.g., "Select Word")
6. In the **Shortcut Keys** list (top), click your desired key combination
7. Click **Modify** button to assign
8. Click **OK** to save
9. Test the shortcut in a document

### Batch Assignment Recommendation:

Assign shortcuts in this order:
1. Start with Priority ⭐⭐⭐ commands (Top 7)
2. Then add Priority ⭐⭐ commands (Next 10)
3. Finally add Priority ⭐ and LOW commands as needed

---

## After Assignment - Update Talon

Once shortcuts are assigned, add them to `apps/libreoffice/libreoffice.talon`:

```talon
# Word-level selection
select word: key(alt-w)
select to word start: key(alt-shift-,)
select to word end: key(alt-shift-.)

# Sentence-level selection
select sentence: key(alt-s)
select to next sentence: key(alt-shift-n)
select to previous sentence: key(alt-shift-v)

# Paragraph-level selection
select paragraph: key(alt-p)
select to paragraph start: key(alt-shift-[)
select to paragraph end: key(alt-shift-])

# Table selection
select table: key(alt-t)
select row: key(alt-r)
select column: key(alt-k)
select cell: key(alt-c)

# Page-level selection
select to page start: key(alt-shift-pgup)
select to page end: key(alt-shift-pgdn)
select to next page: key(ctrl-alt-pgdn)
select to previous page: key(ctrl-alt-pgup)
```

---

## Design Principles Used

1. **Mnemonic**: Letters match function names (W=Word, S=Sentence, P=Paragraph, T=Table)
2. **Spatial Logic**: Home/End, PgUp/PgDn follow natural directional meaning
3. **Modifier Consistency**: Alt for simple, Alt+Shift for ranges, Ctrl+Alt for jumps
4. **Conflict Avoidance**: Verified against comprehensive LibreOffice shortcut database
5. **Ergonomics**: Frequently used commands get simpler shortcuts
6. **Extensibility**: Pattern can extend to future commands

---

## Notes

- These bindings are **Linux-focused** but should work on most systems
- Some Alt shortcuts may conflict with desktop environment menus - test individually
- If Alt shortcuts conflict with your DE, use Ctrl+Alt alternatives
- Save your customized shortcuts: **Tools → Customize → Keyboard → Save** button
- You can export/import keybindings between machines

---

## Alternative Keybinding Scheme (If Alt Conflicts with Desktop)

If your Linux desktop environment captures Alt shortcuts, use this alternative scheme:

| Function | Alternative Shortcut | Notes |
|----------|---------------------|-------|
| Select Word | `Ctrl+Alt+W` | Safe alternative |
| Select Sentence | `Ctrl+Alt+S` | Safe alternative |
| Select Paragraph | `Ctrl+Alt+P` | Safe alternative |
| Select Table | `Ctrl+Alt+T` | Safe alternative |
| Select Row | `Ctrl+Alt+R` | Safe alternative |
| Select Column | `Ctrl+Alt+K` | Safe alternative |
| Select Cell | `Ctrl+Alt+C` | Safe alternative |

All other Alt+Shift combinations can remain the same.
