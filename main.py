import click
from controllers.auth import get_logged_user
from views.cli_auth import auth_commands
from views.cli_users import user_commands
from views.cli_clients import client_commands
from views.cli_contracts import contract_commands
from views.cli_events import event_commands

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = get_logged_user()

cli.add_command(auth_commands, name="auth")
cli.add_command(user_commands, name="users")
cli.add_command(client_commands, name="clients")
cli.add_command(contract_commands, name="contracts")
cli.add_command(event_commands, name="events")

if __name__ == "__main__":
    cli()