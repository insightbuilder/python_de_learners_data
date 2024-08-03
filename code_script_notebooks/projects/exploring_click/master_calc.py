import click
from calculator import (
    add,
    sub,
    div,
    mul
)


@click.group(name='calculator')
def calc():
    pass


calc.add_command(add)
calc.add_command(sub)
calc.add_command(div)
calc.add_command(mul)

if __name__ == '__main__':
    calc()
