# Generated by Django 2.2.14 on 2020-08-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20200804_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
