# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from powers.models import SuretyCompany, User, Defendant, Bond, Powers
from powers.utils import create_powers_batch, create_powers_batch_custom
from django.contrib.auth.models import (Group, Permission)
from powers.forms import TransferPowersForm
from powers.web_bot import run_bot, SC_COUNTIES
# Create your tests here.
from datetime import datetime


class TestModels(TestCase):
	def setUp(self):
		pass
	def test_find__all_counties(self):
