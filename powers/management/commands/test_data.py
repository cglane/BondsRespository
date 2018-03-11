from django.core.management.base import BaseCommand
from django.contrib.auth.models import (Group, Permission)
from django.contrib.contenttypes.models import ContentType
from powers.utils import create_powers_batch
from datetime import datetime
from django.core.files import File
import os

from powers.models import (
    SuretyCompany,
    Defendant,
    User,
    Powers,
    Bond,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Command(BaseCommand):

    super_user = {
        'username': 'charleslane23@gmail.com',
        'password': '1Testing!',
        'first_name': 'Charles',
        'last_name': 'Lane',
        'email': 'charleslane23@gmail.com',
        'is_superuser': True,
        'is_staff': True
        }
        
    surety_company = {
        'title': 'Sinkler Surety',
        'address': '10 Palmetto Way Charleston SC',
        'prefix': 'SSE'
    }
    powers = {
        'powers_type': '5000',
        'surety_company_id': 1,
    }
    defendant = {
        'first_name': 'deshawn',
        'last_name': 'watson',
        'next_court_date': datetime.now()
    }
    bond = {
        'related_court': 'Charleston County',
        'county': 'Charleston',
        'city': 'Charleston',
        'warrant_number': '12345',
        'offences': 'murder and rape',
        'amount': 3000,
        'premium': 100
    }


    def handle(self, *args, **options):
        User.objects.create_user(**self.super_user)

        surety = SuretyCompany(**self.surety_company).save()

        agent = User.objects.create_user(
            contract_rate=.7,
            first_name="pablo",
            last_name="escobar",
            is_staff=True,
            username='test_user',
            email="me@you.com",
            password="1Testing!")

        defendant = Defendant(**self.defendant)
        defendant.save()
        defendant.agents.add(agent)

        new_group, found_group = Group.objects.get_or_create(name='new_group')
        perms = Permission.objects.all()

        # my_perms = [x.name for x in perms]
        my_perms = ['Can add bond', 'Can change bond', 'Can delete bond', 'Can add defendant', 'Can change defendant', 'Can delete defendant', 'Can change powers', 'Can change agent', 'Can add display field', 'Can change display field', 'Can delete display field', 'Can add filter field', 'Can change filter field', 'Can delete filter field', 'Can add format', 'Can change format', 'Can delete format', 'Can add report', 'Can change report', 'Can delete report']
        print (my_perms, 'my perms')
        for p in my_perms:
            perm = Permission.objects.get(name=p)
            new_group.permissions.add(perm)
        agent.groups.add(new_group.id)

        create_powers_batch()

        day = 1
        for power in Powers.objects.all():
            self.bond['powers'] = power
            self.bond['defendant_id'] = defendant.id
            self.bond['agent_id'] = agent.id
            bond = Bond(**self.bond)
            bond.save()
            bond.issuing_date = datetime(2017, 8, day, 20, 40)
            bond.save()
            day = day +1


