# ls.py Script that lists the files in the directory through command line
from pathlib import Path
import click
from collections import deque
from datetime import datetime


# ls.py v4
@click.command()
@click.option("-l", "--long", is_flag=True)
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
)
def cli(paths, long):
    for i, path in enumerate(paths):
        if len(paths) > 1:
            click.echo(f"{path}/:")
        for entry in path.iterdir():
            entry_output = build_output(entry, long)
            click.echo(f"{entry_output:{len(entry_output) + 5}}", nl=long)
        if i < len(paths) - 1:
            click.echo("" if long else "\n")
        elif not long:
            click.echo()


def build_output(entry, long=False):
    if long:
        size = entry.stat().st_size
        date = datetime.fromtimestamp(entry.stat().st_mtime)
        return f"{size:>6d} {date:%b %d %H:%M:%S} {entry.name}"
    return entry.name

# Commands can have arguments that are required / not-named
# Options are not-required, named, and modify the command's behavior
# v5 : implementing single value options for the arguments
# @click.command(help="Works as tails command")
# @click.option("-n", "--lines", type=click.INT,
              # default=5)
# @click.argument('file', type=click.File(mode='r'))
# def cli(file, lines):
    # for line in deque(file, maxlen=lines):
        # click.echo(line, nl=False)

# v4 : Using click to read files, and parameter_type called File
# @click.command('ls',
               # help='Prints content of the file')
# @click.option("-n", "--lines",
              # type=click.INT, default=10)
# @click.argument(
    # "files",
    # nargs=-1,
    # type=click.File(mode='r')
# )
# def cli(files):
    # for file in files:
        # click.echo(file.read().rstrip())
# v3
# Accepting Variadic Arguments: Argument with undetermined no of input args
# n_args argument can be > 1 or -1. in case of -1 the arguments are undetermined
# @click.command("ls",
               # help="Takes any number of folders.")
# @click.argument("paths",
                # nargs=-1,
                # type=click.Path(
                    # exists=True,
                    # file_okay=False,
                    # readable=True,
                    # path_type=Path
                # ))
# def cli(paths):
    # """Any number of paths can be provided, files in all 
    # paths will be listed"""
    # for i, path in enumerate(paths):
        # if len(paths) > 1:
            # click.echo(f"{path}/:")
        # for entry in path.iterdir():
            # click.echo(f"{entry.name:{len(entry.name) + 5}}",
                       # nl=False)
        # if i < len(paths) - 1:
            # click.echo('\n')
        # else:
            # click.echo()

# v2 : App with argument that has a type for its input defined in decorator
# @click.command(help="Program to list the files.")  # instantiates the command
# @click.argument("path",     # Adding a argument that knows the type
                # type=click.Path(
                    # exists=True,
                    # file_okay=False,
                    # readable=True,
                    # path_type=Path
                # ))
# def cli(path):
    # for entry in path.iterdir():
        # click.echo(f"{entry.name:{len(entry.name) + 5}}",
                   # nl=False)
    # click.echo()

# v1 : Plain click app, with argument and command
# @click.command(help="Program to list the files.")  # instantiates the command
# @click.argument("path")  # creates an argument to the command
# def cli(path):
    # tgt_path = Path(path)
    # if not tgt_path.exists():
        # click.echo("No Dir")
        # raise SystemExit(1)
    # for entry in tgt_path.iterdir():
        # click.echo(f"{entry.name:{len(entry.name) + 5}}",
                   # nl=False)
    # click.echo()


if __name__ == '__main__':
    cli()

# python ls.py .\samples