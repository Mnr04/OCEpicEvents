import click

from controllers.auth import login_user, logout_user


@click.group()
def auth_commands():
    pass


@auth_commands.command(name="login")
@click.option(
    '--username',
    prompt="Nom d'utilisateur",
    help="Votre identifiant."
)
@click.password_option(
    '--password',
    prompt="Mot de passe",
    help="Votre mot de passe."
)
def login(username, password):
    token = login_user(username, password)

    if token:
        click.secho(f"Connexion réussie pour {username} !", fg="green")
    else:
        click.secho("Identifiants incorrects.", fg="red")


@auth_commands.command(name="logout")
def logout():
    logout_user()
    click.secho("Vous avez été déconnecté avec succès.", fg="green")
