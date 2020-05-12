# Generated by Django 2.1.15 on 2020-05-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_nowpart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pw', models.CharField(blank=True, max_length=12, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]