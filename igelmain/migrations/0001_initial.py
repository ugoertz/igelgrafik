# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aufgabe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titel', models.CharField(max_length=50)),
                ('zusammenfassung', models.TextField(max_length=500)),
                ('kategorie', models.CharField(max_length=2, choices=[(b'0', b'Einstieg'), (b'1', b'Schleifen'), (b'2', b'Funktionen'), (b'3', b'Bedingungen'), (b'4', b'F\xc3\xbcr Fortgeschrittene')])),
                ('platz', models.FloatField()),
                ('quelltext', models.TextField(max_length=2000)),
                ('doccoHTML', models.TextField(max_length=20000)),
                ('bild', models.ImageField(upload_to=b'tutorial')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Beispiel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titel', models.CharField(max_length=50)),
                ('autor', models.CharField(max_length=200)),
                ('quelltext', models.TextField(max_length=2000)),
                ('doccoHTML', models.TextField(max_length=20000)),
                ('bild', models.ImageField(upload_to=b'tutorial')),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kapitel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titel', models.CharField(max_length=50)),
                ('zusammenfassung', models.TextField(max_length=500)),
                ('kategorie', models.CharField(max_length=2, choices=[(b'0', b'Einstieg'), (b'1', b'Schleifen'), (b'2', b'Funktionen'), (b'3', b'Bedingungen'), (b'4', b'F\xc3\xbcr Fortgeschrittene')])),
                ('platz', models.FloatField()),
                ('quelltext', models.TextField(max_length=2000)),
                ('doccoHTML', models.TextField(max_length=20000)),
                ('bild', models.ImageField(upload_to=b'tutorial')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kategorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.CharField(unique=True, max_length=20)),
                ('intro', models.TextField(blank=True)),
                ('details', models.TextField(blank=True)),
                ('position', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20)),
                ('skript', models.TextField(max_length=2000)),
                ('bild', models.ImageField(null=True, upload_to=b'userskripte')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='skript',
            name='ud',
            field=models.ForeignKey(to='igelmain.Userdata'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beispiel',
            name='category',
            field=models.ForeignKey(blank=True, to='igelmain.Kategorie', null=True),
            preserve_default=True,
        ),
    ]
