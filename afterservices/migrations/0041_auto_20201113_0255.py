# Generated by Django 2.1.15 on 2020-11-13 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0040_auto_20201113_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asregisters',
            name='접수제품분류',
            field=models.CharField(choices=[('단품', '단품'), ('랙', '랙')], default='단품', max_length=10, null=True),
        ),
    ]
