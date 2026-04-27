---
name: talon-list-management
description: Manage and customize Talon lists, vocabulary, CSV files, and homophones. Use for adding custom words, overriding lists, working with .talon-list files, managing vocabulary, or customizing recognition patterns.
---

# Talon List Management

## When to Use

Use when changing vocabulary, homophones, .talon-list files, CSV lists, or list overrides.

## Overview
Talon uses list files (`.talon-list`) and CSV files for customization. This skill covers:
- Adding custom words to vocabulary
- Working with `.talon-list` files
- Overriding lists without forking the repository
- Managing homophones and replacements
- CSV file customization

## Core List Types

### Vocabulary Lists
Located in `core/vocabulary/`:

- **vocabulary.talon-list** - General vocabulary (abbreviations, proper nouns, technical terms)
- **words_to_replace.talon-list** - Common mishearings and corrections
- **homophones.csv** - Words that sound similar but are spelled differently
- **abbreviations.talon-list** - Common abbreviations

### Community Lists
Located throughout the codebase:

- `core/keys/` - Keyboard keys and modifiers
- `lang/` - Programming language-specific lists
- `apps/` - Application-specific commands and terms
- `plugin/` - Plugin-specific lists

## Using Voice Commands to Edit Lists

Talon provides voice commands to customize the most commonly changed lists:

```bash
# Say these voice commands to open for editing:
customize abbreviations      # core/vocabulary/abbreviations.talon-list
customize additional words   # core/vocabulary/additional_words.talon-list (user file)
customize alphabet          # core/keys/alphabet/alphabet-en.talon-list
customize homophones        # core/vocabulary/homophones.csv
customize search engines    # core/vocabulary/search_engines.csv
customize Unix utilities    # core/vocabulary/unix_utilities.talon-list
customize websites          # core/vocabulary/websites.talon-list
customize words to replace  # core/vocabulary/words_to_replace.talon-list
customize contacts json     # settings/contacts.json (user file)
customize contacts csv      # settings/contacts.csv (user file)
```

Commands are defined in `core/vocabulary/edit_vocabulary.talon`.

## Adding Words to Vocabulary

### Via Voice Commands
Use edit_vocabulary.talon commands:
```bash
add to vocabulary <word>     # Add to vocabulary.talon-list
add to replacements <word>   # Add to words_to_replace.talon-list
```

### Manual File Editing
1. Open `core/vocabulary/vocabulary.talon-list`
2. Add entry in format: `<word>: <representation>`
3. Example: `N V I D I A: NVIDIA`

## Overriding Lists (Clean Git Workflow)

**Best Practice:** Create override files instead of modifying existing lists to avoid merge conflicts.

### Method 1: Create New List File with Specific Context
```talon-list
# ~/.talon/user/my-overrides/my-vocabulary.talon-list
os: linux
lang: en
-

# Custom words (more specific context = higher priority)
my custom term: MY_TERM
```

### Method 2: Create in Community Subdirectory
```talon-list
# ~/.talon/user/community/core/vocabulary/my-additional-words.talon-list
lang: en
-

specialized term: SPEC_TERM
```

## talon-list File Format

### Basic Syntax
```talon-list
# Context header (optional, makes list more specific)
os: linux
lang: en
-

# Comments start with #
list_key: spoken form
# Multiple spoken forms with |
list_key: spoken form 1 | spoken form 2
```

### Context Headers (Specificity Order)
Most specific wins (your override beats default):
1. `os: linux` / `os: darwin` / `os: windows`
2. `lang: en` / `lang: de`, etc.
3. Application context
4. General context (no header = lowest specificity)

### Example: Comprehensive List
```talon-list
# ~/.talon/user/community/core/vocabulary/my-vocab.talon-list
lang: en
os: linux
-

# Technical terms
C U D A: CUDA
N V I D I A: NVIDIA
G P U: GPU

# Common corrections
git marge: git merge  # common mishearing
witch: which         # correction

# Abbreviations with alternatives
H T M L: HTML | HTML5
```

## CSV Files for Complex Mappings

### homophones.csv Format
Maps phrases that sound identical to their written forms:
```csv
homophones,replacement
see,C
to,2
four,4
won,1
for,4
be,B
```

Speech recognition alternatives are comma-separated in first column.

### search_engines.csv
```csv
search_engine,engine_url
google,https://google.com/search?q=
duckduckgo,https://duckduckgo.com?q=
github search,https://github.com/search?q=
```

## Common Customization Tasks

### Add a Pronunciation Override
```talon-list
# core/vocabulary/vocabulary.talon-list
my_project: My Project  # Override common mishearing
```

### Create Application-Specific Terms
```talon-list
# core/vocabulary/app-specific.talon-list
os: linux
-

vs code: VSCode
jet brains: JetBrains
```

### Override a Language-Specific List
```talon-list
# core/language-overrides.talon-list
code.language: python
-

decorator: @  # Python-specific override
```

## Managing Changes

Your workflow automatically handles list changes:

### Before Committing
- Verify `.talon-list` files follow proper format
- Test new vocabulary with speech recognition
- Use the Talon debug window to inspect list contents

### Automatic Commit on Exit
Your tmuxinator setup automatically commits:
```bash
git add *.talon-list *.csv
git commit -m "feat: update *.talon-list"
git push
```

## Troubleshooting

### List Not Being Recognized
1. Check files have `.talon-list` or `.csv` extension
2. Verify context header matches (e.g., `os: linux`)
3. Reload Talon to regenerate list caches
4. Use `events.tail()` in REPL to monitor load events

### Duplicate/Conflicting Entries
1. Search for duplicate keys across all list files
2. More specific context (with header) overrides general context
3. Last-defined value wins for same key in same file

### Performance Issues with Large Lists
- Split very large lists into multiple context-specific files
- Use specific context headers to reduce scope
- Avoid overly complex regular expressions in captures

## When to Use This Skill
- User asks about customizing Talon words or vocabulary
- Need to add pronunciation overrides
- Working with homophones or search engine lists
- Cleaning up git workflow with list file updates
- User mentions "customize", "vocabulary", ".talon-list", or "homophones"
- Troubleshooting speech recognition issues with specific words or terms
