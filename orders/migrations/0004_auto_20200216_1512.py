# Generated by Django 2.1.15 on 2020-02-16 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderregister_작성자'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduce',
            name='생산의뢰수주',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='생산요청', to='orders.OrderRegister'),
        ),
    ]