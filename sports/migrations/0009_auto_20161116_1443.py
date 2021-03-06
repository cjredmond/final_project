# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0008_league_weekly_matchup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pts', models.FloatField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='payleague',
            name='player',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_1',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_10',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_11',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_12',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_13',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_14',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_15',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_16',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_17',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_2',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_3',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_4',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_5',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_6',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_7',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_8',
        ),
        migrations.RemoveField(
            model_name='team',
            name='week_9',
        ),
        migrations.AlterField(
            model_name='team',
            name='sport',
            field=models.CharField(choices=[('f', 'football'), ('k', 'basketball'), ('h', 'hockey'), ('s', 'soccer')], max_length=1),
        ),
        migrations.DeleteModel(
            name='PayLeague',
        ),
        migrations.AddField(
            model_name='score',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.Team'),
        ),
    ]
