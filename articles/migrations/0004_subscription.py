# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-17 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20161216_0408'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(editable=False, max_length=40)),
                ('ip', models.CharField(editable=False, max_length=40)),
                ('new_comments', models.SmallIntegerField(default=0)),
                ('checked_comments', models.SmallIntegerField(default=0)),
                ('total_comments', models.SmallIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article')),
            ],
        ),
    ]
