# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-06-26 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0014_bond_issuing_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]