# Generated by Django 2.2 on 2020-08-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='India', max_length=100),
        ),
    ]
