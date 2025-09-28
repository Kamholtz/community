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
- [x] Neovim command for sourcing a lua file
Replace the cut command with carve in all instances

- [ ] PopOS desktop shortcuts
- [ ] Why does clone line cause multiple cursors in cursor
- [ ] Update VSCode config to include cursor as an app
- [ ] Is there markdown filetype that I can use to insert a checkbox
user.insert_snippet_by_name

- [ ] How to do a text search across all files in the project
- [ ] command to tick the checkbox in a markdown file in vscode, obsidian and neovim


- [ ] Maybe I could use custom regex scopes in reporting
https://www.cursorless.org/docs/user/customization/#experimental-cursorless-custom-regex-scopes


## Howto

- [ ] make a vscode task for running commands in talon repl and getting recent logs or getting a recent error
- [ ] select a digit in Cursorless
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

XDG Open
2025-09-20 07:37:51.576    IO removing tag firefox_chatgpt
2025-09-20 07:37:51.576 WARNING tags: skipped because they have no matching declaration: (user.markdown, user.docker)
2025-09-20 07:37:51.726    IO win_event_handler: window.title=tmux:pop-os
2025-09-20 07:37:51.726    IO removing tag firefox_chatgpt
2025-09-20 07:37:51.726 WARNING tags: skipped because they have no matching declaration: (user.markdown, user.docker)
2025-09-20 07:38:03.763 ERROR    10:                      talon/scripting/talon_script.py:606 |
    9:                      talon/scripting/talon_script.py:308 |
    8:                           talon/scripting/actions.py:88  |
    7: user/community/core/edit_text_file/edit_text_file.py:57  | open_with_subprocess(path, ["xdg-open"..
    6:                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    5: user/community/core/edit_text_file/edit_text_file.py:67  | subprocess.run(args, timeout=0.5, chec..
    4:                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    3:                         lib/python3.11/subprocess.py:548 |
    2:                         lib/python3.11/subprocess.py:1026|
    1:                         lib/python3.11/subprocess.py:1950|
FileNotFoundError: [Errno 2] No such file or directory: 'xdg-open'

[The below error was raised while handling the above exception(s)]
2025-09-20 07:38:03.767 ERROR cb error topic="phrase" cb=SpeechSystem.engine_event
   16:      lib/python3.11/threading.py:995 * # cron thread
   15:      lib/python3.11/threading.py:1038*
   14:      lib/python3.11/threading.py:975 *
   13:                    talon/cron.py:156 |
   12:                     talon/vad.py:23  |
   11:                     talon/vad.py:129 |
   10: talon/scripting/speech_system.py:369 |
    9:             talon/engines/w2l.py:742 |
    8:      talon/scripting/dispatch.py:134 | # 'phrase' main:EngineProxy._redispatch()
    7: talon/scripting/speech_system.py:66  |
    6: -------------------------------------# [stack splice]
    5:      talon/scripting/dispatch.py:134 | # 'phrase' main:SpeechSystem.engine_event()
    4: talon/scripting/speech_system.py:442 |
    3:      talon/scripting/executor.py:111 |
    2:  talon/scripting/talon_script.py:707 |
    1:  talon/scripting/talon_script.py:610 |
talon.scripting.talon_script.TalonScriptError:
 in script at /home/carl/.talon/user/community/core/edit_text_file/edit_text_file.talon:2:
 > user.edit_text_file(edit_text_file)
FileNotFoundError: [Errno 2] No such file or directory: 'xdg-open'


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