# Generated by Django 4.2.5 on 2023-09-10 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0021_alter_configuration_cycle_component_amplitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulator',
            name='datasets',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='configs', to='simulator_api.configuration'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='simulator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sim', to='simulator_api.simulator'),
        ),
    ]