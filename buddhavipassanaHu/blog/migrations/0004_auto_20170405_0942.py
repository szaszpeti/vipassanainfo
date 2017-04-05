# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['timestamp', '-updated']},
        ),
        migrations.AlterField(
            model_name='document',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
