# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-22 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0033_auto_20200622_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bond',
            old_name='dischard_explanation',
            new_name='discharged_explanation',
        ),
        migrations.RenameField(
            model_name='bond',
            old_name='discharded_user',
            new_name='discharged_user',
        ),
    ]
