# Generated by Django 2.1.15 on 2020-02-10 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0001_initial'),
        ('orders', '0001_initial'),
        ('stocksingle', '0003_auto_20200209_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockofsingleproductoutrequest',
            name='AS',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='단품출하요청', to='afterservices.ASVisitContents'),
        ),
        migrations.AddField(
            model_name='stockofsingleproductoutrequest',
            name='수주',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='단품출하요청', to='orders.OrderRegister'),
        ),
    ]
