# Generated by Django 2.1.15 on 2020-03-31 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200330_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderregister',
            name='현장명',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
