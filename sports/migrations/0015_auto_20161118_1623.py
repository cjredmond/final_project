# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 16:23
from __future__ import unicode_literals

from django.db import migrations
import csv

def add_team_data(apps, schema_editor):
    Team = apps.get_model("sports", "Team")
    with open('teams.csv') as infile:
        reader = csv.reader(infile)
        for row in reader:
            Team.objects.create(city=row[0], name=row[1], sport=row[2], pts_last=row[3],
             pts_proj=row[4])

class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0014_auto_20161118_1416'),
    ]

    operations = [
    migrations.RunPython(add_team_data)
    ]
