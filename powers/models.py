# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
# from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from datetime import datetime
import pytz

local_tz = pytz.timezone('US/Eastern')

# Create your models here.


class SuretyCompany(models.Model):
    title = models.CharField(max_length=50)
    address = models.TextField()
    seal = models.ImageField(upload_to='static/%Y/%m/%d')
    prefix = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Surety Companies"

    def __str__(self):
        return self.title

    def print_content_one(self):
        content = getattr(settings, 'BOND_PRINT_CONTENT_ONE')
        return content.format(self.title)

    def print_content_two(self):
        content = getattr(settings, 'BOND_PRINT_CONTENT_TWO')
        return content

    def print_content_three(self):
        content = getattr(settings, 'BOND_PRINT_CONTENT_THREE')
        return content

    def print_content_four(self):
        datetime_object = datetime.now()
        local_dt = datetime_object.replace(
            tzinfo=pytz.utc).astimezone(local_tz)
        todays_date = local_tz.normalize(local_dt).strftime(
            "%dth day of %B A.D. %Y")
        content = getattr(settings, 'BOND_PRINT_CONTENT_FOUR')
        return content.format(self.title, todays_date)


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='static/avatars', blank=True, null=True)
    contract_rate = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('agent')
        verbose_name_plural = _('Agents')

    def __str__(self):
        if (self.first_name):
            return self.first_name + ' ' + self.last_name
        return self.username

    def __unicode__(self):
        if (self.first_name):
            return self.first_name + ' ' + self.last_name
        return self.username


class Defendant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    next_court_date = models.DateField()
    agents = models.ManyToManyField(User, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Powers(models.Model):
    POWERS_TYPES = (('5000.00', '5000.00'), ('15000.00', '15000.00'),
                    ('25000.00', '25000.00'), ('50000.00', '50000.00'),
                    ('100000.00', '100000.00'), ('150000.00', '150000.00'),
                    ('250000.00', '250000.00'), ('500000.00', '500000.00'))
    powers_type = models.CharField(max_length=50, choices=POWERS_TYPES)
    start_date_transmission = models.DateTimeField(blank=True, null=True, editable=False)
    end_date_field = models.DateField(editable=True)
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    surety_company = models.ForeignKey(SuretyCompany, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "powers"

    def __str__(self):
        return "ID{0} TP{1}".format(str(self.id), self.powers_type)

    def print_amount_dollars(self):
        amount = float(self.powers_type)
        money = '${:,.2f}'.format(amount)
        return '({0}) DOLLARS'.format(money)

    def print_expires_date(self):
        return self.end_date_field.strftime('%m/%d/%Y')



class Bond(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    defendant = models.ForeignKey(Defendant, on_delete=models.CASCADE)
    has_been_printed = models.BooleanField(default=False)
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    powers = models.OneToOneField(
        Powers,
        on_delete=models.CASCADE,

    )
    issuing_date = models.DateField(
        null=True,
        blank=True,
        auto_now_add=True,
        help_text="This will automatically be set when bond is printed")
    amount = models.FloatField()
    premium = models.FloatField()
    related_court = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20, )
    warrant_number = models.CharField(max_length=50)
    offences = models.TextField()

    def __str__(self):
        return str(self.powers) + ' ' + self.defendant.last_name

    def save(self, *args, **kwargs):
        # Check make sure amount is not greater than the powers.
        if self.amount > float(self.powers.powers_type):
            raise ValueError(
                "Amount of {0} can not be greater than Powers of, {0}".format(
                    self.amount, self.powers.powers_type))
        
        super(Bond, self).save(*args, **kwargs)

    def details(self):
        return [{
            'name': 'Bond Amount',
            'value': '${:,.2f}'.format(self.amount)
        }, {
            'name': 'Defendant',
            'value': self.defendant
        }, {
            'name': 'Court',
            'value': self.related_court
        }, {
            'name': 'Case Number',
            'value': self.warrant_number
        }, {
            'name': 'Premium',
            'value': '${:,.2f}'.format(self.premium)
        }, {
            'name': 'County',
            'value': self.county
        }, {
            'name': 'City/State',
            'value': self.city + '/' + self.state
        }, {
            'name': 'Charge',
            'value': self.offences
        }, {
            'name': 'Executing Agent',
            'value': self.agent
        }]
