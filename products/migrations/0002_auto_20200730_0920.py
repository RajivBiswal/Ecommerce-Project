# Generated by Django 2.2 on 2020-07-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myproduct',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
