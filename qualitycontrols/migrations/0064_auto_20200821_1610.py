# Generated by Django 2.1.15 on 2020-08-21 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0063_auto_20200615_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowmetarial',
            name='검토일',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 21), null=True),
        ),
    ]
