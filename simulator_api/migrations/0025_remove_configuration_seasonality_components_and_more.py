# Generated by Django 4.2.5 on 2023-09-10 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0024_configuration_seasonality_components'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='seasonality_components',
        ),
        migrations.AddField(
            model_name='configuration',
            name='seasonality_components',
            field=models.ManyToManyField(default=None, related_name='seasons', to='simulator_api.seasonalitycomponentdetails'),
        ),
    ]