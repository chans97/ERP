# Generated by Django 2.1.15 on 2020-02-27 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0010_auto_20200227_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialcheck',
            name='수입검사의뢰',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='수입검사', to='qualitycontrols.MaterialCheckRegister'),
        ),
    ]
