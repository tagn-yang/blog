# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-23 08:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000, verbose_name='content')),
                ('nickname', models.CharField(max_length=50, verbose_name='nickname')),
                ('website', models.URLField(verbose_name='website')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete')], default=1, verbose_name='status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.Post', verbose_name='comment target')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comment',
            },
        ),
    ]
