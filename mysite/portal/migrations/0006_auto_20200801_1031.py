# Generated by Django 3.0.8 on 2020-08-01 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_farmerrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='cropType',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='cropType',
        ),
    ]
