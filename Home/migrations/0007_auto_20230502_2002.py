# Generated by Django 3.2.13 on 2023-05-02 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_fromaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='account_sid',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='publish_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
