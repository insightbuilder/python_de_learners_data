# rectangles.py where multi options are implemented in click
import click


@click.command()
@click.argument("name", default="World")
@click.option("--upper/--no-upper", default=False)
def cli(name, upper):
    message = f"Hello, {name}"
    if upper:
        message = message.upper()
    click.echo(message)

# @click.command()
# @click.option('-n', '--name',
              # multiple=True)
# def cli(name):
    # for n in name:
        # click.echo(f"Hello {n}")


# v3 : using different type for options
# @click.command(help="Prints the profile of user")
# @click.option('-p', '--profile', 
              # type=click.Tuple([str, int]))
# def show(profile):
    # click.echo(f"The user name is {profile[0]} \
# and the age is {profile[1]}")

# # v2 : using multiple type for options
# @click.command(help="provides area of rectangle")
# @click.option("--size",
              # type=(click.INT, click.INT))
# def cli(size):
    # wid, hg = size
    # click.echo(f"size: {size}")
    # click.echo(f"{wid} X {hg}")


# v1 : using single type for options
# @click.command()
# @click.option('--size', nargs=2,
              # type=click.INT)
# def cli(size):
    # wid, hig = size
    # click.echo(f"size: {size}")
    # click.echo(f"{wid} * {hig}")

if __name__ == "__main__":
    cli()
    # show()
