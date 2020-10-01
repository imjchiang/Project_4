# Generated by Django 3.0.5 on 2020-10-01 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='current_location',
            field=models.CharField(default='N/A', max_length=300),
        ),
        migrations.AlterField(
            model_name='rider',
            name='current_location',
            field=models.CharField(default='N/A', max_length=300),
        ),
        migrations.AlterField(
            model_name='rider',
            name='destination',
            field=models.CharField(default='N/A', max_length=300),
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_location', models.CharField(default='N/A', max_length=300)),
                ('destination', models.CharField(default='N/A', max_length=300)),
                ('reviewed', models.BooleanField(default=False)),
                ('driver_key', models.IntegerField(default=None)),
                ('rider_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]