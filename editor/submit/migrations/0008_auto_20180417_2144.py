# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-17 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0007_auto_20180416_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='host',
            field=models.CharField(default='0.0.0.0', max_length=128),
        ),
        migrations.AddField(
            model_name='profile',
            name='port',
            field=models.IntegerField(default=12347),
        ),
    ]
