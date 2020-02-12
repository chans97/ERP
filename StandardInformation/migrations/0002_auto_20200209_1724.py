# Generated by Django 2.1.15 on 2020-02-09 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StandardInformation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rackproductmaterial',
            name='랙구성',
            field=models.CharField(blank=True, choices=[('단품', '단품'), ('자재', '자재')], default='단품', max_length=4),
        ),
        migrations.AlterField(
            model_name='rackproductmaterial',
            name='랙구성단품',
            field=models.ManyToManyField(blank=True, related_name='랙구성단품', to='StandardInformation.SingleProduct'),
        ),
        migrations.AlterField(
            model_name='rackproductmaterial',
            name='랙구성자재',
            field=models.ManyToManyField(blank=True, related_name='랙구성자재', to='StandardInformation.Material'),
        ),
    ]