# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from powers.web_bot import BondStatus, SC_COUNTIES, BotException
# Create your tests here.
from datetime import datetime


class TestModels(TestCase):
	def setUp(self):
		self.bond_status = BondStatus()

	def test_find__all_counties(self):
		for key in SC_COUNTIES:
			county_name = key[:-1]
			self.bond_status.find_county(county_name)

	def test_bad_county_name(self):
		try:
			result = self.bond_status.find_county('chast')
			assert not result
		except BotException as e:
			assert 'County not found for name' in str(e)

	def test_bad_warrant_id(self):
		try:
			self.bond_status.find_county("Charleston")
			self.bond_status._accept_terms()
			self.bond_status._fill_form('1222397087087087087087087')
			assert not self.bond_status._parse_results()
		except BotException as e:
			assert "No results with warrant number" in str(e)

	def test_run_bot(self):
		result = self.bond_status.run_bot('Charleston', '20190420152183')
		assert 'Jury Trial' in result
