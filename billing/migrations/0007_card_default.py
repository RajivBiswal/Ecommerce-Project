# Generated by Django 2.2 on 2020-09-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]