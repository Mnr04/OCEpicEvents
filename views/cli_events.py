import click
from controllers.events import (
    create_event, get_all_events, update_event,
    delete_event, get_events_without_support, get_my_events
)
from views.event_view import afficher_tableau_events

@click.group()
def event_commands():
    pass

@event_commands.command(name="create")
@click.option('--contract-id', prompt='ID du Contrat', type=int)
@click.option('--date-start', prompt='Date de début (YYYY-MM-DD HH:MM)')
@click.option('--date-end', prompt='Date de fin (YYYY-MM-DD HH:MM)')
@click.option('--location', prompt='Lieu')
@click.option('--attendees', prompt='Nombre de participants', type=int)
@click.option('--notes', prompt='Notes / Description')
@click.pass_context
def create(ctx, contract_id, date_start, date_end, location, attendees, notes):
    user = ctx.obj
    if not user or user.get('role') != 'Commercial':
        click.secho(" Accès refusé. Seul un Commercial peut créer un événement.", fg="red")
        return

    if create_event(contract_id, date_start, date_end, location, attendees, notes, user.get('role'), user.get('user_id')):
        click.secho(" Événement créé avec succès !", fg="green")
    else:
        click.secho(" Erreur : Contrat introuvable, non signé, ou n'appartenant pas à vos clients.", fg="red")

@event_commands.command(name="list")
@click.option('--filtre', type=click.Choice(['tous', 'sans-support', 'mes-evenements']), default='tous', help="Filtrer les événements.")
@click.pass_context
def list_events(ctx, filtre):
    user = ctx.obj
    if not user:
        click.secho(" Vous devez être connecté.", fg="red")
        return

    if filtre == 'sans-support':
        events = get_events_without_support()
        click.secho("--- Événements sans Support assigné ---", fg="cyan")
    elif filtre == 'mes-evenements':
        events = get_my_events(user.get('user_id'))
        click.secho("--- Mes Événements (Support) ---", fg="cyan")
    else:
        events = get_all_events()

    afficher_tableau_events(events)

@event_commands.command(name="update")
@click.option('--event-id', prompt='ID de l\'événement à modifier', type=int)
@click.option('--support-id', type=int, help='ID du collaborateur Support à assigner (Gestion uniquement).', default=None)
@click.option('--notes', help='Nouvelles notes pour l\'événement (Support uniquement).', default=None)
@click.pass_context
def update(ctx, event_id, support_id, notes):
    user = ctx.obj
    if not user:
        click.secho(" Vous devez être connecté.", fg="red")
        return

    if update_event(event_id, user.get('role'), user.get('user_id'), nouveau_support_id=support_id, nouvelles_notes=notes):
        click.secho(" Événement mis à jour avec succès !", fg="green")
    else:
        click.secho(" Erreur : Modification refusée (mauvais rôle, événement introuvable, etc.).", fg="red")

@event_commands.command(name="delete")
@click.option('--event-id', prompt='ID de l\'événement à supprimer', type=int)
@click.pass_context
def delete(ctx, event_id):
    user = ctx.obj
    if not user or user.get('role') != 'Gestion':
         click.secho(" Accès refusé.", fg="red")
         return

    if click.confirm(f"Êtes-vous sûr de vouloir supprimer l'événement {event_id} ?"):
        if delete_event(event_id):
            click.secho(" Événement supprimé.", fg="green")
        else:
            click.secho(" Erreur : Événement introuvable.", fg="red")