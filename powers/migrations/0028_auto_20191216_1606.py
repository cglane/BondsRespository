# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-12-16 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0027_bond_bot_last_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='bot_error',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
