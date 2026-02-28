import click

from controllers.users import (
    create_user,
    delete_user,
    get_all_users,
    update_user,
)
from views.user_view import display_all_users


@click.group()
def user_commands():
    pass


@user_commands.command(name="create")
@click.option('--nom', prompt='Nom', help="Nom de l'utilisateur.")
@click.option('--email', prompt='Email', help="Email de l'utilisateur.")
@click.password_option(
    '--password',
    prompt='Mot de passe',
    help='Mot de passe.'
)
@click.option(
    '--role',
    type=click.Choice(['Gestion', 'Commercial', 'Support']),
    prompt='Rôle',
    help="Rôle de l'utilisateur."
)
@click.pass_context
def create(ctx, nom, email, password, role):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
        click.secho(
            " Accès refusé. Seule l'équipe Gestion peut créer un utilisateur.",
            fg="red"
        )
        return

    if create_user(nom, email, password, role):
        click.secho(
            f" L'utilisateur {nom} a été créé avec succès !",
            fg="green"
        )
    else:
        click.secho(" Erreur : L'utilisateur n'a pas pu être créé.", fg="red")


@user_commands.command(name="list")
@click.pass_context
def list_users(ctx):
    if not ctx.obj:
        click.secho(
            " Vous devez être connecté pour voir cette liste.",
            fg="red"
        )
        return

    users = get_all_users()
    display_all_users(users)


@user_commands.command(name="update")
@click.option('--nom', prompt="Nom de l'utilisateur à modifier")
@click.option(
    '--role',
    type=click.Choice(['Gestion', 'Commercial', 'Support']),
    prompt='Nouveau rôle'
)
@click.pass_context
def update(ctx, nom, role):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
        click.secho(" Accès refusé.", fg="red")
        return

    if update_user(nom, role):
        click.secho(" Rôle mis à jour !", fg="green")
    else:
        click.secho(" Erreur : Utilisateur introuvable.", fg="red")


@user_commands.command(name="delete")
@click.option('--nom', prompt="Nom de l'utilisateur à supprimer")
@click.pass_context
def delete(ctx, nom):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
        click.secho(" Accès refusé.", fg="red")
        return

    if click.confirm(f"Êtes-vous sûr de vouloir supprimer {nom} ?"):
        if delete_user(nom):
            click.secho(" Utilisateur supprimé.", fg="green")
        else:
            click.secho(" Erreur : Utilisateur introuvable.", fg="red")
