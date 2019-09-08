# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from powers.models import SuretyCompany, User, Defendant, Bond, Powers
from powers.utils import create_powers_batch
from django.contrib.auth.models import (Group, Permission)


# Create your tests here.
from datetime import datetime

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



    def test_powers(self):
        powers = Powers.objects.all()
        powers_types = [float(x.powers_type) for x in powers]
        self.assertEquals(len(powers), 8)
        self.assertEquals(max(powers_types), 500000.00)
        self.assertEquals(min(powers_types), 5000.00)

        agent = User.objects.get(first_name="Juan")
        power = Powers.objects.filter(powers_type='5000.00')[0]
        power.agent = agent
        power.end_date_field = datetime.today()
        power.start_date_transmission = datetime.now()
        power.save()

        self.assertEquals(power.agent.first_name, 'Juan')

    def test_create_bond(self):

        agent = User.objects.get(first_name='Juan')
        power = Powers.objects.all()[0]
        defendant = Defendant.objects.all()[0]
        bond_dict = {
            'amount': 300.00,
            'premium': 200.00,
            'related_court': 'related court',
            'county': 'Charleston',
            'city': 'Charleston',
            'state': 'SC',
            'warrant_number': '234567',
            'offenses': 'crimes and punishment'
        }
        bond_record = Bond(**bond_dict)
        bond_record.defendant = defendant
        bond_record.agent = agent
        bond_record.powers = power
        bond_record.save()

        self.assertEquals(bond_record.has_been_printed, False)
        self.assertEquals(bond_record.powers.powers_type, '5000.00')


