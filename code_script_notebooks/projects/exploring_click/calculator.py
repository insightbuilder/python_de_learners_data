# add.py
# click.STRING	Represents Unicode strings and is the default parameter type for arguments and options
# click.INT	Represents integer numbers
# click.FLOAT	Represents floating-point numbers
# click.BOOL	Represents Boolean values
# click.IntRange	Restricts the input value to a range of integer numbers
# click.FloatRange	Restricts the input value to a range of floating-point numbers
# click.DateTime	Converts date strings into datetime objects

import click


# @click.group(name='calculator')
# def calc():
    # pass


@click.command('add', help='Adds two values')
def add():
    a = click.prompt("Enter an integer", type=click.INT, default=0)
    b = click.prompt("Enter another integer", type=click.INT, default=0)
    click.echo(f"{a} + {b} = {a + b}")


@click.command('sub', help='Subtracts two values')
@click.option("--a", type=click.INT, default=0, prompt="Enter Interger here:")
@click.option("--b", type=click.INT, default=0, prompt='Enter another integer')
def sub(a, b):
    click.echo(f"{a} - {b} = {a - b}")


@click.command('mul', help='Multiplies two values')
def mul():
    a = click.prompt("Enter an integer", type=click.INT, default=0)
    b = click.prompt("Enter another integer", type=click.INT, default=0)
    click.echo(f"{a} * {b} = {a * b}")


@click.command('div', help='Divides two values')
def div():
    a = click.prompt("Enter an integer", type=click.INT, default=0)
    b = click.prompt("Enter another integer", type=click.INT, default=0)
    click.echo(f"{a} / {b} = {a / b}")

if __name__ == "__main__":
    calc()