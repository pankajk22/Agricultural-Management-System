# Generated by Django 2.2.14 on 2020-08-04 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='quantityUnit',
        ),
        migrations.DeleteModel(
            name='quantityUnit',
        ),
    ]
