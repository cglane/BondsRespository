# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-04 13:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0012_auto_20180604_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='powers',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='powers.Powers'),
        ),
        migrations.AlterField(
            model_name='defendant',
            name='next_court_date',
            field=models.CharField(max_length=50),
        ),
    ]
