# Generated by Django 2.1.15 on 2020-02-29 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0017_auto_20200228_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowmetarial',
            name='검토일',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 29), null=True),
        ),
    ]