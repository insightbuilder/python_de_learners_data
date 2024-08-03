import click


@click.command(help="Provides the options to ")
@click.option('--weeday', type=click.Choice([
    "monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"]
    )
)
def cli(weeday):
    click.echo(f"Weekday: {weeday}")


if __name__ == "__main__":
    cli()