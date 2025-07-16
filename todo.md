#  TODO

## Installation

- [ ] Update the install script
  - [ ] Include new repositories
  - [ ] Install Andreas configuration

- [x] Add modifier key alternatives: `modifier_key.talon-list`
- [x] raren, paren
- [x] raren, paren
- [ ] dictation mode command to enter: "feat/fix/refactor:" in git commits
- [x] use clean nvim in vscode to determine if configuration is interferring

- [ ] remap pascal formatter - can't find it in formatters list anymore
- [ ] find where talon hud went
Neovim command for sourcing a lua file
Replace the cut command with carve in all instances

- [ ] PopOS desktop shortcuts
- [ ] Why does clone line cause multiple cursors in cursor

- [ ] Update VSCode config to include cursor as an app

- [ ] Is there markdown filetype that I can use to insert a checkbox
user.insert_snippet_by_name

- [ ] How to do a text search across all files in the project


## Howto

- [ ] Howto trigger commands in neovim: next/- [ ] prev tab, find command OR find :, find command history
- [ ] How to take range in Cursorless
- [ ] Howto use snippets (markdown lists)
- [ ] how to change windows
- [ ] Add key maps for WezTerm
- [ ] How to enable Cursorless snippets
- [ ] How to take inside surrounding pairs

- [ ] How to take to the end of the line
- [ ] how to prevent the onscreen keyboard showing up on pop os
- [ ] hunt this <user.text> search with / in nvim

## Top level config


my-config\user.talon

## Symbols

community\core\keys\symbols.py

## Modifier Keys

community\core\keys\win\modifier_key.talon-list

## Words to Replace

community\settings\words_to_replace.csv


## Abbreviations

The abbreviations.csv file

command mode: "abbreviate work and progress" => wip

## File extensions

./settings/file_extensions.csv

command mode: "dot pie" => .py

## Vocabulary

Words that are used in dictation mode

vocabulary.talon-list

[commands for editing vocabulary](https://github.com/talonhub/community/blob/main/core/vocabulary/edit_vocabulary.talon)

## Example Use File Sets

[text](https://talon.wiki/integrations/talon_user_file_sets/)

## Created Cheatsheet

https://gist.github.com/tararoys/c538b7ae8e1f21db9a794c2c0f5becf4

[Generate A Cheatsheet](https://gist.github.com/tararoys/c538b7ae8e1f21db9a794c2c0f5becf4)


## Cursorless Settings

cursorless-settings\actions.csv


## Range Targets

take < > past end of line
take < > past start of line


Terminal workflow

from slack

If you use VSCode's terminal, you can compose your commands in a regular vscode tab, then say "bring line red bat" from within the terminal and have it appear. (There won't be hats on anything in the terminal itself ... so if I want to e.g. use the output of a command, I'll pipe it to a output.txt file that I then always have open in a tab) (edited)
1:20
Here's my horribly hacky talon command for that:
1:20
~~~
redirect that:
    "!! 2>&1 | tee -a ~/output.txt && echo `history 1` | cut -d' ' -f2- >> ~/output.txt"
        key(enter)
        ~~~


## dictation mouse command

 https://github.com/talonhub/community/blob/main/core/modes/dictation_mode.talon