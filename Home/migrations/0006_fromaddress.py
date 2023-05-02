# Generated by Django 3.2.13 on 2023-05-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_apikey'),
    ]

    operations = [
        migrations.CreateModel(
            name='FromAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('street1', models.TextField(blank=True, null=True)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
