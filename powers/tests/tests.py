# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from powers.models import SuretyCompany, User, Defendant, Bond, Powers
from powers.utils import create_powers_batch, create_powers_batch_custom
from django.contrib.auth.models import (Group, Permission)
from powers.forms import TransferPowersForm

# Create your tests here.
from datetime import datetime

def create_bond(agent):
    bond_dict = {
        'amount': 300.00,
        'premium': 200.00,
        'related_court': 'related court',
        'county': 'Charleston',
        'city': 'Charleston',
        'state': 'SC',
        'warrant_number': '234567',
        'offenses': 'crimes and punishment',
        'bond_fee': 10
    }

    power = Powers.objects.all().filter(agent__id=agent.id, bond__isnull=True).all()[0]
    defendant = Defendant.objects.all()[0]
    bond_record = Bond(**bond_dict)
    bond_record.defendant = defendant
    bond_record.agent = agent
    bond_record.powers = power
    bond_record.save()
    return bond_record


class TestModels(TestCase):
    super_user = {
    'username': 'test_admin',
    'password': '1Testing!',
    'first_name': 'Charles',
    'last_name': 'Lane',
    'email': 'charleslane23@gmail.com',
    'is_superuser': True,
    'is_staff': True
    }

    agent = {
        'username': 'test_user',
        'password': '1Testing!',
        'first_name': 'Juan',
        'last_name':'Pablo',
        'is_superuser': False,
        'is_staff': True
    }
    surety_company = {
        "title": 'Sinkler Surety',
        "address": '300 Shelmore',
        "prefix": 'SSE'
    }

    defendant = {
        "first_name": "James",
        "last_name": 'Watson',
        "next_court_date": datetime.today()
    }
    def setUp(self):
        SuretyCompany.objects.create(**self.surety_company)
        Defendant.objects.create(**self.defendant)
        User.objects.create_user(**self.super_user)
        agent = User.objects.create_user(**self.agent)

        ### Permissions for Agent
        new_group, found_group = Group.objects.get_or_create(name='new_group')
        perms = Permission.objects.all()
        my_perms = ['Can add bond', 'Can change bond', 'Can delete bond', 'Can add defendant', 'Can change defendant', 'Can delete defendant', 'Can change powers', 'Can change agent', 'Can add display field', 'Can change display field', 'Can delete display field', 'Can add filter field', 'Can change filter field', 'Can delete filter field', 'Can add format', 'Can change format', 'Can delete format', 'Can add report', 'Can change report', 'Can delete report']
        for p in my_perms:
            perm = Permission.objects.get(name=p)
            new_group.permissions.add(perm)
        agent.groups.add(new_group.id)

        ## Create Powers
        create_powers_batch()


    def test_create_bond(self):
        type = '5000.00'

        agent = User.objects.get(first_name='Juan')
        transfer_form = TransferPowersForm(agent=agent)
        create_powers_batch_custom(1, type)
        powers_of_type = Powers.objects.all().filter(powers_type=type, bond__isnull=True, agent__isnull=True)
        transfer_form.save(powers=powers_of_type[0])
        # Create Bond
        bond_record = create_bond(agent)

        self.assertEquals(bond_record.has_been_printed, False)
        self.assertEquals(bond_record.powers.powers_type, type)

        agent = User.objects.get(first_name='Juan')
        assert agent.powers_low_message
        assert '5000' in agent.powers_low_message

    def test_powers_low(self):
        type = '25000.00'
        agent = User.objects.get(first_name='Juan')
        create_powers_batch_custom(2, type)
        powers_of_type = Powers.objects.all().filter(powers_type=type, bond__isnull=True, agent__isnull=True)

        # Assign to user
        transfer_form = TransferPowersForm(agent=agent)
        transfer_form.save(powers=powers_of_type[0])

        # Assign to user
        transfer_form = TransferPowersForm(agent=agent)
        transfer_form.save(powers=powers_of_type[1])

        agent = User.objects.get(first_name='Juan')
        assert not agent.powers_low_message

        # Create bond
        bond_record = create_bond(agent)
        agent = User.objects.get(first_name='Juan')
        assert not agent.powers_low_message