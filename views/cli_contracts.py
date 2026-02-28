import click

from controllers.contracts import (
    create_contract,
    delete_contract,
    get_all_contracts,
    get_contracts_unsigned,
    get_contracts_unpaid,
    update_contract,
)
from utils import validate_amount
from views.contract_view import afficher_tableau_contrats


@click.group()
def contract_commands():
    pass


@contract_commands.command(name="create")
@click.option(
    '--client-id',
    prompt='ID du Client',
    type=int,
    help='ID du client lié au contrat.'
)
@click.option(
    '--total',
    prompt='Montant Total (€)',
    type=float,
    help='Montant total du contrat.'
)
@click.option(
    '--reste',
    prompt='Reste à payer (€)',
    type=float,
    help='Montant restant à payer.'
)
@click.pass_context
def create(ctx, client_id, total, reste):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
        click.secho(
            " Accès refusé. Seule l'équipe Gestion peut créer un contrat.",
            fg="red"
        )
        return

    if not validate_amount(total) or not validate_amount(reste):
        click.secho(
            " Erreur : Les montants doivent être des nombres positifs.",
            fg="red"
        )
        return

    if reste > total:
        click.secho(
            " Erreur : Le reste à payer ne peut pas être supérieur au total.",
            fg="red"
        )
        return

    if create_contract(client_id, total, reste, user.get('role')):
        click.secho(" Contrat créé avec succès !", fg="green")
    else:
        click.secho(
            " Erreur : Client introuvable ou échec de création.",
            fg="red"
        )


@contract_commands.command(name="list")
@click.option(
    '--filtre',
    type=click.Choice(['tous', 'non-signes', 'non-payes']),
    default='tous',
    help="Filtrer la liste des contrats."
)
@click.pass_context
def list_contracts(ctx, filtre):
    if not ctx.obj:
        click.secho(" Vous devez être connecté.", fg="red")
        return

    if filtre == 'non-signes':
        contrats = get_contracts_unsigned()
        click.secho("--- Contrats Non Signés ---", fg="cyan")
    elif filtre == 'non-payes':
        contrats = get_contracts_unpaid()
        click.secho("--- Contrats Non Payés ---", fg="cyan")
    else:
        contrats = get_all_contracts()

    afficher_tableau_contrats(contrats)


@contract_commands.command(name="update")
@click.option('--contract-id', prompt='ID du contrat à modifier', type=int)
@click.option(
    '--montant',
    type=float,
    help='Nouveau montant total (Gestion uniquement).',
    default=None
)
@click.option(
    '--signe',
    is_flag=True,
    help='Passer le statut du contrat à SIGNÉ.'
)
@click.pass_context
def update(ctx, contract_id, montant, signe):
    user = ctx.obj
    if not user:
        click.secho(" Vous devez être connecté.", fg="red")
        return

    nouveau_statut = True if signe else None

    if update_contract(
        contract_id,
        user.get('role'),
        user.get('user_id'),
        nouveau_statut=nouveau_statut,
        nouveau_montant=montant
    ):
        click.secho(" Contrat mis à jour avec succès !", fg="green")
    else:
        click.secho(
            " Erreur : Contrat introuvable, ou vous n'avez pas les droits "
            "sur ce contrat.",
            fg="red"
        )


@contract_commands.command(name="delete")
@click.option('--contract-id', prompt='ID du contrat à supprimer', type=int)
@click.pass_context
def delete(ctx, contract_id):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
        click.secho(
            " Accès refusé. Seule l'équipe Gestion peut supprimer.",
            fg="red"
        )
        return

    confirm_msg = f"Êtes-vous sûr de supprimer le contrat {contract_id} ?"
    if click.confirm(confirm_msg):
        if delete_contract(contract_id, user.get('role')):
            click.secho(" Contrat supprimé.", fg="green")
        else:
            click.secho(" Erreur : Contrat introuvable.", fg="red")
