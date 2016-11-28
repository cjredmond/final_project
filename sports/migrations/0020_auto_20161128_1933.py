# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0019_clock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='player',
        ),
        migrations.AddField(
            model_name='clock',
            name='draft',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='sports.Draft'),
            preserve_default=False,
        ),
    ]
