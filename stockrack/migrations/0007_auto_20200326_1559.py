# Generated by Django 2.1.15 on 2020-03-26 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockrack', '0006_auto_20200326_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockofrackproductmaker',
            name='현재공정',
            field=models.CharField(choices=[('배선중', '배선중'), ('소방대기완료', '소방대기완료')], default='배선중', max_length=10, null=True),
        ),
    ]
