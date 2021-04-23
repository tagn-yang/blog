# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-23 08:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='category_name')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete')], default=1, verbose_name='status')),
                ('is_nav', models.BooleanField(default=False, verbose_name='is or not nav')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'category',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, verbose_name='title')),
                ('desc', models.CharField(blank=True, max_length=1024, verbose_name='summary')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete'), (2, 'draft')], default=1, verbose_name='status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.Category', verbose_name='category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'article',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='tag_name')),
                ('status', models.PositiveIntegerField(choices=[(1, 'normal'), (0, 'delete')], default=1, verbose_name='status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tag',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='blog_app.Tag', verbose_name='tag'),
        ),
    ]