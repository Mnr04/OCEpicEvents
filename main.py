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

