# Docs

<https://talon.wiki/Customization/misc-tips>

## REPL

 executing a line like this on Linux would toggle whether Talon is listening to the microphone: bash -c "echo 'actions.speech.toggle()' | ~/.talon/bin/repl".

## Introspection functions

This section lists some built in methods which are useful for developing or debugging Talon behaviour. The following are all imported by default into the REPL and aren't really meant to be used outside that context.

sim("tab close") - Finds the .talon file that would handle the given command in the current context. If the command is not active in the current context, then it prints an error. Useful for finding the relevant code for a voice command. You might want to paste something like import time;time.sleep(5);sim("tab close") in to the REPL to give you a chance to switch to the appropriate context.
mimic("say hello world") - Executes the given voice command like you spoke it in to the microphone. Can be useful to re-run voice commands while editing them so you don't have to keep saying the same thing.
actions.find("string") - Searches the name, documentation, and code implementing an action for the given substring. Prints out a list of matches.
actions.list("edit") - Prints out all registered actions matching the given prefix. If no argument is supplied then lists all actions. See the basic customization page for a trick to copy this output into your clipboard.
events.tail() - If you're not getting enough information about what Talon is doing from the log file you can take a look at this method. It prints out Talon internal events, user actions called, scope changes etc. to the REPL. For even more logging try the events.tail(noisy=True) flag. You can also print out historical events and filter the events, run help(events.tail) to see the options.
registry.commands, registry.lists etc. - Lets you view the currently active set of commands, lists, actions etc. that Talon is considering.
API functions
