from django.db.models import Count
from django.conf import settings

from powers.models import User, Powers


def pluck_type(type, powers):
    for item in powers:
        if item['powers_type'] == type:
            return item['total']
    return 0


def agent_powers_count():
    """Get all the unused powers for an agent"""
    all_agent_return_list = []
    types = [x[0] for x in settings.POWERS_TYPES]
    agents = User.objects.all().filter(is_superuser=False, is_active=True, is_staff=True)
    for local_user in agents:
        agent_list = [local_user.first_name, ]

        # Retrieve agent powers
        # <QuerySet [{'powers_type': '5000.00', 'total': 10}, ]>
        powers = Powers.objects.all()\
            .filter(agent__id=local_user.id,
                    bond__isnull=True)\
            .values('powers_type')\
            .annotate(total=Count('powers_type'))\
            .order_by('total')

        # Order list of values to display
        for type in types:
            agent_list.append(pluck_type(type, powers))

        all_agent_return_list.append(agent_list)
    return all_agent_return_list



def convert_type(type):
    """Format the strings to display as PK.."""
    return str(float(type[0])/1000)[:-2]