# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0009_auto_20161116_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='matchup',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]
