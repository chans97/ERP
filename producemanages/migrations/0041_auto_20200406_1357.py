# Generated by Django 2.1.15 on 2020-04-06 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0040_auto_20200402_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(blank=True, default=datetime.date(2020, 4, 6), null=True),
        ),
    ]
