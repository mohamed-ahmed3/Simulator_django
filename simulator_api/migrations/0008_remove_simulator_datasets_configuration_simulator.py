# Generated by Django 4.2.5 on 2023-09-10 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0007_remove_configuration_simulator_simulator_datasets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulator',
            name='datasets',
        ),
        migrations.AddField(
            model_name='configuration',
            name='simulator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to='simulator_api.simulator'),
        ),
    ]