# Generated by Django 2.1.15 on 2020-06-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0032_auto_20200420_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='asregisters',
            name='비용',
            field=models.CharField(choices=[('유상', '유상'), ('무상', '무상')], default='유상', max_length=10),
        ),
    ]
