# Generated by Django 2.1.15 on 2020-03-08 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderregister_출하구분'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderregister',
            name='랙생산의뢰',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.OrderRegister'),
        ),
    ]
