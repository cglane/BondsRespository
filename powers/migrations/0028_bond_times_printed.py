# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-22 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0027_bond_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='times_printed',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
