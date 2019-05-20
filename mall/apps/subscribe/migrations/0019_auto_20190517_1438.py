# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-17 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe', '0018_auto_20190517_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articledetailmodel',
            name='bids_id',
        ),
        migrations.RemoveField(
            model_name='articledetailmodel',
            name='mid',
        ),
        migrations.AddField(
            model_name='user',
            name='article',
            field=models.ManyToManyField(related_name='addarticle', to='subscribe.Bids'),
        ),
        migrations.DeleteModel(
            name='ArticledetailModel',
        ),
    ]
