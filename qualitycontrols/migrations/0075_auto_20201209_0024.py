# Generated by Django 2.1.15 on 2020-12-09 00:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0074_auto_20201208_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowmetarial',
            name='검토일',
            field=models.DateField(blank=True, default=datetime.date(2020, 12, 9), null=True),
        ),
    ]
