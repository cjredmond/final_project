# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 14:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0010_auto_20161116_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchup',
            old_name='end',
            new_name='tues_end',
        ),
        migrations.RenameField(
            model_name='matchup',
            old_name='start',
            new_name='tues_start',
        ),
    ]
