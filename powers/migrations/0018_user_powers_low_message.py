# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-09-08 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powers', '0017_auto_20190903_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='powers_low_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
