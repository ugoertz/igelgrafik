# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('igelmain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aufgabe',
            name='doccoHTML',
            field=models.TextField(max_length=100000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aufgabe',
            name='quelltext',
            field=models.TextField(max_length=50000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beispiel',
            name='doccoHTML',
            field=models.TextField(max_length=100000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beispiel',
            name='quelltext',
            field=models.TextField(max_length=50000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kapitel',
            name='doccoHTML',
            field=models.TextField(max_length=100000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kapitel',
            name='quelltext',
            field=models.TextField(max_length=50000),
            preserve_default=True,
        ),
    ]
