# Generated by Django 3.2.13 on 2023-04-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20230419_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.PositiveBigIntegerField(default=0, help_text='Set price by cents. Like 100 cents to 1 Dollar')),
            ],
        ),
    ]
