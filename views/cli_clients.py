import click

from controllers.clients import (
    create_client,
    get_all_clients,
    update_client,
)
from utils import validate_email, validate_phone
from views.client_view import afficher_tableau_clients


@click.group()
def client_commands():
    pass


@client_commands.command(name="create")
@click.option('--nom', prompt='Nom', help='Nom du client.')
@click.option('--email', prompt='Email', help='Email du client.')
@click.option('--tel', prompt='Téléphone', help='Téléphone.')
@click.option(
    '--entreprise',
    prompt='Entreprise',
    help="Nom de l'entreprise."
)
@click.pass_context
def create(ctx, nom, email, tel, entreprise):
    user = ctx.obj
    if not user or user.get('role') != 'Commercial':
        click.secho(
            " Accès refusé. Seul un Commercial peut créer un client.",
            fg="red"
        )
        return

    if not validate_email(email):
        click.secho(" Le format de l'email est invalide.", fg="red")
        return

    if not validate_phone(tel):
        click.secho(
            " Le format du numéro de téléphone est invalide.",
            fg="red"
        )
        return

    if create_client(nom, email, tel, entreprise, user.get('user_id')):
        click.secho(" Client créé avec succès !", fg="green")
    else:
        click.secho(" Erreur lors de la création.", fg="red")


@client_commands.command(name="list")
@click.pass_context
def list_clients(ctx):
    if not ctx.obj:
        click.secho(" Vous devez être connecté.", fg="red")
        return

    clients = get_all_clients()
    afficher_tableau_clients(clients)


@client_commands.command(name="update")
@click.option('--nom', prompt='Nom exact du client')
@click.option('--entreprise', prompt="Nouveau nom d'entreprise")
@click.pass_context
def update(ctx, nom, entreprise):
    user = ctx.obj
    if not user or user.get('role') != 'Commercial':
        click.secho(" Accès refusé.", fg="red")
        return

    if update_client(nom, entreprise, user.get('user_id')):
        click.secho(" Client modifié !", fg="green")
    else:
        click.secho(
            " Erreur : Client introuvable ou vous n'êtes pas son "
            "contact commercial.",
            fg="red"
        )
