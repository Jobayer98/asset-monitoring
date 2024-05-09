# Generated by Django 5.0.6 on 2024-05-09 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_monitoring_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset_monitoring_api.company')),
                ('current_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset_monitoring_api.employee')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_out_time', models.DateField()),
                ('returned_time', models.DateTimeField(blank=True, null=True)),
                ('condition_when_handed_out', models.TextField()),
                ('condition_when_returned', models.TextField(blank=True, null=True)),
                ('device', models.ManyToManyField(to='asset_monitoring_api.device')),
            ],
        ),
    ]