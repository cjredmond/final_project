# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0006_auto_20161115_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='league',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]