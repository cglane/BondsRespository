# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-12 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0006_auto_20180312_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='bond_fee',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
