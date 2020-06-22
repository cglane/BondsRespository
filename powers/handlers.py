from django.core.mail import send_mail
from django.conf import settings


def handle_low_powers(agent, powers):
    """Inform admin if agent is low for powers"""

    low_powers_message = "Agent: {} is running low on powers of type: {}".format(agent, powers.powers_type)
    agent.powers_low_message = low_powers_message
    agent.save()

    subject = "Low Powers Inventory"
    send_mail(subject, low_powers_message, settings.LOGIN_HEADER, recipient_list=settings.ADMIN_EMAILS)


def handle_voided_bond(agent, bond, reason_to_void):
    message = f'{agent} has voided bond: {bond}. Reason: {reason_to_void}'
    subject = "Voided Bond"
    send_mail(subject, message, settings.LOGIN_HEADER, recipient_list=settings.ADMIN_EMAILS)