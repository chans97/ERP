# Generated by Django 2.1.15 on 2020-03-11 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0011_auto_20200311_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='작성자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='계측기작성자', to=settings.AUTH_USER_MODEL),
        ),
    ]
