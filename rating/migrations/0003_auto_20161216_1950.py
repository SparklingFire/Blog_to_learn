# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-16 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0002_auto_20161216_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleratingmodel',
            name='dislikes',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='articleratingmodel',
            name='likes',
            field=models.SmallIntegerField(default=0),
        ),
    ]