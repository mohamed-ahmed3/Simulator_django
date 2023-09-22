# Generated by Django 4.2.5 on 2023-09-10 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("simulator_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="configuration",
            name="simulator",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="configurations",
                to="simulator_api.simulator",
            ),
        ),
        migrations.AlterField(
            model_name="simulator",
            name="datasets",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="config",
                to="simulator_api.configuration",
            ),
        ),
    ]
