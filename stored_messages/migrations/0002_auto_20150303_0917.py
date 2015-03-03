# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('stored_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='related_history',
            field=models.CommaSeparatedIntegerField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
    ]
