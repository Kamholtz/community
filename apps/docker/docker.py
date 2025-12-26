from talon import Context, Module

mod = Module()
ctx = Context()

mod.tag("docker", desc="Tag for enabling Docker commands in the terminal")

mod.list("docker_command", desc="Docker commands")
mod.list("docker_arguments", desc="Docker command arguments and flags")


@mod.capture(rule="{user.docker_arguments}+")
def docker_arguments(m) -> str:
    """A non-empty sequence of docker command arguments, preceded by a space."""
    return " " + " ".join(m.docker_arguments)


# Common Docker commands
ctx.lists["user.docker_command"] = {
    "run": "run",
    "exec": "exec",
    "ps": "ps",
    "build": "build",
    "pull": "pull",
    "push": "push",
    "images": "images",
    "start": "start",
    "stop": "stop",
    "restart": "restart",
    "rm": "rm",
    "rmi": "rmi",
    "logs": "logs",
    "inspect": "inspect",
    "tag": "tag",
    "commit": "commit",
    "cp": "cp",
    "diff": "diff",
    "top": "top",
    "stats": "stats",
    "attach": "attach",
    "kill": "kill",
    "pause": "pause",
    "unpause": "unpause",
    "wait": "wait",
    "export": "export",
    "import": "import",
    "save": "save",
    "load": "load",
    "history": "history",
    "info": "info",
    "version": "version",
    "login": "login",
    "logout": "logout",
    "search": "search",
    "network": "network",
    "volume": "volume",
    "system": "system",
    "compose": "compose",
}

# Common Docker arguments and flags
ctx.lists["user.docker_arguments"] = {
    "interactive": " -i",
    "tee": " -t",
    "interactive tee": " -it",
    "detached": " -d",
    "all": " -a",
    "force": " -f",
    "quiet": " -q",
    "verbose": " -v",
    "no cache": " --no-cache",
    "remove": " --rm",
    "privileged": " --privileged",
    "read only": " --read-only",
    "user": " --user",
    "workdir": " --workdir",
    "env": " --env",
    "volume": " --volume",
    "port": " --port",
    "publish": " --publish",
    "network": " --network",
    "name": " --name",
    "label": " --label",
    "tag": " --tag",
    "file": " --file",
    "follow": " --follow",
    "tail": " --tail",
    "since": " --since",
    "until": " --until",
    "format": " --format",
    "filter": " --filter",
    "help": " --help",
}
