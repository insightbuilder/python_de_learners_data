"""You can create user prompts by using either the prompt argument to @click.option 
or the click.prompt() function. You’ll also have dedicated decorators, such as 
@click.password_option and @click.confirmation_option, to create password
and confirmation prompts."""

# user.py

import click


@click.command()
@click.option("--name", prompt="Username")
@click.option("--password", prompt="Password", hide_input=True)
def cli(name, password):
    if name != read_username() or password != read_password():
        click.echo("Invalid user credentials")
    else:
        click.echo(f"User {name} successfully logged in!")


def read_password():
    return "secret"


def read_username():
    return "admin"

if __name__ == "__main__":
    cli()

# change password for a user

# set_password.py

@click.command()
@click.option("--name", prompt="Username")
@click.password_option("--set-password", prompt="Password")
def cli(name, set_password):
    # Change the password here...
    click.echo("Password successfully changed!")
    click.echo(f"Username: {name}")
    click.echo(f"Password: {set_password}")

if __name__ == "__main__":
    cli()