# Generated by Django 3.0.5 on 2020-09-30 02:56

import datetime
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
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_location', models.CharField(default='N/A', max_length=50)),
                ('destination', models.CharField(default='N/A', max_length=50)),
                ('total_trips', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=None)),
                ('no_show', models.IntegerField(default=0)),
                ('user_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('driver_key', models.IntegerField()),
                ('rider_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_location', models.CharField(default='N/A', max_length=50)),
                ('pickup_distance', models.IntegerField(default=1)),
                ('trip_distance', models.IntegerField(default=0)),
                ('rate', models.IntegerField(default=1)),
                ('rush_hour_rate', models.IntegerField(default=1)),
                ('vehicle_type', models.CharField(default='N/A', max_length=250)),
                ('vehicle_make', models.CharField(default='N/A', max_length=250)),
                ('vehicle_model', models.CharField(default='N/A', max_length=250)),
                ('vehicle_year', models.IntegerField(default=0)),
                ('vehicle_insured', models.BooleanField(default=False)),
                ('license_expiration', models.DateField(default=datetime.date(2000, 1, 1))),
                ('total_trips', models.IntegerField(default=0)),
                ('safety_rating', models.IntegerField(default=None)),
                ('time_rating', models.IntegerField(default=None)),
                ('service_rating', models.IntegerField(default=None)),
                ('no_show', models.IntegerField(default=0)),
                ('user_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
