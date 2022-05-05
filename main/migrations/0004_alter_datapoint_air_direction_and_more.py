# Generated by Django 4.0.4 on 2022-05-05 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_datapoint_air_direction_datapoint_air_speed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='air_direction',
            field=models.CharField(choices=[('N', 'North'), ('NE', 'North East'), ('E', 'East'), ('SE', 'South East'), ('S', 'South'), ('SW', 'South West'), ('W', 'West'), ('NW', 'North West')], max_length=2),
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='air_speed',
            field=models.FloatField(verbose_name='Air Speed'),
        ),
    ]