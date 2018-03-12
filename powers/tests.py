# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from powers.models import SuretyCompany, User, Defendant, Bond, Powers
from django.contrib.auth.models import (Group, Permission)
from powers.utils import create_powers_batch

# Create your tests here.

class TestUser(TestCase):
    super_user = {
    'username': 'charleslane23@gmail.com',
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
    def setUp(self):
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

    def test_create_powers_batch(self):
        pass