# hello.py  The first script that will be executed using Click
# This will contain all the variations that is discussed in 
# https://realpython.com/python-click/
from pathlib import Path
import click


# to get multiple functions to register 
# below group to be used
@click.group()
def cli():
    pass  # will act as register


@cli.command("hello",
             help="First hello world code.")
@click.version_option("0.1.0", prog_name="hello")
def hello():
    click.echo("Hello there!!!")

# python hello.py
# python hello.py --version
# python hello.py --help

# argument is a required or optional piece
# of information that a command uses to perform its intended action.
#  variadic argument is one that accepts an
# undetermined number of input values at the command line.
# Options are named, non-required arguments that
# modify a command’s behavior.
# options can:
# >> Prompt for input values
# >> Act as flags or feature switches
# >> Pull their value from environment variables
# Multiple functions can be registered


@cli.command('ls',
             help="This will list the files in given path")  # cli is registered as subcommand
@click.argument("path")
def ls(path):
    tgt_dir = Path(path)
    if not tgt_dir.exists():
        click.echo("Directory absent")
        raise SystemExit(1)
 
    for entry in tgt_dir.iterdir():
        click.echo(f"{entry.name:{len(entry.name) + 5}}", nl=False)

    click.echo()


if __name__ == "__main__":
    cli()
