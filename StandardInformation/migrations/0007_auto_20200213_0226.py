# Generated by Django 2.1.15 on 2020-02-13 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StandardInformation', '0006_auto_20200213_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplypartner',
            name='사업장주소',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
