# Generated by Django 3.2.13 on 2022-07-28 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='API_Device_data',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('serial_no', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Serial No')),
                ('device_password', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Password')),
                ('date', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Date')),
                ('time', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Time')),
                ('hours', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Hours')),
                ('count_input', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Count Input')),
                ('count_output', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Count Output')),
                ('state', models.CharField(blank=True, max_length=2500, null=True, verbose_name='State')),
                ('cadence', models.CharField(blank=True, max_length=2500, null=True, verbose_name='cadence')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'My IOT Device Date',
            },
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('serial_no', models.PositiveIntegerField(blank=True, null=True, verbose_name='Serial No')),
                ('designation', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Designation')),
                ('device_password', models.CharField(blank=True, max_length=2500, null=True, verbose_name='Password')),
                ('status', models.CharField(default='Un Activated', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'My Device',
            },
        ),
    ]
