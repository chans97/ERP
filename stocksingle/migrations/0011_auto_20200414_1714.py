# Generated by Django 2.1.15 on 2020-04-14 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocksingle', '0010_auto_20200414_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockofsingleproductoutrequest',
            old_name='주소',
            new_name='수취인주소',
        ),
    ]