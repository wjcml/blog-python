# Generated by Django 2.0.7 on 2018-10-27 09:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20181027_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 27, 9, 7, 15, 212669, tzinfo=utc)),
        ),
    ]
