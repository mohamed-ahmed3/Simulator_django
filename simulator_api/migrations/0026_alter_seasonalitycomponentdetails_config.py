# Generated by Django 4.2.5 on 2023-09-10 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0025_remove_configuration_seasonality_components_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasonalitycomponentdetails',
            name='config',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='seas', to='simulator_api.configuration'),
        ),
    ]
