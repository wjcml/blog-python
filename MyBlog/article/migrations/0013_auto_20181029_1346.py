# Generated by Django 2.0.7 on 2018-10-29 05:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20181029_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 5, 45, 59, 924365, tzinfo=utc)),
        ),
    ]
