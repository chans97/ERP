# Generated by Django 2.1.15 on 2020-08-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockrack', '0010_auto_20200824_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockofrackproductmaker',
            name='현재공정',
            field=models.CharField(choices=[('배선중', '배선중'), ('소방대기중', '소방대기중'), ('완료', '완료')], default='배선중', max_length=10, null=True),
        ),
    ]