# Generated by Django 2.1.15 on 2020-04-17 10:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0054_auto_20200416_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowmetarial',
            name='검토일',
            field=models.DateField(blank=True, default=datetime.date(2020, 4, 17), null=True),
        ),
    ]