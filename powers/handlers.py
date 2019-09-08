from django.core.mail import EmailMessage


def handle_low_powers(agent, powers):
    """Inform admin if agent is low for powers"""

    low_powers_message = "Agent running low for powers type: {}".format(str(powers.powers_type))
    agent.powers_low_message = low_powers_message
    agent.save()

    email = EmailMessage('Hello', 'World', to=['charleslane23@gmail.com'])
    email.send()
