# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0007_auto_20161115_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='weekly_matchup',
            field=models.BooleanField(default=False),
        ),
    ]
