# Generated by Django 4.2.5 on 2023-09-10 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0012_remove_configuration_simulator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='seasonality_components',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator_api.seasonalitycomponentdetails'),
        ),
    ]
