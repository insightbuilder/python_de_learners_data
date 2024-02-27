import click


@click.command("upper", help="prints the string in upper or lower")
@click.argument("name", default="Universe")
@click.option("--upper", "casing", flag_value="upper")
@click.option("--lower", "casing", flag_value="lower")
def cli(name, casing):
    message = f"Hello, {name}"
    if casing == "upper":
        click.echo(message.upper())
    if casing == "lower":
        click.echo(message.lower())
    click.echo("select a casing")


if __name__ == '__main__':
    cli()
